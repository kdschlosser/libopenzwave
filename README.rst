================
libopenzwave
================

This is a test version of libopenzwave. Do not use this in a production
environment.


This is a highly modified version of python-openzwave Almost the
entire library has been rewritten. This has been done to improve functionality,
ease of use and performance.


------------------
Build Instructions
------------------

Requirements

  * Python 3.8, 3.9 or 3.10.

    * Run `pip install -r build_requirements.txt` and all the needed
      requirements for your python version will be installed
|

  * Windows

    * Visual Studio >= 2019
    * Windows SDK (latest)
|

  * Ubuntu

    * libudev-dev
    * g++
    * libyaml-dev
    * libusb-1.0
    * python "-dev" package for the version of Python you are running.
|

  * OSX
    * ??? It compiles on Azure Pipelines but I do not know what is installed
    onto the VM that is used in the pipeline
    * python "-dev" package for the version of Python you are running.
|

  * FreeBSD

    * libresolv
    * libusb-1.0
    * e2fsprogs-libuuid
    * libiconv (if OS version is < 10.2.0)
    * python "-dev" package for the version of Python you are running.
|

  * NetBSD

    * libresolv
    * libusb-1.0
    * python "-dev" package for the version of Python you are running.
|

  * SunOS

    * libusb-1.0
    * python "-dev" package for the version of Python you are running.
|


There is only one build command you are going to want to use or one install
command The setup program takes all of the funky work to get a proper build
environment. It even works running Python >= 3.10 running on Windows with
Visual Studio > 2019 No need to set up a build environment on Windows. It is
better if you don't as Visual Studio has been known to not set up correct build
environments.

  * `python setup.py build --cython`
  * `python setup.py install --cython`

The `--cython` switch tells the setup program to compile the entire library
into C extensions. It is not a requirement that you compile the whole library
using Cython but I do suggest it because it gives  a signifigant speed boost to
the library. A network with 30 nodes starts up > 10 seconds faster when the
entire library is compiled into C extensions.

Fear not!!!! Your IDE is still going to have auto complete and intellisense
with this library even when it is compiled into C extensions. You will find both
the source files and also the C extensions in the library directory. Python will
load the C extensions but an IDE will use the source files.

There are no Python 3 annotations yet. Most IDE's will use the Sphinx
annotations in the docstrings and most classes, methods and functions have
been done that way.


------------------------------------------
PLEASE BUILD THE DOCUMENTATION AND READ IT
------------------------------------------

Documentation building is not functional ye. Most classes, methods and functions
do have docstrings.

This is not a drop in replacement for python-openzwave. reading the
documentation is going help you to get pyozw up and running. There are way to
many API breaking changes to list.
