###################
 Admin Quick Start
###################

This quick start gives an overview of installation of {Singularity} from
source, a description of the architecture of {Singularity}, and pointers
to configuration files. More information, including alternate
installation options and detailed configuration options can be found
later in this guide.

.. _singularity-architecture:

*******************************
 Architecture of {Singularity}
*******************************

{Singularity} is designed to allow containers to be executed as if they
were native programs or scripts on a host system. No daemon is required
to build or run containers, and the security model is compatible with
shared systems.

As a result, integration with clusters and schedulers such as Univa Grid
Engine, Torque, SLURM, SGE, and many others is as simple as running any
other command. All standard input, output, errors, pipes, IPC, and other
communication pathways used by locally running programs are synchronized
with the applications running locally within the container.

{Singularity} favors an 'integration over isolation' approach to
containers. By default only the mount namespace is isolated for
containers, so that they have their own filesystem view. Access to
hardware such as GPUs, high speed networks, and shared filesystems is
easy and does not require special configuration. Default access to
user home directories, ``/tmp`` space, and installation specific
mounts makes it simple for users to benefit from the reproducibility
of containerized applications without major changes to their existing
workflows. Where more complete isolation is important, {Singularity}
can use additional Linux namespaces and other security and resource
limits to accomplish this.

.. _singularity-security:

************************
 {Singularity} Security
************************

.. note::

   See also the :ref:`security section <security>` of this guide, for more
   detail.

{Singularity} uses a number of strategies to provide safety and
ease-of-use on both single-user and shared systems. Notable security
features include:

   -  The user inside a container is the same as the user who ran the
      container. This means access to files and devices from the
      container is easily controlled with standard POSIX permissions.

   -  Container filesystems are mounted ``nosuid`` and container
      applications run with the ``PR_SET_NO_NEW_PRIVS`` flag. This means
      that applications in a container cannot gain additional
      privileges. A regular user cannot ``sudo`` or otherwise gain root
      privilege on the host via a container.

   -  The Singularity Image Format (SIF) supports encryption of
      containers, as well as cryptographic signing and verification of
      their content.

   -  SIF containers are immutable and their payload is run directly,
      without extraction to disk. This means that the container can
      always be verified, even at runtime, and encrypted content is not
      exposed on disk.

   -  Restrictions can be configured to limit the ownership, location,
      and cryptographic signatures of containers that are permitted to
      be run.

To support the SIF image format, automated networking setup etc., and
older Linux distributions without user namespace support, Singularity
runs small amounts of privileged container setup code via a
``starter-setuid`` binary. This is a 'setuid root' binary, so that
{Singularity} can perform filesystem loop mounts and other operations
that need privilege. The setuid flow is the default mode of operation,
but :ref:`can be disabled <install-nonsetuid>` on build, or in the
``singularity.conf`` configuration file if required.

.. note::

   Running {Singularity} in non-setuid mode requires unprivileged user
   namespace support in the operating system kernel and does not support
   all features, most notably direct mounts of SIF images. This impacts
   integrity/security guarantees of containers at runtime.

   See the :ref:`non-setuid installation section <install-nonsetuid>`
   for further detail on how to install {Singularity} to run in
   non-setuid mode.

**************************
 Installation from Source
**************************

{Singularity} can be installed from source directly, or by building an
RPM package from the source. Linux distributions may also package
{Singularity}, but their packages may not be up-to-date with the
upstream version on GitHub.

To install {Singularity} directly from source, follow the procedure
below. Other methods are discussed in the :ref:`Installation
<installation>` section.

.. Note::

   This quick-start that you will install as ``root`` using ``sudo``, so
   that {Singularity} uses the default ``setuid`` workflow, and all
   features are available. See the :ref:`non-setuid installation
   <install-nonsetuid>` section of this guide for detail of how to
   install as a non-root user, and how this affects the functionality of
   {Singularity}.

Install Dependencies
====================

On Red Hat Enterprise Linux or CentOS install the following
dependencies:

.. code:: sh

   $ sudo yum update -y && \
        sudo yum groupinstall -y 'Development Tools' && \
        sudo yum install -y \
        openssl-devel \
        libuuid-devel \
        libseccomp-devel \
        wget \
        squashfs-tools \
        cryptsetup

On Ubuntu or Debian install the following dependencies:

.. code:: sh

   $ sudo apt-get update && sudo apt-get install -y \
       build-essential \
       uuid-dev \
       libgpgme-dev \
       squashfs-tools \
       libseccomp-dev \
       wget \
       pkg-config \
       git \
       cryptsetup-bin

Install Go
==========

{Singularity} v3 is written primarily in Go, and you will need Go 1.16
or above installed to compile it from source. Versions of Go packaged by
your distribution may not be new enough to build {Singularity}.

The method below is one of several ways to `install and configure Go
<https://golang.org/doc/install>`_.

.. note::

   If you have previously installed Go from a download, rather than an
   operating system package, you should remove your ``go`` directory,
   e.g. ``rm -r /usr/local/go`` before installing a newer version.
   Extracting a new version of Go over an existing installation can lead
   to errors when building Go programs, as it may leave old files, which
   have been removed or replaced in newer versions.

Visit the `Go download page <https://golang.org/dl/>`_ and pick a
package archive to download. Copy the link address and download with
wget. Then extract the archive to ``/usr/local`` (or use other
instructions on go installation page).

.. code::

   $ export VERSION={GoVersion} OS=linux ARCH=amd64 && \
       wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz && \
       sudo tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz && \
       rm go$VERSION.$OS-$ARCH.tar.gz

Then, set up your environment for Go.

.. code::

   $ echo 'export GOPATH=${HOME}/go' >> ~/.bashrc && \
       echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc && \
       source ~/.bashrc

Download {Singularity} from a GitHub release
============================================

You can download {Singularity} from one of the releases. To see a full
list, visit `the GitHub release page
<https://github.com/hpcng/singularity/releases>`_.  After deciding on a
release to install, you can run the following commands to proceed with
the installation.

.. code::

    $ export VERSION={InstallationVersion} && # adjust this as necessary \
        wget https://github.com/hpcng/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
        tar -xzf singularity-${VERSION}.tar.gz && \
        cd singularity

Compile & Install {Singularity}
===============================

{Singularity} uses a custom build system called ``makeit``. ``mconfig``
is called to generate a ``Makefile`` and then ``make`` is used to
compile and install.

.. code::

   $ ./mconfig && \
       make -C ./builddir && \
       sudo make -C ./builddir install

By default {Singularity} will be installed in the ``/usr/local``
directory hierarchy. You can specify a custom directory with the
``--prefix`` option, to ``mconfig``:

.. code::

   $ ./mconfig --prefix=/opt/singularity

This option can be useful if you want to install multiple versions of
Singularity, install a personal version of {Singularity} on a shared
system, or if you want to remove {Singularity} easily after installing
it.

For a full list of ``mconfig`` options, run ``mconfig --help``. Here are
some of the most common options that you may need to use when building
{Singularity} from source.

-  ``--sysconfdir``: Install read-only config files in sysconfdir. This
   option is important if you need the ``singularity.conf`` file or
   other configuration files in a custom location.

-  ``--localstatedir``: Set the state directory where containers are
   mounted. This is a particularly important option for administrators
   installing {Singularity} on a shared file system. The
   ``--localstatedir`` should be set to a directory that is present on
   each individual node.

-  ``-b``: Build {Singularity} in a given directory. By default this is
   ``./builddir``.

***************
 Configuration
***************

{Singularity} is configured using files under ``etc/singularity`` in
your ``--prefix``, or ``--syconfdir`` if you used that option with
``mconfig``. In a default installation from source without a
``--prefix`` set you will find them under
``/usr/local/etc/singularity``. In a default installation from RPM or Deb packages you will find them under ``/etc/singularity``.

You can edit these files directly, or using the ``{Singularity} config
global`` command as the root user to manage them.

``singularity.conf`` contains the majority of options controlling the
runtime behavior of {Singularity}. Additional files control security,
network, and resource configuration. Head over to the
:ref:`Configuration files <singularity_configfiles>` section where the
files and configuration options are discussed.

********************
 Test {Singularity}
********************

You can run a quick test of {Singularity} using a container in the
Sylabs Container Library:

.. code::

   $ singularity exec library://alpine cat /etc/alpine-release
   3.9.2

See the `user guide
<{userdocs}>`__ for more
information about how to use {Singularity}.
