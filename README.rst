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

The build process has been rewritten. It is entirely controlled using distutils
The --flavor option has been removed in favor of using build commands.

There is now a single command line option --dev which will download the master
branch of ozw (OpenZWave) on GitHub. This is the branch that gets used to add
new code that is going to get released. If no --dev option is specified then
the latest release of ozw that will work gets downloaded.

Here are the build commands.

* build

  .. code-block:: cmd

      python setup.py build


and these are the install commands

* install

  .. code-block:: cmd

      python setup.py install

To add the development switch to any of the above

.. code-block:: cmd

      python setup.py {build command} --dev

I am going to recommend building the documentation I have spent quite a bit of
time documenting everything and I have also added quite a few code examples.

.. code-block:: cmd

    python setup.py build_docs


You also can optionally chain the build commands.

.. code-block:: cmd

    python setup.py build build_docs --dev


Any requirements that only get used during the build process do not get
installed into your site-packages folder. This makes for easy cleanup. Any
requirements that are not needed to run are place into the `.egg` directory
where this readme file is located.

all build output is placed into a directory called `build` where this readme
file is located.


------------------------------------------
PLEASE BUILD THE DOCUMENTATION AND READ IT
------------------------------------------

This is not a drop in replacement for python-openzwave. reading the
documentation is going help you to get pyozw up and running. There are way to
many API breaking changes to list.
