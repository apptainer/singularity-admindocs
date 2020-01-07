=================
Admin Quick Start
=================

This document will cover installation and administration points of Singularity
on a Linux host. This will also cover an overview of :ref:`configuring
Singularity <configuring_overview>`, :ref:`Singularity architecture
<singularity-architecture>`, and :ref:`the Singularity security model <singularity-security>`.

For any additional help or support contact the
`Sylabs team <https://www.sylabs.io/contact/>`_, or send a email to
`support@sylabs.io <mailto:support@sylabs.io>`_.

------------
Installation
------------

This section will explain how to install Singularity from an RPM. If you want
more information on installation, including alternate installation procedures
and options for other operating systems, see the `user guide installation page
<https://www.sylabs.io/guides/\{userversion\}/user-guide/installation.html>`_.

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
        squashfs-tools \
        epel-release
    $ sudo yum -y install golang


Download and Build the RPM
--------------------------

The Singularity tarball for building the RPM is available on `the Github release
page <https://github.com/sylabs/singularity/releases>`_.

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

-------------
Configuration
-------------

There are several ways to configuring Singularity. Head over to the
:ref:`Configuration files <singularity_configfiles>` section where most of the
conf files and setting of configuration options are discussed.

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
<https://www.sylabs.io/guides/\{userversion\}/user-guide/signNverify.html>`_.

Administrator Control of Users' Containers
------------------------------------------

Singularity provides several ways for administrators to control the specific
containers that users can run.

* Admins can set directives in the ``singularity.conf`` file to limit container access.

	* `limit container owners`: Only allow containers to be used when they are owned by a given user (default empty)
	* `limit container groups`: Only allow containers to be used when they are owned by a given group (default empty)
	* `limit container paths`: Only allow containers to be used that are located within an allowed path prefix (default empty)
	* `allow container squashfs`: Limit usage of image containing squashfs filesystem (default yes)
	* `allow container extfs`: Limit usage of image containing ext3 filesystem (default yes)
	* `allow container dir`: Limit usage of directory image (default yes)

* Admins can also whitelist or blacklist containers through the ECL (Execution Control List) located in ``ecl.toml``. This method is available in >=3.0:

    This file describes execution groups in which SIF (default format since 3.0) images are checked for authorized loading/execution. The decision is made by validating both the location of the SIF file and by checking against a list of signing entities.

Fakeroot feature
----------------

Fakeroot (or commonly referred as rootless mode) allows an unprivileged user to run a container
as a **"fake root"** user by leveraging `user namespace UID/GID mapping <http://man7.org/linux/man-pages/man7/user_namespaces.7.html>`_.

.. note:: 

	This feature requires a Linux kernel >= 3.8, but the recommended version is >= 3.18


Some distributions doesn't enable user namespace by default, so you will need to enable
it to use fakeroot:

.. code-block:: none

  $ sudo sysctl -w user.max_user_namespaces=10000

.. note::

  If the above command doesn't work, please refer to the documentation of your
  distribution documentation to figure out how to enable user namespace

For unprivileged installation of Singularity or if ``allow setuid = no`` is set in ``singularity.conf``,
Singularity attempts to use external **setuid binaries** ``newuidmap`` and ``newgidmap``, so you need to
install those binaries on your system.

.. note::

  CentOS/RHEL 7 doesn't provide package for ``newuidmap`` and ``newgidmap``, so you will need to
  compile/install **shadow-utils** by yourself.
  
  Singularity expect to find those binaries in one of those standard paths:
  ``/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin``


Basics
======

Fakeroot relies on ``/etc/subuid`` and ``/etc/subgid`` to find the use fakeroot mappings, which
means that users added in those files could use the fakeroot feature, user mappings must be added
in files ``/etc/subuid`` and ``/etc/subgid``, here a valid entry for user ``foo``:

For ``/etc/subuid``:

.. code-block:: none

  foo:100000:65536

where ``foo`` is the username, ``100000`` is the start of UID range and ``65536`` the range count.

Same for ``/etc/subgid``:

.. code-block:: none

  foo:100000:65536

where ``foo`` is the username, ``100000`` is the start of GID range and ``65536`` the range count.

.. note::

  Some distributions already adds the main user by default in those files.

.. warning::

  All entries with a range count different from 65536 are not considered valid
  by Singularity.

  It's also important to ensure that the start range doesn't overlap with existing
  UID/GID on your system.

So if you want to add another user ``bar``, ``/etc/subuid`` and ``/etc/subgid`` will look like:

.. code-block:: none

  foo:100000:65536
  bar:165536:65536

Resulting in the following allocation:

+------+----------+----------------------+
| User | Host UID | UID/GID range        |
+======+==========+======================+
| foo  | 1000     | 100000 to 165535     |
+------+----------+----------------------+
| bar  | 1001     | 165536 to 231071     |
+------+----------+----------------------+

It allows unprivileged users to change current UID/GID to any UID/GID between 0 and 65536 inside container.
It also impacts files and directories ownership depending of UID/GID set in container during file/directory
creation.

Filesystem consideration
========================

Based on the above range, here we can see what happens when the user ``foo`` create files with ``--fakeroot``
feature:

+--------------------------------+----------------------------------+
| Create file with container UID | Created host file owned by UID   |
+================================+==================================+
| 0 (default)                    | 1000                             |
+--------------------------------+----------------------------------+
| 1 (daemon)                     | 100000                           |
+--------------------------------+----------------------------------+
| 2 (bin)                        | 100001                           |
+--------------------------------+----------------------------------+

Network consideration
=====================

With fakeroot, users can request a container network named ``fakeroot``, other networks are restricted and
can only be used by root user. This network is configured to use a network veth pair, it's strongly advised
to not change the network type in ``network/40_fakeroot.conflist`` file for security reasons.

.. warning::

  Unprivileged installation could not use ``fakeroot`` network as it requires privileges to setup the network.

.. _updating_singularity:

--------------------
Updating Singularity
--------------------

Updating Singularity is just like installing it, but with the ``--upgrade`` flag
instead of ``--install``. Make sure you pick the latest tarball from the `Github
release page <https://github.com/sylabs/singularity/releases>`_.

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
