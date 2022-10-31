:orphan:

=========
Changelog
=========

|

* python_openzwave 0.5.0:

    * Dynamic creation of ZWaveNode objects: There are not classes that
      represent the various COMMAND_CLASS_* constants. These classes are added
      to ZWaveNode if a device supports them. The classes add functionality
      that supports that command class.
    * Access to values are now identified by index and command class: The user
      is able to access the values by using an index name instead of a number.
    * Updated signals and notification system: Application code no longer needs
      to import the dispatcher. The sender attribute when registering to
      receive a signal callback now functions.
    * Distutils integrated documentation build system
    * Distutils compilation of OpenZWave.lib (Windows)
    * Build command line options have changed.
    * Build now grabs releases of OpenZWave
    * Removal of the controller thread locks.
    * Adds OpenZWave 1.6.x support.
    * Install and setup requirements handled in the build system

|

* python_openzwave 0.4.6.x:

    * First try to support Windows in pip

|

* python_openzwave 0.4.5.x:

    * Fix bug in node statistics and add test.
    * Update Makefile to build flavor dev
    * Update pyozw_check.
    * Update default flavor : check cython is here before choosing shared
    * Fix controller.update_ozw_config when directory isn't writable

|

* python_openzwave 0.4.4.x:

    * Add new options to pyozw_check to list nodes on network.

|

* python_openzwave 0.4.3.x:

    * Fix bug in default flavor.

|

* python_openzwave 0.4.1.x:

    * Update the default flavor : try to use a precompiled library. If can't
      find one, use the embeded package.
    * Add method to controller to get new config from github.

|

* python_openzwave 0.4.0.x:

    * New installation process via pip
    * Update your install_requires : both libopenzwave, openzwave and the
      manager are merged in python_openzwave package on pypi. Don't need to
      update your imports in code.
    * There will be major updates in the next releases, it's safe to use
      python_openzwave>0.4.0 and python_openzwave<0.5 in your requires.
    * Remove old versions of libopenzwave and openzwave before you update your
      installation with new pip process ... or not.
    * You can use the old installation process (via github), it's the one I
      use to develop.
    * Installation via archive method is no longer supported
      (no release for 0.4.0). Use pip instead with --flavor embed option.
    * Default mode is embed now.
    * Update config path discovery : check for 'device_classes.xml' in
      /etc/openzwave/, /usr/local/etc/openzwave/ and finally in ozw_config in
      python_openzwave module.
    * Add flavor : different ways of building and installing
      openzwave/python_openzwave.
    * Add information on flavor / build date to getPythonLibraryVersion
    * Improve installation on micro machines : embed_shared build and install
      openzwave/python_openzwave in 8 minutes on a raspberry pi 3
    * Add ozwdev and ozwdev_shared flavors : use openzwave dev branch instead
      of master
    * Rename to COMMAND_CLASS_MULTI_CHANNEL_V2 to
      COMMAND_CLASS_MULTI_INSTANCE/CHANNEL
    * Add tests for c++ library sync
    * Add door locks helpers
    * Add helpers for config parameters
    * Add data_items to value's dict

|

* python-openzwave 0.3.3:

    * Openzwave update
    * Update values getter in nodes. See #70
    * Fix setvalue for string types in python3

|

* python-openzwave 0.3.2:

    * Openzwave update
    * Add thermostat
    * Add patch from https://github.com/ebisso/python-openzwave/commit/8776daccc730cb5d7f71a178e9e0cc1d191ad115
    * Can compile dynamically

|

* python-openzwave 0.3.1:

    * Fix bugs and openzwave update

|

* python-openzwave 0.3.0:

    * Fix bugs and openzwave update

|

* python-openzwave 0.3.0-beta8:

    * Add multi instance support
    * Update GROUP notification : please update your code to add the new
      parameter
    * Update VALUE_REMOVED notification : please update your code to add the
      new parameter
    * Improve unicode : you may need to delete your old config file
    * Add Python 3 support
    * Improve controllers_command : add a lock and a way to retrieve current
      status
    * Add support for RGB bulbs

|

* python-openzwave 0.3.0-beta3:

    * Add security rewrite support.
      See https://groups.google.com/forum/#!msg/openzwave/cPjrvJJaESY/toK7QxEgRn0J
    * Add 2 signals for controller commands:
      ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND and
      ZWaveNetwork.SIGNAL_CONTROLLER_WAITING
    * Mark old methods and signals as deprecated. It is strongly recommended
      to use the new schema.
    * Add tests for controller commands.
    * Update isNodeAwake from function to property
    * Rename methods from node to be python compliant: is_awake, is_failed,
      is_ready, query_stage, is_info_received
    * Add facilities to run controller commands directly from node
    * Add request_state for node
    * Add new destroy method to network : use it to clean all openzwave
      c++ ressources

|

* python-openzwave 0.3.0-beta2:

    * Move to OpenZWave git organisation

|

* python-openzwave 0.3.0-beta1:

    * Add pyozwman script: after installing you can launch it wit:
      Usage: ozwsh [--device=/dev/ttyUSB0] [--log=Debug] ...
    * Add pyozwweb confiuration file.
    * Add version management in Makefile.

|

* python-openzwave 0.3.0-alpha3:

    * Fix bug in start/stop in network.
    * Fix bug in start/stop in pyozwweb app and tests.
    * Add map, scenes to PyOzwWeb
    * Add new tests
    * Fix some tests for controller commands
    * Finish the archive install : the lib is already cythonized. No need to
      install cython anymore.
    * Add a dockerfile
    * Add a branch for dockering with ptyhon 3

|

* python-openzwave 0.3.0-alpha2:

    * Fix bugs in lib
    * Fix bugs in API
    * Add kvals to API: allow user to store parameters with nodes,
      controllers, networks, ...
    * A a web demo : Flask + socket.io + jquery
    * Add logging facilities in the lib. Define different loggers for lib
      and api.

|

* python-openzwave 0.3.0-alpha1:

    * Update source tree to use setupttols develop mode:
      https://bitbucket.org/pypa/setuptools/issue/230/develop-mode-does-not-respect-src
    * Rewrite tests to use nosetest
    * Full implementation and tests of Options
    * PyLogLevels is now a dict of dicts to include doc: replace
      PyLogLevels[level] with PyLogLevels[level]['value'] in your code
    * Remove old scripts. Replace them with a Makefile
    * Remove old examples that do not work.
    * Add a constructor for PyOptions: def __init__(self, config_path=None,
      user_path=".", cmd_line=""). Please update your code.
