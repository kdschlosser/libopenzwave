:orphan:

======================================
Installing libopenzwave on Windows
======================================


Install Microsoft tools
=======================
Download and install Visual Studio and appropriate Windows SDK


Install other tools
===================

You need git to clone the repository and python (32 bits or 64 bits)

Install dependencies :

 - for python 3 :

    .. code-block:: bash

        (venvX) pip install Cython

clone repositories
==================

Clone libopenzwave:


.. code-block:: bash

    git clone https://github.com/kdschlosser/libopenzwave.git

And clone openzwave inside libopenzwave :

.. code-block:: bash

    cd libopenzwave
    git clone https://github.com/OpenZWave/open-zwave.git openzwave

It's mandatory to clone the previous repository in a directory called openzwave (not open-zwave)