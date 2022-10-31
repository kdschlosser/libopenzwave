:orphan:

Install the needed tools
========================

You must install git and other tools to get sources of libopenzwave and
openzwave and build them. Look at the documentation of your Linux distribution to do that.

On a debian like distribution :

.. code-block:: bash

    sudo make deps

Build process
=============

Now, you can compile sources :

.. code-block:: bash

    make build

If you have already built libopenzwave or if the build failed
you can use the clean target and build again :

.. code-block:: bash

    sudo make clean
    make build

Do not use root to build libopenzwave as root it will surely fails. Please use a "normal user".


Installation
============

You can now install the packages using the following command :

.. code-block:: bash

    sudo make install

You can remove libopenzwave using :

.. code-block:: bash

    sudo make uninstall

If it fails
===========

Simply remove the libopenzwave-x.y.z directory and extract it again.

