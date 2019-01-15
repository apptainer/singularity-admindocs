.. _admin-quick-start:

Admin Quick Start
=================

This document will cover installation and administration points of Singularity 
on a Linux host. This will also cover an overview of :ref:`configuing 
Singularity <configuing_overview>`, :ref:`Singularity architecture 
<singularity-architecture>`,
and :ref:`the Singularity security model <singularity-security>`.

For any additional help or support contact the
`Sylabs team <https://www.sylabs.io/contact/>`_, or send a email to 
`support@sylabs.io <mailto:support@sylabs.io>`_.

------------
Installation
------------

This section will explain how to install Singularity from an RPM. If you want 
more information on installation, including althernate installation procedures 
and options for other operating systems, see the `user guide instalation page 
<https://www.sylabs.io/guides/3.0/user-guide/installation.html>`_.

Install Build Dependencies
--------------------------

Singularity requires several libraries and development tools to be installed 
before you can build the RPM.

.. code-block:: none

    $ sudo yum update -y && \
        sudo yum groupinstall -y 'Development Tools' && \
        sudo yum install -y \
        openssl-devel \
        libuuid-devel \
        libseccomp-devel \
        wget \
        squashfs-tools

.. ^ I'm not actually sure if all of these are needed when one installs the RPM
.. or not.  I think that RPM may resolve these dependencies for the user.  
.. Perhaps some testing is in order.  

Install Go
----------

Singularity is primarily written in Go, so we will need Go 1.11 or greater build 
Singularity.

If your updating from a previous go version, make sure you completely `uninstall 
go <https://golang.org/doc/install#uninstall>`_. After uninstalling go, you can 
install it by following the instructions below.

.. code-block:: bash

    $ export VERSION=1.11.4 OS=linux ARCH=amd64  # change this as you need.

    $ wget https://dl.google.com/go/go${VERSION}.${OS}-${ARCH}.tar.gz && \
        sudo tar -C /usr/local -xzf go${VERSION}.${OS}-${ARCH}.tar.gz

Post installation, you will need to setup your environment for Go.

.. code-block:: bash

    $ echo 'export GOPATH=${HOME}/go' >> ~/.bashrc && \
        echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc && \
        source ~/.bashrc

Download and Build the RPM
--------------------------

Singularity RPM is available on `the Github relese page <https://github.com/sylabs/singularity/releases>`_.

.. code-block:: bash

    $ export VERSION=3.0.2  # this is the singularity version, change as you need

    $ wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
        rpmbuild -tb singularity-${VERSION}.tar.gz

.. _configuing_overview:

----------
Configuing
----------

There are several ways to configure Singularity. The :ref:`main config file 
<singularity-config-file>` is where most of the config are.
But there is also :ref:`localstatedir <localstatedir-configure>`.

.. localstatedir is really a config option at build time. It's not part of the 
.. config in the same way that the singularity.conf file is part of the config.


The config file (``singularity.conf``)
--------------------------------------

The ``singularity.conf`` file defines the global configuration for Singularity 
across the entire system.  By default, it is installed in the following location
(though its location will obviously differ pass options to install Singularity 
or its components in a custom location).

.. code-block:: none

    /usr/local/etc/singularity/singularity.conf

As a security measure, it must be owned by root and must not be writable by 
users or Singularity will refuse to run.  

Here's an example of some of the configurable options:

``ALLOW SETUID``:
    This allows admins to enable/disable users ability to utilize the ``setuid`` 
    program flow within Singularity.    

``MAX LOOP DEVICES``:
    This allows a admins to change the maximum number of loop devices that 
    Singularity can attempt to utilize when mounting containers.

``ALLOW PID NAMESPACE``:
    Allows admins to enable or disable the ``PID`` namespace allowing or
    preventing containerized processes from making entries in the host systems
    pid table.

The ``singularity.conf`` file is well documented and most information can be 
gleaned by consulting it directly. For more information, see the 
:ref:`configuration pages <singularity-config-file>`.

Configuration (``localstatedir``)
---------------------------------

.. please move the section about the localstatedir to be within the installation
.. section above.  See the user docs installation page for an idea of how to do 
.. this.

This should be shorter...

The local state directories used by ``singularity`` at runtime will be placed 
under the supplied ``prefix`` option. This will cause issues if that directory 
tree is read-only or if it is shared between several hosts or nodes that might
run ``singularity`` simultaneously.

In such cases, you should specify the ``localstatedir`` option. This will 
override the ``prefix`` option, instead placing the local state directories 
within the path explicitly provided. Ideally this should be within the local 
filesystem, specific to only a single host or node.

In the case of a cluster, admins must ensure that the localstatedir exists on 
all nodes with ``root:root`` ownership and ``0755`` permissions

.. code-block:: bash

    ${localstatedir}/singularity/mnt

    ${localstatedir}/singularity/mnt/container

    ${localstatedir}/singularity/mnt/final

    ${localstatedir}/singularity/mnt/overlay

    ${localstatedir}/singularity/mnt/session


.. _singularity-architecture:

------------------------
Singularity Architecture
------------------------

Singularity architecture allows the container to be executed as if they were native programs or scripts on a host system.

As a result, integration with schedulers such as Univa Grid Engine, Torque, SLURM, SGE, and many others is as simple as running
any other command. All standard input, output, errors, pipes, IPC, and other communication pathways used by locally running
programs are synchronized with the applications running locally within the container.

.. _singularity-security:

--------------------
Singularity Security
--------------------

Description... Namespace...
Same host inside the container.

Singularity containers can be signed/verified (via PGP key) ensuring a bit-for-bit reproduction of the original container as the author intended it.
