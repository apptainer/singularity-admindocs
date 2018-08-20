
=========================
Installation Environments
=========================

------------------
Singularity on HPC
------------------

One of the architecturally defined features in Singularity is that it
can execute containers like they are native programs or scripts on a
host computer. As a result, integration with schedulers is simple and
runs exactly as you would expect. All standard input, output, error,
pipes, IPC, and other communication pathways that locally running
programs employ are synchronized with the applications running locally
within the container.
Additionally, because Singularity is not emulating a full hardware
level virtualization paradigm, there is no need to separate out any
sandboxed networks or file systems because there is no concept of
user-escalation within a container. Users can run Singularity
containers just as they run any other program on the HPC resource.

Workflows
=========

We are in the process of developing Singularity Hub, which will allow
for generation of workflows using Singularity containers in an online
interface, and easy deployment on standard research clusters (e.g.,
SLURM, SGE). Currently, the Singularity core software is installed on
the following research clusters, meaning you can run Singularity
containers as part of your jobs:

-  The `Sherlock cluster <http://sherlock.stanford.edu/>`__ at `Stanford
   University <https://srcc.stanford.edu/>`__

-  `SDSC Comet and
   Gordon <https://www.xsede.org/news/-/news/item/7624>`__ (XSEDE)

-  `MASSIVE M1 M2 and M3 <http://docs.massive.org.au/index.html>`__
   (Monash University and Australian National Merit Allocation Scheme)

Integration with MPI
--------------------

Another result of the Singularity architecture is the ability to
properly integrate with the Message Passing Interface (MPI). Work has
already been done for out of the box compatibility with Open MPI (both
in Open MPI v2.1.x as well as part of Singularity). The Open
MPI/Singularity workflow works as follows:

#. mpirun is called by the resource manager or the user directly from a
   shell

#. Open MPI then calls the process management daemon (ORTED)

#. The ORTED process launches the Singularity container requested by the
   mpirun command

#. Singularity builds the container and namespace environment

#. Singularity then launches the MPI application within the container

#. The MPI application launches and loads the Open MPI libraries

#. The Open MPI libraries connect back to the ORTED process via the
   Process Management Interface (PMI)

#. At this point the processes within the container run as they would
   normally directly on the host.

This entire process happens behind the scenes, and from the user’s
perspective running via MPI is as simple as just calling mpirun on the
host as they would normally.
Below are example snippets of building and installing OpenMPI into a
container and then running an example MPI program through Singularity.

Tutorials
---------

:ref:`Using Host libraries: GPU drivers and OpenMPI BTLs <using-host-libraries-gpu-drivers-and-openmpi-btls>`

MPI Development Example
-----------------------

**What are supported Open MPI Version(s)?** To achieve proper
container’ized Open MPI support, you should use Open MPI version 2.1.
There are however three caveats:

#. Open MPI 1.10.x may work but we expect you will need exactly matching
   version of PMI and Open MPI on both host and container (the 2.1
   series should relax this requirement)

#. Open MPI 2.1.0 has a bug affecting compilation of libraries for some
   interfaces (particularly Mellanox interfaces using libmxm are known
   to fail). If your in this situation you should use the master branch
   of Open MPI rather than the release.

#. Using Open MPI 2.1 does not magically allow your container to connect
   to networking fabric libraries in the host. If your cluster has, for
   example, an infiniband network you still need to install OFED
   libraries into the container. Alternatively you could bind mount both
   Open MPI and networking libraries into the container, but this could
   run afoul of glib compatibility issues (its generally OK if the
   container glibc is more recent than the host, but not the other way
   around)

Code Example using Open MPI 2.1.0 Stable
----------------------------------------

.. code-block:: none

    $ # Include the appropriate development tools into the container (notice we are calling

    $ # singularity as root and the container is writable)

    $ sudo singularity exec -w /tmp/Centos-7.img yum groupinstall "Development Tools"

    $

    $ # Obtain the development version of Open MPI

    $ wget https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.0.tar.bz2

    $ tar jtf openmpi-2.1.0.tar.bz2

    $ cd openmpi-2.1.0

    $

    $ singularity exec /tmp/Centos-7.img ./configure --prefix=/usr/local

    $ singularity exec /tmp/Centos-7.img make

    $

    $ # Install OpenMPI into the container (notice now running as root and container is writable)

    $ sudo singularity exec -w -B /home /tmp/Centos-7.img make install

    $

    $ # Build the OpenMPI ring example and place the binary in this directory

    $ singularity exec /tmp/Centos-7.img mpicc examples/ring_c.c -o ring

    $

    $ # Install the MPI binary into the container at /usr/bin/ring

    $ sudo singularity copy /tmp/Centos-7.img ./ring /usr/bin/

    $

    $ # Run the MPI program within the container by calling the MPIRUN on the host

    $ mpirun -np 20 singularity exec /tmp/Centos-7.img /usr/bin/ring


Code Example using Open MPI git master
--------------------------------------

The previous example (using the Open MPI 2.1.0 stable release) should
work fine on most hardware but if you have an issue, try running the
example below (using the Open MPI Master branch):

.. code-block:: none

    $ # Include the appropriate development tools into the container (notice we are calling

    $ # singularity as root and the container is writable)

    $ sudo singularity exec -w /tmp/Centos-7.img yum groupinstall "Development Tools"

    $

    $ # Clone the OpenMPI GitHub master branch in current directory (on host)

    $ git clone https://github.com/open-mpi/ompi.git

    $ cd ompi

    $

    $ # Build OpenMPI in the working directory, using the tool chain within the container

    $ singularity exec /tmp/Centos-7.img ./autogen.pl

    $ singularity exec /tmp/Centos-7.img ./configure --prefix=/usr/local

    $ singularity exec /tmp/Centos-7.img make

    $

    $ # Install OpenMPI into the container (notice now running as root and container is writable)

    $ sudo singularity exec -w -B /home /tmp/Centos-7.img make install

    $

    $ # Build the OpenMPI ring example and place the binary in this directory

    $ singularity exec /tmp/Centos-7.img mpicc examples/ring_c.c -o ring

    $

    $ # Install the MPI binary into the container at /usr/bin/ring

    $ sudo singularity copy /tmp/Centos-7.img ./ring /usr/bin/

    $

    $ # Run the MPI program within the container by calling the MPIRUN on the host

    $ mpirun -np 20 singularity exec /tmp/Centos-7.img /usr/bin/ring



    Process 0 sending 10 to 1, tag 201 (20 processes in ring)

    Process 0 sent to 1

    Process 0 decremented value: 9

    Process 0 decremented value: 8

    Process 0 decremented value: 7

    Process 0 decremented value: 6

    Process 0 decremented value: 5

    Process 0 decremented value: 4

    Process 0 decremented value: 3

    Process 0 decremented value: 2

    Process 0 decremented value: 1

    Process 0 decremented value: 0

    Process 0 exiting

    Process 1 exiting

    Process 2 exiting

    Process 3 exiting

    Process 4 exiting

    Process 5 exiting

    Process 6 exiting

    Process 7 exiting

    Process 8 exiting

    Process 9 exiting

    Process 10 exiting

    Process 11 exiting

    Process 12 exiting

    Process 13 exiting

    Process 14 exiting

    Process 15 exiting

    Process 16 exiting

    Process 17 exiting

    Process 18 exiting

    Process 19 exiting


-----------------
Image Environment
-----------------

Directory access
================

By default Singularity tries to create a seamless user experience
between the host and the container. To do this, Singularity makes
various locations accessible within the container automatically. For
example, the user’s home directory is always bound into the container as
is /tmp and /var/tmp. Additionally your current working directory
(cwd/pwd) is also bound into the container iff it is not an operating
system directory or already accessible via another mount. For almost all
cases, this will work flawlessly as follows:

.. code-block:: none

    $ pwd

    /home/gmk/demo

    $ singularity shell container.img

    Singularity/container.img> pwd

    /home/gmk/demo

    Singularity/container.img> ls -l debian.def

    -rw-rw-r--. 1 gmk gmk 125 May 28 10:35 debian.def

    Singularity/container.img> exit

    $

For directory binds to function properly, there must be an existing
target endpoint within the container (just like a mount point). This
means that if your home directory exists in a non-standard base
directory like “/foobar/username” then the base directory “/foobar”
must already exist within the container.
Singularity will not create these base directories! You must enter the
container with the option ``--writable`` being set, and create the directory
manually.

Current Working Directory
-------------------------

Singularity will try to replicate your current working directory within
the container. Sometimes this is straight forward and possible, other
times it is not (e.g. if the base dir of your current working directory
does not exist). In that case, Singularity will retain the file
descriptor to your current directory and change you back to it. If you
do a ‘pwd’ within the container, you may see some weird things. For
example:

.. code-block:: none

    $ pwd

    /foobar

    $ ls -l

    total 0

    -rw-r--r--. 1 root root 0 Jun  1 11:32 mooooo

    $ singularity shell ~/demo/container.img

    WARNING: CWD bind directory not present: /foobar

    Singularity/container.img> pwd

    (unreachable)/foobar

    Singularity/container.img> ls -l

    total 0

    -rw-r--r--. 1 root root 0 Jun  1 18:32 mooooo

    Singularity/container.img> exit

    $

But notice how even though the directory location is not resolvable, the
directory contents are available.

Standard IO and pipes
=====================

Singularity automatically sends and receives all standard IO from the
host to the applications within the container to facilitate expected
behavior from the interaction between the host and the container. For
example:

.. code-block:: none

    $ cat debian.def | singularity exec container.img grep 'MirrorURL'

    MirrorURL "http://ftp.us.debian.org/debian/"

    $

    Making changes to the container (writable)

    By default, containers are accessed as read only. This is both to enable parallel container execution (e.g. MPI). To enter a container using exec, run, or shell you must pass the --writable flag in order to open the image as read/writable.


Containing the container
========================

By providing the argument ``--contain`` to ``exec``, ``run`` or ``shell`` you will find that shared directories
are no longer shared. For example, the user’s home directory is
writable, but it is non-persistent between non-overlapping runs.

-------
License
-------

.. code-block:: none

    Redistribution and use in source and binary forms, with or without

    modification, are permitted provided that the following conditions are met:


    (1) Redistributions of source code must retain the above copyright notice,

    this list of conditions and the following disclaimer.


    (2) Redistributions in binary form must reproduce the above copyright notice,

    this list of conditions and the following disclaimer in the documentation

    and/or other materials provided with the distribution.


    (3) Neither the name of the University of California, Lawrence Berkeley

    National Laboratory, U.S. Dept. of Energy nor the names of its contributors

    may be used to endorse or promote products derived from this software without

    specific prior written permission.


    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"

    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE

    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE

    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE

    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL

    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR

    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER

    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,

    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE

    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


    You are under no obligation whatsoever to provide any bug fixes, patches, or

    upgrades to the features, functionality or performance of the source code

    ("Enhancements") to anyone; however, if you choose to make your Enhancements

    available either publicly, or directly to Lawrence Berkeley National

    Laboratory, without imposing a separate written license agreement for such

    Enhancements, then you hereby grant the following license: a  non-exclusive,

    royalty-free perpetual license to install, use, modify, prepare derivative

    works, incorporate into other computer software, distribute, and sublicense

    such enhancements or derivative works thereof, in binary and source code form.


    If you have questions about your rights to use or distribute this software,

    please contact Berkeley Lab's Innovation & Partnerships Office at

    IPO@lbl.gov.


    NOTICE.  This Software was developed under funding from the U.S. Department of

    Energy and the U.S. Government consequently retains certain rights. As such,

    the U.S. Government has been granted for itself and others acting on its

    behalf a paid-up, nonexclusive, irrevocable, worldwide license in the Software

    to reproduce, distribute copies to the public, prepare derivative works, and

    perform publicly and display publicly, and to permit other to do so.


In layman terms...
==================

In addition to the (already widely used and very free open source)
standard BSD 3 clause license, there is also wording specific to
contributors which ensures that we have permission to release,
distribute and include a particular contribution, enhancement, or fix as
part of Singularity proper. For example any contributions submitted will
have the standard BSD 3 clause terms (unless specifically and otherwise
stated) and that the contribution is comprised of original new code that
the contributor has authority to contribute.
