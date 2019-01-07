Admin Quick Start
=================

This document will cover installation and administration points of Singularity on a Linux host. For all other information, and installation for other OS(s), see the `user guide <https://www.sylabs.io/guides/3.0/user-guide/installation.html>`_.

For any additional help or support contact the
`Sylabs team <https://www.sylabs.io/contact/>`_, or send a email to `support@sylabs.io <mailto:support@sylabs.io>`_.

------------
Installation
------------

This section will explain how to install Singularity from a RPM.

Install Build Dependencies
--------------------------

Singularity requires several libraries and development tools to be installed before you can build the RPM.

.. code-block:: bash

    $ sudo yum update -y && \
        sudo yum groupinstall -y 'Development Tools' && \
        sudo yum install -y \
        openssl-devel \
        libuuid-devel \
        libseccomp-devel \
        wget \
        squashfs-tools

Install Go
----------

Singularity is primarily written in Go, so we will need Go 1.11 or greater build Singularity.

If your updating from a previous go version, click `here for uninstall instructions <https://golang.org/doc/install#uninstall>`_.
After uninstalling go, you can install it by following the instructions below.

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

    $ export VERSION=3.0.1  # this is the singularity version, change as you need

    $ wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
        rpmbuild -tb singularity-${VERSION}.tar.gz

----------
Configuing
----------

Here are some ways to configure Singularity.

The config file
---------------

For full infoation on the config file, check out this :ref:`config tutarial <singularity-config-file>`. (Comming Soon!)

Here are some thinks you can configure:

congifure 1.
    this lets you change...

congifure 2.
    this lets you change...

Configuration (``localstatedir``)
---------------------------------

The local state directories used by ``singularity`` at runtime will be placed under the supplied ``prefix`` option. This will cause issues if that directory tree is read-only or if it is shared between several hosts or nodes that might run ``singularity`` simultaneously.

In such cases, you should specify the ``localstatedir`` option. This will override the ``prefix`` option, instead placing the local state directories within the path explicitly provided. Ideally this should be within the local filesystem, specific to only a single host or node.

In the case of cluster nodes, you will need to create the following directories on all nodes, with ``root:root`` ownership and ``0755`` permissions

.. code-block:: bash

    ${localstatedir}/singularity/mnt

    ${localstatedir}/singularity/mnt/container

    ${localstatedir}/singularity/mnt/final

    ${localstatedir}/singularity/mnt/overlay

    ${localstatedir}/singularity/mnt/session


.. singularity-architecture:

------------------------
Singularity Architecture
------------------------

A quick description of Singularity architecture (no daemon, security context, default namespaces, why architecture works with batch schedulers) with links to appropriate sections.


.. singularity-security:

--------------------
Singularity Security
--------------------


Description

