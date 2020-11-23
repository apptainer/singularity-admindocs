
.. _installed-files:

===============
Installed Files
===============

An installation of Singularity {InstallationVersion}, performed as root via
``sudo make install`` consists of the following files, with ownership
and permissions required to use the `setuid` workflow:

.. code-block:: none

    # Container session / state
    var/singularity root:root 755 (drwxr-xr-x)
    var/singularity/mnt root:root 755 (drwxr-xr-x)
    var/singularity/mnt/session root:root 755 (drwxr-xr-x)

    # Main executables
    bin/singularity root:root 755 (-rwxr-xr-x)
    bin/run-singularity root:root 755 (-rwxr-xr-x)

    # Helper executables
    libexec/singularity root:root 755 (drwxr-xr-x)
    libexec/singularity/bin root:root 755 (drwxr-xr-x)
    libexec/singularity/bin/starter root:root 755 (-rwxr-xr-x)
    libexec/singularity/bin/starter-suid root:root 4755 (-rwsr-xr-x)
    libexec/singularity/cni root:root 755 (drwxr-xr-x)
    libexec/singularity/cni/bandwidth root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/bridge root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/dhcp root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/firewall root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/flannel root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/host-device root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/host-local root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/ipvlan root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/loopback root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/macvlan root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/portmap root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/ptp root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/static root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/tuning root:root 755 (-rwxr-xr-x)
    libexec/singularity/cni/vlan root:root 755 (-rwxr-xr-x)

    # Singularity configuration
    etc/singularity root:root 755 (drwxr-xr-x)
    etc/singularity/capability.json root:root 644 (-rw-r--r--)
    etc/singularity/cgroups root:root 755 (drwxr-xr-x)
    etc/singularity/cgroups/cgroups.toml root:root 644 (-rw-r--r--)
    etc/singularity/ecl.toml root:root 644 (-rw-r--r--)
    etc/singularity/global-pgp-public root:root 644 (-rw-r--r--)
    etc/singularity/network root:root 755 (drwxr-xr-x)
    etc/singularity/network/00_bridge.conflist root:root 644 (-rw-r--r--)
    etc/singularity/network/10_ptp.conflist root:root 644 (-rw-r--r--)
    etc/singularity/network/20_ipvlan.conflist root:root 644 (-rw-r--r--)
    etc/singularity/network/30_macvlan.conflist root:root 644 (-rw-r--r--)
    etc/singularity/network/40_fakeroot.conflist root:root 644 (-rw-r--r--)
    etc/singularity/nvliblist.conf root:root 644 (-rw-r--r--)
    etc/singularity/remote.yaml root:root 644 (-rw-r--r--)
    etc/singularity/rocmliblist.conf root:root 644 (-rw-r--r--)
    etc/singularity/seccomp-profiles root:root 755 (drwxr-xr-x)
    etc/singularity/seccomp-profiles/default.json root:root 644 (-rw-r--r--)
    etc/singularity/singularity.conf root:root 644 (-rw-r--r--)

    # Bash completion configuration
    etc/bash_completion.d root:root 755 (drwxr-xr-x)
    etc/bash_completion.d/singularity root:root 644 (-rw-r--r--)
