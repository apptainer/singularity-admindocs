.. _singularity_configfiles:

=================================
{Singularity} Configuration Files
=================================

As a {Singularity} Administrator, you will have access to various configuration
files, that will let you manage container resources, set security restrictions
and configure network options etc, when installing {Singularity} across the system.
All these files can be found in ``/usr/local/etc/singularity`` by default (though
its location will obviously differ based on options passed during the
installation). This page will describe the following configuration files and
the various parameters contained by them. They are usually self documenting
but here are several things to pay special attention to:

----------------
singularity.conf
----------------
Most of the configuration options are set using the file ``singularity.conf``
that defines the global configuration for {Singularity} across the entire system.
Using this file, system administrators can have direct say as to what functions
the users can utilize. As a security measure, for ``setuid`` installations of
{Singularity} it must be owned by root and must not be writable by users or
{Singularity} will refuse to run. This is not the case for ``non-setuid``
installations that will only ever execute with user priviledge and thus do not
require such limitations. The options for this configuration are listed below.
Options are grouped together based on relevance, the order of options within
``singularity.conf`` differs.

Setuid and Capabilities
=======================

``ALLOW SETUID``:
To use all features of {Singularity} containers, {Singularity} will need to have
access to some privileged system calls. One way {Singularity} achieves this is by
using binaries with the ``setuid`` bit enabled. This variable lets you
enable/disable users ability to utilize these binaries within {Singularity}. By
default, it is set to "yes", but when disabled, various {Singularity} features
will not function. Please see
:ref:`Unprivileged Installations <userns-limitations>` for more information
about running {Singularity} without ``setuid`` enabled.

``ROOT DEFAULT CAPABILITIES``:
{Singularity} allows the specification of capabilities kept by the root user
when running a container by default. Options include:

* full: all capabilities are maintained, this gives the same behavior as the ``--keep-privs`` option.
* file: only capabilities granted in ``/usr/local/etc/singularity/capabilities/user.root`` are maintained.
* no: no capabilities are maintained, this gives the same behavior as the ``--no-privs`` option.

.. note::

  The root user can manage the capabilities granted to individual containers when they
  are launched through the ``--add-caps`` and ``drop-caps`` flags.
  Please see `Linux Capabilities <\{userdocs\}/security_options.html#linux-capabilities>`_
  in the user guide for more information.

Loop Devices
============

{Singularity} uses loop devices to facilitate the mounting of container
filesystems from SIF images.

``MAX LOOP DEVICES``:
This option allows an admin to limit the total number of loop devices
{Singularity} will consume at a given time.

``SHARED LOOP DEVICES``:
This allows containers running the same image to share a single loop device.
This minimizes loop device usage and helps optimize kernel cache usage.
Enabling this feature can be particularly useful for MPI jobs.

Namespace Options
=================

``ALLOW PID NS``:
This option determines if users can leverage the PID namespace when running
their containers through the ``--pid`` flag.

.. note::
  For some HPC systems, using the PID namespace has the potential of confusing
  some resource managers as well as some MPI implementations.

Configuration Files
===================

{Singularity} allows for the automatic configuration of several system
configuration files within containers to ease usage across systems.

.. note::

  These options will do nothing unless the file or directory path exists within
  the container or {Singularity} has either overlay or underlay support enabled.

``CONFIG PASSWD``:
This option determines if {Singularity} should automatically append an entry to
``/etc/passwd`` for the user running the container.

``CONFIG GROUP``:
This option determines if {Singularity} should automatically append the calling
user's group entries to the containers ``/etc/group``.

``CONFIG RESOLV_CONF``:
This option determines if {Singularity} should automatically bind the host's
``/etc/resolv/conf`` within the container.

Session Directory and System Mounts
===================================

``SESSIONDIR MAX SIZE``:
In order for the {Singularity} runtime to create a container it needs to create a
``sessiondir`` to manage various components of the container, including
mounting filesystems over the base image filesystem. This option
specifies how large the default ``sessiondir`` should be (in MB) and will
only affect users who use the ``--contain`` options without also specifying a
location to perform default read/writes to via the ``--workdir`` or ``--home``
options.

``MOUNT PROC``:
This option determines if {Singularity} should automatically bind mount ``/proc``
within the container.

``MOUNT SYS``:
This option determines if {Singularity} should automatically bind mount ``/sys``
within the container.

``MOUNT DEV``:
Should be set to "YES", if you want {Singularity} to automatically bind mount
`/dev` within the container. If set to 'minimal', then only 'null', 'zero',
'random', 'urandom', and 'shm' will be included.

``MOUNT DEVPTS``:
This option determines if {Singularity} will mount a new instance of ``devpts``
when there is a ``minimal`` ``/dev`` directory as explained above, or when the
``--contain`` option is passed.

.. note::
  This requires either a kernel configured with
  ``CONFIG_DEVPTS_MULTIPLE_INSTANCES=y``, or a kernel version at or newer than
  ``4.7``.

``MOUNT HOME``:
When this option is enabled, {Singularity} will automatically determine the
calling user's home directory and attempt to mount it into the container.

``MOUNT TMP``:
When this option is enabled, {Singularity} will automatically bind mount
``/tmp`` and ``/var/tmp`` into the container from the host. If the
``--contain`` option is passed, {Singularity} will create both locations within
the ``sessiondir`` or within the directory specified by the ``--workdir``
option if that is passed as well.

``MOUNT HOSTFS``:
This option will cause {Singularity} to probe the host for all mounted
filesystems and bind those into containers at runtime.

``MOUNT SLAVE``:
{Singularity} automatically mounts a handful host system directories to the
container by default. This option determines if filesystem changes on the host
should automatically be propogated to those directories in the container.

.. note::
  This should be set to ``yes`` when autofs mounts in the system should
  show up in the container.

``MEMORY FS TYPE``:
This option allows admins to choose the temporary filesystem used by
{Singularity}. Temporary filesystems are primarily used for system
directories like ``/dev`` when the host system directory is not mounted
within the container.

.. note::

  For Cray CLE 5 and 6, up to CLE 6.0.UP05, there is an issue (kernel panic) when Singularity
  uses tmpfs, so on affected systems it's recommended to set this value to ramfs to avoid a
  kernel panic

Bind Mount Management
=====================

``BIND PATH``:
This option is used for defining a list of files or directories to
automatically be made available when {Singularity} runs a container.
In order to successfully mount listed paths the file or directory path must
exist within the container, or {Singularity} has either overlay or underlay
support enabled.

.. note::
  This option is ignored when containers are invoked with the ``--contain`` option.

You can define the a bind point where the source and destination are identical:

.. code-block:: none

  bind path = /etc/localtime

Or you can specify different source and destination locations using:

.. code-block:: none

  bind path = /etc/singularity/default-nsswitch.conf:/etc/nsswitch.conf


``USER BIND CONTROL``:
This allows admins to decide if users can define bind points at runtime.
By Default, this option is set to ``YES``, which means users can specify bind
points, scratch and tmp locations.

Limiting Container Execution
============================

There are several ways to limit container execution as an admin listed below.
If stricter controls are required, check out the
:ref:`Execution Control List <execution_control_list>`.

``LIMIT CONTAINER OWNERS``:
This restricts container execution to only allow conatiners that are owned by
the specified user.

.. note::

  This feature will only apply when {Singularity} is running in SUID mode and the
  user is non-root. By default this is set to `NULL`.

``LIMIT CONTAINER GROUPS``:
This restricts container execution to only allow conatiners that are owned by
the specified group.

.. note::

  This feature will only apply when {Singularity} is running in SUID mode and the
  user is non-root. By default this is set to `NULL`.

``LIMIT CONTAINER PATHS``:
This restricts container execution to only allow containers that are located
within the specified path prefix.

.. note::

  This feature will only apply when {Singularity} is running in SUID mode and the
  user is non-root. By default this is set to `NULL`.

``ALLOW CONTAINER ${TYPE}``:
This option allows admins to limit the types of image formats that can be
leveraged by users with {Singularity}. Formats include ``squashfs`` which is used
by SIF and v2.x Singularity images, ``extfs`` which is used for writable
overlays and some legacy Singularity images, ``dir`` which is used by sandbox
images and ``encrypted`` which is only used by SIF images to encrypt filesystem
contents.

.. note::
  These limitations do not apply to the root user.

Networking Options
==================

The ``--network`` option can be used to specify a CNI networking
configuration that will be used when running a container with `network
virtualization
<\{userdocs\}/networking.html>`_. Unrestricted
use of CNI network configurations requires root privilege, as certain
configurations may disrupt the host networking environment.

{Singularity} 3.8 allows specific users or groups to be granted the
ability to run containers with adminstrator specified CNI
configurations.

``ALLOW NET USERS``:
Allow specified root administered CNI network configurations to be used by the
specified list of users. By default only root may use CNI configuration,
except in the case of a fakeroot execution where only 40_fakeroot.conflist
is used. This feature only applies when {Singularity} is running in
SUID mode and the user is non-root.

``ALLOW NET GROUPS``:
Allow specified root administered CNI network configurations to be used by the
specified list of users. By default only root may use CNI configuration,
except in the case of a fakeroot execution where only 40_fakeroot.conflist
is used. This feature only applies when {Singularity} is running in
SUID mode and the user is non-root.

``ALLOW NET NETWORKS``:
Specify the names of CNI network configurations that may be used by users and
groups listed in the allow net users / allow net groups directives. Thus feature
only applies when {Singularity} is running in SUID mode and the user is non-root.


GPU Options
===========

{Singularity} provides integration with GPUs in order to facilitate GPU based
workloads seamlessly. Both options listed below are particularly useful in
GPU only environments. For more information on using GPUs with Singularity
checkout :ref:`GPU Library Configuration <gpu_library_configuration>`.

``ALWAYS USE NV ${TYPE}``:
Enabling this option will cause every action command
(``exec/shell/run/instance``) to be executed with the ``--nv`` option
implicitly added.

``ALWAYS USE ROCM ${TYPE}``:
Enabling this option will cause every action command
(``exec/shell/run/instance``) to be executed with the ``--rocm`` option
implicitly added.

Supplemental Filesystems
========================

``ENABLE FUSEMOUNT``:
This will allow users to mount fuse filesystems inside containers using the
``--fusemount`` flag.

``ENABLE OVERLAY``:
This option will allow {Singularity} to create bind mounts at paths that do not
exist within the container image. This option can be set to ``try``, which will
try to use an overlayfs. If it fails to create an overlayfs in this case the
bind path will be silently ignored.

``ENABLE UNDERLAY``:
This option will allow {Singularity} to create bind mounts at paths that do not
exist within the container image, just like ``ENABLE OVERLAY``, but instead
using an underlay. This is suitable for systems where overlay is not possible
or not working. If the overlay option is available and working, it will be
used instead.

External Tooling Paths
======================

Internally, {Singularity} leverages several pieces of tooling in order to provide
a wide breadth of features for users. Locations for these tools can be
customized by system admins and referenced with the options below:

``CNI CONFIGURATION PATH``:
This option allows admins to specify a custom path for the CNI configuration
that {Singularity} will use for `Network Virtualization <\{userdocs\}/networking.html>`_.

``CNI PLUGIN PATH``:
This option allows admins to specify a custom path for {Singularity} to access
CNI plugin executables. Check out the `Network Virtualization <\{userdocs\}/networking.html>`_
section of the user guide for more information.

``MKSQUASHFS PATH``:
This allows an admin to specify the location of ``mksquashfs`` if it is not
installed in a standard location. If set, ``mksquashfs`` at this path will be
used instead of a ``mksquashfs`` found in ``PATH``.

``CRYPTSETUP PATH``:
The location for ``cryptsetup`` is recorded by {Singularity} at build time and
will use that value if this is undefined. This option allows an admin to set
the path of ``cryptsetup`` if it is located in a custom location and will
override the value recorded at build time.

Updating Configuration Options
==============================

In order to manage this configuration file, {Singularity} has a ``config global``
command group that allows you to get, set, reset, and unset values through the
CLI. It's important to note that these commands must be run with elevated
priveledges because the ``singularity.conf`` can only be modified by an
administrator.

Example
-------

In this example we will changing the ``BIND PATH`` option described above.
First we can see the current list of bind paths set within our system
configuration:

.. code-block:: none

  $ sudo singularity config global --get "bind path"
  /etc/localtime,/etc/hosts

Now we can add a new path and verify it was successfully added:

.. code-block:: none

  $ sudo singularity config global --set "bind path" /etc/resolv.conf
  $ sudo singularity config global --get "bind path"
  /etc/resolv.conf,/etc/localtime,/etc/hosts

From here we can remove a path with:

.. code-block:: none

  $ sudo singularity config global --unset "bind path" /etc/localtime
  $ sudo singularity config global --get "bind path"
  /etc/resolv.conf,/etc/hosts

If we want to reset the option to the default at installation, then we can
reset it with:

.. code-block:: none

  $ sudo singularity config global --reset "bind path"
  $ sudo singularity config global --get "bind path"
  /etc/localtime,/etc/hosts

And now we are back to our original option settings. You can also test what a
change would look like by using the ``--dry-run`` option in conjunction with
the above commands. Instead of writing to the configuration file, it will
output what would have been written to the configuration file if the command
had been run without the ``--dry-run`` option:

.. code-block:: none

  $ sudo singularity config global --dry-run --set "bind path" /etc/resolv.conf
  # SINGULARITY.CONF
  # This is the global configuration file for Singularity. This file controls
  [...]
  # BIND PATH: [STRING]
  # DEFAULT: Undefined
  # Define a list of files/directories that should be made available from within
  # the container. The file or directory must exist within the container on
  # which to attach to. you can specify a different source and destination
  # path (respectively) with a colon; otherwise source and dest are the same.
  # NOTE: these are ignored if singularity is invoked with --contain.
  bind path = /etc/resolv.conf
  bind path = /etc/localtime
  bind path = /etc/hosts
  [...]
  $ sudo singularity config global --get "bind path"
  /etc/localtime,/etc/hosts

Above we can see that ``/etc/resolv.conf`` is listed as a bind path in the
output of the ``--dry-run`` command, but did not affect the actual bind paths
of the system.

------------
cgroups.toml
------------

Cgroups or Control groups let you implement metering and limiting on the
resources used by processes. You can limit memory, CPU. You can block IO,
network IO, set SEL permissions for device nodes etc.

.. note::

  The ``--apply-cgroups`` option can only be used with root privileges.

Examples
========

When you are limiting resources, apply the settings in the TOML file by using
the path as an argument to the ``--apply-cgroups`` option like so:

.. code-block:: none

  $ sudo singularity shell --apply-cgroups /path/to/cgroups.toml my_container.sif


Limiting memory
===============
To limit the amount of memory that your container uses to 500MB (524288000 bytes):

.. code-block:: none

  [memory]
      limit = 524288000

Start your container like so:

.. code-block:: none

  $ sudo singularity instance start --apply-cgroups path/to/cgroups.toml my_container.sif instance1

After that, you can verify that the container is only using 500MB of memory.
(This example assumes that ``instance1`` is the only running instance.)

.. code-block:: none

  $ cat /sys/fs/cgroup/memory/singularity/*/memory.limit_in_bytes
    524288000

Do not forget to stop your instances after configuring the options.

Similarly, the remaining examples can be tested by starting instances and
examining the contents of the appropriate subdirectories of ``/sys/fs/cgroup/``.

Limiting CPU
============

Limit CPU resources using one of the following strategies. The ``cpu`` section
of the configuration file can limit memory with the following:

**shares**

This corresponds to a ratio versus other cgroups with cpu shares. Usually the
default value is ``1024``. That means if you want to allow to use 50% of a
single CPU, you will set ``512`` as value.

.. code-block:: none

  [cpu]
      shares = 512

A cgroup can get more than its share of CPU if there are enough idle CPU cycles
available in the system, due to the work conserving nature of the scheduler, so
a contained process can consume all CPU cycles even with a ratio of 50%. The
ratio is only applied when two or more processes conflicts with their needs of
CPU cycles.

**quota/period**

You can enforce hard limits on the CPU cycles a cgroup can consume, so
contained processes can't use more than the amount of CPU time set for the
cgroup. ``quota`` allows you to configure the amount of CPU time that a cgroup
can use per period. The default is 100ms (100000us). So if you want to limit
amount of CPU time to 20ms during period of 100ms:

.. code-block:: none

  [cpu]
      period = 100000
      quota = 20000

**cpus/mems**

You can also restrict access to specific CPUs and associated memory nodes by
using ``cpus/mems`` fields:

.. code-block:: none

  [cpu]
      cpus = "0-1"
      mems = "0-1"

Where container has limited access to CPU 0 and CPU 1.

.. note::

  It's important to set identical values for both ``cpus`` and ``mems``.


Limiting IO
===========

You can limit and monitor access to I/O for block devices.  Use the
``[blockIO]`` section of the configuration file to do this like so:

.. code-block:: none

  [blockIO]
      weight = 1000
      leafWeight = 1000

``weight`` and ``leafWeight`` accept values between ``10`` and ``1000``.

``weight`` is the default weight of the group on all the devices until and
unless overridden by a per device rule.

``leafWeight`` relates to weight for the purpose of deciding how heavily to
weigh tasks in the given cgroup while competing with the cgroup's child
cgroups.

To override ``weight/leafWeight`` for ``/dev/loop0`` and ``/dev/loop1`` block
devices you would do something like this:

.. code-block:: none

  [blockIO]
      [[blockIO.weightDevice]]
          major = 7
          minor = 0
          weight = 100
          leafWeight = 50
      [[blockIO.weightDevice]]
          major = 7
          minor = 1
          weight = 100
          leafWeight = 50

You could limit the IO read/write rate to 16MB per second for the ``/dev/loop0``
block device with the following configuration.  The rate is specified in bytes
per second.

.. code-block:: none

  [blockIO]
      [[blockIO.throttleReadBpsDevice]]
          major = 7
          minor = 0
          rate = 16777216
      [[blockIO.throttleWriteBpsDevice]]
          major = 7
          minor = 0
          rate = 16777216

.. _execution_control_list:

--------
ecl.toml
--------

The execution control list is defined here. You can authorize the containers by
validating both the location of the SIF file in the filesystem and by
checking against a list of signing entities.

.. code-block:: none

  [[execgroup]]
    tagname = "group2"
    mode = "whitelist"
    dirpath = "/tmp/containers"
    keyfp = ["7064B1D6EFF01B1262FED3F03581D99FE87EAFD1"]

Only the containers running from and signed with above-mentioned path and keys
will be authorized to run.

Three possible list modes you can choose from:

**Whitestrict**: The SIF must be signed by *ALL* of the keys mentioned.

**Whitelist**: As long as the SIF is signed by one or more of the keys, the
container is allowed to run.

**Blacklist**: Only the containers whose keys are not mentioned in the group
are allowed to run.

.. note::

    The ECL checks will use the new signature format introduced in
    {Singularity} 3.6.0. Containers signed with older versions of Singularity
    {Singularity} will not pass ECL checks.

    To temporarily permit the use of legacy insecure signatures, set
    ``legacyinsecure = true`` in ``ecl.toml``.

Managing ECL public keys
========================

In {Singularity} 3.6, public keys associated with fingerprints specified in ECL rules
were required to be present in user's local keyring which is not very
convenient. {Singularity} 3.7.0 provides a mechanism to administrators for managing
a global keyring that ECL uses during signature verification, for that purpose a
``--global`` option was added for:

  * ``singularity key import`` (root user only)
  * ``singularity key pull`` (root user only)
  * ``singularity key remove`` (root user only)
  * ``singularity key export``
  * ``singularity key list``

.. note::
    For security reasons, it is not possible to import private keys
    into this global keyring because it must be accessible by users
    and is stored in the file ``SYSCONFDIR/singularity/global-pgp-public``.

.. _gpu_library_configuration:

-------------------------
GPU Library Configuration
-------------------------

When a container includes a GPU enabled application, {Singularity} (with
the ``--nv`` or ``--rocm`` options) can properly inject the required
Nvidia or AMD GPU driver libraries into the container, to match the
host's kernel. The GPU ``/dev`` entries are provided in containers run
with ``--nv`` or ``--rocm`` even if the ``--contain`` option is used
to restrict the in-container device tree.

Compatibility between containerized CUDA/ROCm/OpenCL applications and
host drivers/libraries is dependent on the versions of the GPU compute
frameworks that were used to build the applications. Compatibility and
usage information is discussed in the `GPU Support` section of the
`user guide
<\{userdocs\}>`__


NVIDIA GPUs / CUDA
==================

By default, the ``nvliblist.conf`` configuration file is used to
specify libraries and executables that need to be injected into the
container when running {Singularity} with the ``--nv`` Nvidia GPU
support option. The provided ``nvliblist.conf`` is suitable for CUDA
11, but may need to be modified if you need to include additional
libraries, or further libraries are added to newer versions of the
Nvidia driver/CUDA distribution.

When adding new entries to ``nvliblist.conf`` use the bare filename of
executables, and the ``xxxx.so`` form of libraries. Libraries are
resolved via ``ldconfig -p``, and exectuables are found by searching
``$PATH``.

Experimental nvidia-container-cli Support
-----------------------------------------

The `nvidia-container-cli
<https://github.com/NVIDIA/libnvidia-container>`_ tool is Nvidia's
officially support method for configuring containers to use a GPU. It
is targeted at OCI container runtimes.

{Singularity} 3.9 introduces an experimental ``--nvccli`` option,
which will call out to ``nvidia-container-cli`` for container GPU
setup, rather than use the ``nvliblist.conf`` approach.

To use ``--nvccli`` a root-owned ``nvidia-container-cli`` binary must
be present on the host. The binary that is run is controlled by the
``nvidia-container-cli`` directive in ``singularity.conf``. During
installation of {Singularity}, the ``./mconfig`` step will set the
correct value in ``singularity.conf`` if ``nvidia-container-cli`` is
found on the ``$PATH``. If the value of ``nvidia-container-cli path`` is
empty, {Singularity} will look for the binary on ``$PATH`` at runtime.

.. note::

   To prevent use of ``nvidia-container-cli`` via the ``--nvccli``
   flag, you may set ``nvidia-container-cli path`` to ``/bin/false``
   in ``singularity.conf``.

``nvidia-container-cli`` is run as the ``root`` user during setuid
operation of {Singularity}. The container starter process grants a
number of Linux capabilities to ``nvidia-container-cli``, which are
required for it to configure the container for GPU operation. The
operations performed by ``nvidia-container-cli`` are broadly similar
to those which {Singularity} carries out when setting up a GPU
container from ``nvliblist.conf``.

AMD Radeon GPUs / ROCm
======================

The ``rocmliblist.conf`` file is used to specify libraries and
executables that need to be injected into the container when running
{Singularity} with the ``--rocm`` Radeon GPU support option. The provided
``rocmliblist.conf`` is suitable for ROCm 4.0, but may need to modified
if you need to include additional libraries, or further libraries are
added to newer versions of the ROCm distribution.

When adding new entries to ``rocmlist.conf`` use the bare filename of
executables, and the ``xxxx.so`` form of libraries. Libraries are
resolved via ``ldconfig -p``, and exectuables are found by searching
``$PATH``.

GPU liblist format
==================

The ``nvliblist.conf`` and ``rocmliblist`` files list the basename of
executables and libraries to be bound into the container, without path
information.

Binaries are found by searching ``$PATH``:

.. code-block:: none

    # put binaries here
    # In shared environments you should ensure that permissions on these files
    # exclude writing by non-privileged users.
    rocm-smi
    rocminfo

Libraries should be specified without version information,
i.e. ``libname.so``, and are resolved using ``ldconfig``.

.. code-block:: none

   # put libs here (must end in .so)
   libamd_comgr.so
   libcomgr.so
   libCXLActivityLogger.so

If you receive warnings that binaries or libraries are not found,
ensure that they are in a system path (binaries), or available in paths
configured in ``/etc/ld.so.conf`` (libraries).


---------------
capability.json
---------------

.. note::
     It is extremely important to recognize that **granting users Linux
     capabilities with the** ``capability`` **command group is usually identical
     to granting those users root level access on the host system**. Most if not
     all capabilities will allow users to "break out" of the container and
     become root on the host. This feature is targeted toward special use cases
     (like cloud-native architectures) where an admin/developer might want to
     limit the attack surface within a container that normally runs as root.
     This is not a good option in multi-tenant HPC environments where an admin
     wants to grant a user special privileges within a container. For that and
     similar use cases, the :ref:`fakeroot feature <fakeroot>` is a better
     option.

{Singularity} provides full support for admins to grant and revoke Linux
capabilities on a user or group basis. The ``capability.json`` file is
maintained by {Singularity} in order to manage these capabilities. The
``capability`` command group allows you to ``add``, ``drop``, and ``list``
capabilities for users and groups.

For example, let us suppose that we have decided to grant a user (named
``pinger``) capabilities to open raw sockets so that they can use ``ping`` in
a container where the binary is controlled via capabilities.

To do so, we would issue a command such as this:

.. code-block:: none

    $ sudo singularity capability add --user pinger CAP_NET_RAW

This means the user ``pinger`` has just been granted permissions (through Linux
capabilities) to open raw sockets within {Singularity} containers.

We can check that this change is in effect with the ``capability list``
command.

.. code-block:: none

    $ sudo singularity capability list --user pinger
    CAP_NET_RAW

To take advantage of this new capability, the user ``pinger`` must also request
the capability when executing a container with the ``--add-caps`` flag.
``pinger`` would need to run a command like this:

.. code-block:: none

    $ singularity exec --add-caps CAP_NET_RAW library://sylabs/tests/ubuntu_ping:v1.0 ping -c 1 8.8.8.8
    PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
    64 bytes from 8.8.8.8: icmp_seq=1 ttl=52 time=73.1 ms

    --- 8.8.8.8 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 73.178/73.178/73.178/0.000 ms

If we decide that it is no longer necessary to allow the user ``pinger``
to open raw sockets within {Singularity} containers, we can revoke the
appropriate Linux capability like so:

.. code-block:: none

    $ sudo singularity capability drop --user pinger CAP_NET_RAW

Now if ``pinger`` tries to use ``CAP_NET_RAW``, {Singularity} will not give the
capability to the container and ``ping`` will fail to create a socket:

.. code-block:: none

    $ singularity exec --add-caps CAP_NET_RAW library://sylabs/tests/ubuntu_ping:v1.0 ping -c 1 8.8.8.8
    WARNING: not authorized to add capability: CAP_NET_RAW
    ping: socket: Operation not permitted

The ``capability add`` and ``drop`` subcommands will also accept the case
insensitive keyword ``all`` to grant or revoke all Linux capabilities to a user
or group.

For more information about individual Linux capabilities check out the
`man pages <http://man7.org/linux/man-pages/man7/capabilities.7.html>`_ or
use the ``capability avail`` command to output available capabilities with a
description of their behaviors.

----------------
seccomp-profiles
----------------

Secure Computing (seccomp) Mode is a feature of the Linux kernel that allows an
administrator to filter system calls being made from a container. Profiles made
up of allowed and restricted calls can be passed to different containers.
*Seccomp* provides more control than *capabilities* alone, giving a smaller
attack surface for an attacker to work from within a container.

You can set the default action with ``defaultAction`` for a non-listed system
call. Example: ``SCMP_ACT_ALLOW`` filter will allow all the system calls if it
matches the filter rule and you can set it to ``SCMP_ACT_ERRNO`` which will have
the thread receive a return value of *errno* if it calls a system call that matches
the filter rule.
The file is formatted in a way that it can take a list of additional system calls
for different architecture and {Singularity} will automatically take syscalls
related to the current architecture where it's been executed.
The ``include``/``exclude``-> ``caps`` section will include/exclude the listed
system calls if the user has the associated capability.

Use the ``--security`` option to invoke the container like:

.. code-block:: none

  $ sudo singularity shell --security seccomp:/home/david/my.json my_container.sif

For more insight into security options, network options, cgroups, capabilities,
etc, please check the `Userdocs <\{userdocs\}>`_
and it's `Appendix <\{userdocs\}/appendix.html>`_.

------------
remote.yaml
------------

System-wide remote endpoints are defined in a configuration file typically
located at ``/usr/local/etc/singularity/remote.yaml`` (this location may
vary depending on installation parameters) and can be managed by
administrators with the ``remote`` command group.

Remote Endpoints
================

Sylabs introduced the online `Sylabs Cloud
<https://cloud.sylabs.io/home>`_ to enable users to `Create
<https://cloud.sylabs.io/builder>`_, `Secure
<https://cloud.sylabs.io/keystore?sign=true>`_, and `Share
<https://cloud.sylabs.io/library/guide#create>`_ their container
images with others.

{Singularity} allows users to login to an account on the Sylabs Cloud, or
configure {Singularity} to use an API compatable container service such as
a local installation of {Singularity} Enterprise, which provides an on-premise
private Container Library, Remote Builder and Key Store.

.. note::

   A fresh installation of {Singularity} is automatically configured
   to connect to the public `Sylabs Cloud <https://cloud.sylabs.io>`__
   services.

**Examples**


Use the ``remote`` command group with the ``--global`` flag to create a
system-wide remote endpoint:

.. code-block:: none

    $ sudo singularity remote add --global company-remote https://enterprise.example.com
    [sudo] password for dave:
    INFO:    Remote "company-remote" added.
    INFO:    Global option detected. Will not automatically log into remote.

Conversely, to remove a system-wide endpoint:

.. code-block:: none

    $ sudo singularity remote remove --global company-remote
    [sudo] password for dave:
    INFO:    Remote "company-remote" removed.

{Singularity} 3.7 introduces the ability for an administrator to make a remote
the only usable remote for the system by using the ``--exclusive`` flag:

.. code-block:: none

    $ sudo singularity remote use --exclusive company-remote
    [sudo] password for dave:
    INFO:    Remote "company-remote" now in use.
    $ singularity remote list
    Cloud Services Endpoints
    ========================

    NAME            URI                     ACTIVE  GLOBAL  EXCLUSIVE
    SylabsCloud     cloud.sylabs.io         NO      YES     NO
    company-remote  enterprise.example.com  YES     YES     YES
    myremote        enterprise.example.com  NO      NO      NO

    Keyservers
    ==========

    URI                       GLOBAL  INSECURE  ORDER
    https://keys.example.com  YES     NO        1*

    * Active cloud services keyserver

For more details on the ``remote`` command group and managing remote endpoints,
please check the `Remote Userdocs <\{userdocs\}/endpoint.html>`_.


.. note::

   Once users login to a system wide endpoint, a copy of the endpoint will be listed in
   a their ``~/.singularity/remote.yaml`` file. This means modifications or removal of
   the system-wide endpoint will not be reflected in the users configuration unless they
   remove the endpoint themselves.

Keyserver Configuration
=======================

By default, {Singularity} will use the keyserver correlated to the active cloud
service endpoint. This behavior can be changed or supplemented via the
``add-keyserver`` and ``remove-keyserver`` commands. These commands allow an
administrator to create a global list of key servers used to verify container
signatures by default.

For more details on the ``remote`` command group and managing keyservers,
please check the `Remote Userdocs <\{userdocs\}/endpoint.html>`_.
