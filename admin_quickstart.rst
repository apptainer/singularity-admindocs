Admin Quick Start
=================

This document will cover installation and administration points of
``Singularity`` on a Linux host. For all other information, see the
`user guide <https://www.sylabs.io/guides/3.0/user-guide/>`_.

For any additional help or support contact the
`Sylabs team <https://www.sylabs.io/contact/>`_.

------------
Installation
------------

This section will explain the process of installing ``Singularity`` from
source and building your own binary packages.

Install Build Dependencies
--------------------------

``Singularity`` requires several libraries and development tools to be
installed before you can build it from source.

.. code-block:: none

    $ sudo yum -y update
    $ sudo yum -y groupinstall "Development Tools"
    $ sudo yum -y install git libseccomp-devel libuuid-devel openssl-devel squashfs-tools wget

.. note:: Both ``squashfs-tools`` and ``libseccomp-devel`` are optional
    dependencies but are required for full functionality.

Install Go
----------

``Singularity`` is written primarily in Go, and you will need Go >= 1.11
installed to build it from source.

.. code-block:: none

    $ export VERSION=1.11 OS=linux ARCH=amd64
    $ wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz
    $ sudo tar -C /usr/local -xzf go$VERSION.$OS-$ARCH.tar.gz

Post installation, you will need to setup your environment for Go.

.. code-block:: none

    $ echo 'export GOPATH=${HOME}/go' >> ~/.bashrc
    $ echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc
    $ source ~/.bashrc

.. note:: You may need to add the path ``/usr/local/go/bin`` to the
    ``secure_path`` option in your ``sudoers`` config.

Download Source
---------------

``Singularity`` source code is available on ``Github``. You can either
download a versioned tarball from the
`releases page <https://github.com/sylabs/singularity/releases>`_ or
clone our ``git`` repository.

After you clone the ``git`` repository, you can optionally ``checkout`` the
``tag`` of a specific version to install (e.g. ``v3.0.1``)

.. code-block:: none

    $ mkdir -p $GOPATH/src/github.com/sylabs
    $ cd $GOPATH/src/github.com/sylabs
    $ git clone https://github.com/sylabs/singularity
    $ git tag --list
    $ git checkout v3.0.1

Configure the Build
-------------------

``Singularity`` uses a custom build system. You will configure the build using
the ``mconfig`` script.

.. note:: You can see all of the options for ``mconfig`` by using the ``-h``
    option.

.. code-block:: none

    $ cd $GOPATH/src/github.com/sylabs/singularity
    $ ./mconfig --prefix=/usr/local --localstatedir=/var

Configuration (``localstatedir``)
---------------------------------

The local state directories used by ``Singularity`` at runtime will be placed
under the supplied ``prefix`` option. This will cause issues if that directory
tree is read-only or if it is shared between several hosts or nodes that might
run ``Singularity`` simultaneously.

In such cases, you should specify the ``localstatedir`` option. This will
override the ``prefix`` option, instead placing the local state directories
within the path explicitly provided. Ideally this should be within the local
filesystem, specific to only a single host or node.

In the case of cluster nodes, you will need to create the following
directories on all nodes, with ``root:root`` ownership and ``0755`` permissions

.. code-block:: none

    ${localstatedir}/singularity/mnt

    ${localstatedir}/singularity/mnt/container

    ${localstatedir}/singularity/mnt/final

    ${localstatedir}/singularity/mnt/overlay

    ${localstatedir}/singularity/mnt/session

Build from Source
-----------------

After you configure the build you can finish building ``Singularity`` from
source.

.. code-block:: none

    $ make -C builddir
    $ sudo make -C builddir install

.. note:: ``Singularity`` must be installed as ``root`` for full functionality.

.. note:: ``Singularity`` must be installed to a file system that allows SUID
    programs for full functionality.

Build an RPM from Source
------------------------

.. note:: This process was greatly improved in version ``3.0.1`` and we suggest
    you use at least that version if you wish to build RPMs.

You will use the ``rpm`` ``Makefile`` target to build a ``Singularity`` RPM.

.. code-block:: none

    $ ./mconfig
    $ make -C builddir rpm

You will find the ``Singularity`` RPMs built in your home directory,
at ``~/rpmbuild/``.

If you would like to further customize the ``Singularity`` installation,
you can instead use the ``dist`` ``Makefile`` target and run ``rpmbuild``
yourself.

.. code-block:: none

    $ ./mconfig
    $ make -C builddir dist
    $ rpmbuild -tb --define="_prefix /opt/singularity" singularity-*.tar.gz
