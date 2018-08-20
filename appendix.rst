
========
Appendix
========

.. _using-host-libraries-gpu-drivers-and-openmpi-btls:

--------------------------------------------------
Using Host libraries: GPU drivers and OpenMPI BTLs
--------------------------------------------------

.. _sec:tutorial-gpu-drivers-and-openmpi:

.. note:: **Much of the GPU portion of this tutorial is deprecated by the** ``--nv`` **option
    that automatically binds host system driver libraries into your container at
    runtime. See the** ``exec`` **command for an example.**

Singularity does a fantastic job of isolating you from the host so you don’t have to muck
about with ``LD_LIBRARY_PATH``, you just get exactly the library versions you want. However,
in some situations you need to use library versions that match host exactly. Two common ones
are NVIDIA gpu driver user-space libraries, and OpenMPI transport drivers for high performance
networking. There are many ways to solve these problems. Some people build a container and copy
the version of the libs (installed on the host) into the container.

What We will learn today
========================

This document describes how to use a bind mount, symlinks and ldconfig so that when the host
libraries are updated the container does not need to be rebuilt.

Note this tutorial is tested with Singularity commit `945c6ee343a1e6101e22396a90dfdb5944f442b6 <https://github.com/singularityware/singularity/commit/945c6ee343a1e6101e22396a90dfdb5944f442b6>`_,
which is part of the (current) development branch, and thus it should work with version 2.3 when
that is released. The version of OpenMPI used is 2.1.0 (versions above 2.1 should work).

Environment
===========

In our environment we run CentOS 7 hosts with:

#. slurm located on ``/opt/slurm-<version>`` and the slurm user ``slurm``

#. Mellanox network cards with drivers installed to ``/opt/mellanox`` ( Specifically we run a RoCEv1
   network for Lustre and MPI communications)
#. NVIDIA GPUs with drivers installed to ``/lib64``
#. OpenMPI (by default) for MPI processes


Creating your image
===================

Since we are building an ubuntu image, it may be easier to create an ubuntu VM to create the image.
Alternatively you can follow the recipe `here <https://singularity-admindoc.readthedocs.io/en/latest/appendix.html#building-an-ubuntu-image-on-a-rhel-host>`_.

Use the following def file to create the image.

.. code-block:: none

    Bootstrap: debootstrap

    MirrorURL: http://us.archive.ubuntu.com/ubuntu/

    OSVersion: xenial

    Include: apt



    %post

    apt install -y software-properties-common

    apt-add-repository -y universe

    apt update

    apt install -y wget

    mkdir /usr/local/openmpi || echo "Directory exists"

    mkdir /opt/mellanox || echo "Directory exists"

    mkdir /all_hostlibs || echo "Directory exists"

    mkdir /desired_hostlibs || echo "Directory exists"

    mkdir /etc/libibverbs.d || echo "Directory exists"

    echo "driver mlx4" > /etc/libibverbs.d/mlx4.driver

    echo "driver mlx5" > /etc/libibverbs.d/mlx5.driver

    adduser slurm || echo "User exists"

    wget https://gist.githubusercontent.com/l1ll1/89b3f067d5b790ace6e6767be5ea2851/raw/422c8b5446c6479285cd29d1bf5be60f1b359b90/desired_hostlibs.txt -O /tmp/desired_hostlibs.txt

    cat /tmp/desired_hostlibs.txt | xargs -I{} ln -s /all_hostlibs/{} /desired_hostlibs/{}

    rm /tmp/desired_hostlibs.txt


The mysterious ``wget`` line gets a list of all the libraries that the CentOS host has in ``/lib64`` that we
think its safe to use in the container. Specifically these are things like nvidia drivers.

.. code-block:: none

    libvdpau_nvidia.so

    libnvidia-opencl.so.1

    libnvidia-ml.so.1

    libnvidia-ml.so

    libnvidia-ifr.so.1

    libnvidia-ifr.so

    libnvidia-fbc.so.1

    libnvidia-fbc.so

    libnvidia-encode.so.1

    libnvidia-encode.so

    libnvidia-cfg.so.1

    libnvidia-cfg.so

    libicudata.so.50

    libicudata.so

    libcuda.so.1

    libcuda.so

    libGLX_nvidia.so.0

    libGLESv2_nvidia.so.2

    libGLESv1_CM_nvidia.so.1

    libEGL_nvidia.so.0

    libibcm.a

    libibcm.so

    libibcm.so.1

    libibcm.so.1.0.0

    libibdiag-2.1.1.so

    libibdiag.a

    libibdiag.la

    libibdiag.so

    libibdiagnet_plugins_ifc-2.1.1.so

    libibdiagnet_plugins_ifc.a

    libibdiagnet_plugins_ifc.la

    libibdiagnet_plugins_ifc.so

    libibdmcom-2.1.1.so

    libibdmcom.a

    libibdmcom.la

    libibdmcom.so

    libiberty.a

    libibis-2.1.1.so.3

    libibis-2.1.1.so.3.0.3

    libibis.a

    libibis.la

    libibis.so

    libibmad.a

    libibmad.so

    libibmad.so.5

    libibmad.so.5.5.0

    libibnetdisc.a

    libibnetdisc.so

    libibnetdisc.so.5

    libibnetdisc.so.5.3.0

    libibsysapi-2.1.1.so

    libibsysapi.a

    libibsysapi.la

    libibsysapi.so

    libibumad.a

    libibumad.so

    libibumad.so.3

    libibumad.so.3.1.0

    libibus-1.0.so.5

    libibus-1.0.so.5.0.503

    libibus-qt.so.1

    libibus-qt.so.1.3.0

    libibverbs.a

    libibverbs.so

    libibverbs.so.1

    libibverbs.so.1.0.0

    liblustreapi.so

    libmlx4-rdmav2.so

    libmlx4.a

    libmlx5-rdmav2.so

    libmlx5.a

    libnl.so.1

    libnuma.so.1

    libosmcomp.a

    libosmcomp.so

    libosmcomp.so.3

    libosmcomp.so.3.0.6

    libosmvendor.a

    libosmvendor.so

    libosmvendor.so.3

    libosmvendor.so.3.0.8

    libpciaccess.so.0

    librdmacm.so.1

    libwrap.so.0



Also note:

#. in ``hostlibs.def`` we create a slurm user. Obviously if your ``SlurmUser`` is different you should change this name.
#. We make directories for ``/opt`` and ``/usr/local/openmpi``. We’re going to bindmount these from the host so we get
   all the bits of OpenMPI and Mellanox and Slurm that we need.

Executing your image
====================

On our system we do:

.. code-block:: none

    SINGULARITYENV_LD_LIBRARY_PATH=/usr/local/openmpi/2.1.0-gcc4/lib:/opt/munge-0.5.11/lib:/opt/slurm-16.05.4/lib:/opt/slurm-16.05.4/lib/slurm:/desired_hostlibs:/opt/mellanox/mxm/lib/

    export SINGULARITYENV_LD_LIBRARY_PATH

then

.. code-block:: none

    srun  singularity exec -B /usr/local/openmpi:/usr/local/openmpi -B /opt:/opt -B /lib64:/all_hostlibs hostlibs.img <path to binary>


---------------------------------------
Building an Ubuntu image on a RHEL host
---------------------------------------

.. _sec:building-ubuntu-rhel-host:

This recipe describes how to build an Ubuntu image using Singularity on a RHEL compatible host.

.. note:: This tutorial is intended for Singularity release 2.1.2,
    and reflects standards for that version.

In order to do this, you will need to first install the ‘debootstrap’ package onto your host. Then, you will create
a definition file that will describe how to build your Ubuntu image. Finally, you will build the image using the Singularity
commands ‘create’ and ``bootstrap``.

Preparation
===========

This recipe assumes that you have already installed Singularity on your computer. If you have not, follow the instructions here
to install. After Singularity is installed on your computer, you will need to install the ‘debootstrap’ package. The ‘debootstrap’
package is a tool that will allow you to create Debian-based distributions such as Ubuntu. In order to install ‘debootstrap’, you will
also need to install ‘epel-release’. You will need to download the appropriate RPM from the EPEL website. Make sure you download the correct
version of the RPM for your release.

.. code-block:: none

    # First, wget the appropriate RPM from the EPEL website (https://dl.fedoraproject.org/pub/epel/)

    # In this example we used RHEL 7, so we downloaded epel-release-latest-7.noarch.rpm

    $ wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm


    # Then, install your epel-release RPM

    $ sudo yum install epel-release-latest-7.noarch.rpm


    # Finally, install debootstrap

    $ sudo yum install debootstrap


Creating the Definition File
----------------------------

You will need to create a definition file to describe how to build your Ubuntu image. Definition files are plain text files that contain Singularity
keywords. By using certain Singularity keywords, you can specify how you want your image to be built. The extension ‘.def’ is recommended for user clarity.
Below is a definition file for a minimal Ubuntu image:

.. code-block:: none

    DistType "debian"

    MirrorURL "http://us.archive.ubuntu.com/ubuntu/"

    OSVersion "trusty"



    Setup

    Bootstrap



    Cleanup

    The following keywords were used in this definition file:


-  DistType: DistType specifies the distribution type of your intended operating system. Because we are trying to build an Ubuntu image, the type “debian” was chosen.
-  MirrorURL: The MirrorURL specifies the download link for your intended operating system. The Ubuntu archive website is a great mirror link to use if you are building an Ubuntu image.
-  OSVersion: The OSVersion is used to specify which release of a Debian-based distribution you are using. In this example we chose “trusty” to specify that we wanted to build an Ubuntu
   14.04 (Trusty Tahr) image.
-  Setup: Setup creates some of the base files and components for an OS and is highly recommended to be included in your definition file.
-  Bootstrap: Bootstrap will call apt-get to install the appropriate package to build your OS.
-  Cleanup: Cleanup will remove temporary files from the installation.

While this definition file is enough to create a working Ubuntu image, you may want increased customization of your image. There are several Singularity keywords that allow the user to do
things such as install packages or files. Some of these keywords are used in the example below:

.. code-block:: none

    DistType "debian"

    MirrorURL "http://us.archive.ubuntu.com/ubuntu/"

    OSVersion "trusty"


    Setup

    Bootstrap


    InstallPkgs python

    InstallPkgs wget

    RunCmd wget https://bootstrap.pypa.io/get-pip.py

    RunCmd python get-pip.py

    RunCmd ln -s /usr/local/bin/pip /usr/bin/pip

    RunCmd pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.9.0-cp27-none-linux_x86_64.whl


    Cleanup

Before going over exactly what image this definition file specifies, the remaining Singularity keywords should be introduced.

-  InstallPkgs: InstallPkgs allows you to install any packages that you want on your newly created image.
-  InstallFile: InstallFile allows you to install files from your computer to the image.
-  RunCmd: RunCmd allows you to run a command from within the new image during the installation.
-  RunScript: RunScript adds a new line to the runscript invoked by the Singularity subcommand ‘run’. See the run page for more information.

Now that you are familiar with all of the Singularity keywords, we can take a closer look at the example above. As with the previous example, an Ubuntu image is created with the specified DistType,
MirrorURL, and OSVersion. However, after Setup and Bootstrap, we used the InstallPkgs keyword to install ‘python’ and ‘wget’. Then we used the RunCmd keyword to first download the pip installation wheel,
and then to install ‘pip’. Subsequently, we also used RunCmd to pip install ``TensorFlow``. Thus, we have created a definition file that will install ‘python’, ‘pip’, and ‘Tensorflow’ onto the new image.

Creating your image
-------------------

Once you have created your definition file, you will be ready to actually create your image. You will do this by utilizing the Singularity ‘create’ and ‘bootstrap’ subcommands. The process for doing this
can be seen below:

.. note:: We have saved our definition file as “ubuntu.def”

.. code-block:: none

    # First we will create an empty image container called ubuntu.img

    $ sudo singularity create ubuntu.img

    Creating a sparse image with a maximum size of 1024MiB...

    INFO   : Using given image size of 1024

    Formatting image (/sbin/mkfs.ext3)

    Done. Image can be found at: ubuntu.img


    # Next we will bootstrap the image with the operating system specified in our definition file

    $ sudo singularity bootstrap ubuntu.img ubuntu.def

    W: Cannot check Release signature; keyring file not available /usr/share/keyrings/ubuntu-archive-keyring.gpg

    I: Retrieving Release

    I: Retrieving Packages

    I: Validating Packages

    I: Resolving dependencies of required packages...

    I: Resolving dependencies of base packages...

    I: Found additional base dependencies: gcc-4.8-base gnupg gpgv libapt-pkg4.12 libreadline6 libstdc++6 libusb-0.1-4 readline-common ubuntu-keyring

    I: Checking component main on http://us.archive.ubuntu.com/ubuntu...

    I: Retrieving adduser 3.113+nmu3ubuntu3

    I: Validating adduser 3.113+nmu3ubuntu3

    I: Retrieving apt 1.0.1ubuntu2

    I: Validating apt 1.0.1ubuntu2

    snip...

    Downloading pip-8.1.2-py2.py3-none-any.whl (1.2MB)

    100% |################################| 1.2MB 1.1MB/s

    Collecting setuptools

    Downloading setuptools-24.0.2-py2.py3-none-any.whl (441kB)

    100% |################################| 450kB 2.7MB/s

    Collecting wheel

    Downloading wheel-0.29.0-py2.py3-none-any.whl (66kB)

    100% |################################| 71kB 9.9MB/s

    Installing collected packages: pip, setuptools, wheel

    Successfully installed pip-8.1.2 setuptools-24.0.2 wheel-0.29.0

    At this point, you have successfully created an Ubuntu image with 'python', 'pip', and 'TensorFlow' on your RHEL computer.

    Tips and Tricks

    Here are some tips and tricks that you can use to create more efficient definition files:


Use here documents with RunCmd
------------------------------

Using here documents with conjunction with RunCmd can be a great way to decrease the number of RunCmd keywords that you need to include
in your definition file. For example, we can substitute a here document into the previous example:

.. code-block:: none

    DistType "debian"

    MirrorURL "http://us.archive.ubuntu.com/ubuntu/"

    OSVersion "trusty"


    Setup

    Bootstrap


    InstallPkgs python

    InstallPkgs wget

    RunCmd /bin/sh <<EOF

    wget https://bootstrap.pypa.io/get-pip.py

    python get-pip.py

    ln -s /usr/local/bin/pip /usr/bin/pip

    pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.9.0-cp27-none-linux_x86_64.whl

    EOF


    Cleanup


As you can see, using a here document allowed us to decrease the number of RunCmd keywords from 4 to 1. This can be useful when your definition file
has a lot of RunCmd keywords and can also ease copying and pasting command line recipes from other sources.

Use InstallPkgs with multiple packages
--------------------------------------

The InstallPkgs keyword is able to install multiple packages with a single keyword. Thus, another way you can increase the efficiency of your code is to
use a single InstallPkgs keyword to install multiple packages, as seen below:

.. code-block:: none

    DistType "debian"

    MirrorURL "http://us.archive.ubuntu.com/ubuntu/"

    OSVersion "trusty"


    Setup

    Bootstrap


    InstallPkgs python wget

    RunCmd /bin/sh <<EOF

    wget https://bootstrap.pypa.io/get-pip.py

    python get-pip.py

    ln -s /usr/local/bin/pip /usr/bin/pip

    pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.9.0-cp27-none-linux_x86_64.whl

    EOF


    Cleanup


Using a single InstallPkgs keyword to install both ‘python’ and ‘wget’ allowed to decrease the number of InstallPkgs keywords we had to use in our definition file.
This slimmed down our definition file and helped reduce clutter.
