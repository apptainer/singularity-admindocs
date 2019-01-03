.. _singularity-config-file:

Singularity Config File
=======================

The Singularity config file lets you edit/change the behavior of Singularity.

This is the global configuration file for Singularity. This file controls what the container is allowed to do on a particular host, and as a result this file must be owned by root.

.. _modifying-the-config-file:

-------------------------
Modifying the Config File
-------------------------

blab.........

To change the config file, you will need root access, and a text editor, obviously.

The config file is located in ``/wherever/the/file/is``, so you just need to edit that file:

.. code-block:: bash

    $ sudo vim /wherever/the/file/is


Allow SETUID
------------

Should we allow users to utilize the setuid program flow within Singularity?


.. note::
    This is the default mode, and to utilize all features, this option will need to be enabled.

    If this option is disabled, it will rely on the user namespace exclusively which has not been integrated equally between the different Linux distributions.


.. code-block:: bash

    # ALLOW SETUID: [BOOL]
    # DEFAULT: yes
    allow setuid = yes


Max Loop
--------

Set the maximum number of loop devices that Singularity should ever attempt to utilize.

.. code-block:: bash

    # MAX LOOP DEVICES: [INT]
    # DEFAULT: 256
    max loop devices = 256


Allow pid
---------

Should we allow users to request the PID namespace? Note that for some HPC resources, the PID namespace may confuse the resource manager and break how some MPI implementations utilize shared memory. (note, on some older systems, the PID namespace is always used)

.. code-block:: bash

    # ALLOW PID NS: [BOOL]
    # DEFAULT: yes
    allow pid ns = yes

Config Password
---------------

If ``/etc/passwd`` exists within the container, this will automatically append an entry for the calling user.

.. code-block:: bash

    # CONFIG PASSWD: [BOOL]
    # DEFAULT: yes
    config passwd = yes

Config Group
------------

If ``/etc/group`` exists within the container, this will automatically append group entries for the calling user.

.. code-block:: bash

    # CONFIG GROUP: [BOOL]
    # DEFAULT: yes
    config group = yes

Config Resolve
--------------

If there is a bind point within the container, use the host's ``/etc/resolv.conf``.

.. code-block:: bash

    # CONFIG RESOLV_CONF: [BOOL]
    # DEFAULT: yes
    config resolv_conf = yes

Mount Proc
----------

Should we automatically bind mount ``/proc`` within the container?

.. code-block:: bash

    # MOUNT PROC: [BOOL]
    # DEFAULT: yes
    mount proc = yes

Mount SYS
---------

Should we automatically bind mount ``/sys`` within the container?

.. code-block:: bash

    # MOUNT SYS: [BOOL]
    # DEFAULT: yes
    mount sys = yes

Mount DEV
---------

Should we automatically bind mount ``/dev`` within the container? If ``minimal`` is chosen, then only ``null``, ``zero``, ``random``, ``urandom``, and ``shm`` will be included (the same effect as the ``--contain`` options)

.. code-block:: bash

    # MOUNT DEV: [yes/no/minimal]
    # DEFAULT: yes
    mount dev = yes


...and so on...
