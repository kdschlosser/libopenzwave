# -*- coding: utf-8 -*-

# **libopenzwave** is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# **libopenzwave** is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libopenzwave. If not, see http://www.gnu.org/licenses.

"""

This file is part of the **libopenzwave** project

:platform: Unix, Windows, OSX
:license: GPL(v3)
:synopsis: wrapper for :py:class:`libopenzwave.PyManager`

.. moduleauthor:: Kevin G Schlosser
"""

import os
import sys
import logging
from logging import NullHandler

import _libopenzwave  # NOQA

FORMAT = '%(asctime)-15s - %(message)s'

logging.lastResort = None
logging.basicConfig(level=None, format=FORMAT)


LOGGING_DATA_PATH = 60
LOGGING_DATA_PATH_WITH_RETURN = 70
LOGGING_TIME_FUNCTION_CALLS = 80

logging.addLevelName(
    LOGGING_DATA_PATH,
    'LOGGING_DATA_PATH'
)
logging.addLevelName(
    LOGGING_DATA_PATH_WITH_RETURN,
    'LOGGING_DATA_PATH_WITH_RETURN'
)
logging.addLevelName(
    LOGGING_TIME_FUNCTION_CALLS,
    'LOGGING_TIME_FUNCTION_CALLS'
)

_loggerClass = logging._loggerClass  # NOQA


class _Logger(logging.Logger):

    def __new__(cls, name):
        if (
            name.startswith(__name__.rsplit('.', 1)[0]) or
            name == '_libopenzwave'
        ):
            return super(_Logger, cls).__new__(cls)

        return _loggerClass.__new__(cls)

    def __init__(self, name):
        logging.Logger.__init__(self, name)
        self.__console_output = False
        self.__log_file = None
        self.__file_mode = 'w'

    def write_mode(self, mode):
        self.__file_mode = mode

    write_mode = property(fset=write_mode)

    def log_file(self, file_path):

        path, file_name = os.path.split(file_path)

        if self.name == '_libopenwave':
            file_name = 'Lib' + file_name
        else:
            file_name = 'Py' + file_name

        handler = logging.FileHandler(
            os.path.join(path, file_name),
            self.__file_mode
        )
        handler.setLevel(self.getEffectiveLevel())

        formatter = logging.Formatter(FORMAT)
        handler.setFormatter(formatter)

        self.addHandler(handler)

    log_file = property(fset=log_file)

    def console_output(self, value):
        self.__console_output = value

    console_output = property(fset=console_output)

    def callHandlers(self, record):
        """
        Pass a record to all relevant handlers.

        Loop through all handlers for this logger and its parents in the
        logger hierarchy. If no handler was found, output a one-off error
        message to sys.stderr. Stop searching up the hierarchy whenever a
        logger with the "propagate" attribute set to zero is found - that
        will be the last logger whose handlers are called.
        """
        c = self
        found = 0
        while c:
            for hdlr in c.handlers:
                found = found + 1
                if (
                    not isinstance(hdlr, logging.NullHandler) and
                    hasattr(hdlr, 'stream') and
                    hdlr.stream == sys.stderr and  # NOQA
                    self.__console_output
                ):
                    if record.levelno >= hdlr.level:
                        hdlr.handle(record)

                elif record.levelno >= hdlr.level:
                    hdlr.handle(record)

            if not c.propagate:
                c = None
            else:
                c = c.parent

    def setLevel(self, level):
        if level == self.getEffectiveLevel():
            return

        logging.Logger.setLevel(self, level)

        log_level_mapping = {
            logging.DEBUG: 'Debug',
            logging.WARNING: 'Warning',
            logging.ERROR: 'Error',
            logging.INFO: 'Info',
            logging.NOTSET: 'None',
            LOGGING_DATA_PATH: 'Debug',
            LOGGING_DATA_PATH_WITH_RETURN: 'Debug',
            LOGGING_TIME_FUNCTION_CALLS: 'Debug'
        }

        save_log_level = log_level_mapping[level]

        from .option import ZWaveOption

        for options in ZWaveOption._instances.values():  # NOQA
            if not options.areLocked():
                options.save_log_level = save_log_level

                if level == logging.NOTSET:
                    options.logging = False


logging._loggerClass = _Logger

openzwave_logger = logging.getLogger(__name__.rsplit('.', 1)[0])
openzwave_logger.addHandler(NullHandler())
openzwave_logger.setLevel(logging.INFO)

libopenzwave_logger = logging.getLogger('_libopenzwave')
libopenzwave_logger.addHandler(NullHandler())
libopenzwave_logger.setLevel(logging.INFO)


class Logger(object):
    """
    Wrapper class for logging

    This class handles logging changes made for both libopenzwave and
    _libopenzwave it can be accessed by using `libopenzwave.logger`.

    We have also set into place a wrapper around the logging.Logger class.
    This wrapper is what gets used when calling
    `logging.getLogger(module_name)`. The wrapper class overrides the __new__
    method and does a check of the name being passed to it. if the name is
    "_libopenzwave" or name.startswith(__name__.rsplit('.', 1)[0]) the latter
    would normally be "openzwave" but allows for the library to be embedded
    into other libraries it will wrap the Logging class. otherwise it will
    return the usual class `logging.Logger`. The wrapped class does a special
    thing, any changes made to the wrapped instance is going to also make
    changes to any `libopenzwave.ZWaveOption` instance that exists. because
    openzwave and python-openzwave handle logging individually We wanted to
    create a mechanism that would remove have to have any knowledge of there
    being 2 places where logging would need to be set. This process also works
    in reverse any changes made to a `libopenzwave.ZWaveOption` instance is going
    to adjust the logging in python as well.

    * `ZWaveOption.logging`: boolean to enable or disable logging.
      This is also going to enable or disable the python logging.
    * `ZWaveOption.save_log_level`:
      Here is the mapping from save_log_level to python log level mapping
      'Debug' = `logging.DEBUG`
      'Warning' = `logging.WARNING`
      'Error' = `logging.ERROR`
      'Info' = `logging.INFO`
      'None' = `logging.NOTSET`

      and here is the python log level to save_log_level mapping.
      `logging.DEBUG` = 'Debug'
      `logging.WARNING` = 'Warning'
      `logging.ERROR` = 'Error'
      `logging.INFO` = 'Info'
      `logging.NOTSET` = 'None'
      `libopenzwave.logger.LOGGING_DATA_PATH` = 'Debug'
      `libopenzwave.logger.LOGGING_DATA_PATH_WITH_RETURN` = 'Debug'
      `libopenzwave.logger.LOGGING_TIME_FUNCTION_CALLS` = 'Debug'

    * `ZWaveOption.console_output`: this is going to also enable or disable
      the console output for the python logging.
    * `ZWaveOptions.log_file`: If this gets set the python logging will use
      the same path but it is going to prepend "Py" to the filename.
    * `ZWaveOption.append_log_file`: sets the write mode on the python logging
    """

    LOGGING_DATA_PATH = LOGGING_DATA_PATH
    LOGGING_DATA_PATH_WITH_RETURN = LOGGING_DATA_PATH_WITH_RETURN
    LOGGING_TIME_FUNCTION_CALLS = LOGGING_TIME_FUNCTION_CALLS

    def __init__(self):
        pass

    def __getattr__(self, item):

        try:
            ozw_attr = getattr(openzwave_logger, item)
            libozw_attr = getattr(libopenzwave_logger, item)
        except AttributeError:
            try:
                return getattr(logging, item)
            except AttributeError:
                raise AttributeError(item)

        if hasattr(ozw_attr, '__call__'):
            class Wrapper(object):

                def __init__(self, func1, func2):
                    self._func1 = func1
                    self._func2 = func2

                def __call__(self, *args, **kwargs):
                    self._func2(*args, **kwargs)
                    return self._func1(*args, **kwargs)

            return Wrapper(ozw_attr, libozw_attr)

        return ozw_attr

    def __setattr__(self, key, value):
        setattr(openzwave_logger, key, value)
        setattr(libopenzwave_logger, key, value)
