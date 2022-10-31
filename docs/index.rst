============================================
Welcome to libopenzwave's documentation!
============================================

OK so lets get some of the formalities out of the way.

|
|

Copyright information
---------------------

libopenzwave is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

libopenzwave is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with libopenzwave. If not, see http://www.gnu.org/licenses.

:license: GPL(v3)
:platform: Unix, Windows, OSX

|
|

Authors
-------

This library has has many contributors. We want to thank everyone that has
contributed.

:author: Kevin G Schlosser
:author: bibi21000 @bibi21000 <bibi21000@gmail.com>
:author: maarten damen


|
|

Bug Reports
-----------

While we all do hate stumbling across an issue in the program it does require
you to inform us if the problem. If we do not know there is a problem then we
do not know to fix it.

We do know it can be a real pain to report these issues so we want to keep it
as simple as possible.

This library is typically an addon component to a larger application. While we
do want to know of an issue in our code we need to make sure the issue is in
python-openzwave and not in the application code that uses this library.

The best thing to do if you encounter a bug is to report it to the authors of
the application first. Most times if there is an issue in python-openzwave
the authors of the application will either correct the problem and submit the
fix for us to add it, or they will inform us there is a problem.

In order to know 100% that the problem is in libopenzwave we may ask you to
separate the application from libopenzwave. This is not a difficult thing
to accomplish, you will have to create a test script that only uses
libopenzwave. In that test script you will need to code in whatever is
needed to make the problem reproducible. Once you have done this creating an
issue on GitHub <https://github.com/kdschlosser/libopenzwave> is the best way
to get our attention.

The E-mail addresses contained within this help document are not to be used to
communicate with us. Chances are unless we know you are using the e-mail we
are not going to be checking it. Because this is a public document there is
going to be no spam filter capable of dealing with the amount of spam messages
the e-mail addresses in this document receive. We will not go hunting for a
missed e-mail. So please use the issue tracker on GitHub.

|
|

Issue Template
--------------

*Operating System:* Windows, Linux Flavor, OSX
*Operating System Version:*

*Application Name:* Name of the application that you are using.
*Application Version:*
*Application Website:*

*Affected node type:* dimmer switch, motion sensor, etc...
*Affected node manufacturer:* the manufacturer name for the node.
*Affected node model number:*

*Description of the problem:* If there is an error you can paste the error here
Please use \`\`\` before the error and \`\`\` after the error. This will keep
the formatting correct. If there is no error produced but the data/behavior is
not correct provide as much detail as you can on what is not right and what
the expected data/behavior is supposed to be.

*How to replicate the problem:* Many times in order to track down a problem
some way of being able to reproduce the issue is needed. We do prefer this to
be code that is already written that we will just have to run. If you are not
a developer or do not know how to produce the problem by writing a script
then providing as much detail as to what you think is taking place will be
helpful. If you do not provide any information on how to reproduce the issue
it will be extremely difficult for us to isolate and fix the problem. Many
times if there is an error produced this is going to contain all of the
information needed to be able to repair the problem. So make sure that you do
provide the entire error output.

|
|

========
Contents
========

.. toctree::
    :maxdepth: 2

    Installation Instructions. </install/index>
    The libopenzwave modules. <modules>
    Changelog. <CHANGELOG>
    Development information. <DEVEL>
    Copyright. <COPYRIGHT>

|
|

==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

