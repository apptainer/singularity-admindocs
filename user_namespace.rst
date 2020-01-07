.. _userns:

==========================
User Namespaces & Fakeroot
==========================

User namespaces are an isolation feature that allow processes to run
with different user identifiers and/or privileges inside that
namespace than are permitted outside. A user may have a ``uid`` of
``1001`` on a system outside of a user namespace, but run programs
with a different ``uid`` with different privileges inside the
namespace.

User namespaces are used with containers to make it possible to setup
a container without privileged operations, and so that a normal user
can act as root inside a container to perform administrative tasks,
without being root on the host outside.


Singularity uses user namespaces in 3 situations:

 - When the ``setuid`` workflow is disabled or Singularity was
   installed without root.
 - When a container is run with the ``--userns`` option.
 - When ``--fakeroot`` is used to impersonate a root user when
   building or running a container.

.. _userns-requirements:
   
---------------------------
User Namespace Requirements
---------------------------

To allow unprivileged creation of user namespaces a kernel >=3.8 is
required, with >=3.18 being recommended as it adds OverlayFS support.

Additionally, some Linux distributions require that unprivileged user
namespace creation is enabled using a ``sysctl`` or kernel command
line parameter. Please consult your distribution documentation or
vendor to confirm the steps necessary to 'enable unprivileged user
namespace creation'.

Debian
======

.. code-block:: none

  sudo sysctl -w kernel.unprivileged_userns_clone=1

RHEL/CentOS 7
=============

From 7.4, kernel support is included but must be enabled with:

.. code-block:: none

  echo 10000 > /proc/sys/user/max_user_namespaces


.. _userns-limitations:
  
--------------------------
Unprivileged Installations  
--------------------------

As detailed in the :ref:`non-setuid installation <install-nonsetuid>`
section, Singularity can be compiled or configured with the ``allow
setuid = no`` option in ``singularity.conf`` to not perform privileged
operations using the ``starter-setuid`` binary.

When singularity does not use ``setuid`` all container execution will
use a user namespace. In this mode of operation, some features are not
available, and there are impacts to the security/integrity guarantees
when running SIF container images:

 - All containers must be run from sandbox directories. SIF images are
   extracted to a sandbox directory on the fly, preventing
   verification at runtime, and potentially allowing external
   modification of the container at runtime.
 - Filesystem image, and SIF-embedded persistent overlays cannot be
   used.
 - Encrypted containers cannot be used. Singularity mounts encrypted
   containers directly through the kernel, so that encrypted content
   is not extracted to disk. This requires the setuid workflow.
 - Fakeroot functionality will rely on external setuid root
   ``newuidmap`` and ``newgidmap`` binaries which may be provided by
   the distribution.

---------------
--userns option
---------------

The ``--userns`` option to `singularity run/exec/shell` will start a
container using a user namespace, avoiding the setuid privileged
workflow for container setup even if Singularity was compiled and
configured to use setuid by default.

The same limitations apply as in an unprivileged installation.

.. _fakeroot:

----------------
Fakeroot feature
----------------

Fakeroot (or commonly referred as rootless mode) allows an
unprivileged user to run a container as a **"fake root"** user by
leveraging user namespaces with `user namespace UID/GID mapping
<http://man7.org/linux/man-pages/man7/user_namespaces.7.html>`_.

User namespace UID/GID mapping allows a user to act as a different
UID/GID in the container than they are on the host. A user can access
a configured range of UIDs/GIDs in the container, which map back to
(generally) unprivileged user UIDs/GIDs on the host. This allows a
user to be ``root (uid 0)`` in a container, install packages etc., but
have no privilege on the host.

Requirements
============

In addition to user namespace support, Singularity must manipulate
``subuid`` and ``subgid`` maps for the user namepsace it creates. By
default this happens transparently in the setuid workflow. With
unprivileged installations of Singularity or where ``allow setuid =
no`` is set in ``singularity.conf``, Singularity attempts to use
external setuid binaries ``newuidmap`` and ``newgidmap``, so you
need to install those binaries on your system.

.. note::

  CentOS/RHEL 7 doesn't provide a package for ``newuidmap`` and
  ``newgidmap``, so you will need to compile/install **shadow-utils**
  by yourself.
  
  Singularity expects to find these binaries in one of those standard
  paths:
  ``/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin``


Basics
======

Fakeroot relies on ``/etc/subuid`` and ``/etc/subgid`` files to find
configured mappings from real user and group IDs, to a range of
otherwise vacant IDs for each user on the host system that can be
remapped in the usernamespace. A user must have an entry in these
system configuration files to use the fakeroot feature.

For user ``foo`` an entry in ``/etc/subuid`` might be:

.. code-block:: none

  foo:100000:65536

where ``foo`` is the username, ``100000`` is the start of the UID
range that can be used by ``foo`` in a user namespace uid mapping, and
``65536`` number of UIDs available for mapping.

Same for ``/etc/subgid``:

.. code-block:: none

  foo:100000:65536

.. note::

  Some distributions add users to these files on installation, or when
  ``useradd``, ``adduser``, etc. utilities are used to manage local
  users.

  The glibc nss name service switch mechanism does not currently
  support managing ``subuid`` and ``subgid`` mappings with external
  directory services such as LDAP. You must manage or provision
  mapping files direct to systems where fakeroot will be used.

.. warning::

  Singularity requires that a range of at least ``65536`` IDs is used
  for each mapping. Larger ranges may be defined without error.

  It is also important to ensure that the subuid and subgid ranges
  defined in these files don't overlap with any real UIDs and GIDs on
  the host system.

So if you want to add another user ``bar``, ``/etc/subuid`` and
``/etc/subgid`` will look like:

.. code-block:: none

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

Inside a user namespace / container, ``foo`` and ``bar`` can now act
as any UID/GID between 0 and 65536, but these UIDs are confined to the
container. For ``foo`` UID 0 in the container will map to ``100000``
outside of the container etc. This impacts the ownership of files,
which will have different IDs inside and outside of the container.


Filesystem consideration
========================

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


Network configurations
======================

With fakeroot, users can request a container network named
``fakeroot``, other networks are restricted and can only be used by
the real host root user. By default the ``fakeroot`` network is
configured to use a network veth pair.

.. warning::

   Do not change the ``fakeroot`` network type in
   ``etc/singularity/network/40_fakeroot.conflist`` without
   considering the security implications.

.. note::

  Unprivileged installations of Singularity cannot use ``fakeroot``
  network as it requires privilege during container creation to setup
  the network.

.. _updating_singularity:
