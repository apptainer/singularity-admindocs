.. _userns:

############################
 User Namespaces & Fakeroot
############################

User namespaces are an isolation feature that allow processes to run
with different user identifiers and/or privileges inside that namespace
than are permitted outside. A user may have a ``uid`` of ``1001`` on a
system outside of a user namespace, but run programs with a different
``uid`` with different privileges inside the namespace.

User namespaces are used with containers to make it possible to setup a
container without privileged operations, and so that a normal user can
act as root inside a container to perform administrative tasks, without
being root on the host outside.

{Singularity} uses user namespaces in 3 situations:

-  When the ``setuid`` workflow is disabled or {Singularity} was
   installed without root.
-  When a container is run with the ``--userns`` option.
-  When ``--fakeroot`` is used to impersonate a root user when building
   or running a container.

.. _userns-requirements:

*****************************
 User Namespace Requirements
*****************************

To allow unprivileged creation of user namespaces a kernel >=3.8 is
required, with >=3.18 being recommended due to security fixes for user
namespaces (3.18 also adds OverlayFS support which is used by
Singularity).

Additionally, some Linux distributions require that unprivileged user
namespace creation is enabled using a ``sysctl`` or kernel command line
parameter. Please consult your distribution documentation or vendor to
confirm the steps necessary to 'enable unprivileged user namespace
creation'.

Debian
======

.. code::

   sudo sh -c 'echo kernel.unprivileged_userns_clone=1 \
       >/etc/sysctl.d/90-unprivileged_userns.conf'
   sudo sysctl -p /etc/sysctl.d /etc/sysctl.d/90-unprivileged_userns.conf

RHEL/CentOS 7
=============

From 7.4, kernel support is included but must be enabled with:

.. code::

   sudo sh -c 'echo user.max_user_namespaces=15000 \
       >/etc/sysctl.d/90-max_net_namespaces.conf'
   sudo sysctl -p /etc/sysctl.d /etc/sysctl.d/90-max_net_namespaces.conf

.. _userns-limitations:

****************************
 Unprivileged Installations
****************************

As detailed in the :ref:`non-setuid installation <install-nonsetuid>`
section, {Singularity} can be compiled or configured with the ``allow
setuid = no`` option in ``singularity.conf`` to not perform privileged
operations using the ``starter-setuid`` binary.

When {Singularity} does not use ``setuid`` all container execution will
use a user namespace. In this mode of operation, some features are not
available, and there are impacts to the security/integrity guarantees
when running SIF container images:

-  All containers must be run from sandbox directories. SIF images are
   extracted to a sandbox directory on the fly, preventing verification
   at runtime, and potentially allowing external modification of the
   container at runtime.

-  Filesystem image, and SIF-embedded persistent overlays cannot be
   used.

-  Encrypted containers cannot be used. {Singularity} mounts encrypted
   containers directly through the kernel, so that encrypted content is
   not extracted to disk. This requires the setuid workflow.

-  Fakeroot functionality will rely on external setuid root
   ``newuidmap`` and ``newgidmap`` binaries which may be provided by the
   distribution.

*****************
 --userns option
*****************

The ``--userns`` option to ``singularity run/exec/shell`` will start a
container using a user namespace, avoiding the setuid privileged
workflow for container setup even if {Singularity} was compiled and
configured to use setuid by default.

The same limitations apply as in an unprivileged installation.

.. _fakeroot:

******************
 Fakeroot feature
******************

Fakeroot (or commonly referred as rootless mode) allows an unprivileged
user to run a container as a **"fake root"** user by leveraging user
namespaces with `user namespace UID/GID mapping
<http://man7.org/linux/man-pages/man7/user_namespaces.7.html>`_.

User namespace UID/GID mapping allows a user to act as a different
UID/GID in the container than they are on the host. A user can access a
configured range of UIDs/GIDs in the container, which map back to
(generally) unprivileged user UIDs/GIDs on the host. This allows a user
to be ``root (uid 0)`` in a container, install packages etc., but have
no privilege on the host.

Requirements
============

In addition to user namespace support, {Singularity} must manipulate
``subuid`` and ``subgid`` maps for the user namespace it creates. By
default this happens transparently in the setuid workflow. With
unprivileged installations of {Singularity} or where ``allow setuid =
no`` is set in ``singularity.conf``, {Singularity} attempts to use
external setuid binaries ``newuidmap`` and ``newgidmap``, so you need to
install those binaries on your system.

Basics
======

Fakeroot relies on ``/etc/subuid`` and ``/etc/subgid`` files to find
configured mappings from real user and group IDs, to a range of
otherwise vacant IDs for each user on the host system that can be
remapped in the user namespace. A user must have an entry in these system
configuration files to use the fakeroot feature. {Singularity} provides
a :ref:`config fakeroot <config-fakeroot>` command to assist in managing
these files, but it is important to understand how they work.

For user ``foo`` an entry in ``/etc/subuid`` might be:

.. code::

   foo:100000:65536

where ``foo`` is the username, ``100000`` is the start of the UID range
that can be used by ``foo`` in a user namespace uid mapping, and
``65536`` number of UIDs available for mapping.

Same for ``/etc/subgid``:

.. code::

   foo:100000:65536

.. note::

   Some distributions add users to these files on installation, or when
   ``useradd``, ``adduser``, etc. utilities are used to manage local
   users.

   The glibc nss name service switch mechanism does not currently
   support managing ``subuid`` and ``subgid`` mappings with external
   directory services such as LDAP. You must manage or provision mapping
   files direct to systems where fakeroot will be used.

.. warning::

   {Singularity} requires that a range of at least ``65536`` IDs is used
   for each mapping. Larger ranges may be defined without error.

   It is also important to ensure that the subuid and subgid ranges
   defined in these files don't overlap with each other, or any real UIDs
   and GIDs on the host system.

So if you want to add another user ``bar``, ``/etc/subuid`` and
``/etc/subgid`` will look like:

.. code::

   foo:100000:65536
   bar:165536:65536

Resulting in the following allocation:

+------+----------+----------------------+
| User | Host UID | Sub UID/GID range    |
+======+==========+======================+
| foo  | 1000     | 100000 to 165535     |
+------+----------+----------------------+
| bar  | 1001     | 165536 to 231071     |
+------+----------+----------------------+

Inside a user namespace / container, ``foo`` and ``bar`` can now act as
any UID/GID between 0 and 65536, but these UIDs are confined to the
container. For ``foo`` UID 0 in the container will map to the host
``foo`` UID ``1000`` and ``1 to 65536`` will map to ``100000-165535``
outside of the container etc. This impacts the ownership of files, which
will have different IDs inside and outside of the container.

.. note::

   If you are managing large numbers of fakeroot mappings you may wish
   to specify users by UID rather than username in the ``/etc/subuid``
   and ``/etc/subgid`` files. The man page for ``subuid`` advises:

   "When large number of entries (10000-100000 or more) are defined in
   /etc/subuid, parsing performance penalty will become noticeable. In
   this case it is recommended to use UIDs instead of login names.
   Benchmarks have shown speed-ups up to 20x."

Filesystem considerations
=========================

Based on the above range, here we can see what happens when the user
``foo`` create files with ``--fakeroot`` feature:

+--------------------------------+----------------------------------+
| Create file with container UID | Created host file owned by UID   |
+================================+==================================+
| 0 (default)                    | 1000                             |
+--------------------------------+----------------------------------+
| 1 (daemon)                     | 100000                           |
+--------------------------------+----------------------------------+
| 2 (bin)                        | 100001                           |
+--------------------------------+----------------------------------+

Outside of the fakeroot container the user may not be able to remove
directories and files created with a subuid, as they do not match with
the user's UID on the host. The user can remove these files by using a
container shell running with fakeroot.

Network configuration
=====================

With fakeroot, users can request a container network named ``fakeroot``,
other networks are restricted and can only be used by the real host root
user. By default the ``fakeroot`` network is configured to use a network
veth pair.

.. warning::

   Do not change the ``fakeroot`` network type in
   ``etc/singularity/network/40_fakeroot.conflist`` without considering
   the security implications.

.. note::

   Unprivileged installations of {Singularity} cannot use ``fakeroot``
   network as it requires privilege during container creation to setup
   the network.

.. _config-fakeroot:

Configuration with ``config fakeroot``
======================================

{Singularity} 3.5 and above provides a ``config fakeroot`` command that
can be used by a root user to administer local system ``/etc/subuid``
and ``/etc/subgid`` files in a simple manner. This allows users to be
granted the ability to use Singularity's fakeroot functionality without
editing the files manually. The ``config fakeroot`` command will
automatically ensure that generated subuid/subgid ranges are an
appropriate size, and do not overlap.

``config fakeroot`` must be run as the ``root`` user, or via ``sudo
singularity config fakeroot`` as the ``/etc/subuid`` and ``/etc/subgid``
files form part of the system configuration, and are security sensitive.
You may ``--add`` or ``--remove`` user subuid/subgid mappings. You can
also ``--enable`` or ``--disable`` existing mappings.

.. note::

   If you deploy {Singularity} to a cluster you will need to make
   arrangements to synchronize ``/etc/subuid`` and ``/etc/subgid``
   mapping files to all nodes.

   At this time, the glibc name service switch functionality does not
   support subuid or subgid mappings, so they cannot be defined in a
   central directory such as LDAP.

Adding a fakeroot mapping
-------------------------

Use the ``-a/--add <user>`` option to ``config fakeroot`` to create new
mapping entries so that ``<user>`` can use the fakeroot feature of
Singularity:

.. code::

   $ sudo singularity config fakeroot --add dave

   # Show generated `/etc/subuid`
   $ cat /etc/subuid
   1000:4294836224:65536

   # Show generated `/etc/subgid`
   $ cat /etc/subgid
   1000:4294836224:65536

The first subuid range will be set to the top of the 32-bit UID
space. Subsequent subuid ranges for additional users will be created
working down from this value. This minimizes the change of overlap
with real UIDs on most systems.

.. note::

   The ``config fakeroot`` command generates mappings specified using
   the user's uid, rather than their username. This is the preferred
   format for faster lookups when configuring a large number of
   mappings, and the command can be used to manipulate these by
   username.

Deleting, disabling, enabling mappings
--------------------------------------

Use the ``-r/--remove <user>`` option to ``config fakeroot`` to
completely remove mapping entries. The ``<user>`` will no longer be able
to use the fakeroot feature of Singularity:

.. code::

   $ sudo singularity config fakeroot --remove dave

.. warning::

   If a fakeroot mapping is removed, the subuid/subgid range may be
   assigned to another user via ``--add``. Any remaining files from the
   prior user that were created with this mapping will be accessible to
   the new user via fakeroot.

The ``-d/--disable`` and ``-e/--enable`` options will comment and
uncomment entries in the mapping files, to temporarily disable and
subsequently re-enable fakeroot functionality for a user. This can be
useful to disable fakeroot for a user, but ensure the subuid/subgid
range assigned to them is reserved, and not re-assigned to a different
user.

.. code::

   # Disable dave
   $ sudo singularity config fakeroot --disable dave

   # Entry is commented
   $ cat /etc/subuid
   !1000:4294836224:65536

   # Enable dave
   $ sudo singularity config fakeroot --enable dave

   # Entry is active
   $ cat /etc/subuid
   1000:4294836224:65536
