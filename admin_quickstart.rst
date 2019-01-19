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
more information on installation, including alternate installation procedures 
and options for other operating systems, see the `user guide instalation page 
<https://www.sylabs.io/guides/3.0/user-guide/installation.html>`_.

Install Dependencies
--------------------

Before we build the RPM, we need to install some dependencies:

.. code-block:: none

    $ sudo yum -y update && sudo yum -y install \
        wget \
        rpm-build \
        git \
        gcc \
        libuuid-devel \
        openssl-devel \
        libseccomp-devel \
        squashfs-tools


Download and Build the RPM
--------------------------

The Singularity tarball for building the RPM is available on `the Github release 
page <https://github.com/sylabs/singularity/releases>`_.

Go and all other build dependencies will be downloaded automatically just to 
build the RPM, and will then be automatically removed.

.. code-block:: none

    $ export VERSION=3.0.2  # this is the singularity version, change as you need

    $ wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
        rpmbuild -tb singularity-${VERSION}.tar.gz && \
        sudo rpm --install -vh ~/rpmbuild/RPMS/x86_64/singularity-${VERSION}-1.el7.x86_64.rpm && \
        rm -rf ~/rpmbuild singularity-${VERSION}*.tar.gz

Setting ``localstatedir``
-------------------------

The local state directories used by ``singularity`` at runtime will be placed 
under the supplied ``prefix`` option. This will cause issues if that directory 
tree is read-only or if it is shared between several hosts or nodes that might
run ``singularity`` simultaneously.

In such cases, you should specify the ``localstatedir`` option. This will 
override the ``prefix`` option, instead placing the local state directories 
within the path explicitly provided. Ideally this should be within the local 
filesystem, specific to only a single host or node.

In the case of a cluster, admins must ensure that the ``localstatedir`` exists 
on all nodes with ``root:root`` ownership and ``0755`` permissions

.. code-block:: none

    rpmbuild -tb --define='_localstatedir /mnt' singularity-${VERSION}.tar.gz

.. _configuring_overview:

-----------
Configuring
-----------

There are several ways to configure Singularity. The :ref:`main config file 
<singularity-config-file>` is where most of the configuration options are set.


The Config File (``singularity.conf``)
--------------------------------------

The ``singularity.conf`` file defines the global configuration for Singularity 
across the entire system.  By default, it is installed in the following location
(though its location will obviously differ based on options passed by the user
during the Singularity installation).

.. code-block:: none

    /usr/local/etc/singularity/singularity.conf

As a security measure, it must be owned by root and must not be writable by 
users or Singularity will refuse to run.  

Here's an example of some of the configurable options:

``ALLOW SETUID``:
    This allows admins to enable/disable users ability to utilize the ``setuid`` 
    program flow within Singularity.    

``MAX LOOP DEVICES``:
    This allows admins to change the maximum number of loop devices that 
    Singularity can attempt to utilize when mounting containers.

``ALLOW PID NAMESPACE``:
    Allows admins to enable or disable the ``PID`` namespace allowing or
    preventing containerized processes from making entries in the host system's
    pid table.

The ``singularity.conf`` file is well documented and most information can be 
gleaned by consulting it directly. For more information, see the 
:ref:`configuration pages <singularity-config-file>`.

.. _singularity-architecture:

------------------------
Singularity Architecture
------------------------

The architecture of Singularity allows containers to be executed as if they were 
native programs or scripts on a host system.

As a result, integration with schedulers such as Univa Grid Engine, Torque, 
SLURM, SGE, and many others is as simple as running any other command. All 
standard input, output, errors, pipes, IPC, and other communication pathways 
used by locally running programs are synchronized with the applications running 
locally within the container.

.. _singularity-security:

--------------------
Singularity Security
--------------------

Security of the Container Runtime
---------------------------------

The Singularity security model is unique among container platforms. The bottom 
line? **Untrusted users** (those who don't have root access and aren't getting 
it) can run **untrusted containers** (those that have not been vetted by admins) 
**safely**. There are a few pieces of the model to consider.

First, Singularity's design forces a user to have the same UID and GID context
inside and outside of the container. This is accomplished by dynamically writing
entries to ``/etc/passwd`` and ``/etc/groups`` at runtime. This design makes it
trivially easy for a user inside the container to safely read and write data to 
the host system with correct ownership, and it's also a cornerstone of the 
Singularity security context.

Second, Singularity mounts the container file system with the ``nosuid`` flag
and executes processes within the container with the ``PR_SET_NO_NEW_PRIVS``
bit set. Combined with the fact that the user is the same inside and outside of
the container, this prevents a user from escalating privileges. 

Taken together, this design means your users can run whatever containers they 
want, and you don't have to worry about them damaging your precious system.  

Security of the Container Itself
--------------------------------

A malicious container may not be able to damage your system, but it could still 
do harm in the user's space without escalating privileges. 

Starting in Singularity 3.0, containers may be cryptographically signed when
they are built and verified at runtime via PGP keys. This allows a user to 
ensure that a container is a bit-for-bit reproduction of the container produced 
by the original author before they run it. As long as the user trusts the 
individual or company that created the container, they can run the container 
without worrying.

Key signing and verification is made easy using the `Sylabs Keystore 
infrastructure <https://cloud.sylabs.io/keystore>`_. Join the party! And get 
more information about signing and verifying in the `Singularity user guide 
<https://www.sylabs.io/guides/3.0/user-guide/signNverify.html>`_.

.. _updating_singularity:

--------------------
Updating Singularity
--------------------

Updating Singularity is just like installing it, but with the ``--upgrade`` flag 
instead of ``--install``. Make sure you pick the latest tarball from the `Github 
relese page <https://github.com/sylabs/singularity/releases>`_.

.. code-block:: none

    $ export VERSION=3.0.2  # the newest singularity version, change as you need

    $ wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
        rpmbuild -tb singularity-${VERSION}.tar.gz && \
        sudo rpm --upgrade -vh ~/rpmbuild/RPMS/x86_64/singularity-${VERSION}-1.el7.x86_64.rpm && \
        rm -rf ~/rpmbuild singularity-${VERSION}*.tar.gz

.. _uninstalling_singularity:

------------------------
Uninstalling Singularity
------------------------

If you install Singularity using RPM, you can uninstall it again in just a one 
command: (Just use ``sudo``, or do this as root)

.. code-block:: none

    $ sudo rpm --erase singularity

