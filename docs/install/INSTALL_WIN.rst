:orphan:

======================================
Installing libopenzwave on Windows
======================================


PIP Install
===========

The easiest way to get openzwave running is by using pip

.. code-block:: doscon

    pip install libopenzwave



Build openzwave
==================

You will need a few things in order to build openzwave


Install Microsoft tools
=======================

You need to have an MSVC Compiler version >= 14 installed

You will need to have the proper Windows SDK version installed for the
compiler you are using.

MSVC Compiler is included in Visual Studio, Visual C++ and also Visual Studio Build Tools



Clone python-openzwave GitHub Repository
========================================

.. code-block:: doscon

    git clone https://github.com/kdschlosser/libopenzwave.git


Python-openzwave
================

Build:

    .. code-block:: doscon

        python setup.py build

Install:

    .. code-block:: doscon

        python setup.py install

Build Documentation:

    .. code-block:: doscon

        python setup.py build_docs

Build development:

    .. code-block:: doscon

        python setup.py build --dev

Install development:

    .. code-block:: doscon

        python setup.py install --dev

