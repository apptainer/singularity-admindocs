.. _singularity_configfiles:

===============================
Singularity Configuration Files
===============================

As a Singularity Administrator, you will have access to various configuration
files, that will let you manage container resources, set security restrictions
and configure network options etc, when installing Singularity across the system.
All these files can be found in ``/usr/local/etc/singularity`` by default (though
its location will obviously differ based on options passed during the
installation). This page will describe the following configuration files and
the various parameters contained by them. They are usually self documented
but here are several things to pay special attention to:

-----------------
singularity.conf
-----------------
Most of the configuration options are set using the file ``singularity.conf``
that defines the global configuration for Singularity across the entire system.
System administrators can have direct say as to what functions the users can
utilize when running as root. As a security measure, it must be owned by root
and must not be writable by users or Singularity will refuse to run.

The following are some of the configurable options:

``ALLOW SETUID``:
To use containers, your users will have to have access to some privileged system
calls. One way singularity achieves this is by using ``Setuid`` component in the
workflow. This variable lets you enable/disable users ability to utilize this
component within Singularity. By default, it is set to "Yes", but when disabled,
various Singularity features will not function (e.g. mounting of the Singularity
image file format).

``USER BIND CONTROL``:
This allows admins to enable/disable users to define bind points at runtime.
By Default, its "YES", which means users can specify bind points, scratch and
tmp locations.

.. note::

  User bind control is only allowed if the host also supports `PR_SET_NO_NEW_PRIVS`

``BIND PATH``:
Used for setting of  automatic `bind points` entries. You can define a list
of files/directories that should be made available from within the container.
If the file exists within the container on which to attach to use the path
like:

.. code-block:: none

  bind path = /etc/localtime

You can specify different source and destination locations using:

.. code-block:: none

  bind path = /etc/singularity/default-nsswitch.conf:/etc/nsswitch.conf

``MOUNT DEV``:
Should be set to "YES", if you want to automatically bind mount `/dev`
within the container. If set to 'minimal', then only 'null', 'zero',
'random', 'urandom', and 'shm' will be included.

``MOUNT HOME``:
To automatically determine the calling of user's home directory and
attempt to mount it's base path into the container.

Limiting containers
====================

There are several ways in which you can limit the running of containers in your
system:

 ``LIMIT CONTAINER OWNERS``: Only allow containers to be used that are owned by a
 given user.

 ``LIMIT CONTAINER GROUPS``: Only allow containers to be used that are owned by
 a given group.

 ``LIMIT CONTAINER PATHS``: Only allow containers to be used that are located
 within an allowed path prefix.

.. note::

  These features will only apply when Singularity is running in SUID mode and the
  user is non-root. By default they all are set to `NULL`.


The ``singularity.conf`` file is well documented and most information can be
gleaned by consulting it directly.

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
----------------
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
-------------

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
------------

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
weigh tasks in the given cgroup while competing with the cgroup's child cgroups.

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

--------
ecl.toml
--------

The execution control list is defined here. You can authorize the containers by
validating both the location of the SIF file in the file system and by
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

--------------
nvliblist.conf
--------------

When a container includes a GPU enabled application and libraries, Singularity
(with the ``--nv`` option) can properly inject the required Nvidia GPU driver
libraries into the container, to match the host's kernel, i.e., Singularity can
figure out the compatible versions that might be required by some processes
running inside the container. This config file is the place where it searches
for NVIDIA libraries in your host system.

Examples
--------

For GPU and CUDA support this is how it works:

.. code-block:: none

  $ singularity exec --nv ubuntu.sif gpu_program.exec
  $ singularity run --nv docker://tensorflow/tensorflow:gpu_latest

You can also mention libraries/binaries and they will be mounted into the
container when the ``--nv`` option is passed.

---------------
capability.json
---------------

Singularity provides full support for granting and revoking Linux capabilities
on a user or group basis. By default, all Linux capabilities are dropped when a
user enters the container system. When you decide to add/revoke some capabilities,
you can do so using the ``Singularity capability`` options: ``Add``, ``Drop``
and ``List``.

For example, if you do:

.. code-block:: none

  $ sudo singularity capability add --user david CAP_SYS_RAWIO

You've let the user David to perform I/O port operations, perform a range of
device-specific operations on other devices etc.
To perform the same for a group of users do:

.. code-block:: none

  $ sudo singularity capability add --group mygroup audit_write

Use ``drop`` in the same format for revoking their capabilities.

To see a list of all users and their capabilities, simply do:

.. code-block:: none

  $ sudo singularity capability list --all

Alternatively, you can view the *capability.json* file where all these changes
will be reflected.

To know more about the capabilities you can add do:

.. code-block:: none

  $ singularity capability add --help

.. note::

  The above commands can only be issued by root user(admin).

The `--add-caps <https://www.sylabs.io/guides/3.0/user-guide/security_options.html?highlight=seccomp#security-related-action-options>`_ and
related options will let the user request the capability when executing a container.

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
for different architecture and Singularity will automatically take syscalls
related to the current architecture where it's been executed.
The ``include``/``exclude``-> ``caps`` section will include/exclude the listed
system calls if the user has the associated capability.

Use the ``--security`` option to invoke the container like:

.. code-block:: none

  $ sudo singularity shell --security seccomp:/home/david/my.json my_container.sif

For more insight into security options, network options, cgroups, capabilities,
etc, please check the `Userdocs <https://www.sylabs.io/guides/3.0/user-guide/>`_
and it's `Appendix <https://www.sylabs.io/guides/3.0/user-guide/appendix.html>`_.
