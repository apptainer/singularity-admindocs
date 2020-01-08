.. _installation:

######################
Installing Singularity
######################

This section will guide you through the process of installing
Singularity {InstallationVersion} via several different methods. (For
instructions on installing earlier versions of Singularity please see
`earlier versions of the docs <https://www.sylabs.io/docs/>`_.)

=====================
Installation on Linux
=====================

Singularity can be installed on any modern Linux distribution, on
bare-metal or inside a Virtual Machine. Nested installations inside
containers are not recommended, and require the outer container to be
run with full privilege.

-------------------
System Requirements
-------------------

Singularity requires ~140MiB disk space once compiled and installed.

There are no specific CPU or memory requirements at runtime, though
2GB of RAM is recommended when building from source.

Full functionality of Singularity requires that the kernel supports:

 - **OverlayFS mounts** - (minimum kernel >=3.18) Required for full
   flexiblity in bind mounts to containers, and to support persistent
   overlays for writable containers.
 - **Unprivileged user namespaces** - (minimum kernel >=3.8, >=3.18
   recommended) Required to run containers without root or setuid
   privilege.

RHEL & CentOS 6 do not support these features, but Singularity can be
used with some limitations.


Filesystem support
==================

Singularity supports most filesystems, but there are limitations when
installing Singularity on, or running containers from common parallel
/ network filesystems:

 - We strongly recommend installing Singularity on local disk on each
   compute node.
 - If Singularity is installed to a network location, a
   ``--localstatedir`` must be provided on each node, and Singularity
   configured to use it.
 - The ``--localstatedir`` filesystem should support overlay mounts.
 - When running sandbox containers with the ``--fakeroot`` option,
   filesystem user namespace support is required. User namespace
   support is known to be incomplete on Lustre, and GPFS.


----------------
Before you begin
----------------

If you have an earlier version of Singularity installed, you should
:ref:`remove it <remove-an-old-version>` before executing the
installation commands.  You will also need to install some
dependencies and install `Go <https://golang.org/>`_.

.. _install-dependencies:

-------------------
Install from Source
-------------------

To use the latest version of Singularity from GitHub you will need to
build and install it from source. This may sound daunting, but the
process is straightforward, and detailed below:


Install Dependencies
====================

On Red Hat Enterprise Linux or CentOS install the following dependencies:

.. code-block:: sh

   $ sudo yum update -y && \
        sudo yum groupinstall -y 'Development Tools' && \
        sudo yum install -y \
        openssl-devel \
        libuuid-devel \
        libseccomp-devel \
        wget \
        squashfs-tools \
        cryptsetup

        
On Ubuntu or Debian install the following dependencies:

.. code-block:: sh

    $ sudo apt-get update && sudo apt-get install -y \
        build-essential \
        uuid-dev \
        libgpgme-dev \
        squashfs-tools \
        libseccomp-dev \
        wget \
        pkg-config \
        git \
        cryptsetup-bin

.. note::

   You can build Singularity (3.5+) without ``cryptsetup`` available, but will
   not be able to use encrypted containers without it installed on your system.

.. _install-go:

Install Go
==========

Singularity v3 is written primarily in Go, and you will need Go 1.13
or above installed to compile it from source.

This is one of several ways to `install and configure Go
<https://golang.org/doc/install>`_.

.. note::

   If you have previously installed Go from a download, rather than an
   operating system package, you should remove your ``go`` directory,
   e.g. ``rm -r /usr/local/go`` before installing a newer
   version. Extracting a new version of Go over an existing
   installation can lead to errors when building Go programs, as it
   may leave old files, which have been removed or replaced in newer
   versions.


Visit the `Go download page <https://golang.org/dl/>`_ and pick a package
archive to download. Copy the link address and download with wget.  Then extract
the archive to ``/usr/local`` (or use other instructions on go installation
page).

.. code-block:: none

    $ export VERSION=1.13.5 OS=linux ARCH=amd64 && \
        wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz && \
        sudo tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz && \
        rm go$VERSION.$OS-$ARCH.tar.gz

Then, set up your environment for Go.

.. code-block:: none

    $ echo 'export GOPATH=${HOME}/go' >> ~/.bashrc && \
        echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc && \
        source ~/.bashrc

Download Singularity from a release
===================================

You can download Singularity from one of the releases. To see a full
list, visit `the GitHub release page
<https://github.com/sylabs/singularity/releases>`_.  After deciding on
a release to install, you can run the following commands to proceed
with the installation.

.. code-block:: none

    $ export VERSION={InstallationVersion} && # adjust this as necessary \
        wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
        tar -xzf singularity-${VERSION}.tar.gz && \
        cd singularity

Checkout Code from Git
======================

The following commands will install Singularity from the `GitHub repo
<https://github.com/sylabs/singularity>`_ to ``/usr/local``. This
method will work for >=v{InstallationVersion}. To install an older
tagged release see `older versions of the docs
<https://www.sylabs.io/docs/>`_.

When installing from source, you can decide to install from either a
**tag**, a **release branch**, or from the **master branch**.

- **tag**: GitHub tags form the basis for releases, so installing from
  a tag is the same as downloading and installing a `specific release
  <https://github.com/sylabs/singularity/releases>`_.  Tags are
  expected to be relatively stable and well-tested.

- **release branch**: A release branch represents the latest version
  of a minor release with all the newest bug fixes and enhancements
  (even those that have not yet made it into a point release).  For
  instance, to install v3.2 with the latest bug fixes and enhancements
  checkout ``release-3.2``.  Release branches may be less stable than
  code in a tagged point release.

- **master branch**: The ``master`` branch contains the latest,
  bleeding edge version of Singularity. This is the default branch
  when you clone the source code, so you don't have to check out any
  new branches to install it. The ``master`` branch changes quickly
  and may be unstable.

To ensure that the Singularity source code is downloaded to the
appropriate directory use these commands.

.. code-block:: none

    $ git clone https://github.com/sylabs/singularity.git && \
        cd singularity && \
        git checkout v{InstallationVersion}

Compile Singularity
===================

Singularity uses a custom build system called ``makeit``.  ``mconfig``
is called to generate a ``Makefile`` and then ``make`` is used to
compile and install.

To support the SIF image format, automated networking setup etc., and
older Linux distributions without user namespace support, Singularity
must be ``make install``ed as root or with ``sudo``, so it can install
the ``libexec/singularity/bin/starter-setuid`` binary with root
ownership and setuid permissions for privileged operations. If you
need to install as a normal user, or do not want to use setuid
functionality :ref:`see below <install-nonsetuid>`.

.. code-block:: none

    $ ./mconfig && \
        make -C ./builddir && \
        sudo make -C ./builddir install

By default Singularity will be installed in the ``/usr/local``
directory hierarchy. You can specify a custom directory with the
``--prefix`` option, to ``mconfig`` like so:

.. code-block:: none

    $ ./mconfig --prefix=/opt/singularity

This option can be useful if you want to install multiple versions of
Singularity, install a personal version of Singularity on a shared
system, or if you want to remove Singularity easily after installing
it.

For a full list of ``mconfig`` options, run ``mconfig --help``.  Here
are some of the most common options that you may need to use when
building Singularity from source.

- ``--sysconfdir``: Install read-only config files in sysconfdir.
  This option is important if you need the ``singularity.conf`` file
  or other configuration files in a custom location.

- ``--localstatedir``: Set the state directory where containers are
  mounted. This is a particularly important option for administrators
  installing Singularity on a shared file system.  The
  ``--localstatedir`` should be set to a directory that is present on
  each individual node.

- ``-b``: Build Singularity in a given directory. By default this is
  ``./builddir``.

.. _install-nonsetuid:


Unprivileged (non-setuid) Installation
======================================

If you need to install Singularity as a non-root user, or do not wish
to allow the use of a setuid root binary, you can configure
singularity with the ``--without-setuid`` option to mconfig:

.. code-block:: none

    $ ./mconfig --without-setuid --prefix=/home/dave/singularity && \
        make -C ./builddir && \
        make -C ./builddir install

If you have already installed Singularity you can disable the setuid
flow by setting the option ``allow setuid = no`` in
``etc/singularity/singularity.conf`` within your installation
directory.

When singularity does not use setuid all container execution will use
a user namespace. This requires support from your operating system
kernel, and imposes some limitations on functionality. You should
review the :ref:`requirements <userns-requirements>` and
:ref:`limitations <userns-limitations>` in the :ref:`user namespace
<userns>` section of this guide.

  
Source bash completion file
===========================

To enjoy bash shell completion with Singularity commands and options,
source the bash completion file:

.. code-block:: none

    $ . /usr/local/etc/bash_completion.d/singularity

Add this command to your `~/.bashrc` file so that bash completion
continues to work in new shells.  (Adjust the path if you
installed Singularity to a different location.)

.. _install-rpm:

------------------------
Build and install an RPM
------------------------

If you use RHEL, CentOS or SUSE, building and installing a Singularity
RPM allows your Singularity installation be more easily managed,
upgraded and removed. In Singularity >=v3.0.1 you can build an RPM
directly from the `release tarball
<https://github.com/sylabs/singularity/releases>`_.

.. note::

    Be sure to download the correct asset from the `GitHub releases
    page <https://github.com/sylabs/singularity/releases>`_.  It
    should be named `singularity-<version>.tar.gz`.

After installing the :ref:`dependencies <install-dependencies>` and
installing :ref:`Go <install-go>` as detailed above, you are ready to
download the tarball and build and install the RPM.

.. code-block:: none

    $ export VERSION={InstallationVersion} && # adjust this as necessary \
        wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
        rpmbuild -tb singularity-${VERSION}.tar.gz && \
        sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/singularity-$VERSION-1.el7.x86_64.rpm && \
        rm -rf ~/rpmbuild singularity-$VERSION*.tar.gz

If you encounter a failed dependency error for golang but installed it
from source, build with this command:

.. code-block:: none

    rpmbuild -tb --nodeps singularity-${VERSION}.tar.gz


Options to ``mconfig`` can be passed using the familiar syntax to
``rpmbuild``.  For example, if you want to force the local state
directory to ``/mnt`` (instead of the default ``/var``) you can do the
following:

.. code-block:: none

    rpmbuild -tb --define='_localstatedir /mnt' singularity-$VERSION.tar.gz

.. note::

     It is very important to set the local state directory to a
     directory that physically exists on nodes within a cluster when
     installing Singularity in an HPC environment with a shared file
     system. 

.. _remove-an-old-version:

---------------------
Remove an old version
---------------------

In a standard installation of Singularity 3.0.1 and beyond (when
building from source), the command ``sudo make install`` lists all the
files as they are installed. You must remove all of these files and
directories to completely remove Singularity.

.. code-block:: none

    $ sudo rm -rf \
        /usr/local/libexec/singularity \
        /usr/local/var/singularity \
        /usr/local/etc/singularity \
        /usr/local/bin/singularity \
        /usr/local/bin/run-singularity \
        /usr/local/etc/bash_completion.d/singularity

If you anticipate needing to remove Singularity, it might be easier to
install it in a custom directory using the ``--prefix`` option to
``mconfig``.  In that case Singularity can be uninstalled simply by
deleting the parent directory. Or it may be useful to install
Singularity :ref:`using a package manager <install-rpm>` so that it
can be updated and/or uninstalled with ease in the future.

------------------------------------
Distribution packages of Singularity
------------------------------------

.. note::

    Packaged versions of Singularity in Linux distribution repos are
    maintained by community members. They may be older releases of
    Singularity, as it can take time to package and distribute new
    versions. For the latest upstream versions of Singularity it is
    recommended that you build from source using one of the methods
    detailed above.

Install the CentOS/RHEL package using yum
=========================================

The EPEL (Extra Packages for Enterprise Linux) repos contain
Singularity rpms that are regularly updated. To install Singularity
from the epel repos, first install the epel-release package and then
install Singularity.  For instance, on CentOS 6/7/8 do the following:

.. code-block:: none

    $ sudo yum update -y && \
        sudo yum install -y epel-release && \
        sudo yum update -y && \
        sudo yum install -y singularity

==============================
Installation on Windows or Mac
==============================

Linux container runtimes like Singularity cannot run natively on
Windows or Mac because of basic incompatibilities with the host
kernel. (Contrary to a popular misconception, MacOS does not run on a
Linux kernel. It runs on a kernel called Darwin originally forked
from BSD.)

For this reason, the Singularity community maintains a set of Vagrant
Boxes via `Vagrant Cloud <https://www.vagrantup.com/>`__, one of
`Hashicorp's <https://www.hashicorp.com/#open-source-tools>`_ open
source tools. The current versions can be found under the `sylabs
<https://app.vagrantup.com/sylabs>`_ organization.

Sylabs has also developed a beta version of Singularity Desktop for
Mac, which runs Singularity in a lightweight virtual machine, in a
transparent manner.

-------
Windows
-------

Install the following programs:

 -  `Git for Windows <https://git-for-windows.github.io/>`_
 -  `VirtualBox for Windows <https://www.virtualbox.org/wiki/Downloads>`_
 -  `Vagrant for Windows <https://www.vagrantup.com/downloads.html>`_
 -  `Vagrant Manager for Windows <http://vagrantmanager.com/downloads/>`_

---
Mac
---

To use Singularity Desktop for macOS (Beta Preview):

Download a Mac installer package `here
<https://www.sylabs.io/singularity-desktop-macos/>`__.

Singularity is also available via Vagrant (installable with
`Homebrew <https://brew.sh>`_ or manually) or with the Singularity Desktop for
macOS (Alpha Preview).

To use Vagrant via Homebrew:

.. code-block:: none

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    $ brew cask install virtualbox && \
        brew cask install vagrant && \
        brew cask install vagrant-manager

-----------------------        
Singularity Vagrant Box
-----------------------

Run Git Bash (Windows) or open a terminal (Mac) and create and enter a
directory to be used with your Vagrant VM.

.. code-block:: none

    $ mkdir vm-singularity && \
        cd vm-singularity

If you have already created and used this folder for another VM, you will need
to destroy the VM and delete the Vagrantfile.

.. code-block:: none

    $ vagrant destroy && \
        rm Vagrantfile

Then issue the following commands to bring up the Virtual Machine. (Substitute a
different value for the ``$VM`` variable if you like.)

.. code-block:: none

    $ export VM=sylabs/singularity-3.5-ubuntu-bionic64 && \
        vagrant init $VM && \
        vagrant up && \
        vagrant ssh

You can check the installed version of Singularity with the following:

.. code-block:: none

    vagrant@vagrant:~$ singularity version
    3.5.2


Of course, you can also start with a plain OS Vagrant box as a base and then
install Singularity using one of the above methods for Linux.
