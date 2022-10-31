# -*- coding: utf-8 -*-
__license__ = """
This file is part of **python-openzwave** project

License : GPL(v3)

**libopenzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**libopenzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with libopenzwave. If not, see http://www.gnu.org/licenses.
"""
__copyright__ = "Copyright © 2022 Kevin G Schlosser"
__author__ = 'Kevin G Schlosser'
__email__ = ''
__version__ = '0.5.0'

try:
    __import__('pkg_resources').declare_namespace("libopenzwave")
except:  # NOQA
    # bootstrapping
    pass

from . import signals as _signals
from . import logger

LOGGING_DATA_PATH = logger.LOGGING_DATA_PATH
"""
Displays the data path.
"""
LOGGING_DATA_PATH_WITH_RETURN = logger.LOGGING_DATA_PATH_WITH_RETURN
"""
Displays the data path with returned values
"""
LOGGING_TIME_FUNCTION_CALLS = logger.LOGGING_TIME_FUNCTION_CALLS
"""
Displays code execution times.
"""


logger = logger.Logger()
"""
Instance of :py:class:`libopenzwave.logger.Logging`

The logging in openzwave is broken into 2 pieces, openzwave and libopenzwave.
This instance is a convenience feature that provides a single entry point to 
make changes to both pieces at the same time.
"""

SIGNAL_NODES_LOADED = _signals.SIGNAL_NODES_LOADED
SIGNAL_NODES_LOADED_SOME_DEAD = _signals.SIGNAL_NODES_LOADED_SOME_DEAD
SIGNAL_NODES_LOADED_AWAKE = _signals.SIGNAL_NODES_LOADED_AWAKE
SIGNAL_NODES_LOADED_ALL = _signals.SIGNAL_NODES_LOADED_ALL
SIGNAL_NETWORK_FAILED = _signals.SIGNAL_NETWORK_FAILED
SIGNAL_NETWORK_READY = _signals.SIGNAL_NETWORK_READY
SIGNAL_NETWORK_RESET = _signals.SIGNAL_NETWORK_RESET
SIGNAL_NETWORK_STARTED = _signals.SIGNAL_NETWORK_STARTED
SIGNAL_NETWORK_STOPPED = _signals.SIGNAL_NETWORK_STOPPED
SIGNAL_NETWORK_DATASET_LOADED = _signals.SIGNAL_NETWORK_DATASET_LOADED
SIGNAL_USER_ALERTS = _signals.SIGNAL_USER_ALERTS
SIGNAL_ALERT_DNS_ERROR = _signals.SIGNAL_ALERT_DNS_ERROR
SIGNAL_ALERT_UNSUPPORTED_CONTROLLER = (
    _signals.SIGNAL_ALERT_UNSUPPORTED_CONTROLLER
)
SIGNAL_ALERT_APPLICATION_STATUS_RETRY = (
    _signals.SIGNAL_ALERT_APPLICATION_STATUS_RETRY
)
SIGNAL_ALERT_APPLICATION_STATUS_QUEUED = (
    _signals.SIGNAL_ALERT_APPLICATION_STATUS_QUEUED
)
SIGNAL_ALERT_APPLICATION_STATUS_REJECTED = (
    _signals.SIGNAL_ALERT_APPLICATION_STATUS_REJECTED
)
SIGNAL_NETWORK_MANUFACTURER_DB_READY = (
    _signals.SIGNAL_NETWORK_MANUFACTURER_DB_READY
)
SIGNAL_NETWORK_CONTROLLER_COMMAND = _signals.SIGNAL_NETWORK_CONTROLLER_COMMAND
SIGNAL_NOTIFICATION = _signals.SIGNAL_NOTIFICATION
SIGNAL_VALUE_ADDED = _signals.SIGNAL_VALUE_ADDED
SIGNAL_VALUE_DATASET_LOADED = _signals.SIGNAL_VALUE_DATASET_LOADED
SIGNAL_VALUE_READY = _signals.SIGNAL_VALUE_READY
SIGNAL_VALUE_CHANGED = _signals.SIGNAL_VALUE_CHANGED
SIGNAL_VALUE_REFRESHED = _signals.SIGNAL_VALUE_REFRESHED
SIGNAL_VALUE_REMOVED = _signals.SIGNAL_VALUE_REMOVED
SIGNAL_NODE_ADDED = _signals.SIGNAL_NODE_ADDED
SIGNAL_NODE_DATASET_LOADED = _signals.SIGNAL_NODE_DATASET_LOADED
SIGNAL_NODE_NEW = _signals.SIGNAL_NODE_NEW
SIGNAL_NODE_LOADING_ESSENTIAL = _signals.SIGNAL_NODE_LOADING_ESSENTIAL
SIGNAL_NODE_READY = _signals.SIGNAL_NODE_READY
SIGNAL_NODE_REMOVED = _signals.SIGNAL_NODE_REMOVED
SIGNAL_NODE_RESET = _signals.SIGNAL_NODE_RESET
SIGNAL_ALERT_CONFIG_OUT_OF_DATE = _signals.SIGNAL_ALERT_CONFIG_OUT_OF_DATE
SIGNAL_ALERT_MFS_OUT_OF_DATE = _signals.SIGNAL_ALERT_MFS_OUT_OF_DATE
SIGNAL_ALERT_CONFIG_FILE_DOWNLOAD_FAILED = (
    _signals.SIGNAL_ALERT_CONFIG_FILE_DOWNLOAD_FAILED
)
SIGNAL_ALERT_RELOAD_REQUIRED = _signals.SIGNAL_ALERT_RELOAD_REQUIRED
SIGNAL_NODE_BUTTON_OFF = _signals.SIGNAL_NODE_BUTTON_OFF
SIGNAL_NODE_BUTTON_ON = _signals.SIGNAL_NODE_BUTTON_ON
SIGNAL_NODE_CREATE_BUTTON = _signals.SIGNAL_NODE_CREATE_BUTTON
SIGNAL_NODE_DELETE_BUTTON = _signals.SIGNAL_NODE_DELETE_BUTTON
SIGNAL_NODE_ASSOCIATION_GROUP = _signals.SIGNAL_NODE_ASSOCIATION_GROUP
SIGNAL_NODE_CONTROLLER_COMMAND = _signals.SIGNAL_NODE_CONTROLLER_COMMAND
SIGNAL_NODE_POLLING_DISABLED = _signals.SIGNAL_NODE_POLLING_DISABLED
SIGNAL_NODE_POLLING_ENABLED = _signals.SIGNAL_NODE_POLLING_ENABLED
SIGNAL_NODE_EVENT = _signals.SIGNAL_NODE_EVENT
SIGNAL_NODE_NAMING = _signals.SIGNAL_NODE_NAMING
SIGNAL_NODE_PROTOCOL_INFO = _signals.SIGNAL_NODE_PROTOCOL_INFO
SIGNAL_MSG_COMPLETE = _signals.SIGNAL_MSG_COMPLETE

SIGNAL_VIRTUAL_NODE_READY = _signals.SIGNAL_VIRTUAL_NODE_READY
SIGNAL_VIRTUAL_NODE_REMOVED = _signals.SIGNAL_VIRTUAL_NODE_REMOVED
SIGNAL_VIRTUAL_NODE_DATASET_LOADED = _signals.SIGNAL_VIRTUAL_NODE_DATASET_LOADED
SIGNAL_VIRTUAL_NODE_ADDED = _signals.SIGNAL_VIRTUAL_NODE_ADDED


from . import singleton as _singleton  # NOQA
from . import command_classes as _command_classes  # NOQA
from . import association_group as _association_group  # NOQA
from . import controller as _controller  # NOQA
from . import exception as _exception  # NOQA
from . import icon_type as _icon_type  # NOQA
from . import location as _location  # NOQA
from . import manager as _manager  # NOQA
from . import network as _network  # NOQA
from . import node as _node  # NOQA
from . import node_types as _node_types  # NOQA
from . import notification_handler as _notification_handler  # NOQA
from . import object as _object  # NOQA
from . import option as _option  # NOQA
from . import state as _state  # NOQA
from . import value as _value  # NOQA

ZWaveOption = _option.ZWaveOption
ZWaveNetwork = _network.ZWaveNetwork
ZWaveException = _exception.ZWaveException
ZWaveCommandClassException = _exception.ZWaveCommandClassException
ZWaveTypeException = _exception.ZWaveTypeException
subclass_zwave_class = _singleton.subclass_zwave_class
"""
Use this decorator to subclass ZWave classes.

This allows for injection of application code into the dynamic 
creation of quite a few objects
"""

del _command_classes
del _association_group
del _controller
del _exception
del _icon_type
del _location
del _manager
del _network
del _node
del _node_types
del _notification_handler
del _object
del _option
del _state
del _value
del _signals
