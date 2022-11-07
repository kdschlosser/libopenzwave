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
:synopsis: OpenZWave options

.. moduleauthor:: Kevin G Schlosser
"""

import os
import logging

import traceback
from platform import system as platform_system

import _libopenzwave
from .exception import ZWaveException
from .singleton import InstanceSingleton


logger = logging.getLogger(__name__)


def _expand_path(path):
    if path is None:
        return path

    if '$' in path or '%' in path:
        path = os.path.expandvars(path)

    if '~' in path:
        path = path.replace(
            '~',
            os.path.expanduser('~')
        )

    return os.path.abspath(path)


VENDOR_IDS = ('0658',)


def _get_z_stick():
    try:
        # noinspection PyPackageRequirements
        import serial.tools.list_ports
    except ImportError:
        return None

    for port in serial.tools.list_ports.comports():
        if port.vid is None:
            continue
        if port.product is not None and 'Zigbee' in port.product:
            continue
        if port.interface is not None and 'Zigbee' in port.interface:
            continue
        if port.description is not None and 'Zigbee' in port.description:
            continue

        for vid in VENDOR_IDS:
            if vid.upper() == hex(port.vid)[2:].upper().zfill(4):
                return port.device
    return None

import weakref


class ZWaveOption(_libopenzwave.PyOptions):
    """
    Represents a Zwave option used to start the manager.
    """

    _instances = {}

    def __del__(self):
        args = (
            self.device,
            self.config_path,
            self.user_path,
            self.cmd_line
        )
        if args in ZWaveOption._instances:
            del ZWaveOption._instances[args]

    def __init__(
        self,
        device='',
        config_path='',
        user_path='',
        cmd_line=''
    ):
        """
        Create an option object and check that parameters are valid.

        :param device: The device to use or None for auto detection.
          Optionally you can set this to the ip and port of a remote server.
        :type device: str, optional

        :param config_path: The openzwave config directory. If None, try to
            configure automatically.
        :type config_path: str, optional

        :param user_path: The user directory
        :type user_path: str, optional

        :param cmd_line: The "command line" options of the openzwave library
        :type cmd_line: str, optional
        """
        self.__use_server = False
        self.__server_port = 61611
        self.__server_ip = '127.0.0.1'
        self.__admin_password = None
        self.__ssl_key_path = None
        self.__ssl_server_cert_path = None
        self.__ssl_client_cert_path = None
        self._local_connection = True
        self.__is_locked = False

        self.__append_log_file = False
        self.__logging = True
        self.__console_output = True
        self.__log_file = None
        self.__save_log_level = _libopenzwave.PyLogLevels[7]

        if device is None:
            device = _get_z_stick()

            if not device:
                raise RuntimeError(
                    'Unable to automatically locate USB Stick. '
                    'You will need to provide a serial port.'
                )

        for port in ('COM', 'CNC', '\\', '/', 'TTY'):
            if device.upper().startswith(port):
                break
        else:
            if ':' in device:
                hostname, port = device.split(':')
            else:
                hostname = device
                port = '61611'

            self._device = '{0}:{1}'.format(hostname, port)
            self._local_connection = False
            return

        if platform_system() == 'Windows':
            if device and not device.startswith('\\\\.\\'):
                device = '\\\\.\\' + device

            self._device = device
        else:
            # For linux
            try:
                if os.path.exists(device):
                    if (
                        os.access(device, os.R_OK) and
                        os.access(device, os.W_OK)
                    ):
                        self._device = device
                    else:
                        raise ZWaveException(
                            "Can't write to device %s : %s" % (
                                device,
                                traceback.format_exc()
                            )
                        )
                else:
                    raise ZWaveException(
                        "Can't find device %s : %s" % (
                            device,
                            traceback.format_exc()
                        )
                    )
            except:
                raise ZWaveException(
                    "Error when retrieving device %s : %s" % (
                        device,
                        traceback.format_exc()
                    )
                )

        if user_path is None:
            if platform_system() == 'Windows':
                user_path = os.path.expandvars('%PROGRAMDATA%')
            else:
                user_path = os.path.expanduser('~')

            if user_path:
                user_path = os.path.join(user_path, '.openzwave')
                if not os.path.exists(user_path):
                    os.mkdir(user_path)
            else:
                user_path = None

        config_path = _expand_path(config_path)
        user_path = _expand_path(user_path)

        _libopenzwave.PyOptions.__init__(
            self,
            config_path=config_path,
            user_path=user_path,
            cmd_line=cmd_line
        )

        args = (
            self.device,
            self.config_path,
            self.user_path,
            self.cmd_line
        )
        if args in ZWaveOption._instances:
            instance = ZWaveOption._instances[args]()

            if instance is None:
                del ZWaveOption._instances[args]
                ZWaveOption._instances[args] = weakref.ref(self)
            else:
                self.__dict__.update(instance.__dict__)

        else:
            ZWaveOption._instances[args] = weakref.ref(self)

    def create(self):
        if self._local_connection:
            _libopenzwave.PyOptions.create(self)

    create.__doc__ = _libopenzwave.PyOptions.create.__doc__

    def destroy(self):
        if self._local_connection:
            _libopenzwave.PyOptions.destroy(self)

        logger.info('options destroyed')

    destroy.__doc__ = _libopenzwave.PyOptions.destroy.__doc__

    def lock(self):
        if not self.areLocked():
            log_level_mapping = {
                'Debug':   logging.DEBUG,
                'Warning': logging.WARNING,
                'Error':   logging.ERROR,
                'Info':    logging.INFO,
                'None_':   logging.NOTSET,
            }

            log_level = self.save_log_level
            console_output = self.console_output
            log_file = self.log_file

            if log_file == 'OZW_Log.txt':
                log_file = os.path.join(self._user_path, log_file)

            disabled = not self.logging
            write_mode = 'a' if self.append_log_file else 'w'

            lib_logger = logging.getLogger('libopenzwave')
            ozw_logger = logging.getLogger(__name__.rsplit('.', 1)[0])

            if log_level in log_level_mapping:

                lib_logger.setLevel(log_level_mapping[log_level])
                ozw_logger.setLevel(log_level_mapping[log_level])

            lib_logger.write_mode = write_mode
            ozw_logger.write_mode = write_mode

            lib_logger.log_file = log_file
            ozw_logger.log_file = log_file

            lib_logger.console_output = console_output
            ozw_logger.console_output = console_output

            lib_logger.disabled = disabled
            ozw_logger.disabled = disabled

        if self._local_connection:
            res = _libopenzwave.PyOptions.lock(self)
            return res

        else:
            self.__is_locked = True
            return True

    lock.__doc__ = _libopenzwave.PyOptions.lock.__doc__

    def areLocked(self):
        if self._local_connection:
            return _libopenzwave.PyOptions.areLocked(self)
        else:
            return self.__is_locked

    areLocked.__doc__ = _libopenzwave.PyOptions.areLocked.__doc__

    def addOptionBool(self, name, value):
        if self._local_connection:
            _libopenzwave.PyOptions.addOptionBool(self, name, value)

    addOptionBool.__doc__ = _libopenzwave.PyOptions.addOptionBool.__doc__

    def addOptionInt(self, name, value):
        if self._local_connection:
            _libopenzwave.PyOptions.addOptionInt(self, name, value)

    addOptionInt.__doc__ = _libopenzwave.PyOptions.addOptionInt.__doc__

    def addOptionString(self, name, value, append=False):
        if self._local_connection:
            _libopenzwave.PyOptions.addOptionString(self, name, value, append)

    addOptionString.__doc__ = _libopenzwave.PyOptions.addOptionString.__doc__

    def getOptionAsBool(self, name):
        if self._local_connection:
            return _libopenzwave.PyOptions.getOptionAsBool(self, name)

    getOptionAsBool.__doc__ = _libopenzwave.PyOptions.getOptionAsBool.__doc__

    def getOptionAsInt(self, name):
        if self._local_connection:
            return _libopenzwave.PyOptions.getOptionAsInt(self, name)

    getOptionAsInt.__doc__ = _libopenzwave.PyOptions.getOptionAsInt.__doc__

    def getOptionAsString(self, name):
        if self._local_connection:
            return _libopenzwave.PyOptions.getOptionAsString(self, name)

    getOptionAsString.__doc__ = _libopenzwave.PyOptions.getOptionAsString.__doc__

    @property
    def single_notification_handler(self):
        """
        Use a single thread for handling openzwave notifications.

        Any information that openzwave needs to relay to python-openzwave that
        was not asked for directly by using a function gets gets sent via a
        callback. openzwave calls these notifications. openzwave has a single
        thread that handles the notifications, in previous versions of
        python-openzwave when the callback got called by openzwave the
        notification as never handed off to another thread. The thread from
        openzwave will follow all the way through processing all of the code
        right into the application. In the application if the processing of
        any GUI information took place in the signal callback that meant that
        the openzwave thread was doing the processing. The longer that thread
        remains busy doing other things it is not doing what it is supposed to
        be doing, processing the notifications. this would cause the
        appearance of "lag" in the network. when in reality it is the program.

        So what I have done is created a thread worker to handle this problem.
        This option if set to true will only use a single thread to process
        the incoming notifications from openzwave. a single thread is a good
        thing if you have low resources or a small network that is not busy.

        on the flip side if you have ample resources and have a lot of nodes
        you will want to keep this option set to False. if set to False you
        will have num_nodes + 1 thread workers. The +1 is a thread worker for
        network notifications. The threads for each node are not always
        running. There is a 3 second timeout for each thread worker. This
        allows for resources to be released. No point in consuming resources
        when doing nothing. if the timeout expires the worker thread creates
        the new thread but does not start it. The network worker is not too
        terribly busy this is the thread we use to check if a node has
        any notifications to process and if it does it starts the nodes thread.
        This is to keep the performance hit to as small as possible. We want to
        keep that openzwave thread doing what it needs to be doing.

        Defaulted to `False`

        :param value: `True`/`False`
        :type value: bool

        :return: `True`/`False`
        :rtype: bool
        """
        from . import notification_handler
        return notification_handler.use_single_handler

    @single_notification_handler.setter
    def single_notification_handler(self, value):
        from . import notification_handler

        notification_handler.use_single_handler = value

    @property
    def admin_password(self):
        """
        Get/Set Client/Server password.

        This must be set if using the server or using the client!
        The server and client passwords must be identical.

        :param value: password
        :type value: str

        :rtype: str
        """
        return self.__admin_password

    @admin_password.setter
    def admin_password(self, value):
        self.__admin_password = value

    @property
    def use_server(self):
        """
        Get/Set server active.

        Defaulted to `False`

        :param value: `True` to use the server and `False` to not.
        :type value: bool

        :rtype: bool
        """
        return self.__use_server

    @use_server.setter
    def use_server(self, value):
        if self._local_connection:
            self.__use_server = value

    @property
    def ssl_key_path(self):
        """
        Get/Set SSL key.

        If you want to use SSL you will need to provide the server and
        client cert paths as well as the path to the key.

        :param value: key path or None
        :type value: str, None

        :rtype: str, None
        """
        return self.__ssl_key_path

    @ssl_key_path.setter
    def ssl_key_path(self, value):
        if value is None:
            self.__ssl_key_path = None
        else:
            value = _expand_path(value)

            if os.path.exists(value):
                self.__ssl_key_path = value

    @property
    def ssl_client_cert_path(self):
        """
        Get/Set SSL client certificate.

        If you want to use SSL you will need to provide the server and
        client cert paths as well as the path to the key.

        :param value: client cert path or None
        :type value: str, None

        :rtype: str, None
        """
        return self.__ssl_client_cert_path

    @ssl_client_cert_path.setter
    def ssl_client_cert_path(self, value):
        if value is None:
            self.__ssl_client_cert_path = None
        else:
            value = _expand_path(value)

            if os.path.exists(value):
                self.__ssl_client_cert_path = value

    @property
    def ssl_server_cert_path(self):
        """
        Get/Set SSL server certificate.

        If you want to use SSL you will need to provide the server and
        client cert paths as well as the path to the key.

        :param value: server cert path or None
        :type value: str, None

        :rtype: str, None
        """
        return self.__ssl_server_cert_path

    @ssl_server_cert_path.setter
    def ssl_server_cert_path(self, value):
        if value is None:
            self.__ssl_server_cert_path = None
        else:
            value = _expand_path(value)

            if os.path.exists(value):
                self.__ssl_server_cert_path = value

    @property
    def server_port(self):
        """
        Get/Set the port to use for the server.

        Defaulted to `61611`

        :param value: port to use
        :type value: int

        :rtype: int
        """

        return self.__server_port

    @server_port.setter
    def server_port(self, value):
        self.__server_port = value

    @property
    def server_ip(self):
        """
        Get/Set the bind ip address for the server.

        Defaulted to 127.0.0.1

        :param value: ip address
        :type value: str

        :rtype: str
        """
        return self.__server_ip

    @server_ip.setter
    def server_ip(self, value):
        self.__server_ip = value

    @property
    def log_file(self):
        """
        Set the log file location.

        :param logfile: The location of the log file
        :type logfile: str

        :rtype: str
        """

        if self._local_connection:
            return self.getOptionAsString("LogFileName")
        elif self.__log_file is None:
            return os.path.join(self._user_path, 'OZW_Log.txt')
        else:
            return self.__log_file

    @log_file.setter
    def log_file(self, logfile):
        logfile = _expand_path(logfile)

        if self._local_connection:
            self.addOptionString("LogFileName", logfile)
        else:
            self.__log_file = logfile

    @property
    def logging(self):
        """
        Set the status of logging.

        :param status: `True` to activate logs, `False` to disable
        :type status: bool

        :return: `True`/`False`
        :rtype: bool
        """
        if self._local_connection:
            return self.getOptionAsString("Logging")
        else:
            return self.__logging

    @logging.setter
    def logging(self, status):
        if self._local_connection:
            self.addOptionBool("Logging", status)
        else:
            self.__logging = status

    @property
    def append_log_file(self):
        """
        Append new session logs to existing log file.

        :param status: `False` = overwrite
        :type status: bool

        :return: `True`/`False`
        :rtype: bool
        """
        if self._local_connection:
            return self.getOptionAsBool("AppendLogFile")
        else:
            return self.__append_log_file

    @append_log_file.setter
    def append_log_file(self, status):
        if self._local_connection:
            self.addOptionBool("AppendLogFile", status)
        else:
            self.__append_log_file = status

    @property
    def console_output(self):
        """
        Display log information on console (as well as save to disk).

        :param status: `True` = output to console
        :type status: bool

        :return: `True`/`False`
        :rtype: bool
        """
        if self._local_connection:
            return self.getOptionAsBool("ConsoleOutput")
        else:
            return self.__console_output

    @console_output.setter
    def console_output(self, status):
        if self._local_connection:
            self.addOptionBool("ConsoleOutput", status)
        else:
            self.__console_output = status

    @property
    def save_log_level(self):
        """
        Save (to file) log messages equal to or above LogLevel_Detail.

        :param level:
            PyLogLevels:

                * `"None"`: Disable all logging.
                * `"Always"`: These messages should always be shown.
                * `"Fatal"`: A likely fatal issue in the library.
                * `"Error"`: A serious issue with the library or the network.
                * `"Warning"`: A minor issue from which the library should be
                  able to recover.
                * `"Alert"`: Something unexpected by the library about which
                  the controlling application should be aware.
                * `"Info"`: Everything Is working fine... These messages
                  provide streamlined feedback on each message.
                * `"Detail"`: Detailed information on the progress of each
                  message.
                * `"Debug"`: Very detailed information on progress that will
                  create a huge log file quickly.
                * `"StreamDetail"`: Will include low-level byte transfers from
                  controller to buffer to application and back.
                * `"Internal"`: Used only within the log class
                  (uses existing timestamp, etc.).

        :type level: str, None

        :rtype: str, None
        """

        if self._local_connection:
            level = self.getOptionAsInt("SaveLogLevel")
            if level == 1:
                return None

            return _libopenzwave.PyLogLevels[level]
        else:
            return self.__save_log_level

    @save_log_level.setter
    def save_log_level(self, level):
        if level is None:
            level = str(level)

        level = level.replace('None', 'None_')

        if self._local_connection:
            self.addOptionInt(
                "SaveLogLevel",
                getattr(_libopenzwave.PyLogLevels, level).value
            )
        else:
            log_level_mapping = [
                'Invalid'
                'None_'
                'Always'
                'Fatal'
                'Error'
                'Warning'
                'Alert'
                'Info'
                'Detail'
                'Debug'
                'StreamDetail'
                'Internal'
            ]
            self.__save_log_level = (
                _libopenzwave.PyLogLevels[log_level_mapping.index(level)]
            )

    @property
    def queue_log_level(self):
        """
        Save (in RAM) log messages equal to or above LogLevel_Debug.

        :param level:
            PyLogLevels:
                * `"None"`: Disable all logging.
                * `"Always"`: These messages should always be shown.
                * `"Fatal"`: A likely fatal issue in the library.
                * `"Error"`: A serious issue with the library or the network.
                * `"Warning"`: A minor issue from which the library should be
                  able to recover.
                * `"Alert"`: Something unexpected by the library about which
                  the controlling application should be aware.
                * `"Info"`: Everything Is working fine... These messages
                  provide streamlined feedback on each message.
                * `"Detail"`: Detailed information on the progress of each
                  message.
                * `"Debug"`: Very detailed information on progress that will
                  create a huge log file quickly.
                * `"StreamDetail"`: Will include low-level byte transfers from
                  controller to buffer to application and back.
                * `"Internal"`: Used only within the log class
                  (uses existing timestamp, etc.).

        :type level: str, None

        :rtype: str, None
        """
        if self._local_connection:

            level = self.getOptionAsInt("QueueLogLevel")
            if level == 1:
                return None

            return _libopenzwave.PyLogLevels[level]

    @queue_log_level.setter
    def queue_log_level(self, level):
        if self._local_connection:
            if level is None:
                level = str(level)

            level = level.replace('None', 'None_')
            self.addOptionInt(
                "QueueLogLevel",
                getattr(_libopenzwave.PyLogLevels, level).value
            )

    @property
    def dump_trigger_level(self):
        """
        Default is to never dump RAM-stored log messages.

        :param level:
            PyLogLevels:
                * `"None"`: Disable all logging.
                * `"Always"`: These messages should always be shown.
                * `"Fatal"`: A likely fatal issue in the library.
                * `"Error"`: A serious issue with the library or the network.
                * `"Warning"`: A minor issue from which the library should be
                  able to recover.
                * `"Alert"`: Something unexpected by the library about which
                  the controlling application should be aware.
                * `"Info"`: Everything Is working fine... These messages
                  provide streamlined feedback on each message.
                * `"Detail"`: Detailed information on the progress of each
                  message.
                * `"Debug"`: Very detailed information on progress that will
                  create a huge log file quickly.
                * `"StreamDetail"`: Will include low-level byte transfers from
                  controller to buffer to application and back.
                * `"Internal"`: Used only within the log class
                  (uses existing timestamp, etc.).

        :type level: str, None

        :rtype: str, None
        """
        if self._local_connection:

            level = self.getOptionAsInt("DumpTriggerLevel")
            if level == 1:
                return None

            return _libopenzwave.PyLogLevels[level]

    @dump_trigger_level.setter
    def dump_trigger_level(self, level):
        if self._local_connection:
            if level is None:
                level = str(level)

            level = level.replace('None', 'None_')
            self.addOptionInt(
                "DumpTriggerLevel",
                getattr(_libopenzwave.PyLogLevels, level).value
            )

    @property
    def include_instance_label(self):
        """
        Should we include the Instance Label in Value Labels on
        MultiInstance Devices

        :param flag: `True`/`False`
        :return: bool

        :return: `True`/`False`
        :rtype: bool, None
        """
        if self._local_connection:
            return self.getOptionAsBool("IncludeInstanceLabel")

    @include_instance_label.setter
    def include_instance_label(self, flag):
        if self._local_connection:
            self.addOptionBool("IncludeInstanceLabel", flag)

    @property
    def reload_nodes_after_config_update(self):
        """
        The Node will be reloaded depending upon the Option
        "ReloadAfterUpdate"

        :param option: Valid Options include:

            * `"Never"`: Never Reload a Node after updating the Config File.
              Manual Reload is Required.
            * `"Immediate"`: Reload the Node Immediately after downloading
              the latest revision
            * `"Awake"`: Reload Nodes only when they are awake
              (Always-On Nodes will reload immediately, Sleeping Nodes will
              reload when they wake up
        :type option: str

        :rtype: str, None
        """
        if self._local_connection:
            return self.getOptionAsString("ReloadAfterUpdate")

    @reload_nodes_after_config_update.setter
    def reload_nodes_after_config_update(self, option):
        if self._local_connection:
            self.addOptionString("ReloadAfterUpdate", option)

    @property
    def associate(self):
        """
        Enable automatic association of the controller with group one of every
        device.

        :param status: `True` to enable logs, `False` to disable
        :type status: bool

        :return: `True`/`False`
        :rtype: bool, None
        """
        if self._local_connection:
            return self.getOptionAsBool("Associate")

    @associate.setter
    def associate(self, status):
        if self._local_connection:
            self.addOptionBool("Associate", status)

    @property
    def exclude(self):
        """
        Remove support for the added command classes.

        :param command_class: The command class to exclude
        :type command_class: str

        :rtype: str, None
        """
        if self._local_connection:
            return self.getOptionAsString("Exclude")

    @exclude.setter
    def exclude(self, command_class):
        if self._local_connection:
            self.addOptionString("Exclude", command_class, True)

    @property
    def include(self):
        """
        Only handle the specified command classes.

        The Exclude option is ignored if anything is seted here.

        :param command_class: The location of the log file
        :type command_class: str

        :rtype: str, None
        """
        if self._local_connection:
            return self.getOptionAsString("Include")

    @include.setter
    def include(self, command_class):
        if self._local_connection:
            self.addOptionString("Include", command_class, True)

    @property
    def notify_transactions(self):
        """
        Notifications when transaction complete is reported.

        :param status: True to enable, False to disable
        :type status: bool

        :return: `True`/`False`
        :rtype: bool, None
        """
        if self._local_connection:
            return self.getOptionAsBool("NotifyTransactions")

    @notify_transactions.setter
    def notify_transactions(self, status):
        if self._local_connection:
            self.addOptionBool("NotifyTransactions", status)

    @property
    def interface(self):
        """
        Identify the serial port to be accessed

        TODO: change the code so more than one serial
          port can be specified and HID

        :param port: The serial port
        :type port: str

        :rtype: str, None
        """
        if self._local_connection:
            return self.getOptionAsString("Interface")

    @interface.setter
    def interface(self, port):
        if self._local_connection:
            self.addOptionString("Interface", port, True)

    @property
    def save_configuration(self):
        """
        Save the XML configuration upon driver close.

        :param status: `True` to enable, `False` to disable
        :type status: bool

        :return: `True`/`False`
        :rtype: bool, None
        """
        if self._local_connection:
            return self.getOptionAsBool("SaveConfiguration")

    @save_configuration.setter
    def save_configuration(self, status):
        if self._local_connection:
            self.addOptionBool("SaveConfiguration", status)

    @property
    def driver_max_attempts(self):
        """
        Set the driver max attempts before raising an error.

        :param attempts: Number of attempts
        :type attempts: int

        :rtype: int, None
        """
        if self._local_connection:
            return self.getOptionAsInt("DriverMaxAttempts")

    @driver_max_attempts.setter
    def driver_max_attempts(self, attempts):
        if self._local_connection:
            self.addOptionInt("DriverMaxAttempts", attempts)

    @property
    def poll_interval(self):
        """
        30 seconds (can easily poll 30 values in this time; ~120 values is
        the effective limit for 30 seconds).

        :param interval: interval in seconds
        :type interval: int

        :rtype: int, None
        """
        if self._local_connection:
            return self.getOptionAsInt("PollInterval")

    @poll_interval.setter
    def poll_interval(self, interval):
        if self._local_connection:
            self.addOptionInt("PollInterval", interval)

    @property
    def interval_between_polls(self):
        """
        Notifications when transaction complete is reported.

        :param status: if `False`, try to execute the entire poll set within
            the PollInterval time frame. If true, wait for PollInterval
            milliseconds between polls
        :type status: bool

        :return: `True`/`False`
        :rtype: bool, None
        """
        if self._local_connection:
            return self.getOptionAsBool("IntervalBetweenPolls")

    @interval_between_polls.setter
    def interval_between_polls(self, status):
        if self._local_connection:
            self.addOptionBool("IntervalBetweenPolls", status)

    @property
    def suppress_value_refresh(self):
        """
        if `True`, notifications for refreshed (but unchanged) values will not
        be sent.

        :param status: `True` to enable, `False` to disable
        :type status: bool

        :return: `True`/`False`
        :rtype: bool, None
        """
        if self._local_connection:
            return self.getOptionAsBool("SuppressValueRefresh")

    @suppress_value_refresh.setter
    def suppress_value_refresh(self, status):
        if self._local_connection:
            self.addOptionBool("SuppressValueRefresh", status)

    @property
    def security_strategy(self):
        """
        Should we encrypt CC's that are available via both clear text and
        Security CC?

        :param strategy: The security strategy : SUPPORTED|ESSENTIAL|CUSTOM
        :type strategy: str

        :rtype: str, None
        """
        if self._local_connection:
            return self.getOptionAsString("SecurityStrategy")

    @security_strategy.setter
    def security_strategy(self, strategy='SUPPORTED'):
        if self._local_connection:
            self.addOptionString("SecurityStrategy", strategy)

    @property
    def custom_secured_cc(self):
        """
        What List of Custom CC should we always encrypt if SecurityStrategy
        is CUSTOM.

        :param custom_cc: List of Custom CC
        :type custom_cc: str

        :rtype: str, None
        """
        if self._local_connection:
            return self.getOptionAsString("CustomSecuredCC")

    @custom_secured_cc.setter
    def custom_secured_cc(self, custom_cc='0x62,0x4c,0x63'):
        if self._local_connection:
            self.addOptionString("CustomSecuredCC", custom_cc)

    @property
    def cmd_line(self):
        """
        :rtype: str
        """
        return self._cmd_line

    @property
    def device(self):
        """
        The device used by the controller.

        :rtype: str
        """
        return self._device

    @property
    def config_path(self):
        """
        The config path.

        :rtype: str, None
        """
        if self._local_connection:
            return self._config_path

    @property
    def user_path(self):
        """
        The user path.

        :rtype: str, None
        """
        if self._local_connection:
            return self._user_path
