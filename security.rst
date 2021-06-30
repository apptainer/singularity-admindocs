.. _security:

***********************************
Security in Singularity Containers
***********************************

Containers are all the rage today for many good reasons. They are light weight, easy to spin-up and require reduced IT management resources as compared to hardware VM environments. More importantly, container technology facilitates advanced research computing by granting the ability to package software in highly portable and reproducible environments encapsulating all dependencies, including the operating system. But there are still some challenges to container security. 

Singularity, which is a container paradigm created by necessity for scientific and application driven workloads, addresses some 
core missions of containers : Mobility of Compute, Reproducibility, HPC support, and **Security**. This document intends to inform
admins of different security features supported by Singularity.

Singularity Runtime
###################

The Singularity runtime enforces a unique security model that makes it appropriate for *untrusted users* to run *untrusted containers* 
safely on multi-tenant resources. Because the Singularity runtime dynamically writes UID and GID information to the appropriate files 
within the container, the user remains the same *inside* and *outside* the container, i.e., if you're an unprivileged 
user while entering the container, you'll remain an unprivileged user inside the container. A privilege separation model is in place
to prevent users from escalating privileges once they are inside of a container. The container file system is mounted using the 
``nosuid`` option, and processes are spawned with the ``PR_NO_NEW_PRIVS`` flag. Taken together, this approach provides a secure way 
for users to run containers and greatly simplifies things like reading and writing data to the host system with appropriate 
ownership.

It is also important to note that the philosophy of Singularity is *Integration* over *Isolation*. Most container run times strive 
to isolate your container from the host system and other containers as much as possible. Singularity, on the 
other hand, assumes that the user’s primary goals are portability, reproducibility, and ease of use and that isolation is often a 
tertiary concern. Therefore, Singularity only isolates the mount namespace by default, and will also bind mount several host 
directories such as ``$HOME`` and ``/tmp`` into the container at runtime. If needed, additional levels of isolation can be achieved
by passing options causing Singularity to enter any or all of the other kernel namespaces and to prevent automatic bind mounting.
These measures allow users to interact with the host system from within the container in sensible ways.

Singularity Image Format (SIF)
##############################

The Singularity community addresses container security as a continuous process. It attempts to provide container integrity throughout the distribution
pipeline.. i.e., at rest, in transit and while running. Hence, the SIF has been designed to achieve these goals. 

A SIF file is an immutable container runtime image. It is a physical representation of the container environment itself. An 
important component of SIF that elicits security feature is the ability to cryptographically sign a container, creating a signature
block within the SIF file which can guarantee immutability and provide accountability as to who signed it. Singularity follows the 
`OpenPGP <https://www.openpgp.org/>`_ standard to create and manage these keys. After building an image within Singularity, users can
``singularity sign`` the container and push it to the Library along with its public PGP key(Stored in :ref:`Keystore <keystore>`) which 
later can be verified (``singularity verify``) while pulling or downloading the image. This feature in particular 
protects collaboration within and between systems and teams. 

SIF Encryption
**************

In Singularity 3.4 and above the container root filesystem that
resides in the squashFS partition of a SIF can be encrypted, rendering
it's contents inaccessible without a secret. Unlike other platforms,
where encrypted layers must be assembled into an unencrypted runtime
directory on disk, Singularity mounts the encrypted root file system
directly from the SIF using Kernel dm-crypt/LUKS functionality, so
that the content is not exposed on disk. Singularity containers
provide a comparable level of security to LUKS2 full disk encryption
commonly deployed on Linux server and desktop systems.

As with all matters of security, a layered approach must be taken and
the system as a whole considered. For example, it is possible that
decrypted memory pages could be paged out the system swap file or
device, which could result in decrypted information being stored at
rest on physical media. Operating system level mitigations such as
encrypted swap space may be required depending on the needs of your
application.

Encryption and decryption of containers requires ``cryptsetup``
version 2. The SIF root filesystem will be encrypted using the
default LUKS cipher on the host. The current default cipher used by
``cryptsetup`` for LUKS2 in mainstream Linux distributions is
``aes-xts-plain64`` with a 256 bit key size. The default key
derivation function for LUKS2 is ``argon2i``.

Singularity currently supports 2 types of secrets for encrypted
containers:

  - *Passphrase*: a text passphrase is passed directly to
    ``cryptsetup`` for LUKS encryption of the root fs.
  - *Asymmetric RSA keypair*: a randomly generated 256-bit secret is
    used to perform LUKS encryption of the rootfs.  This secret is
    encrypted with a user-provided RSA public key, and the ciphertext
    stored in the SIF file. At runtime the RSA private key must be
    provided to decrypt the secret and allow decryption of the root
    filesystem to use the container.

.. note::

   You can verify the default LUKS2 cipher and PBKDF on your system by
   running ``cryptsetup --help``.

   ``cryptsetup`` sets a memory cost for the ``argon2i`` PBKDF based on
   the RAM available in the system used for encryption, up to a
   maximum of 1GiB. Encrypted containers created on systems with >2GiB
   RAM may be unusable on systems with <1GiB of free RAM.



Admin Configurable Files
#########################

Singularity Administrators have the ability to access various configuration files, that will let them set security 
restrictions, grant or revoke a user’s capabilities, manage resources and authorize containers etc. One such file interesting in this context is `ecl.toml <https://singularity.hpcng.org/admin-docs/master/configfiles.html#ecl-toml>`_ 
which allows blacklisting and whitelisting of containers. You can find all the configuration files and their parameters
documented `here <https://singularity.hpcng.org/admin-docs/\{adminversion\}/configfiles.html>`__. 

cgroups support
****************

Starting v3.0, Singularity added native support for ``cgroups``, allowing users to limit the resources their containers consume 
without the help of a separate program like a batch scheduling system. This feature helps in preventing  DoS attacks where one 
container seizes control of all available system resources in order to stop other containers from operating properly. 
To utilize this feature, a user first creates a configuration file. An example configuration file is installed by default with 
Singularity to provide a guide. At runtime, the ``--apply-cgroups`` option is used to specify the location of the configuration 
file and cgroups are configured accordingly. More about cgroups support `here <https://singularity.hpcng.org/admin-docs/\{adminversion\}/configfiles.html#cgroups-toml>`__.

``--security`` options
***********************

Singularity supports a number of methods for specifying the security scope and context when running Singularity containers. 
Additionally, it supports new flags that can be passed to the action commands; ``shell``, ``exec``, and ``run`` allowing fine 
grained control of security. Details about them are documented `here <https://singularity.hpcng.org/admin-docs/\{adminversion\}/security_options.html>`__.

Security in SCS
################

`Singularity Container Services (SCS) <https://cloud.sylabs.io/home>`_ consist of a Remote Builder, a Container Library, and a 
Keystore. Taken together, the Singularity Container Services provide an end-to-end solution for packaging and distributing 
applications in secure and trusted containers.

Remote Builder
**************

As mentioned earlier, the Singularity runtime prevents executing code with root-level permissions on the host system. But building a 
container requires elevated privileges that most production environments do not grant to users. `The Remote Builder <https://cloud.sylabs.io/builder>`_ 
solves this challenge by allowing unprivileged users a service that can be used to build containers targeting one or more CPU 
architectures. System administrators can use the system to monitor which users are building containers, and the contents of those 
containers. Starting with Singularity 3.0, the CLI has native integration with the Build Service from version 3.0 onwards. In 
addition, a web GUI interface to the Build Service also exists, which allows users to build containers using only a web browser.

.. note::

    Please see the :ref:`Fakeroot feature <fakeroot>` which is a secure option for admins in multi-tenant HPC environments and 
    similar use cases where they might want to grant a user special privileges inside a container.

Container Library
*****************

The `Container Library <https://cloud.sylabs.io/library>`_ enables users to store and share Singularity container images based on 
the Singularity Image Format (SIF). A web front-end allows users to create new projects within the Container Library, edit 
documentation associated with container images, and discover container images published by their peers.

.. _keystore:

Key Store
*********

The `Key Store <https://cloud.sylabs.io/keystore>`_ is a key management system offered by Sylabs that utilizes `OpenPGP implementation <https://gnupg.org/>`_ to facilitate sharing and maintaining of PGP public keys used to sign and verify Singularity container images. This service is based on the OpenPGP HTTP Keyserver Protocol (HKP), with several enhancements:

- The Service requires connections to be secured with Transport Layer Security (TLS).
- The Service implements token-based authentication, allowing only authenticated users to add or modify PGP keys.
- A web front-end allows users to view and search for PGP keys using a web browser.


Security Considerations of Cloud Services:
******************************************

1. Communications between users, the auth service and the above-mentioned services are secured via TLS.

2. The services support authentication of users via authentication tokens.

3. There is no implicit trust relationship between Auth and each of these services. Rather, each request between the services is authenticated using the authentication token supplied by the user in the associated request.

4. The services support MongoDB authentication as well as TLS/SSL. 

.. note::

   SingularityPRO is a professionally curated and licensed version of Singularity that provides added security, stability, and 
   support beyond that offered by the open source project. Subscribers receive advanced access to security patches through regular 
   updates so, when a CVE is announced publicly PRO subscribers are already using patched software.


Security is not a check box that one can tick and forget.  It’s an ongoing process that begins with software architecture, and 
continues all the way through to ongoing security practices.  In addition to ensuring that containers are run without elevated 
privileges where appropriate, and that containers are produced by trusted sources, users must monitor their containers for newly 
discovered vulnerabilities and update when necessary just as they would with any other software. The Singularity community is constantly probing to 
find and patch vulnerabilities within Singularity, and will continue to do so.
