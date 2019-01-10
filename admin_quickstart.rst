.. _admin-quick-start:

Admin Quick Start
=================

This document will cover installation of Singularity, and all the dependencies. This will also cover an
overview of :ref:`configuing <configuing_overview>`, :ref:`Singularity architecture <singularity-architecture>`,
and :ref:`Singularity security <singularity-security>`.

.. This document will cover installation and administration points of Singularity on a Linux host. This will also cover an
.. overview of :ref:`configuing <configuing_overview>`, :ref:`Singularity architecture <singularity-architecture>`,
.. and :ref:`Singularity security <singularity-security>`.

For all other information, and installation for other OS(s), see
the `user installation guide <https://www.sylabs.io/guides/3.0/user-guide/installation.html>`_.

For any additional help or support contact the
`Sylabs team <https://www.sylabs.io/contact/>`_, or send a email to `support@sylabs.io <mailto:support@sylabs.io>`_.

------------
Installation
------------

This section will explain how to install Singularity from a RPM. If you want more information on installation,
check out our other `instalation page <https://www.sylabs.io/guides/3.0/user-guide/installation.html>`_.

Install Dependencies
--------------------

Singularity requires several libraries in order to function propley. Because we will be installing Singularity from a RPM,
you don't have to install build dependencies.

.. Singularity requires several libraries and development tools to be installed before you can build the RPM. So update,
.. then install all the dependencies:

.. code-block:: bash

    $ sudo yum update -y && \
        sudo yum groupinstall -y 'Development Tools' && \
        sudo yum install -y \
        openssl-devel \
        libuuid-devel \
        libseccomp-devel \
        wget \
        squashfs-tools

.. Install Go
.. ----------
.. 
.. Singularity is primarily written in Go, so we will need Go 1.11 or greater build Singularity.
.. 
.. If your updating from a previous go version, make sure you completely `uninstall go <https://golang.org/doc/install#uninstall>`_.
.. After uninstalling go, you can install it by following the instructions below.
.. 
.. .. code-block:: bash
.. 
..     $ export VERSION=1.11.4 OS=linux ARCH=amd64  # change this as you need.
.. 
..     $ wget https://dl.google.com/go/go${VERSION}.${OS}-${ARCH}.tar.gz && \
..         sudo tar -C /usr/local -xzf go${VERSION}.${OS}-${ARCH}.tar.gz
.. 
.. Post installation, you will need to setup your environment for Go.
.. 
.. .. code-block:: bash
.. 
..     $ echo 'export GOPATH=${HOME}/go' >> ~/.bashrc && \
..         echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc && \
..         source ~/.bashrc
.. 

Download and Build the RPM
--------------------------

Singularity RPM is available on `the Github relese page <https://github.com/sylabs/singularity/releases>`_.

Golang, and all other build dependencies will be downloaded automatically just to build the RPM, then will magically disappear.

.. code-block:: bash

    $ export VERSION=3.0.2  # this is the singularity version, change as you need

    $ wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
        rpmbuild -tb singularity-${VERSION}.tar.gz && \
        sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/singularity-${VERSION}-1.el7.x86_64.rpm && \
        rm -rf ~/rpmbuild singularity-${VERSION}*.tar.gz

.. _configuing_overview:

----------
Configuing
----------

There are sevral ways to configuing Singularity. The :ref:`main config file <singularity-config-file>` is were most of the config are.
But there is also :ref:`localstatedir <localstatedir-configure>`.

The config file (``singularity.conf``)
--------------------------------------

Here are some things you can configure:

``ALLOW SETUID``:
    This lets you change users to utilize the ``setuid`` program flow within Singularity.    

``MAX LOOP DEVICES``:
    This lets you change the maximum number of loop devices that Singularity should ever attempt to utilize.

``ALLOW PID NAMESPACE``:
    This lets you allow users to request the ``PID`` namespace.

For full infoation on the config file, check out this :ref:`config tutarial <singularity-config-file>`. (Comming Soon!)

Configuration (``localstatedir``)
---------------------------------

This should be shorter...

The local state directories used by ``singularity`` at runtime will be placed under the supplied ``prefix`` option.
This will cause issues if that directory tree is read-only or if it is shared between several hosts or nodes that might
run ``singularity`` simultaneously.

In such cases, you should specify the ``localstatedir`` option. This will override the ``prefix`` option, instead placing
the local state directories within the path explicitly provided. Ideally this should be within the local filesystem, specific
to only a single host or node.

In the case of cluster nodes, you will need to create the following directories on all nodes, with ``root:root`` ownership
and ``0755`` permissions

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
