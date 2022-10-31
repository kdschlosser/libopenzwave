# -*- coding: utf-8 -*-
#cython: c_string_type=unicode, c_string_encoding=utf8

"""
.. module:: _libopenzwave

This file is part of **libopenzwave** project

:platform: Unix, Windows, MacOS X
:synopsis: openzwave C++

.. moduleauthor: Kevin Schlosser @kdschlosser <kevin.g.schlosser@gmail.com>
.. moduleauthor: bibi21000 aka Sebastien GALLET <bibi21000@gmail.com>
.. moduleauthor: Maarten Damen <m.damen@gmail.com>

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
import traceback

# noinspection PyUnresolvedReferences
from cython.operator cimport dereference as deref

from libcpp.map cimport map, pair
from libcpp cimport bool as bool_t
from libcpp.vector cimport vector
from libc.stdint cimport uint32_t, uint64_t, int32_t, int16_t, uint8_t, int8_t
from libc.stdlib cimport malloc, free
from mylibc cimport string
from mylibc cimport PyEval_InitThreads, Py_Initialize
from group cimport InstanceAssociation
from node cimport NodeData_t
from driver cimport DriverData_t, DriverData
from group cimport InstanceAssociation_t, InstanceAssociation
from driver cimport ControllerState, ControllerError
from notification cimport const_notification
from values cimport ValueID
from options cimport Options, Create as CreateOptions
from manager cimport Manager, Create as CreateManager, Get as GetManager
from manager cimport struct_associations, int_associations

from notification cimport Notification
from notification cimport (
    Type_ValueAdded,
    Type_ValueRemoved,
    Type_ValueChanged,
    Type_ValueRefreshed,
    Type_Group,
    Type_NodeEvent,
    Type_SceneEvent,
    Type_CreateButton,
    Type_DeleteButton,
    Type_ButtonOn,
    Type_ButtonOff,
    Type_DriverReset,
    Type_Notification,
    Type_DriverRemoved,
    Type_ControllerCommand,
    Type_UserAlerts,
)

# noinspection PyPackageRequirements
import six

import logging
import os
import sys
from shutil import copyfile
from pkg_resources import get_distribution, DistributionNotFound

try:
    import __builtin__
except ImportError:
    import builtins as __builtin__

logger = logging.getLogger('libopenzwave')

PY3 = sys.version_info[0] >= 3

cdef extern from 'pyversion.h':
    string PY_LIB_VERSION_STRING
    string PY_LIB_FLAVOR_STRING
    string PY_LIB_BACKEND_STRING
    string PY_LIB_DATE_STRING
    string PY_LIB_TIME_STRING

__version__ = PY_LIB_VERSION_STRING

#For historical ways of working
libopenzwave_location = 'not_installed'
libopenzwave_file = 'not_installed'

try:
    _dist = get_distribution('libopenzwave')
except DistributionNotFound:
    pass
else:
    libopenzwave_location = _dist.location

if libopenzwave_location == 'not_installed' :
   try:
        _dist = get_distribution('libopenzwave')
        libopenzwave_file = _dist.__file__
   except AttributeError:
        libopenzwave_file = 'not_installed'
   except DistributionNotFound:
        libopenzwave_file = 'not_installed'


# noinspection PyMissingOrEmptyDocstring

cdef string _str_to_cstr(s):
    return string(s)

def _str(s):
    if not isinstance(s, str):
        return s.decode('utf-8')

    return s

def _cstr(s):
    """
    Convert String
    """
    try:
        s = s.encode('utf-8')
    except:
        pass

    return _str_to_cstr(s)


class LibZWaveException(Exception):
    """
    Exception class for LibOpenZWave
    """
    def __init__(self, value):
        """
        :param value:
        """
        Exception.__init__(self)
        self.msg = "LibOpenZwave Generic Exception"
        self.value = value

    def __str__(self):
        return repr(self.msg+' : '+self.value)


PYLIBRARY = __version__
PY_OZWAVE_CONFIG_DIRECTORY = "config"
OZWAVE_CONFIG_DIRECTORY = "share/openzwave/config"
CWD_CONFIG_DIRECTORY = "openzwave/config"

# noinspection PyPep8Naming
class StatItem(object):
    doc = ''

class _bool(int):
    """
    This class is a workaround for a bug found in python by @cgarwood.
    Every data type class in python can be subclassed except for bool. I am not
    sure of the reason why but because we want to add a tooltip/doc attribute
    that is accessable by the user we ned to be able to subclass the data type.

    This class gets used as a parent class to a dynamically created class
    along with StatItem
    """

    _value = 0

    def __and__(self, y):
        return self._value & y

    @classmethod
    def __new__(cls, *args, **kwargs):
        value = args[1]
        args = list(args)
        if value:
            value = 1
        else:
            value = 0

        args[1] = value

        self = super(_bool, cls).__new__(cls, *args, **kwargs)
        setattr(self, '_value', value)
        return self

    def __or__(self, y):
        return self._value | y

    def __rand__(self, y):
        return y & self._value

    def __repr__(self):
        if self._value:
            return 'True'
        return 'False'

    def __ror__(self, y):
        return y | self._value

    def __rxor__(self, y):
        """ x.__rxor__(y) <==> y^x """
        return y ^ self._value

    def __str__(self):
        return 'True' if self._value else 'False'

    def __xor__(self, y):
        return self._value ^ y


# noinspection PyPep8Naming
class EnumItem(str):
    """
    Represents an actual enumeration entry.

    This is a wrapper around the `str` class. We want the entry to be a
    string and carry with it all of the usual string related functions. We
    wanted to be able to provide information related to an entry. like the
    data type the entry represents and also a description of the entry.

    the added bits of information can be accessed by using one of the
    attribute names below

    * index: The entry number of the item. An enumeration is a grouping of
      variables that have a number associated with them. In C++ this number is
      automatically assigned as the entry before it + 1 if a number is not
      assigned. In Python we do not have the ability to do this.

      We do want to have access to that number and the index attribute of the
      entry is how we can identify it. This is mainly used for backwards
      compatibility

    * doc: A description of what the entry is
    * type: The data type the entry represents.
    """

    doc = ''
    idx = -1
    type = None
    _value = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """
        self = super(EnumItem, cls).__new__(*args, **kwargs)
        return self

    def __int__(self):
        return self.index

    def __call__(self, cls, value):
        """
        :param cls:
        :param value:
        """
        try:
            cls = type(
                'StatItem',
                (StatItem, cls),
                {'doc': self.doc}
            )
        except TypeError:
            cls = type(
                'StatItem',
                (StatItem, _bool),
                {'doc': self.doc}
            )

            value = _bool(int(value))

        item = cls(value)
        return item

    # noinspection PyMissingOrEmptyDocstring
    def set(self, idx, doc, type_=None, value=None):
        """
        :param idx:
        :type idx: int

        :param doc:
        :type doc: str

        :param type_:
        :type type_: int, optional

        :param value:
        :type value: str, optional

        :rtype: "EnumItem"
        """
        self.doc = doc
        self.idx = idx
        self.type = type_
        self._value = value
        return self

    @property
    def value(self):
        """
        :rtype: int, str
        """
        if self._value is None:
            return self.idx

        return self._value


class Enum(dict):
    """
    This is the Enumeration helper class.

    It works the same as a python dictionary and a python list combined. We
    combined those 2 classes because in previous versions of libopenzwave
    there were 2 different types of enumerations created. We wanted to remove
    the need to know which enumerations were a dic and which were list. So we
    combined the 2 classes together to create this helper class.


    To access an entry using a dict key

    .. code-block:: python

        entry = enum['entry']

    To access an enum entry using a list index

    .. code-block:: python

        entry = enum[0]

    To get the index number of an enumeration entry (this can be done 2 ways)

    .. code-block:: python

        entry_index = enum['entry'].index
        entry_index = enum.index('entry')

    We also added the ability to directly get an entry by attribute name

    .. code-block:: python

        entry = enum.Entry

    """

    def __init__(self, **kwargs):
        """
        :param **kwargs:
        """
        super(Enum, self).__init__()
        for key, value in kwargs.items():
            self[key] = EnumItem(key.rstrip('_')).set(*value)

    def __getitem__(self, item):
        """
        :param item:
        :type item: int, str
        """
        if isinstance(item, int):
            for value in self.values():
                if value.idx == item:
                    return value
            raise IndexError(item)

        if item in self:
            return dict.__getitem__(self, item)

        if item + '_' in self:
            return dict.__getitem__(self, item + '_')

    def index(self, key):
        """
        :param key:
        :type key: str
        """
        if key not in self:
            raise ValueError(key)

        return self[key].idx

    def __iter__(self):
        return iter(self.values())

    def __getattr__(self, item):
        """
        :param item:
        :type item: str
        """
        if item in self.__dict__:
            return self.__dict__[item]

        if item in self:
            return self[item]

        raise AttributeError(item)

class NotificationItem(EnumItem):
    _handler = None

    def __eq__(self, other):
        """
        :param other:
        :type other: int, str

        :rtype: bool
        """
        if isinstance(other, int):
            return other == self.idx

        return str.__eq__(self, other)

    def __ne__(self, other):
        """
        :param other:
        :type other: int, str

        :rtype: bool
        """
        if isinstance(other, int):
            return other != self.idx

        return str.__ne__(self, other)

    def __int__(self):
        """
        :rtype: int
        """
        return self.idx

    def __hash__(self):
        """
        :rtype: hash
        """
        return hash(str(self))


class NotificationEnum(Enum):

    def __init__(self, **kwargs):
        """
        :param **kwargs:
        """

        super(NotificationEnum, self).__init__(**kwargs)

        for key, value in kwargs.items():
            self[key] = NotificationItem(key.rstrip('_')).set(*value)


PyNotifications = NotificationEnum(
    ValueAdded=(0, (
        "A new node value has been added to OpenZWave's set. "
        "These notifications occur after a node has been discovered, "
        "and details of its command classes have been received. "
        "Each command class may generate one or more values depending on the "
        "complexity of the item being represented."
    )),
    ValueRemoved=(1, (
        "A node value has been removed from OpenZWave's set. "
        "This only occurs when a node is removed."
    )),
    ValueChanged=(2, (
        "A node value has been updated from the Z-Wave network "
        "and it is different from the previous value."
    )),
    ValueRefreshed=(3, (
        "A node value has been updated from the Z-Wave network."
    )),
    Group=(4, (
        "The associations for the node have changed. "
        "The application should rebuild any group "
        "information it holds about the node."
    )),
    NodeNew=(5, (
        "A new node has been found (not already stored in zwcfg*.xml file)."
    )),
    NodeAdded=(6, (
        "A new node has been added to OpenZWave's set. This may be due to a "
        "device being added to the Z-Wave network, or because the application "
        "is initializing itself."
    )),
    NodeRemoved=(7, (
        "A node has been removed from OpenZWave's set. This may be due to a "
        "device being removed from the Z-Wave network, or because the "
        "application is closing."
    )),
    NodeProtocolInfo=(8, (
        "Basic node information has been received, such as whether the node "
        "is a listening device, a routing device and its baud rate and basic, "
        "generic and specific types. It is after this notification that you "
        "can call Manager::GetNodeType to obtain a label containing the "
        "device description."
    )),
    NodeNaming=(9, (
        "One of the node names has changed (name, manufacturer, product)."
    )),
    NodeEvent=(10, (
        "A node has triggered an event. This is commonly caused "
        "when a node sends a Basic_Set command to the controller. "
        "The event value is stored in the notification."
    )),
    PollingDisabled=(11, (
        "Polling of a node has been successfully "
        "turned off by a call to Manager::DisablePoll."
    )),
    PollingEnabled=(12, (
        "Polling of a node has been successfully "
        "turned on by a call to Manager::EnablePoll."
    )),
    SceneEvent=(13, "Scene Activation Set received."),
    CreateButton=(14, "Handheld controller button event created."),
    DeleteButton=(15, "Handheld controller button event deleted."),
    ButtonOn=(16, "Handheld controller button on pressed event."),
    ButtonOff=(17, "Handheld controller button off pressed event."),
    DriverReady=(18, (
        "A driver for a PC Z-Wave controller has been added and is "
        "ready to use. The notification will contain the controller's "
        "Home ID, which is needed to call most of the Manager methods."
    )),
    DriverFailed=(19, "Driver failed to load."),
    DriverReset=(20, (
        "All nodes and values for this driver have been removed. "
        "This is sent instead of potentially hundreds of individual "
        "node and value notifications."
    )),
    EssentialNodeQueriesComplete=(21, (
        "The queries on a node that are essential to its operation "
        "have been completed. The node can now handle incoming messages."
    )),
    NodeQueriesComplete=(22, (
        "All the initialisation queries on a node have been completed."
    )),
    AwakeNodesQueried=(23, (
        "All awake nodes have been queried, so client application "
        "can expected complete data for these nodes."
    )),
    AllNodesQueriedSomeDead=(24, (
        "All nodes have been queried but some dead nodes found."
    )),
    AllNodesQueried=(25, (
        "All nodes have been queried, so client "
        "application can expected complete data."
    )),
    Notification=(26, "A manager notification report."),
    DriverRemoved=(27, "The Driver is being removed."),
    ControllerCommand=(28, (
        "When Controller Commands are executed, Notifications of "
        "Success/Failure etc are communicated via this Notification."
    )),
    NodeReset=(29, (
        "A node has been reset from OpenZWave's set. The Device has "
        "been reset and thus removed from the NodeList in OZW."
    )),
    UserAlerts=(30, (
        "Warnings and Notifications Generated by the library that "
        "should be displayed to the user (eg, out of date config files)"
    )),
    ManufacturerSpecificDBReady=(31, (
        "The ManufacturerSpecific Database Is Ready"
    ))
)

PyUserAlerts = NotificationEnum(
    None_=(0, "No alert currently present."),
    ConfigOutOfDate=(1, (
        "A config file is out of date"
    )),
    MFSOutOfDate=(2, "A manufacturer_specific.xml file is out of date."),
    ConfigFileDownloadFailed=(3, "A config file failed to download."),
    DNSError=(4, "An error occurred performing a DNS Lookup."),
    NodeReloadRequired=(5, (
        "A new config file has been discovered for this node, a node "
        "reload is required to have the new configuration take affect."
    )),
    UnsupportedController=(6, (
        "The controller is not running a firmware "
        "library that is supported by OpenZWave."
    )),
    ApplicationStatus_Retry=(7, (
        "The Application Status Command Class "
        "returned the message \"Retry Later\"."
    )),
    ApplicationStatus_Queued=(8, (
        "The command has been queued for later execution."
    )),
    ApplicationStatus_Rejected=(9, "The command was rejected."),
)


PyNotificationCodes = NotificationEnum(
    MsgComplete=(0, "Completed messages."),
    Timeout=(1, (
        "Messages that timeout will send a Notification with this code."
    )),
    NoOperation=(2, "Report on NoOperation message sent completion."),
    Awake=(3, "Report when a sleeping node wakes."),
    Sleep=(4, "Report when a node goes to sleep."),
    Dead=(5, "Report when a node is presumed dead."),
    Alive=(6, "Report when a node is revived."),
)

PyGenres = Enum(
    Basic=(0, (
        "The 'level' as controlled by basic commands. "
        "Usually duplicated by another command class."
    )),
    User=(1, "Basic values an ordinary user would be interested in."),
    Config=(2, (
        "Device-specific configuration parameters. These "
        "cannot be automatically discovered via Z-Wave, "
        "and are usually described in the user manual instead."
    )),
    System=(3, (
        "Values of significance only to users "
        "who understand the Z-Wave protocol"
    )),
)

PyValueTypes = Enum(
    Bool=(0, "Boolean, true or false"),
    Byte=(1, "8-bit unsigned value"),
    Decimal=(2, (
        "Represents a non-integer value as a string, "
        "to avoid floating point accuracy issues."
    )),
    Int=(3, "32-bit signed value"),
    List=(4, "List from which one item can be selected"),
    Schedule=(5, (
        "Complex type used with the Climate Control Schedule command class"
    )),
    Short=(6, "16-bit signed value"),
    String=(7, "Text string"),
    Button=(8, (
        "A write-only value that is the equivalent of "
        "pressing a button to send a command to a device"
    )),
    Raw=(9, "Raw byte values"),
    BitSet=(10, "Group of boolean values"),
)

PyControllerState = Enum(
    Normal=(0, "No command in progress."),
    Starting=(1, "The command is starting."),
    Cancel=(2, "The command was cancelled."),
    Error=(3, "Command invocation had error(s) and was aborted."),
    Waiting=(4, "Controller is waiting for a user action."),
    Sleeping=(5, "Controller command is on a sleep queue wait for device."),
    InProgress=(6, (
        "The controller is communicating with "
        "the other device to carry out the command."
    )),
    Completed=(7, "The command has completed successfully."),
    Failed=(8, "The command has failed."),
    NodeOK=(9, (
        "Used only with ControllerCommand_HasNodeFailed to "
        "indicate that the controller thinks the node is OK."
    )),
    NodeFailed=(10, (
        "Used only with ControllerCommand_HasNodeFailed to "
        "indicate that the controller thinks the node has failed."
    )),
)

PyControllerCommand = Enum(
    None_=(0, "No command."),
    AddDevice=(1, (
        "Add a new device (but not a controller) to the Z-Wave network."
    )),
    CreateNewPrimary=(2, (
        "Add a new controller to the Z-Wave network. The "
        "new controller will be the primary, and the current "
        "primary will become a secondary controller."
    )),
    ReceiveConfiguration=(3, (
        "Receive Z-Wave network configuration "
        "information from another controller."
    )),
    RemoveDevice=(4, (
        "Remove a device (but not a controller) from the Z-Wave network."
    )),
    RemoveFailedNode=(5, (
        "Move a node to the controller's failed nodes list. "
        "This command will only work if the node cannot respond."
    )),
    HasNodeFailed=(6, (
        "Check whether a node is in the controller's failed nodes list."
    )),
    ReplaceFailedNode=(7, (
        "Replace a non-responding node with another. The node must be in "
        "the controller's list of failed nodes for this command to succeed."
    )),
    TransferPrimaryRole=(8, "Make a different controller the primary."),
    RequestNetworkUpdate=(9, "Request network information from the SUC/SIS."),
    RequestNodeNeighborUpdate=(10, (
        "Get a node to rebuild its neighbour list. This "
        "method also does ControllerCommand_RequestNodeNeighbors."
    )),
    AssignReturnRoute=(11, "Assign a network return routes to a device."),
    DeleteAllReturnRoutes=(12, "Delete all return routes from a device."),
    SendNodeInformation=(13, "Send a node information frame."),
    ReplicationSend=(14, "Send information from primary to secondary."),
    CreateButton=(15, "Create an id that tracks handheld button presses."),
    DeleteButton=(16, "Delete id that tracks handheld button presses."),
)

PyControllerError = Enum(
    None_=(0, "No Error."),
    ButtonNotFound=(1, "Button not found."),
    NodeNotFound=(2, "Node not found."),
    NotBridge=(3, "Controller is not a bridge controller"),
    NotSUC=(4, "Controller is not static update controller."),
    NotSecondary=(5, "Controller is not secondary controller."),
    NotPrimary=(6, "Controller is not primary controller."),
    IsPrimary=(7, "Controller is not secondary controller."),
    NotFound=(8, "Node not found."),
    Busy=(9, "Node busy."),
    Failed=(10, "Command failed."),
    Disabled=(11, "Node disabled."),
    Overflow=(12, "Overflow error."),
)

PyControllerInterface = Enum(
    Unknown=(0, "Controller interface use unknown protocol."),
    Serial=(1, "Controller interface use serial protocol."),
    Hid=(2, "Controller interface use human interface device protocol."),
)

PyOptionType = Enum(
    Invalid=(0, "Invalid type."),
    Bool=(1, "Boolean."),
    Int=(2, "Integer."),
    String=(3, "String."),
)

PyOptionList = Enum(
    SaveLogLevel=(
        0,
        'Save (to file) log messages equal to or above LogLevel_Detail.',
        'Int'
    ),
    AppendLogFile=(
        1,
        'Append new session logs to existing log file (false = overwrite).',
        'Bool'
    ),
    LogFileName=(
        2,
        'Name of the log file (can be changed via Log::SetLogFileName).',
        'String',
    ),
    EnableSIS=(
        3,
        'Automatically become a SUC if there is no SUC on the network.',
        'Bool'
    ),
    DumpTriggerLevel=(
        4,
        'Default is to never dump RAM-stored log messages.',
        'Int'
    ),
    Logging=(
        5,
        'Enable logging of library activity.',
        'Bool'
    ),
    Include=(
        6,
        (
            'Only handle the specified command classes. The '
            'Exclude option is ignored if anything is listed here.'
        ),
        'String',
    ),
    IntervalBetweenPoll=(
        7,
        (
            'If false, try to execute the entire poll list within the '
            'PollInterval time frame. If true, wait for PollInterval '
            'milliseconds between polls.'
        ),
        'Bool'
    ),
    Associate=(
        8,
        (
            'Enable automatic association of the '
            'controller with group one of every device.'
        ),
        'Bool'
    ),
    ConfigPath=(
        9,
        'Path to the OpenZWave config folder.',
        'String'
    ),
    NetworkKey=(
        10,
        (
            'Key used to negotiate and communicate with '
            'devices that support Security Command Class'
        ),
        'String',
    ),
    Interface=(
        11,
        (
            'Identify the serial port to be accessed (TODO: change the '
            'code so more than one serial port can be specified and HID).'
        ),
        'String'
    ),
    SaveConfiguration=(
        12,
        'Save the XML configuration upon driver close.',
        'Bool'
    ),
    DriverMaxAttempts=(
        13,
        '.',
        'Int'
    ),
    PollInterval=(
        14,
        (
            '30 seconds (can easily poll 30 values in this time; '
            '~120 values is the effective limit for 30 seconds).'
        ),
        'Int'
    ),
    UserPath=(
        15,
        'Path to the user\'s data folder.',
        'String'
    ),
    AssumeAwake=(
        16,
        (
            'Assume Devices that Support the Wakeup CC '
            'are awake when we first query them ...'
        ),
        'Bool'
    ),
    PerformReturnRoutes=(
        17,
        'If true, return routes will be updated.',
        'Bool'
    ),
    QueueLogLevel=(
        18,
        'Save (in RAM) log messages equal to or above LogLevel_Debug.',
        'Int'
    ),
    SuppressValueRefresh=(
        19,
        (
            'If true, notifications for refreshed '
            '(but unchanged) values will not be sent.'
        ),
        'Bool',
    ),
    SecurityStrategy=(
        20,
        (
            'Should we encrypt CC\'s that are available '
            'via both clear text and Security CC?.'
        ),
        'String'
        'SUPPORTED',
    ),
    RefreshAllUserCodes=(
        21,
        (
            'If true, during startup, we refresh all the UserCodes the '
            'device reports it supports. If False, we stop after we get '
            'the first "Available" slot (Some devices have 250+ usercode '
            'slots! - That makes our Session Stage Very Long ).'
        ),
        'Bool'
    ),
    CustomSecuredCC=(
        22,
        (
            'What List of Custom CC should we always '
            'encrypt if SecurityStrategy is CUSTOM.'
        ),
        'String'
        '0x62,0x4c,0x63',
    ),
    EnforceSecureReception=(
        23,
        (
            'If we recieve a clear text message for a '
            'CC that is Secured, should we drop the message'
        ),
        'Bool'
    ),
    NotifyOnDriverUnload=(
        24,
        (
            'Should we send the Node/Value Notifications on Driver '
            'Unloading - Read comments in Driver::~Driver() method '
            'about possible race conditions.'
        ),
        'Bool'
    ),
    NotifyTransactions=(
        25,
        'Notifications when transaction complete is reported.',
        'Bool'
    ),
    Exclude=(
        26,
        'Remove support for the listed command classes.',
        'String'
    ),
    RetryTimeout=(
        27,
        'How long do we wait to timeout messages sent.',
        'Int'
    ),
    ConsoleOutput=(
        28,
        'Display log information on console (as well as save to disk).',
        'Bool'
    ),
    ReloadAfterUpdate=(
        29,
        (
            'Changes the node reloading after '
            'downloading a new device config file'
        ),
        'String'
    ),
    IncludeInstanceLabel=(
        30,
        (
            'Should we include the Instance Label in '
            'Value Labels on MultiInstance Devices'
        ),
        'Bool'
    )
)

PyStatDriver = Enum(
    SOFCnt=(0, "Number of SOF bytes received"),
    ACKWaiting=(1, "Number of unsolicited messages while waiting for an ACK"),
    readAborts=(2, "Number of times read were aborted due to timeouts"),
    badChecksum=(3, "Number of bad checksums"),
    readCnt=(4, "Number of messages successfully read"),
    writeCnt=(5, "Number of messages successfully sent"),
    CANCnt=(6, "Number of CAN bytes received"),
    NAKCnt=(7, "Number of NAK bytes received"),
    ACKCnt=(8, "Number of ACK bytes received"),
    OOFCnt=(9, "Number of bytes out of framing"),
    dropped=(10, "Number of messages dropped & not delivered"),
    retries=(11, "Number of messages retransmitted"),
    callbacks=(12, "Number of unexpected callbacks"),
    badroutes=(13, "Number of failed messages due to bad route response"),
    noack=(14, "Number of no ACK returned errors"),
    netbusy=(15, "Number of network busy/failure messages"),
    nondelivery=(16, "Number of messages not delivered to network"),
    routedbusy=(17, "Number of messages received with routed busy status"),
    broadcastReadCnt=(18, "Number of broadcasts read"),
    broadcastWriteCnt=(19, "Number of broadcasts sent"),
)

PyStatNode = Enum(
    sentCnt=(0, "Number of messages sent from this node"),
    sentFailed=(1, "Number of sent messages failed"),
    retries=(2, "Number of message retries"),
    receivedCnt=(3, "Number of messages received from this node"),
    receivedDups=(4, "Number of duplicated messages received"),
    receivedUnsolicited=(5, "Number of messages received unsolicited"),
    lastRequestRTT=(6, "Last message request RTT"),
    lastResponseRTT=(7, "Last message response RTT"),
    sentTS=(8, "Last message sent time"),
    receivedTS=(9, "Last message received time"),
    averageRequestRTT=(10, "Average Request round trip time"),
    averageResponseRTT=(11, "Average Response round trip time"),
    quality=(12, "Node quality measure"),
    lastReceivedMessage=(13, "Place to hold last received message"),
    ccData=(14, "Command Class Data"),
    txStatusReportSupported = (15, "if Extended Status Reports are available"),
    txTime=(16, "Time Taken to Transmit the last frame"),
    hops=(17, "Hops taken in transmitting last frame"),
    rssi_1=(18, "RSSI Level of last transmission"),
    rssi_2=(19, "RSSI Level of last transmission"),
    rssi_3=(20, "RSSI Level of last transmission"),
    rssi_4=(21, "RSSI Level of last transmission"),
    rssi_5=(22, "RSSI Level of last transmission"),
    ackChannel=(23, "Channel we received the last ACK on"),
    lastTxChannel=(24, "Channel we transmitted the last frame on"),
    routeScheme=(25, "The Scheme used to route the last frame"),
    routeUsed=(26, "The Route Taken in the last frame"),
    routeSpeed=(27, "Baud Rate of the last frame"),
    routeTries=(28, "The number of attempts to route the last frame"),
    lastFailedLinkFrom=(29, "The last failed link from"),
    lastFailedLinkTo=(30, "The last failed link to")
)

PyCommandClassData = Enum(
    commandClassId=(0, "Num type of CommandClass id."),
    sentCnt=(1, "Number of messages sent from this CommandClass."),
    receivedCnt=(2, "Number of messages received from this CommandClass")
)


PyLogLevels = Enum(
    Invalid=(0, 'Invalid Log Status'),
    None_=(1, 'Disable all logging'),
    Always=(2, 'These messages should always be shown'),
    Fatal=(3, 'A likely fatal issue in the library'),
    Error=(4, 'A serious issue with the library or the network'),
    Warning=(5, (
        'A minor issue from which the library should be able to recover'
    )),
    Alert=(6, (
        'Something unexpected by the library about which '
        'the controlling application should be aware'
    )),
    Info=(7, (
        "Everything's working fine...these messages "
        "provide streamlined feedback on each message"
    )),
    Detail=(8, 'Detailed information on the progress of each message'),
    Debug=(9, (
        'Very detailed information on progress that will create a huge '
        'log file quickly but this level (as others) can be queued and '
        'sent to the log only on an error or warning'
    )),
    StreamDetail=(10, (
        'Will include low-level byte transfers from '
        'controller to buffer to application and back'
    )),
    Internal=(11, (
        'Used only within the log class (uses existing timestamp, etc',
    )),
)


# noinspection PyUnresolvedReferences
cdef map[uint64_t, ValueID] _values_map


# noinspection PyMissingOrEmptyDocstring,PyPep8Naming,PyUnresolvedReferences
cdef _getValueFromType(Manager *manager, valueId, pos=None):
    """
    Translate a value in the right type
    """
    cdef float type_float
    cdef bool_t type_bool
    cdef uint8_t type_byte
    cdef int32_t type_int
    cdef int16_t type_short
    cdef string type_string
    cdef uint8_t* vectraw = NULL
    cdef uint8_t size
    cdef string s

    c = ""
    ret = None
    if _values_map.find(valueId) != _values_map.end():
        datatype = PyValueTypes[_values_map.at(valueId).GetType()]
        logger.debug('value id: {0}, value type {1}'.format(valueId, datatype))
        if datatype == "Bool":
            cret = manager.GetValueAsBool(
                _values_map.at(valueId),
                &type_bool
            )
            ret = type_bool if cret else None
            return ret
        elif datatype == "Byte":
            cret = manager.GetValueAsByte(
                _values_map.at(valueId),
                &type_byte
            )
            ret = type_byte if cret else None
            return ret
        elif datatype == "Raw":
            cret = manager.GetValueAsRaw(
                _values_map.at(valueId),
                &vectraw,
                &size
            )
            if cret:
                for x in range (0, size):
                    c += chr(vectraw[x])
            ret = c if cret else None
            free(vectraw)
            return ret
        elif datatype == "Decimal":
            cret = manager.GetValueAsFloat(
                _values_map.at(valueId),
                &type_float
            )
            ret = type_float if cret else None
            return ret
        elif datatype == "Int":
            cret = manager.GetValueAsInt(
                _values_map.at(valueId),
                &type_int
            )
            ret = type_int if cret else None
            return ret
        elif datatype == "Short":
            cret = manager.GetValueAsShort(
                _values_map.at(valueId),
                &type_short
            )
            ret = type_short if cret else None
            return ret
        elif datatype == "String":
            cret = manager.GetValueAsString(
                _values_map.at(valueId),
                &type_string
            )
            ret = _str(type_string.c_str()) if cret else None
            return ret
        elif datatype == "Button":
            cret = manager.GetValueAsBool(
                _values_map.at(valueId),
                &type_bool
            )
            ret = type_bool if cret else None
            return ret
        elif datatype == "List":
            cret = manager.GetValueListSelection(
                _values_map.at(valueId),
                &type_string
            )
            ret = _str(type_string.c_str()) if cret else None
            return ret
        elif datatype == "BitSet":
            if pos is not None:
                type_byte = pos
                cret = manager.GetValueAsBitSet(
                    _values_map.at(valueId),
                    type_byte, &type_bool
                )
                ret = type_bool if cret else None
                return ret
            else:
                cret = manager.GetValueAsByte(
                    _values_map.at(valueId),
                    &type_byte
                )
                ret = type_byte if cret else None
                value_str = "{0:b}".format(ret)
                bit_set = list(__builtin__.bool(int(item)) for item in list(value_str))
                bit_set = list(bit_set[i] for i in range(len(value_str) - 1, -1, -1))
                return bit_set
        else :
            cret = manager.GetValueAsString(
                _values_map.at(valueId),
                &type_string
            )
            ret = type_string.c_str() if cret else None
    logger.debug("getValueFromType return %s", ret)
    return ret

# noinspection PyMissingOrEmptyDocstring,PyPep8Naming,PyUnresolvedReferences
cdef _delValueId(ValueID v, n):
    logger.debug("delValueId : ValueID : %s", v.GetId())
    if _values_map.find(v.GetId()) != _values_map.end():
        _values_map.erase(_values_map.find(v.GetId()))


# noinspection PyMissingOrEmptyDocstring,PyPep8Naming,PyUnresolvedReferences
cdef _addValueId(ValueID v, n, add_data=True):
    #check is a valid value
    if v.GetInstance() == 0:
        return

    cdef Manager *manager = GetManager()

    if _values_map.find(v.GetId()) == _values_map.end():
        item = new pair[uint64_t, ValueID](v.GetId(), v)
        _values_map.insert(deref(item))
        del item

    n.command_class = v.GetCommandClassId()
    n.instance = v.GetInstance()
    n.index = v.GetIndex()
    n.genre = PyGenres[v.GetGenre()]
    n.is_read_only = manager.IsValueReadOnly(v)
    n.label = _str(manager.GetValueLabel(v).c_str())
    n.units = _str(manager.GetValueUnits(v).c_str())
    n.type = PyValueTypes[v.GetType()]

    logger.debug("Value -- node_id: {0} : {1}".format(v.GetNodeId(), str(n)[1:-1]))

    if add_data:
        n.data = _getValueFromType(manager, v.GetId())

class Value(object):
    id = 0
    command_class = 0
    instance = 0
    index = 0
    genre = None
    type = None
    data = None
    label = ''
    units = ''
    is_read_only = False

    def __init__(self, id):
        """
        :param id:
        :type id: int
        """
        self.id = id
        self.command_class = None
        self.instance = None
        self.index = None
        self.genre = None
        self.type = None
        self.data = None
        self.label = None
        self.units = None
        self.is_read_only = None

    def __str__(self):
        if self.command_class is None:
            command_class = 0
            s_command_class = None
        else:
            command_class = self.command_class
            s_command_class = PyManager.COMMAND_CLASS_DESC[self.command_class]


        return (
            "[id={0};command_class={1:02X} ({10});instance={2!r};"
            "index={3!r};genre={4!r};type={5!r};data={6!r};label={7!r};"
            "units={8!r};is_read_only={9!r}"
            "]"
        ).format(
            self.id, command_class, self.instance, self.index,
            self.genre, self.type, self.data, self.label, self.units,
            self.is_read_only,s_command_class
        )


class ZWaveNotification(object):
    type = 0
    home_id = 0
    node_id = 0
    value = 0
    group_id = 0
    event = 0
    notification_code = 0
    controller_state = 0
    controller_error = 0
    controller_command = 0
    button_id = 0
    scene_id = 0
    user_alert = 0

    Value = Value

    def __init__(self, notification_type, home_id, node_id):
        """
        :param notification_type:

        :param home_id:

        :param node_id:
        """
        self.type = notification_type
        self.home_id = home_id
        self.node_id = node_id
        self.value = None
        self.group_id = None
        self.event = None
        self.notification_code = None
        self.controller_state = None
        self.controller_error = None
        self.controller_command = None
        self.button_id = None
        self.scene_id = None
        self.user_alert = None

    def __str__(self):
        return (
            "type={0};home_id={1};node_id={2};group_id={3};event={4};"
            "notification_code={5};controller_state={6};controller_error={7};"
            "controller_command={8};button_id={9};scene_id={10};"
            "user_alert={11};value={12}"
        ).format(
            self.type, self.home_id, self.node_id, self.group_id, self.event,
            self.notification_code, self.controller_state,
            self.controller_error, self.controller_command, self.button_id,
            self.scene_id, self.user_alert, str(self.value)
        )

    def __eq__(self, other):
        """
        :param other:

        :rtype: bool
        """
        return other == self.type

    def __ne__(self, other):
        """
        :param other:

        :rtype: bool
        """
        return not self.__eq__(other)

    def __repr__(self):
        return object.__repr__(self) + str(self)


# noinspection PyPep8Naming,PyUnresolvedReferences
cdef void _notif_callback(
    const_notification _notification,
    void* _context
) with gil:
    """
    Notification callback to the C++ library
    """
    logger.debug("notif_callback : new notification")
    cdef Notification* notification = <Notification*>_notification

    notif_type = PyNotifications[notification.GetType()]
    node_id = notification.GetNodeId()
    home_id = notification.GetHomeId()

    logger.debug(
        "notif_callback : notification_type: %s, home_id: %s, node_id: %s",
        notif_type,
        home_id,
        node_id
    )

    n = ZWaveNotification(notif_type, home_id, node_id)

    try:
        if notif_type.idx == Type_Group:
            n.group_id = notification.GetGroupIdx()
        elif notif_type.idx == Type_NodeEvent:
            n.event = notification.GetEvent()
        elif notif_type.idx == Type_Notification:
            n.notification_code = notification.GetNotification()
        elif notif_type.idx == Type_ControllerCommand:
            n.controller_state=(
                PyControllerState[notification.GetEvent()]
            )
            n.controller_error=(
                PyControllerError[notification.GetNotification()]
            )
            n.controller_command=(
                PyControllerCommand[notification.GetCommand()]
            )
        elif notif_type.idx in (
            Type_CreateButton,
            Type_DeleteButton,
            Type_ButtonOn,
            Type_ButtonOff
        ):
            n.button_id = notification.GetButtonId()
        elif notif_type.idx == Type_DriverRemoved:
            logger.debug(
                "Notification : Type_DriverRemoved received : "
                "clean all value ids"
            )
            _values_map.empty()
        elif notif_type.idx == Type_DriverReset:
            logger.debug(
                "Notification : Type_DriverReset received : "
                "clean all value ids"
            )
            _values_map.empty()
        elif notif_type.idx == Type_SceneEvent:
            n.scene_id = notification.GetSceneId()
        elif notif_type.idx in (
            Type_ValueAdded,
            Type_ValueChanged,
            Type_ValueRefreshed
        ):
            n.value = n.Value(notification.GetValueID().GetId())

            if notif_type.idx == Type_ValueAdded:
                _addValueId(notification.GetValueID(), n.value, False)
            else:
                _addValueId(notification.GetValueID(), n.value)

        elif notif_type.idx == Type_ValueRemoved:
            n.value = n.Value(notification.GetValueID().GetId())
        elif notif_type.idx == Type_UserAlerts:
            n.user_alert = PyUserAlerts[notification.GetUserAlertType()]
    except:
        err = traceback.format_exc()
        logger.error(
            "notif_callback exception Type_{0}, Node: {1}\n{2}".format(
                notif_type,
                node_id,
                err
            )
        )
        return

    # elif (
    #     notification.GetType() in (Type_PollingEnabled, Type_PollingDisabled)
    # ):
    #     # Maybe we should enable/disable this
    #     _addValueId(notification.GetValueID(), n)
    logger.debug("notif_callback : call callback context")
    try:
        (<object>_context)(n)
    except:
        err = traceback.format_exc()
        logger.error(
            "notif_callback exception callback context\n"
            "Type_{0}, Node: {1}\n{2}".format(notif_type, node_id, err)
        )

    if notification.GetType() == Type_ValueRemoved:
        try:
            _delValueId(notification.GetValueID(), n)
        except:
            err = traceback.format_exc()
            logger.error(
                "notif_callback exception Type_ValueRemoved delete, "
                "Node: {0}\n{1}".format(node_id, err)

            )

    logger.debug("notif_callback : end")


# noinspection PyMissingOrEmptyDocstring,PyPep8Naming
# cpdef object driverData():
#     cdef DriverData data


# noinspection PyPep8Naming
def _configPath():
    """
    Retrieve the config path. This directory hold the xml files.

    :return: A string containing the library config path or None.
    :rtype: str, None
    """
    if os.path.isfile(os.path.join("/etc/openzwave/",'device_classes.xml')):
        #At first, check in /etc/openzwave
        return "/etc/openzwave/"
    elif os.path.isfile(
        os.path.join("/usr/local/etc/openzwave/",'device_classes.xml')
    ):
        #Next, check in /usr/local/etc/openzwave
        return "/usr/local/etc/openzwave/"
    else :
        #Check in libopenzwave.resources
        dirn = None

        try:
            from pkg_resources import resource_filename
            dirn = resource_filename(
                'libopenzwave.ozw_config',
                '__init__.py'
            )
            dirn = os.path.dirname(dirn)
        except ImportError:
            resource_filename = None
            dirn = None

        if (
            dirn is not None and
            os.path.isfile(os.path.join(dirn,'device_classes.xml'))
        ):
            #At first, check in /etc/openzwave
            return dirn

        elif os.path.isfile(
            os.path.join("openzwave/config",'device_classes.xml')
        ):
            return os.path.abspath('openzwave/config')
        #For historical reasons.

        config_dirs = (
            os.path.join("/usr", PY_OZWAVE_CONFIG_DIRECTORY),
            os.path.join("/usr/local", PY_OZWAVE_CONFIG_DIRECTORY),
            os.path.join("/usr", OZWAVE_CONFIG_DIRECTORY),
            os.path.join("/usr/local", OZWAVE_CONFIG_DIRECTORY),
            os.path.join(
                os.path.dirname(libopenzwave_file),
                PY_OZWAVE_CONFIG_DIRECTORY
            ),
            os.path.join(os.getcwd() ,CWD_CONFIG_DIRECTORY),
            os.path.join(libopenzwave_location, PY_OZWAVE_CONFIG_DIRECTORY),
            os.path.join(libopenzwave_location, PY_OZWAVE_CONFIG_DIRECTORY)
        )

        for config_dir in config_dirs:
            if os.path.isdir(config_dir):
                return config_dir

    return None


# noinspection PyPep8Naming,PyClassicStyleClass,PyAttributeOutsideInit
cdef class PyOptions:
    """
    Manage options manager
    """

    cdef readonly str _config_path
    cdef readonly str _user_path
    cdef readonly str _cmd_line

    cdef Options *options

    def __init__(self, config_path='', user_path='', cmd_line=''):
        """
        Create an option object and check that parameters are valid.

        :param config_path: The openzwave config directory. If None,
            try to configure automatically.
        :type config_path: str, optional

        :param user_path: The user directory
        :type user_path: str, optional

        :param cmd_line: The "command line" options of the
            openzwave library
        :type cmd_line: str, optional
        """

        if not config_path:
            config_path = self.getConfigPath()

        if config_path is None:
            raise LibZWaveException("Can't autoconfigure path to config")

        if os.path.exists(config_path):
            if not os.path.exists(
                os.path.join(config_path, "zwcfg.xsd")
            ):
                raise LibZWaveException(
                    "Can't retrieve zwcfg.xsd from %s" % config_path
                )

            self._config_path = config_path

        else:
            raise LibZWaveException(
                "Can't find config directory %s" % config_path
            )

        if not user_path:
            user_path = "."

        if os.path.exists(user_path):
            if False not in (
                os.access(user_path, os.W_OK),
                os.access(user_path, os.R_OK)
            ):
                self._user_path = user_path
            else:
                raise LibZWaveException(
                    "Can't write in user directory %s" % user_path
                )

        else:
            raise LibZWaveException("Can't find user directory %s" % user_path)

        self._cmd_line = cmd_line

    def create(self):
        """
        Create an option object used to start the manager
        
        :rtype: bool
        """

        self.options = CreateOptions(
            _cstr(self._config_path),
            _cstr(self._user_path),
            _cstr(self._cmd_line)
        )

        return True

    def destroy(self):
        """
        Deletes the Options and cleans up any associated objects.

        The application is responsible for destroying the Options object,
        but this must not be done until after the Manager object has been
        destroyed.

        :return: The result of the operation.
        :rtype: bool
        """
        return self.options.Destroy()

    def lock(self):
        """
        Lock the options.

        Needed to start the manager

        :return: The result of the operation.
        :rtype: bool
        """

        user_options_path = os.path.join(self._user_path,'options.xml')
        config_options_path = os.path.join(self._config_path,'options.xml')

        if not os.path.isfile(user_options_path):
            if os.path.isfile(config_options_path):
                copyfile(config_options_path, user_options_path)
            else:
                logger.warning(
                    "Can't find options.xml in %s" % self._config_path
                )
        return self.options.Lock()

    def areLocked(self):
        """
        Test whether the options have been locked.

        :return: true if the options have been locked.
        :rtype: bool
        """
        return self.options.AreLocked()

    def addOptionBool(self, name, value):
        """
        Add a boolean option.

        :param name: The name of the option.
        :type name: str

        :param value: The value of the option.
        :type value: bool

        :return: The result of the operation.
        :rtype: bool
        """
        return self.options.AddOptionBool(_cstr(name), value)

    def addOptionInt(self, name, value):
        """
        Add an integer option.

        :param name: The name of the option.
        :type name: str

        :param value: The value of the option.
        :type value: int

        :return: The result of the operation.
        :rtype: bool
        """
        return self.options.AddOptionInt(_cstr(name), value)

    def addOptionString(self, name, value, append=False):
        """
        Add a string option.

        :param name: The name of the option.
            Option names are case insensitive and must be unique.
        :type name: str

        :param value: The value of the option.
        :type value: str

        :param append: Setting append to true will cause values read from
            the command line or XML file to be concatenated into a comma
            delimited set.  If _append is false, newer values will
            overwrite older ones.
        :type append: bool, optional

        :return: The result of the operation.
        :rtype: bool
        """

        return self.options.AddOptionString(
            _cstr(name),
            _cstr(value),
            append
        )

    def addOption(self, name, value):
        """
        Add an option.

        :param name: The name of the option.
        :type name: str

        :param value: The value of the option.
        :type value: bool, int, str

        :return: The result of the operation.
        :rtype: bool
        """
        if name not in PyOptionList:
            return False
        if PyOptionList[name]['type'] == "String":
            return self.addOptionString(name, value)
        elif PyOptionList[name]['type'] == "Bool":
            return self.addOptionBool(name, value)
        elif PyOptionList[name]['type'] == "Int":
            return self.addOptionInt(name, value)
        return False

    def getOption(self, name):
        """
        Retrieve option of a value.

        :param name: The name of the option.
        :type name: str

        :return: The value
        :rtype: bool, int, str, optional
        """
        if name not in PyOptionList:
            return None
        if PyOptionList[name]['type'] == "String":
            return self.getOptionAsString(name)
        elif PyOptionList[name]['type'] == "Bool":
            return self.getOptionAsBool(name)
        elif PyOptionList[name]['type'] == "Int":
            return self.getOptionAsInt(name)
        return False

    def getOptionAsBool(self, name):
        """
        Retrieve boolean value of an option.

        :param name: The name of the option.
        :type name: str

        :return: The value or None
        :rtype: bool, optional
        """
        cdef bool_t type_bool
        cret = self.options.GetOptionAsBool(_cstr(name), &type_bool)
        ret = type_bool if cret==True else None
        return ret

    def getOptionAsInt(self, name):
        """
        Retrieve integer value of an option.

        :param name: The name of the option.
        :type name: str

        :return: The value or None
        :rtype: int, optional
        """
        cdef int32_t type_int
        cret = self.options.GetOptionAsInt(_cstr(name), &type_int)
        ret = type_int if cret==True else None
        return ret

    def getOptionAsString(self, name):
        """
        Retrieve string value of an option.

        :param name: The name of the option.
        :type name: str

        :return: The value or None
        :rtype: str, optional
        """

        cdef string type_string
        cret = self.options.GetOptionAsString(
            _cstr(name),
            &type_string
        )

        ret = _str(type_string.c_str()) if cret==True else None
        return ret

    def getConfigPath(self):
        """
        Retrieve the config path. This directory hold the xml files.

        :return: A string containing the library config path or None.
        :rtype: str
        """
        return _configPath()


# noinspection PyClassicStyleClass
cdef class _RetAlloc:
    """
    Map an array of uint8_t used when retrieving sets.
    Allocate memory at init and free it when no more reference to it exist.
    Give it to lion as Nico0084 says :
    http://blog.naviso.fr/wordpress/wp-sphinxdoc/uploads/2011/11/
    MemoryLeaks3.jpg

    """
    cdef uint32_t siz
    cdef uint8_t* data

    def __cinit__(self,  uint32_t siz):
        self.siz = siz
        self.data = <uint8_t*>malloc(sizeof(uint8_t) * siz)

    def __dealloc__(self):
        free(self.data)


def _data_type(d):
    cls = type(d)
    return cls, d


class PyInstanceAssociation(object):
    node_id = 0
    instance = 0

    def __init__(self):
        self.node_id = None
        self.instance = None

    def __eq__(self, other):
        return other.node_id == self.node_id and other.instance == self.instance

    def __ne__(self, other):
        return not self.__eq__(other)


cdef class _InstanceAssociationAlloc:
    """
    Map an array of InstanceAssociation_t used when retrieving sets of associationInstances.
    Allocate memory at init and free it when no more reference to it exist.
    Give it to lion as Nico0084 says : http://blog.naviso.fr/wordpress/wp-sphinxdoc/uploads/2011/11/MemoryLeaks3.jpg
    """
    cdef uint32_t siz
    cdef uint8_t* data

    def __cinit__(self,  uint32_t siz):
        self.siz = siz
        self.data = <uint8_t*>malloc(sizeof(uint8_t) * siz * 2)

    def __dealloc__(self):
        free(self.data)


# noinspection PyPep8Naming,PyClassicStyleClass
class CommandClassData(object):
    """
    Command Class Data
    
    Attributes:
    
    * `commandClassId`: Num type of CommandClass id.
    * `sentCnt`: Number of messages sent from this CommandClass.
    * `receivedCnt`: Number of messages received from this CommandClass
    """
    
    commandClassId = 0
    sentCnt = 0
    receivedCnt = 0


# noinspection PyPep8Naming,PyClassicStyleClass
class NodeStats(object):
    """
    Node Statistics
    
    Attributes:

    * `sentCnt`: Number of messages sent from this node.
    * `sentFailed`: Number of sent messages failed.
    * `retries`: Number of message retries.
    * `receivedCnt`: Number of messages received from this node.
    * `receivedDups`: Number of duplicated messages received.
    * `receivedUnsolicited`: Number of messages received unsolicited.
    * `lastRequestRTT`: Last message request RTT.
    * `lastResponseRTT`: Last message response RTT.
    * `sentTS`: Last message sent time.
    * `receivedTS`: Last message received time.
    * `averageRequestRTT`: Average Request Round Trip Time (ms).
    * `averageResponseRTT`: Average response round trip time.
    * `quality`: Node quality measure.
    * `lastReceivedMessage`: Place to hold last received message.
    * `ccData`: Command Class Data
    * `txStatusReportSupported`:  if Extended Status Reports are available
    * `txTime`: Time Taken to Transmit the last frame
    * `hops`: Hops taken in transmitting last frame
    * `rssi_1`: RSSI Level of last transmission
    * `rssi_2`: RSSI Level of last transmission
    * `rssi_3`: RSSI Level of last transmission
    * `rssi_4`: RSSI Level of last transmission
    * `rssi_5`: RSSI Level of last transmission
    * `ackChannel`: Channel we received the last ACK on
    * `lastTxChannel`: Channel we transmitted the last frame on
    * `routeScheme`: The Scheme used to route the last frame
    * `routeUsed`: The Route Taken in the last frame
    * `routeSpeed`: Baud Rate of the last frame
    * `routeTries`: The number of attempts to route the last frame
    * `lastFailedLinkFrom`: The last failed link from
    * `lastFailedLinkTo`: The last failed link to
    """

    sentCnt = 0
    sentFailed = 0
    retries = 0
    receivedCnt = 0
    receivedDups = 0
    receivedUnsolicited = 0
    lastRequestRTT = 0
    lastResponseRTT = 0
    sentTS = ''
    receivedTS = ''
    averageRequestRTT = 0
    averageResponseRTT = 0
    quality = 0
    lastReceivedMessage = [0]
    ccData = [CommandClassData()]
    txStatusReportSupported = False
    txTime = 0
    hops = 0
    rssi_1 = ''
    rssi_2 = ''
    rssi_3 = ''
    rssi_4 = ''
    rssi_5 = ''
    ackChannel = 0
    lastTxChannel = 0
    routeScheme = 0
    routeUsed = 0
    routeSpeed = 0
    routeTries = 0
    lastFailedLinkFrom = 0
    lastFailedLinkTo = 0




# noinspection PyPep8Naming,PyClassicStyleClass
class DriverStats(object):
    """
    Driver Statistics
    
    Attributes: 
    
    * `SOFCnt`: Number of SOF bytes received
    * `ACKWaiting`: Number of unsolicited messages while waiting
                    for an ACK
    * `readAborts`: Number of times read were aborted due to
                    timeouts
    * `badChecksum`: Number of bad check sums
    * `readCnt`: Number of messages successfully read
    * `writeCnt`: Number of messages successfully sent
    * `CANCnt`: Number of CAN bytes received
    * `NAKCnt`: Number of NAK bytes received
    * `ACKCnt`: Number of ACK bytes received
    * `OOFCnt`: Number of bytes out of framing
    * `dropped`: Number of messages dropped & not delivered
    * `retries`: Number of messages retransmitted
    * `callbacks`: Number of unexpected callbacks
    * `badroutes`: Number of failed messages due to bad route
                   response
    * `noack`: Number of no ACK returned errors
    * `netbusy`: Number of network busy/failure messages
    * `nondelivery`: Number of messages not delivered to network
    * `routedbusy`: Number of messages received with routed busy
                    status
    * `broadcastReadCnt`: Number of broadcasts read
    * `broadcastWriteCnt`: Number of broadcasts sent
    """

    SOFCnt = 0
    ACKWaiting = 0
    readAborts = 0
    badChecksum = 0
    readCnt = 0
    writeCnt = 0
    CANCnt = 0
    NAKCnt = 0
    ACKCnt = 0
    OOFCnt = 0
    dropped = 0
    retries = 0
    callbacks = 0
    badroutes = 0
    noack = 0
    netbusy = 0
    nondelivery = 0
    routedbusy = 0
    broadcastReadCnt = 0
    broadcastWriteCnt = 0
        


# noinspection PyPep8Naming,PyClassicStyleClass,PyUnresolvedReferences,PyAttributeOutsideInit
cdef class PyManager:
    """
    The main public interface to OpenZWave.

    A singleton class providing the main public interface to OpenZWave.
    The Manager class exposes all the functionality required to add Z-Wave
    support to an application.  It handles the sending and receiving of
    Z-Wave messages as well as the configuration of a Z-Wave network and
    its devices, freeing the library user from the burden of learning the
    low-level details of the Z-Wave protocol.

    All Z-Wave functionality is accessed via the Manager class. While this
    does not make for the most efficient code structure, it does enable
    the library to handle potentially complex and hard-to-debug issues
    such as multi-threading and object lifespans behind the scenes.
    Application development is therefore simplified and less prone to bugs.

    There can be only one instance of the Manager class, and all
    applications will start by calling Manager::Create static method to
    create that instance.  From then on, a call to the Manager::Get static
    method will return the pointer to the Manager object. On application
    exit, Manager::Destroy should be called to allow OpenZWave to clean up
    and delete any other objects it has created.

    Once the Manager has been created, a call should be made to
    Manager::AddWatcher to install a notification callback handler. This
    handler will receive notifications of Z-Wave network changes and
    updates to device values, and is an essential element of OpenZWave.

    Next, a call should be made to Manager::AddDriver for each Z-Wave
    controller attached to the PC.  Each Driver will handle the sending
    and receiving of messages for all the devices in its controller's
    Z-Wave network.  The Driver will read any previously saved
    configuration and then query the Z-Wave controller for any missing
    information.  Once that process is complete, a DriverReady
    notification callback will be sent containing the Home ID of the
    controller, which is required by most of the other Manager class
    methods.

    After the DriverReady notification is sent, the Driver will poll each
    node on the network to update information about each node.  After all
    "awake" nodes have been polled, an "AllAwakeNodesQueried" notification
    is sent. This is when a client application can expect all of the node
    information (both static information, like the physical device's
    capabilities, session information (like [associations and/or names]
    and dynamic information (like temperature or on/off state) to be
    available. Finally, after all nodes (whether setening or sleeping)
    have been polled, an "AllNodesQueried" notification is sent.
    """
    COMMAND_CLASS_DESC = {
        0x00: 'COMMAND_CLASS_NO_OPERATION',
        0x20: 'COMMAND_CLASS_BASIC',
        0x21: 'COMMAND_CLASS_CONTROLLER_REPLICATION',
        0x22: 'COMMAND_CLASS_APPLICATION_STATUS',
        0x23: 'COMMAND_CLASS_ZIP_SERVICES',
        0x24: 'COMMAND_CLASS_ZIP_SERVER',
        0x25: 'COMMAND_CLASS_SWITCH_BINARY',
        0x26: 'COMMAND_CLASS_SWITCH_MULTILEVEL',
        0x27: 'COMMAND_CLASS_SWITCH_ALL',
        0x28: 'COMMAND_CLASS_SWITCH_TOGGLE_BINARY',
        0x29: 'COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL',
        0x2A: 'COMMAND_CLASS_CHIMNEY_FAN',
        0x2B: 'COMMAND_CLASS_SCENE_ACTIVATION',
        0x2C: 'COMMAND_CLASS_SCENE_ACTUATOR_CONF',
        0x2D: 'COMMAND_CLASS_SCENE_CONTROLLER_CONF',
        0x2E: 'COMMAND_CLASS_ZIP_CLIENT',
        0x2F: 'COMMAND_CLASS_ZIP_ADV_SERVICES',
        0x30: 'COMMAND_CLASS_SENSOR_BINARY',
        0x31: 'COMMAND_CLASS_SENSOR_MULTILEVEL',
        0x32: 'COMMAND_CLASS_METER',
        0x33: 'COMMAND_CLASS_COLOR',
        0x34: 'COMMAND_CLASS_ZIP_ADV_CLIENT',
        0x35: 'COMMAND_CLASS_METER_PULSE',
        0x3C: 'COMMAND_CLASS_METER_TBL_CONFIG',
        0x3D: 'COMMAND_CLASS_METER_TBL_MONITOR',
        0x3E: 'COMMAND_CLASS_METER_TBL_PUSH',
        0x38: 'COMMAND_CLASS_THERMOSTAT_HEATING',
        0x40: 'COMMAND_CLASS_THERMOSTAT_MODE',
        0x42: 'COMMAND_CLASS_THERMOSTAT_OPERATING_STATE',
        0x43: 'COMMAND_CLASS_THERMOSTAT_SETPOINT',
        0x44: 'COMMAND_CLASS_THERMOSTAT_FAN_MODE',
        0x45: 'COMMAND_CLASS_THERMOSTAT_FAN_STATE',
        0x46: 'COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE',
        0x47: 'COMMAND_CLASS_THERMOSTAT_SETBACK',
        0x4c: 'COMMAND_CLASS_DOOR_LOCK_LOGGING',
        0x4E: 'COMMAND_CLASS_SCHEDULE_ENTRY_LOCK',
        0x50: 'COMMAND_CLASS_BASIC_WINDOW_COVERING',
        0x51: 'COMMAND_CLASS_MTP_WINDOW_COVERING',
        0x56: 'COMMAND_CLASS_CRC_16_ENCAP',
        0x5A: 'COMMAND_CLASS_DEVICE_RESET_LOCALLY',
        0x5B: 'COMMAND_CLASS_CENTRAL_SCENE',
        0x5E: 'COMMAND_CLASS_ZWAVE_PLUS_INFO',
        0x60: 'COMMAND_CLASS_MULTI_INSTANCE/CHANNEL',
        0x61: 'COMMAND_CLASS_DISPLAY',
        0x62: 'COMMAND_CLASS_DOOR_LOCK',
        0x63: 'COMMAND_CLASS_USER_CODE',
        0x64: 'COMMAND_CLASS_GARAGE_DOOR',
        0x66: 'COMMAND_CLASS_BARRIER_OPERATOR',
        0x70: 'COMMAND_CLASS_CONFIGURATION',
        0x71: 'COMMAND_CLASS_ALARM',
        0x72: 'COMMAND_CLASS_MANUFACTURER_SPECIFIC',
        0x73: 'COMMAND_CLASS_POWERLEVEL',
        0x75: 'COMMAND_CLASS_PROTECTION',
        0x76: 'COMMAND_CLASS_LOCK',
        0x77: 'COMMAND_CLASS_NODE_NAMING',
        0x78: 'COMMAND_CLASS_ACTUATOR_MULTILEVEL',
        0x79: 'COMMAND_CLASS_KICK',
        0x7A: 'COMMAND_CLASS_FIRMWARE_UPDATE_MD',
        0x7B: 'COMMAND_CLASS_GROUPING_NAME',
        0x7C: 'COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE',
        0x7D: 'COMMAND_CLASS_REMOTE_ASSOCIATION',
        0x80: 'COMMAND_CLASS_BATTERY',
        0x81: 'COMMAND_CLASS_CLOCK',
        0x82: 'COMMAND_CLASS_HAIL',
        0x83: 'COMMAND_CLASS_NETWORK_STAT',
        0x84: 'COMMAND_CLASS_WAKE_UP',
        0x85: 'COMMAND_CLASS_ASSOCIATION',
        0x86: 'COMMAND_CLASS_VERSION',
        0x87: 'COMMAND_CLASS_INDICATOR',
        0x88: 'COMMAND_CLASS_PROPRIETARY',
        0x89: 'COMMAND_CLASS_LANGUAGE',
        0x8A: 'COMMAND_CLASS_TIME',
        0x8B: 'COMMAND_CLASS_TIME_PARAMETERS',
        0x8C: 'COMMAND_CLASS_GEOGRAPHIC_LOCATION',
        0x8D: 'COMMAND_CLASS_COMPOSITE',
        0x8E: 'COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION',
        0x8F: 'COMMAND_CLASS_MULTI_CMD',
        0x90: 'COMMAND_CLASS_ENERGY_PRODUCTION',
        0x91: 'COMMAND_CLASS_MANUFACTURER_PROPRIETARY',
        0x92: 'COMMAND_CLASS_SCREEN_MD',
        0x93: 'COMMAND_CLASS_SCREEN_ATTRIBUTES',
        0x94: 'COMMAND_CLASS_SIMPLE_AV_CONTROL',
        0x95: 'COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD',
        0x96: 'COMMAND_CLASS_AV_RENDERER_STATUS',
        0x97: 'COMMAND_CLASS_AV_CONTENT_SEARCH_MD',
        0x98: 'COMMAND_CLASS_SECURITY',
        0x99: 'COMMAND_CLASS_AV_TAGGING_MD',
        0x9A: 'COMMAND_CLASS_IP_CONFIGURATION',
        0x9B: 'COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION',
        0x9C: 'COMMAND_CLASS_SENSOR_ALARM',
        0x9D: 'COMMAND_CLASS_SILENCE_ALARM',
        0x9E: 'COMMAND_CLASS_SENSOR_CONFIGURATION',
        0xEF: 'COMMAND_CLASS_MARK',
        0xF0: 'COMMAND_CLASS_NON_INTEROPERABLE'
    }
    """
    The command classes
    """

    CALLBACK_DESC = (
        'value added',
        'value removed',
        'value changed',
        'groups changed',
        'new node',
        'node added',
        'node removed',
        'node protocol info',
        'node naming',
        'node event',
        'polling disabled',
        'polling enabled',
        'driver ready',
        'driver reset',
        'message complete',
        'node queries complete',
        'awake nodes queried',
        'all nodes queried'
    )

    cdef Manager *manager
    cdef object _watcherCallback
    cdef object _controllerCallback

    def create(self):
        """
        Creates the Manager singleton object.

        The Manager provides the public interface to OpenZWave, exposing
        all the functionality required to add Z-Wave support to an
        application. There can be only one Manager in an OpenZWave
        application. An Options object must be created and Locked first,
        otherwise the call to Manager::Create will fail. Once the Manager
        has been created, call AddWatcher to install a notification
        callback handler, and then call the AddDriver method for each
        attached PC Z-Wave controller in turn.
        
        :rtype: None
        """
        #Commented to try to fix seg fault at import
        Py_Initialize()
        PyEval_InitThreads()
        self.manager = CreateManager()

    def destroy(self):
        """
        Deletes the Manager and cleans up any associated objects.
        
        :rtype: None
        """
        self.manager.Destroy()

    #
    # -------------------------------------------------------------------------
    # Configuration
    # -------------------------------------------------------------------------
    # For saving the Z-Wave network configuration so that the entire network
    # does not need to be polled every time the application starts.
    #
    def writeConfig(self, home_id):
        """
        Saves the configuration of a PC Controller's Z-Wave network to the
        application's user data folder.

        This method does not normally need to be called, since OpenZWave
        will save the state automatically during the shutdown process. It
        is provided here only as an aid to development. The configuration
        of each PC Controller's Z-Wave network is stored in a separate
        file. The filename consists of the 8 digit hexadecimal version of
        the controller's Home ID, prefixed with the string "zwcfg_*".
        This convention allows OpenZWave to find the correct configuration
        file for a controller, even if it is attached to a different
        serial port, USB device path, etc.

        :param home_id: The Home ID of the Z-Wave controller to save.
        :type home_id: int
        
        :rtype: None
        """
        self.manager.WriteConfig(home_id)

    # -------------------------------------------------------------------------
    # Drivers
    # -------------------------------------------------------------------------
    # Methods for adding and removing drivers and obtaining basic
    # controller information.
    #
    def addDriver(self, serial_port):
        """
        Creates a new driver for a Z-Wave controller.

        This method creates a Driver object for handling communications
        with a single Z-Wave controller. In the background, the driver
        first tries to read configuration data saved during a previous
        run. It then queries the controller directly for any missing
        information, and a refresh of the set of nodes that it controls.
        Once this information has been received, a DriverReady
        notification callback is sent, containing the Home ID of the
        controller. This Home ID is required by most of the OpenZWave
        Manager class methods.

        :param serial_port: The string used to open the controller.
            On Windows this might be something like "\\.\\COM3",
            or on Linux "/dev/ttyUSB0".
        :type serial_port: str

        :return: True if a new driver was created
        :rtype: bool
        """
        self.manager.AddDriver(_cstr(serial_port))

    def removeDriver(self, serial_port):
        """
        Removes the driver for a Z-Wave controller,
        and closes the controller.

        Drivers do not need to be explicitly removed before calling
        Destroy - this is handled automatically.

        :param serial_port: The same string as was passed in the original
            call toAddDriver.
        :type serial_port: str

        :return: True if the driver was removed, False if it could not be
            found.
        :rtype: bool
        """
        self.manager.RemoveDriver(_cstr(serial_port))

    def getControllerInterfaceType(self, home_id):
        """
        Retrieve controller interface type, Unknown, Serial, Hid

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :return: The controller interface type
        :rtype: str
        """
        # noinspection PyShadowingBuiltins
        type = self.manager.GetControllerInterfaceType(home_id)
        return PyControllerInterface[type]

    def getControllerPath(self, home_id):
        """Retrieve controller interface path, name or path used to
        open the controller hardware

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :return: The controller interface type
        :rtype: str
        """
        cdef string c_string = self.manager.GetControllerPath(home_id)
        return _str(c_string.c_str())

    def getControllerNodeId(self, home_id):
        """
        Get the node ID of the Z-Wave controller.

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :return: The node ID of the Z-Wave controller
        :rtype: int
        """
        return self.manager.GetControllerNodeId(home_id)

    def getSUCNodeId(self, home_id):
        """
        Get the node ID of the Static Update Controller.

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :return: the node ID of the Z-Wave controller.
        :rtype: int
        """
        return self.manager.GetSUCNodeId(home_id)

    def isPrimaryController(self, home_id):
        """
        Query if the controller is a primary controller.

        The primary controller is the main device used to configure and
        control a Z-Wave network.  There can only be one primary
        controller - all other controllers are secondary controllers.

        The only difference between a primary and secondary controller is
        that the primary is the only one that can be used to add or remove
        other devices. For this reason, it is usually better for the
        primary controller to be portable, since most devices must be
        added when installed in their final location.

        Calls to BeginControllerCommand will fail if the controller is
        not the primary.

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :return: `True` if it is a primary controller, `False` if not.
        :rtype: bool
        """
        return self.manager.IsPrimaryController(home_id)

    def isStaticUpdateController(self, home_id):
        """
        Query if the controller is a static update controller (SUC).

        A Static Update Controller (SUC) is a controller that must never
        be moved in normal operation and which can be used by other nodes
        to receive information about network changes.

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :return: `True` if it is a static update controller,
            `False` if not.
        :rtype: bool
        """
        return self.manager.IsStaticUpdateController(home_id)

    def isBridgeController(self, home_id):
        """
        Query if the controller is using the bridge controller library.

        A bridge controller is able to create virtual nodes that can be
        associated with other controllers to enable events to be passed on.

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :return: `True` if it is a bridge controller, `False` if not.
        :rtype: bool
        """
        return self.manager.IsBridgeController(home_id)

    def getLibraryVersion(self, home_id):
        """
        Get the version of the Z-Wave API library used by a controller.

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :return: A string containing the library version. For example,
            `"Z-Wave 2.48"`.
        :rtype: str
        """
        cdef string c_string = self.manager.GetLibraryVersion(home_id)
        return _str(c_string.c_str())

    def getPythonLibraryFlavor(self):
        """
        Get the flavor of the python library.

        :return: A string containing the python library flavor.
            For example, `"embed"`.
        :rtype: str
        """
        return "%s" % (PY_LIB_FLAVOR_STRING,)

    def getPythonLibraryVersion(self):
        """
        Get the version of the python library.

        :return: A string containing the python library version.
            For example, `"libopenzwave version 0.1"`.
        :rtype: str
        """
        return "libopenzwave version %s (%s-%s / %s - %s)" % (
            PYLIBRARY,
            PY_LIB_FLAVOR_STRING,
            PY_LIB_BACKEND_STRING,
            PY_LIB_DATE_STRING,
            PY_LIB_TIME_STRING
        )

    def getPythonLibraryVersionNumber(self):
        """
        Get the python library version number

        :return: A string containing the python library version.
            For example, `"0.1"`.
        :rtype: str
        """
        return PYLIBRARY

    def getOzwLibraryVersion(self):
        """
        Get a string containing the openzwave library version.

        :return: A string containing the library type.
        :rtype: str
        """
        cdef string c_string = self.manager.getVersionAsString()
        return _str(c_string.c_str())

    def getOzwLibraryLongVersion(self):
        """
        Get a string containing the openzwave library version.

        :return: A string containing the library type.
        :rtype: str
        """
        cdef string c_string = self.manager.getVersionLongAsString()
        return _str(c_string.c_str())

    def getOzwLibraryVersionNumber(self):
        """
        Get the openzwave library version number.

        :return: A string containing the library type.
        :rtype: str
        """
        cdef string c_string = self.manager.getVersionAsString()
        return _str(c_string.c_str())

    def getLibraryTypeName(self, home_id):
        """
        Get a string containing the Z-Wave API library type used by a
        controller.

        The controller should never return a slave library type.
        For a more efficient test of whether a controller is a Bridge
        Controller, use the IsBridgeController method.

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :return: A string containing the library type.

        The possible library types are:

            * `"Static Controller"`
            * `"Controller"`
            * `"Enhanced Slave"`
            * `"Slave"`
            * `"Installer"`
            * `"Routing Slave"`
            * `"Bridge Controller"`
            * `"Device Under Test"`

        :rtype: str
        """
        cdef string c_string = self.manager.GetLibraryTypeName(home_id)
        return _str(c_string.c_str())

    def getSendQueueCount(self, home_id):
        """
        Get count of messages in the outgoing send queue.

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :return: Message count
        :rtype: int
        """
        return self.manager.GetSendQueueCount(home_id)

    def logDriverStatistics(self, home_id):
        """
        Send current driver statistics to the log file.

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int
        
        :rtype: None
        """
        self.manager.LogDriverStatistics(home_id)

    #--------------------------------------------------------------------------
    # Statistics interface
    #--------------------------------------------------------------------------
    def getDriverStatistics(self, home_id):
        """
        Retrieve statistics from driver.

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :return: A class object containing statistics of the driver.

        Attributes:

            * `SOFCnt`: Number of SOF bytes received
            * `ACKWaiting`: Number of unsolicited messages while waiting
              for an ACK
            * `readAborts`: Number of times read were aborted due to
              timeouts
            * `badChecksum`: Number of bad check sums
            * `readCnt`: Number of messages successfully read
            * `writeCnt`: Number of messages successfully sent
            * `CANCnt`: Number of CAN bytes received
            * `NAKCnt`: Number of NAK bytes received
            * `ACKCnt`: Number of ACK bytes received
            * `OOFCnt`: Number of bytes out of framing
            * `dropped`: Number of messages dropped & not delivered
            * `retries`: Number of messages retransmitted
            * `callbacks`: Number of unexpected callbacks
            * `badroutes`: Number of failed messages due to bad route
              response
            * `noack`: Number of no ACK returned errors
            * `netbusy`: Number of network busy/failure messages
            * `nondelivery`: Number of messages not delivered to network
            * `routedbusy`: Number of messages received with routed busy
              status
            * `broadcastReadCnt`: Number of broadcasts read
            * `broadcastWriteCnt`: Number of broadcasts sent

        :rtype: DriverStats
       """
        cdef DriverData_t data
        self.manager.GetDriverStatistics( home_id, &data )

        namespace = {}

        namespace['SOFCnt'] = PyStatDriver.SOFCnt(*_data_type(data.m_SOFCnt))
        namespace['ACKWaiting'] = PyStatDriver.ACKWaiting(*_data_type(data.m_ACKWaiting))
        namespace['readAborts'] = PyStatDriver.readAborts(*_data_type(data.m_readAborts))
        namespace['badChecksum'] = PyStatDriver.badChecksum(*_data_type(data.m_badChecksum))
        namespace['readCnt'] = PyStatDriver.readCnt(*_data_type(data.m_readCnt))
        namespace['writeCnt'] = PyStatDriver.writeCnt(*_data_type(data.m_writeCnt))
        namespace['CANCnt'] = PyStatDriver.CANCnt(*_data_type(data.m_CANCnt))
        namespace['NAKCnt'] = PyStatDriver.NAKCnt(*_data_type(data.m_NAKCnt))
        namespace['ACKCnt'] = PyStatDriver.ACKCnt(*_data_type(data.m_ACKCnt))
        namespace['OOFCnt'] = PyStatDriver.OOFCnt(*_data_type(data.m_OOFCnt))
        namespace['dropped'] = PyStatDriver.dropped(*_data_type(data.m_dropped))
        namespace['retries'] = PyStatDriver.retries(*_data_type(data.m_retries))
        namespace['callbacks'] = PyStatDriver.callbacks(*_data_type(data.m_callbacks))
        namespace['badroutes'] = PyStatDriver.badroutes(*_data_type(data.m_badroutes))
        namespace['noack'] = PyStatDriver.noack(*_data_type(data.m_noack))
        namespace['netbusy'] = PyStatDriver.netbusy(*_data_type(data.m_netbusy))
        namespace['nondelivery'] = PyStatDriver.nondelivery(*_data_type(data.m_nondelivery))
        namespace['routedbusy'] = PyStatDriver.routedbusy(*_data_type(data.m_routedbusy))
        namespace['broadcastReadCnt'] = PyStatDriver.broadcastReadCnt(
            *_data_type(data.m_broadcastReadCnt)
        )
        namespace['broadcastWriteCnt'] = PyStatDriver.broadcastWriteCnt(
            *_data_type(data.m_broadcastWriteCnt)
        )

        return type('DriverStats', (DriverStats,), namespace)

    # -------------------------------------------------------------------------
    # Network Commands
    # -------------------------------------------------------------------------
    # Commands for Z-Wave network for testing, routing and other
    # internal operations.
    #
    def testNetworkNode(self, home_id, node_id, count):
        """
        Test network node.

        Sends a series of messages to a network node for testing
        network reliability.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :param count: This is the number of test messages to send.
        :type count: int
        
        :rtype: None
        """
        self.manager.TestNetworkNode(home_id, node_id, count)

    def testNetwork(self, home_id, count):
        """
        Test network.

        Sends a series of messages to every node on the network for
        testing network reliability.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param count: This is the number of test messages to send.
        :type count: int
        
        :rtype: None
        """
        self.manager.TestNetwork(home_id, count)

    def healNetworkNode(self, home_id, node_id, up_node_route=False):
        """
        Heal network node by requesting the node rediscover their
        neighbors.

        Sends a ControllerCommand_RequestNodeNeighborUpdate to the node.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :param up_node_route: Whether to perform return routes
            initialization. (default = `False`).
        :type up_node_route: bool, optional
        
        :rtype: None
        """
        self.manager.HealNetworkNode(home_id, node_id,  up_node_route)

    def healNetwork(self, home_id, up_node_route=False):
        """
        Heal network by requesting nodes rediscover their neighbors.

        Sends a ControllerCommand_RequestNodeNeighborUpdate to every node.
        Can take a while on larger networks.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param up_node_route: Whether to perform return routes
            initialization. (default = `False`).
        :type up_node_route: bool, optional
        
        :rtype: None
        """
        self.manager.HealNetwork(home_id, up_node_route)

    # -------------------------------------------------------------------------
    # Polling Z-Wave devices
    # -------------------------------------------------------------------------
    # Methods for controlling the polling of Z-Wave devices. Modern devices
    # will not require polling. Some old devices need to be polled as the only
    # way to detect status changes.
    #
    def getPollInterval(self):
        """
        Get the time period between polls of a nodes state

        :return: The number of milliseconds between polls
        :rtype: int
        """
        return self.manager.GetPollInterval()

    def setPollInterval(self, milliseconds, b_interval_between_polls):
        """
        Set the time period between polls of a nodes state.

        Due to patent concerns, some devices do not report state changes
        automatically to the controller. These devices need to have their
        state polled at regular intervals. The length of the interval is
        the same for all devices. To even out the Z-Wave network traffic
        generated by polling, OpenZWave divides the polling interval by
        the number of devices that have polling enabled, and polls each in
        turn. It is recommended that if possible, the interval should not
        be set shorter than the number of polled devices in seconds
        (so that the network does not have to cope with more than one poll
        per second).

        :param milliseconds: The length of the polling interval in
            milliseconds.
        :type milliseconds: int

        :param b_interval_between_polls: If set to true (via SetPollInterval),
            the pollInterval will be interspersed between each poll
            (so a much smaller m_pollInterval like 100, 500, or 1,000 may
            be appropriate). If false, the library attempts to complete
            all polls within m_pollInterval
        :type b_interval_between_polls: bool
        
        :rtype: None
        """
        self.manager.SetPollInterval(milliseconds, b_interval_between_polls)

    def enablePoll(self, value_id, intensity=1):
        """
        Enable the polling of a device's state.

        :param value_id: The ID of the value to start polling
        :type value_id: int

        :param intensity: The intensity of the poll (default = 1)
        :type intensity: int, optional

        :return: True if polling was enabled.
        :rtype: bool
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.EnablePoll(_values_map.at(value_id), intensity)
        else :
            return False

    def disablePoll(self, value_id):
        """
        Disable polling of a value.

        :param value_id: The ID of the value to disable polling.
        :type value_id: int

        :return: True if polling was disabled.
        :rtype: bool
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.DisablePoll(_values_map.at(value_id))
        else :
            return False

    def isPolled(self, value_id):
        """
.        Check polling status of a value

        :param value_id: The ID of the value to check polling.
        :type value_id: int

        :return: True if polling is active.
        :rtype: bool
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.isPolled(_values_map.at(value_id))
        else :
            return False

    def getPollIntensity(self, value_id):
        """
        Get the intensity with which this value is polled
        (0=none, 1=every time through the list, 2-every other time, etc).

        :param value_id: The ID of a value.
        :type value_id: int

        :return: A integer containing the poll intensity
        :rtype: int
       """
        if _values_map.find(value_id) != _values_map.end():
            intensity = self.manager.GetPollIntensity(_values_map.at(value_id))
            return intensity
        else :
            return 0

    def setPollIntensity(self, value_id, intensity):
        """
        Set the frequency of polling (0=none, 1=every time through the
        set, 2-every other time, etc)

        :param value_id: The ID of the value whose intensity should be set
        :type value_id: int

        :param intensity: the intensity of the poll
        :type intensity: int
        
        :rtype: None
        """
        if _values_map.find(value_id) != _values_map.end():
            self.manager.SetPollIntensity(_values_map.at(value_id), intensity)

    #
    # -------------------------------------------------------------------------
    # Node information
    # -------------------------------------------------------------------------
    # Methods for accessing information on individual nodes..
    #
    def getNodeStatistics(self, home_id, node_id):
        """
        Retrieve statistics per node

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: A class object containing statistics.
        :rtype: NodeStats
       """
        cdef NodeData_t data

        self.manager.GetNodeStatistics(home_id, node_id, &data)

        namespace = {}

        ccData = []

        while not data.m_ccData.empty():
            cc = data.m_ccData.back()

            namespace = dict(
                commandClassId=PyCommandClassData.commandClassId(*_data_type(cc.m_commandClassId)),
                sentCnt=PyCommandClassData.sentCnt(*_data_type(cc.m_sentCnt)),
                receivedCnt= PyCommandClassData.receivedCnt(*_data_type(cc.m_receivedCnt))
            )

            ccData.append(type('CommandClassData', (CommandClassData,), namespace))
            data.m_ccData.pop_back()


        namespace['sentCnt'] = PyStatNode.sentCnt(
            *_data_type(data.m_sentCnt)
        )
        namespace['sentFailed'] = PyStatNode.sentFailed(
            *_data_type(data.m_sentFailed)
        )
        namespace['retries'] = PyStatNode.retries(
            *_data_type(data.m_retries)
        )
        namespace['receivedCnt'] = PyStatNode.receivedCnt(
            *_data_type(data.m_receivedCnt)
        )
        namespace['receivedDups'] = PyStatNode.receivedDups(
            *_data_type(data.m_receivedDups)
        )
        namespace['receivedUnsolicited'] = PyStatNode.receivedUnsolicited(
            *_data_type(data.m_receivedUnsolicited)
        )
        namespace['sentTS'] = PyStatNode.sentTS(
            *_data_type(_str(data.m_sentTS.c_str()))
        )
        namespace['receivedTS'] = PyStatNode.receivedTS(
            *_data_type(_str(data.m_receivedTS.c_str()))
        )
        namespace['lastRequestRTT'] = PyStatNode.lastRequestRTT(
            *_data_type(data.m_lastRequestRTT)
        )
        namespace['averageRequestRTT'] = PyStatNode.averageRequestRTT(
            *_data_type(data.m_averageRequestRTT)
        )
        namespace['lastResponseRTT'] = PyStatNode.lastResponseRTT(
            *_data_type(data.m_lastResponseRTT)
        )
        namespace['averageResponseRTT'] = PyStatNode.averageResponseRTT(
            *_data_type(data.m_averageResponseRTT)
        )
        namespace['quality'] = PyStatNode.quality(
            *_data_type(data.m_quality)
        )
        namespace['lastReceivedMessage'] = PyStatNode.lastReceivedMessage(
            *_data_type([])
        )
        namespace['txStatusReportSupported'] = PyStatNode.txStatusReportSupported(
            *_data_type(data.m_txStatusReportSupported),
        )
        namespace['ccData'] = PyStatNode.ccData(
            *_data_type(ccData)
        )
        namespace['txStatusReportSupported'] = PyStatNode.txStatusReportSupported(
            *_data_type(data.m_averageRequestRTT)
        )
        namespace['txTime'] = PyStatNode.txTime(
            *_data_type(data.m_txTime)
        )
        namespace['hops'] = PyStatNode.hops(
            *_data_type(data.m_hops)
        )
        namespace['rssi_1'] = PyStatNode.rssi_1(
            *_data_type(_str(data.m_rssi_1))
        )
        namespace['rssi_2'] = PyStatNode.rssi_2(
            *_data_type(_str(data.m_rssi_2))
        )
        namespace['rssi_3'] = PyStatNode.rssi_3(
            *_data_type(_str(data.m_rssi_3))
        )
        namespace['rssi_4'] = PyStatNode.rssi_4(
            *_data_type(_str(data.m_rssi_4))
        )
        namespace['rssi_5'] = PyStatNode.rssi_5(
            *_data_type(_str(data.m_rssi_5))
        )
        namespace['ackChannel'] = PyStatNode.ackChannel(
            *_data_type(data.m_ackChannel)
        )
        namespace['lastTxChannel'] = PyStatNode.lastTxChannel(
            *_data_type(data.m_lastTxChannel)
        )
        namespace['routeScheme'] = PyStatNode.routeScheme(
             *_data_type([
                'IDLE', 'DIRECT', 'CACHED_ROUTE_SR', 'CACHED_ROUTE',
                'CACHED_ROUTE_NLWR', 'ROUTE', 'RESORT_DIRECT',
                'RESORT_EXPLORE'
            ][data.m_routeScheme])
        )
        namespace['routeUsed'] = PyStatNode.routeUsed(
            *_data_type([])
        )
        namespace['routeSpeed'] = PyStatNode.routeSpeed(
            *_data_type(['AUTO', '9600', '40K', '100K'][data.m_routeSpeed])
        )
        namespace['routeTries'] = PyStatNode.routeTries(
            *_data_type(data.m_routeTries)
        )
        namespace['lastFailedLinkFrom'] = PyStatNode.lastFailedLinkFrom(
            *_data_type(data.m_lastFailedLinkFrom)
        )
        namespace['lastFailedLinkTo'] = PyStatNode.lastFailedLinkTo(
            *_data_type(data.m_lastFailedLinkTo)
        )

        namespace['lastReceivedMessage'] = []
        for i in range(0, 254):
            namespace['lastReceivedMessage'].append(data.m_lastReceivedMessage[i])

        namespace['routeUsed'] = []
        for i in range(0, 4):
            namespace['routeUsed'].append(data.m_routeUsed[i])

        stats = type('NodeStats', (NodeStats,), namespace)
        return stats

    def requestNodeDynamic(self, home_id, node_id):
        """
        Trigger the fetching of fixed data about a node.

        Causes the nodes data to be obtained from the Z-Wave network in
        the same way as if it had just been added. This method would
        normally be called automatically by OpenZWave, but if you know
        that a node has been changed, calling this method will force a
        refresh of the data held by the library. This can be especially
        useful for devices that were asleep when the application was
        first run.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: 'True' if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.RequestNodeDynamic(home_id, node_id)

    def refreshNodeInfo(self, home_id, node_id):
        """
        Trigger the fetching of fixed data about a node.

        Causes the nodes data to be obtained from the Z-Wave network in
        the same way as if it had just been added. This method would
        normally be called automatically by OpenZWave, but if you know
        that a node has been changed, calling this method will force a
        refresh of the data held by the library. This can be especially
        useful for devices that were asleep when the application was
        first run.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.RefreshNodeInfo(home_id, node_id)

    def requestNodeState(self, home_id, node_id):
        """
        Trigger the fetching of just the dynamic value data for a node.

        Causes the node's values to be requested from the Z-Wave network.
        This is the same as the query state starting from the
        dynamic state.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.RequestNodeState(home_id, node_id)

    def isNodeBeamingDevice(self, home_id, node_id):
        """
        Get whether the node is a beam capable device.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the node is a beaming device
        :rtype: bool
        """
        return self.manager.IsNodeBeamingDevice(home_id, node_id)


    def isNodeListeningDevice(self, home_id, node_id):
        """
        Get whether the node is a setening device that does not go to sleep

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if it is a listening node.
        :rtype: bool
        """
        return self.manager.IsNodeListeningDevice(home_id, node_id)

    def isNodeFrequentListeningDevice(self, home_id, node_id):
        """
        Get whether the node is a frequent setening device that goes to
        sleep but can be woken up by a beam.

        Useful to determine node and controller consistency.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if it is a frequent listening node.
        :rtype: bool
        """
        return self.manager.IsNodeFrequentListeningDevice(home_id, node_id)

    def isNodeSecurityDevice(self, home_id, node_id):
        """
        Get the security attribute for a node. True if node
        supports security features.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if security features implemented.
        :rtype: bool
        """
        return self.manager.IsNodeSecurityDevice(home_id, node_id)

    def isNodeRoutingDevice(self, home_id, node_id):
        """
        Get whether the node is a routing device that passes messages to
        other nodes

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the node is a routing device
        :rtype: bool
        """
        return self.manager.IsNodeRoutingDevice(home_id, node_id)

    def getNodeMaxBaudRate(self, home_id, node_id):
        """
        Get the maximum baud rate of a nodes communications

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: The baud rate in bits per second.
        :rtype: int
        """
        return self.manager.GetNodeMaxBaudRate(home_id, node_id)

    def getNodeVersion(self, home_id, node_id):
        """
        Get the version number of a node

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: The node version number
        :rtype: int
        """
        return self.manager.GetNodeVersion(home_id, node_id)

    def getNodeSecurity(self, home_id, node_id):
        """
        Get the security byte for a node.

        Bit meanings are still to be determined.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: The node security byte
        :rtype: int
        """
        return self.manager.GetNodeSecurity(home_id, node_id)

    def getNodeBasic(self, home_id, node_id):
        """
        Get the basic type of a node.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: The node basic type.
        :rtype: int
        """
        return self.manager.GetNodeBasic(home_id, node_id)

    def getNodeGeneric(self, home_id, node_id):
        """
        Get the generic type of a node.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: The node generic type.
        :rtype: int
        """
        return self.manager.GetNodeGeneric(home_id, node_id)

    def getNodeSpecific(self, home_id, node_id):
        """
        Get the specific type of a node.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type home_id: int

        :return: The node specific type.
        :rtype: int
        """
        return self.manager.GetNodeSpecific(home_id, node_id)

    def getNodeType(self, home_id, node_id):
        """
        Get a human-readable label describing the node

        The label is taken from the Z-Wave specific, generic or basic
        type, depending on which of those values are specified by the node.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: A string containing the label text.
        :rtype: str
        """
        cdef string c_string = self.manager.GetNodeType(home_id, node_id)
        return _str(c_string.c_str())

    def getNodeNeighbors(self, home_id, node_id):
        """
        Get the bitmap of this node's neighbors.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: A list containing neighboring node IDs
        :rtype: list
        """
        data = set()
        #Allocate memory for the c++ function
        #Return value is pointer to uint8_t[]
        cdef uint8_t** dbuf = <uint8_t**>malloc(sizeof(uint8_t)*29)

        #Get the number of neighbors
        cdef uint32_t count = self.manager.GetNodeNeighbors(
            home_id,
            node_id,
            dbuf
        )

        if count == 0:
            #Don't need to allocate memory.
            free(dbuf)
            return data

        #Allocate memory for the returned values
        cdef _RetAlloc retuint8 = _RetAlloc(count)
        cdef uint8_t* p
        cdef uint32_t start = 0

        if count:
            try:
                p = dbuf[0] # p is now pointing at first element of array
                for i in range(start, count):
                    #cdef uint8_t = retuint8[i]
                    retuint8.data[i] = p[0]
                    data.add(retuint8.data[i])
                    p += 1
            finally:
                #Free memory
                free(dbuf)
                pass

        return list(item for item in data)

    def getNodeManufacturerName(self, home_id, node_id):
        """
        Get the manufacturer name of a device

        The manufacturer name would normally be handled by the
        Manufacturer Specific command class, taking the manufacturer ID
        reported by the device and using it to look up the name from the
        manufacturer_specific.xml file in the OpenZWave config folder.

        However, there are some devices that do not support the command
        class, so to enable the user to manually set the name, it is
        stored with the node data and accessed via this method rather than
        being reported via a command class Value object.

        :param home_id: The Home ID of the Z-Wave controller that
            manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: A string containing the nodes manufacturer name.
        :rtype: str
        """
        cdef string manufacturer_string = self.manager.GetNodeManufacturerName(
            home_id,
            node_id
        )
        return _str(manufacturer_string.c_str())

    def getNodeProductName(self, home_id, node_id):
        """
        Get the product name of a device

        The product name would normally be handled by the Manufacturer
        Specific command class, taking the product Type and ID reported
        by the device and using it to look up the name from the
        manufacturer_specific.xml file in the OpenZWave config folder.

        However, there are some devices that do not support the command
        class, so to enable the user to manually set the name, it is
        stored with the node data and accessed via this method rather than
        being reported via a command class Value object.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: A string containing the nodes product name.
        :rtype: str
        """
        cdef string productname_string = self.manager.GetNodeProductName(
            home_id,
            node_id
        )
        return _str(productname_string.c_str())

    def getNodeName(self, home_id, node_id):
        """
        Get the name of a node

        The node name is a user-editable label for the node that would
        normally be handled by the Node Naming command class, but many
        devices do not support it. So that a node can always be named,
        OpenZWave stores it with the node data, and provides access
        through this method and SetNodeName, rather than reporting it via
        a command class Value object. The maximum length of a node name is
        16 characters.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: A string containing the node name.
        :rtype: str
        """
        cdef string c_string = self.manager.GetNodeName(home_id, node_id)
        return _str(c_string.c_str())

    def getNodeLocation(self, home_id, node_id):
        """
        Get the location of a node

        The node location is a user-editable string that would normally
        be handled by the Node Naming command class, but many devices do
        not support it.  So that a node can always report its location,
        OpenZWave stores it with the node data, and provides access
        through this method and SetNodeLocation, rather than reporting it
        via a command class Value object.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: A string containing the nodes location.
        :rtype: str
        """
        cdef string c_string = self.manager.GetNodeLocation(home_id, node_id)
        return _str(c_string.c_str())

    def getNodeManufacturerId(self, home_id, node_id):
        """
        Get the manufacturer ID of a device

        The manufacturer ID is a four digit hex code and would normally
        be handled by the Manufacturer-Specific command class, but not
        all devices support it. Although the value reported by this method
        will be an empty string if the command class is not supported and
        cannot be set by the user, the manufacturer

        ID is still stored with the node data (rather than being
        reported via a command class Value object) to retain a consistent
        approach with the other manufacturer specific data.

        :param home_id: The Home ID of the Z-Wave controller that manages
            the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: A string containing the nodes manufacturer ID, or an
            empty string if the manufacturer-specific command class is not
            supported by the device.
        :rtype: str
        """
        cdef string c_string = self.manager.GetNodeManufacturerId(
            home_id,
            node_id
        )
        return _str(c_string.c_str())

    def getNodeProductType(self, home_id, node_id):
        """
        Get the product type of a device

        The product type is a four digit hex code and would normally be
        handled by the Manufacturer Specific command class, but not all
        devices support it. Although  the value reported by this method
        will be an empty string if the command class is not supported and
        cannot be set by the user, the product type is still stored with
        the node data (rather than being reported via a command class Value
        object) to retain a consistent approach with the other
        manufacturer specific data.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: A string containing the nodes product type, or an empty
            string if the manufacturer-specific command class is not
            supported by the device.
        :rtype: str
        """
        cdef string c_string = self.manager.GetNodeProductType(
            home_id,
            node_id
        )
        return _str(c_string.c_str())

    def getNodeProductId(self, home_id, node_id):
        """
        Get the product ID of a device

        The product ID is a four digit hex code and would normally be
        handled by the Manufacturer-Specific command class, but not all
        devices support it.  Although the value reported by this method
        will be an empty string if the command class is not supported and
        cannot be set by the user, the product ID is still stored with the
        node data (rather than being reported via a command class Value
        object) to retain a consistent approach with the other
        manufacturer specific data.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: A string containing the nodes product ID, or an empty
            string if the manufacturer-specific command class is not
            supported by the device.
        :rtype: str
        """
        cdef string c_string = self.manager.GetNodeProductId(home_id, node_id)
        return _str(c_string.c_str())

    def setNodeManufacturerName(self, home_id, node_id, manufacturer_name):
        """
        Set the manufacturer name of a device

        The manufacturer name would normally be handled by the
        Manufacturer Specific command class, taking the manufacturer ID
        reported by the device and using it to look up the name from the
        manufacturer_specific.xml file in the OpenZWave config folder.
        However, there are some devices that do not support the command
        class, so to enable the user to manually set the name, it is s
        tored with the node data and accessed via this method rather than
        being reported via a command class Value object.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :param manufacturer_name: A string containing the nodes
            manufacturer name.
        :type manufacturer_name: str, None
        
        :rtype: None
        """
        self.manager.SetNodeManufacturerName(
            home_id,
            node_id,
            _cstr(manufacturer_name)
        )

    def setNodeProductName(self, home_id, node_id, product_name):
        """
        Set the product name of a device

        The product name would normally be handled by the Manufacturer
        Specific command class, taking the product Type and ID reported
        by the device and using it to look up the name from the
        manufacturer_specific.xml file in the OpenZWave config folder.
        However, there are some devices that do not support the command
        class, so to enable the user to manually set the name, it is
        stored with the node data and accessed via this method rather
        than being reported via a command class Value object.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :param product_name: A string containing the nodes product name.
        :type product_name: str
        
        :rtype: None
        """
        self.manager.SetNodeProductName(
            home_id,
            node_id,
            _cstr(product_name)
        )

    def setNodeName(self, home_id, node_id, name):
        """
        Set the name of a node

        The node name is a user-editable label for the node that would
        normally be handled by the Node Naming command class, but many
        devices do not support it. So that a node can always be named,
        OpenZWave stores it with the node data, and provides access
        through this method and GetNodeName, rather than reporting it via
        a command class Value object. If the device does support the Node
        Naming command class, the new name will be sent to the node. The
        maximum length of a node name is 16 characters.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :param name: A string containing the nodes name.
        :type name: str
        
        :rtype: None
        """
        self.manager.SetNodeName(home_id, node_id, _cstr(name))

    def setNodeLocation(self, home_id, node_id, location):
        """
        Set the location of a node

        The node location is a user-editable string that would normally
        be handled by the Node Naming command class, but many devices do
        not support it. So that a node can always report its location,
        OpenZWave stores it with the node data, and provides access
        through this method and GetNodeLocation, rather than
        reporting it via a command class Value object. If the device does
        support the Node Naming command class, the new location will be
        sent to the node.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :param location: A string containing the nodes location.
        :type location: int
        
        :rtype: None
        """
        self.manager.SetNodeLocation(home_id, node_id, _cstr(location))

    def setNodeOn(self, home_id, node_id):
        """
        Turns a node on

        This is a helper method to simplify basic control of a node.
        It is the equivalent of changing the level reported by the nodes
        Basic command class to 255, and will generate a ValueChanged
        notification from that class. This command will turn on the device
        at its last known level, if supported by the device, otherwise it
        will turn it on at 100%.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to be changed.
        :type node_id: int
        
        :rtype: None
        """
        self.manager.SetNodeOn(home_id, node_id)

    def setNodeOff(self, home_id, node_id):
        """
        Turns a node off

        This is a helper method to simplify basic control of a node.
        It is the equivalent of changing the level reported by the nodes
        Basic command class to zero, and will generate a ValueChanged
        notification from that class.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to be changed.
        :type node_id: int
        
        :rtype: None
        """
        self.manager.SetNodeOff(home_id, node_id)

    def setNodeLevel(self, home_id, node_id, level):
        """
       Sets the basic level of a node

        This is a helper method to simplify basic control of a node.
        It is the equivalent of changing the value reported by the nodes
        Basic command class and will generate a ValueChanged notification
        from that class.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to be changed.
        :type node_id: int

        :param level: The level to set the node.
            Valid values are 0-99 and 255.  Zero is off and 99 is fully on.
            255 will turn on the device at its last known level
            (if supported).
        :type level: int
        
        :rtype: None
        """
        self.manager.SetNodeLevel(home_id, node_id, level)

    def isNodeInfoReceived(self, home_id, node_id):
        """
        Get whether the node information has been received

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the node information has been received yet
        :rtype: bool
        """
        return self.manager.IsNodeInfoReceived(home_id, node_id)

    def getNodeRole(self, home_id, node_id):
        """
        Get the node role as reported in the Z-Wave+ Info report.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: The node version number
        :rtype: int
        """
        return self.manager.GetNodeRole(home_id, node_id)

    def getNodeRoleString(self, home_id, node_id):
        """
        Get the node role (string) as reported in the Z-Wave+ Info report.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: name of current query stage as a string.
        :rtype: str
        """
        cdef string c_string = self.manager.GetNodeRoleString(home_id, node_id)
        return _str(c_string.c_str())

    def getNodeDeviceType(self, home_id, node_id):
        """
        Get the node DeviceType as reported in the Z-Wave+ Info report.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: The node version number
        :rtype: int
        """
        return self.manager.GetNodeDeviceType(home_id, node_id)

    def getNodeDeviceTypeString(self, home_id, node_id):
        """
        Get the node DeviceType (string) as reported in the Z-Wave+
        Info report.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: device type as a string..
        :rtype: str
        """
        cdef string c_string = self.manager.GetNodeDeviceTypeString(
            home_id,
            node_id
        )
        return _str(c_string.c_str())

    def getNodePlusType(self, home_id, node_id):
        """
        Get the node plus type as reported in the Z-Wave+ Info report.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: The node version number
        :rtype: int
        """
        return self.manager.GetNodePlusType(home_id, node_id)

    def getNodePlusTypeString(self, home_id, node_id):
        """
        Get the node plus type (string) as reported in the Z-Wave+
        Info report.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: name of current query stage as a string.
        :rtype: str
        """
        cdef string c_string = self.manager.GetNodePlusTypeString(
            home_id,
            node_id
        )

        return _str(c_string.c_str())

    def getNodeClassInformation(
        self,
        home_id,
        node_id,
        command_class_id,
        class_name=None,
        class_version=None
    ):
        """
        Helper method to return whether a particular class is
        available in a node

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :param command_class_id: control class to query
        :type command_class_id: int

        :param class_name: Specific name of class to query
            (default = `None`)
        :type class_name: str, optional

        :param class_version: Specific class version
            (default = `None`)
        :type class_version: int, optional

        :return: True if the node does have the class instantiated,
            will return name & version
        :rtype: bool
        """
        cdef string oclassName
        cdef uint8_t oclassVersion
        ret=self.manager.GetNodeClassInformation(
            home_id,
            node_id,
            command_class_id,
            &oclassName,
            &oclassVersion
        )

        if ret :
            # className = oclassName.c_str()
            # classVersion = oclassVersion
            return ret

        else:
            return False

    def isNodeAwake(self, home_id, node_id):
        """
        Get whether the node is awake or asleep

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the node is awake.
        :rtype: bool
        """
        return self.manager.IsNodeAwake(home_id, node_id)


    def isNodeFailed(self, home_id, node_id):
        """
        Get whether the node is working or has failed

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the node has failed and is no longer
            part of the network.
        :rtype: bool

        """
        return self.manager.IsNodeFailed(home_id, node_id)


    def isNodeZWavePlus(self, home_id, node_id):
        """
        Get whether the node is a ZWave+ one

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the node has failed and is no longer
            part of the network.
        :rtype: bool
        """
        return self.manager.IsNodeZWavePlus(home_id, node_id)


    def getNodeQueryStage(self, home_id, node_id):
        """
        Get whether the node's query stage as a string

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: name of current query stage as a string.
        :rtype: str
        """
        cdef string c_string = self.manager.GetNodeQueryStage(home_id, node_id)
        return _str(c_string.c_str())


    def getNodeQueryStageCode(self, query_stage):
        """
        Get code value from a query stage description

        :param query_stage: The query stage description.
        :type query_stage: str

        :return: code value.
        :rtype: int, optional
        """
        query_stage_mapping = [
            # Retrieve protocol information
            # QueryStage_ProtocolInfo
            "ProtocolInfo",
            # Ping device to see if alive
            # QueryStage_Probe
            "Probe",
            # Start wake up process if a sleeping node
            # QueryStage_WakeUp
            "WakeUp",
            # Retrieve manufacturer name and product ids if
            # ProtocolInfo lets us
            # QueryStage_ManufacturerSpecific1
            "ManufacturerSpecific1",
            # Retrieve info about supported, controlled command classes
            # QueryStage_NodeInfo
            "NodeInfo",
            # Retrieve manufacturer name and product ids
            # QueryStage_ManufacturerSpecific2
            "ManufacturerSpecific2",
            # Retrieve version information
            # QueryStage_Versions
            "Versions",
            # Retrieve information about multiple command class instances
            # QueryStage_Instances
            "Instances",
            # Retrieve static information (doesn't change)
            # QueryStage_Static
            "Static",
            # Ping a device upon starting with configuration
            # QueryStage_Probe1
            "Probe1",
            # Retrieve information about associations
            # QueryStage_Associations
            "Associations",
            # Retrieve node neighbor list
            # QueryStage_Neighbors
            "Neighbors",
            # Retrieve session information (changes infrequently)
            # QueryStage_Session
            "Session",
            # Retrieve dynamic information (changes frequently)
            # QueryStage_Dynamic
            "Dynamic",
            # Retrieve configurable parameter information (only done on request)
            # QueryStage_Configuration
            "Configuration",
            # Query process is completed for this node
            # QueryStage_Complete
            "Complete",
            # Query process hasn't started for this node
            # QueryStage_None
            "None"
        ]

        if query_stage in query_stage_mapping:
            return query_stage_mapping.index(query_stage)

    # -------------------------------------------------------------------------
    # Values
    # -------------------------------------------------------------------------
    # Methods for accessing device values. All the methods require a
    # ValueID, which will have been provided in the ValueAdded
    # Notification callback when the the value was first discovered by
    # OpenZWave.
    #
    def setValue(self, value_id, value, pos=0):
        """
        Sets the value of a device.

        Due to the possibility of a device being asleep, the command is
        assumed to succeed, and the value held by the node is updated
        directly. This will be reverted by a future status message from
        the device if the Z-Wave message actually failed to get through.
        Notification callbacks will be sent in both cases.

        :param value_id: The ID of a value.
        :type value_id: int

        :param value: The value to set.
        :type value: int

        :param pos: Use for the BitSet value type
        :type pos: int

        :return: An integer representing the result of the operation

            * `0`: The C method fails.
            * `1`: The C method succeed.
            * `2`: Can't find id in the map.

        :rtype: int
        """
        cdef float type_float
        cdef bool_t type_bool
        cdef uint8_t type_byte
        cdef int32_t type_int
        cdef int16_t type_short
        cdef string type_string
        cdef uint8_t* type_raw
        ret = 2

        if _values_map.find(value_id) != _values_map.end():
            datatype = PyValueTypes[_values_map.at(value_id).GetType()]
            if datatype == "Bool":
                type_bool = value
                cret = self.manager.SetValue(
                    _values_map.at(value_id),
                    type_bool
                )
                ret = 1 if cret else 0

            elif datatype == "Byte":
                type_byte = value
                cret = self.manager.SetValue(
                    _values_map.at(value_id),
                    type_byte
                )
                ret = 1 if cret else 0

            elif datatype == "Raw":
                type_raw = <uint8_t*> malloc(len(value)*sizeof(uint8_t))
                for x in range(0, len(value)):
                    #print value[x]
                    type_raw[x] = ord(value[x])
                cret = self.manager.SetValue(
                    _values_map.at(value_id),
                    type_raw,
                    len(value)
                )
                ret = 1 if cret else 0
                free(type_raw)

            elif datatype == "Decimal":
                type_float = value
                cret = self.manager.SetValue(
                    _values_map.at(value_id),
                    type_float
                )
                ret = 1 if cret else 0

            elif datatype == "Int":
                type_int = value
                cret = self.manager.SetValue(
                    _values_map.at(value_id),
                    type_int
                )
                ret = 1 if cret else 0

            elif datatype == "Short":
                type_short = value
                cret = self.manager.SetValue(
                    _values_map.at(value_id),
                    type_short
                )
                ret = 1 if cret else 0

            elif datatype == "String":
                type_string =  _cstr(value)

                cret = self.manager.SetValue(
                    _values_map.at(value_id),
                    type_string
                )
                ret = 1 if cret else 0

            elif datatype == "Button":
                type_bool = value
                cret = self.manager.SetValue(
                    _values_map.at(value_id),
                    type_bool
                )
                ret = 1 if cret else 0

            elif datatype == "List":
                logger.debug("SetValueListSelection %s", value)
                if six.PY3:
                    type_string = _cstr(value)
                else:
                    type_string = _cstr(string(value))

                cret = self.manager.SetValueListSelection(
                    _values_map.at(value_id),
                    type_string
                )
                logger.debug("SetValueListSelection %s", cret)
                ret = 1 if cret else 0

            elif datatype == "BitSet":
                type_bool = value
                type_byte = pos
                cret = self.manager.SetValue(
                    _values_map.at(value_id),
                    type_byte,
                    type_bool
                )
                ret = 1 if cret else 0
        return ret

    def refreshValue(self, value_id):
        """
        Refreshes the specified value from the Z-Wave network.

        A call to this function causes the library to send a message to
        the network to retrieve the current value of the specified ValueID
        (just like a poll, except only one-time, not recurring).

        :param value_id: The unique identifier of the value to be
            refreshed.
        :type value_id: int

        :return: `True` if the driver and node were found,
            `False` otherwise
        :rtype: bool
        """
        return self.manager.RefreshValue(_values_map.at(value_id))

    def getValueLabel(self, value_id):
        """
        Gets the user-friendly label for the value

        :param value_id: The ID of a value.
        :type value_id: int

        :return: A string containing the user-friendly label of the value
        :rtype: str, optional
       """
        cdef string c_string
        if _values_map.find(value_id) != _values_map.end():
            c_string = self.manager.GetValueLabel(_values_map.at(value_id))
            return _str(c_string.c_str())
        else :
            return None

    def setValueLabel(self, value_id, label):
        """
        Sets the user-friendly label for the value

        :param value_id: The ID of a value.
        :type value_id: int

        :param label: The label of the value.
        :type label: str
        
        :rtype: None
        """
        if _values_map.find(value_id) != _values_map.end():
            self.manager.SetValueLabel(
                _values_map.at(value_id),
                _cstr(label)
            )

    def getValueUnits(self, value_id):
        """
        Gets the units that the value is measured in.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: A string containing the value of the units.
        :rtype: str, optional
        """
        cdef string c_string
        if _values_map.find(value_id) != _values_map.end():
            c_string = self.manager.GetValueUnits(_values_map.at(value_id))
            return _str(c_string.c_str())
        else :
            return None

    def setValueUnits(self, value_id, unit):
        """
        Sets the units that the value is measured in.

        :param value_id: The ID of a value.
        :type value_id: int

        :param unit: The new value of the units.
        :type unit: str
        
        :rtype: None
        """
        if _values_map.find(value_id) != _values_map.end():
            self.manager.SetValueUnits(
                _values_map.at(value_id),
                _cstr(unit)
            )

    def getValueHelp(self, value_id):
        """
        Gets a help string describing the value's purpose and usage.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: A string containing the value help text.
        :rtype: str, optional
        """
        cdef string c_string
        if _values_map.find(value_id) != _values_map.end():
            c_string = self.manager.GetValueHelp(_values_map.at(value_id))
            return _str(c_string.c_str())
        else :
            return None

    def setValueHelp(self, value_id, help):
        """
        Sets a help string describing the value's purpose and usage.

        :param value_id: the ID of a value.
        :type value_id: int

        :param help: The new value of the help text.
        :type help: str
        
        :rtype: None
        """
        if _values_map.find(value_id) != _values_map.end():
            self.manager.SetValueHelp(
                _values_map.at(value_id),
                _cstr(help)
            )

    def getValueMin(self, value_id):
        """
        Gets the minimum that this value may contain.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The value minimum.
        :rtype: int, optional
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.GetValueMin(_values_map.at(value_id))
        else :
            return None

    def getValueMax(self, value_id):
        """
        Gets the maximum that this value may contain.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The value maximum.
        :rtype: int, optional

        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.GetValueMax(_values_map.at(value_id))
        else :
            return None

    def isValueReadOnly(self, value_id):
        """
        Test whether the value is read-only.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: `True` if the value cannot be changed by the user.
        :rtype: bool, optional
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.IsValueReadOnly(_values_map.at(value_id))
        else :
            return None

    def isValueWriteOnly(self, value_id):
        """
        Test whether the value is write-only.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: `True` if the value can only be written to and not read.
        :rtype: bool, optional
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.IsValueWriteOnly(_values_map.at(value_id))
        else :
            return None

    def isValueSet(self, value_id):
        """
        Test whether the value has been set.

        :param value_id: the ID of a value.
        :type value_id: int

        :return: True if the value has actually been set by a status
            message from the device, rather than simply being the default.
        :rtype: bool, optional
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.IsValueSet(_values_map.at(value_id))
        else :
            return None

    def isValuePolled(self, value_id):
        """
        Test whether the value is currently being polled.

        :param value_id: the ID of a value.
        :type value_id: int

        :return: `True` if the value is being polled, otherwise `False`.
        :rtype: bool, optional
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.IsValuePolled(_values_map.at(value_id))
        else :
            return None

    def getValueGenre(self, value_id):
        """
        Get the genre of the value.

        The genre classifies a value to enable low-level system or
        configuration parameters to be filtered out by the application.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: A string containing the type of the value
        :rtype: str, optional
       """
        if _values_map.find(value_id) != _values_map.end():
            genre = PyGenres[_values_map.at(value_id).GetGenre()]
            return genre
        else :
            return None

    def getValueCommandClass(self, value_id):
        """
        Get the command class instance of this value.

        It is possible for there to be multiple instances of a command
        class, although currently it appears that only the
        SensorMultilevel command class ever does this. Knowledge of
        instances and command classes is not required to use OpenZWave,
        but this information is exposed in case it is of interest.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The command class of the value
        :rtype: int, optional
       """
        if _values_map.find(value_id) != _values_map.end():
            cmd_cls = _values_map.at(value_id).GetCommandClassId()
            return cmd_cls
        else :
            return None

    def getValueInstance(self, value_id):
        """
        Get the command class instance of this value.

        It is possible for there to be multiple instances of a command
        class, although currently it appears that only the
        SensorMultilevel command class ever does this.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: A string containing the type of the value
        :rtype: str, optional
       """
        if _values_map.find(value_id) != _values_map.end():
            genre = _values_map.at(value_id).GetInstance()
            return genre
        else :
            return None

    def getValueIndex(self, value_id):
        """
        Get the value index.

        The index is used to identify one of multiple values created and
        managed by a command class. In the case of configurable
        parameters (handled by the configuration command class),
        the index is the same as the parameter ID.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: A string containing the type of the value
        :rtype: str, optional
       """
        if _values_map.find(value_id) != _values_map.end():
            genre = _values_map.at(value_id).GetIndex()
            return genre
        else :
            return None

    def getValueType(self, value_id):
        """
        Gets the type of the value

        :param value_id: The ID of a value.
        :type value_id: int

        :return: A string containing the type of the value
        :rtype: str, optional
       """
        if _values_map.find(value_id) != _values_map.end():
            datatype = PyValueTypes[_values_map.at(value_id).GetType()]
            return datatype
        else :
            return None

    def getValue(self, value_id):
        """
        Gets a value.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: Depending of the type of the valueId, None otherwise
        :rtype: int, str, float, bool
        """
        return _getValueFromType(self.manager, value_id)

    def getValueAsBool(self, value_id):
        """
        Gets a value as a bool.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The value
        :rtype: bool
        """
        return _getValueFromType(self.manager, value_id)

    def getValueAsByte(self, value_id):
        """
        Gets a value as an 8-bit unsigned integer.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The value
        :rtype: int
        """
        return _getValueFromType(self.manager, value_id)

    def getValueAsFloat(self, value_id):
        """
        Gets a value as a float.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The value
        :rtype: float
        """
        return _getValueFromType(self.manager, value_id)

    def getValueAsShort(self, value_id):
        """
        Gets a value as a 16-bit signed integer.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The value
        :rtype: int
        """
        return _getValueFromType(self.manager, value_id)

    def getValueAsInt(self, value_id):
        """
        Gets a value as a 32-bit signed integer.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The value
        :rtype: int
        """
        return _getValueFromType(self.manager, value_id)

    def getValueAsString(self, value_id):
        """
        Gets a value as a string.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The value
        :rtype: str
        """
        return _getValueFromType(self.manager, value_id)

    def getValueAsRaw(self, value_id):
        """
        Gets a value as raw.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The value
        :rtype: str
        """
        return _getValueFromType(self.manager, value_id)

    def getValueAsBitSet(self, value_id, pos):
        """
        Gets a value as a bool.

        :param value_id: The ID of a value.
        :type value_id: int

        :param pos: The position of the bit to get LSB first
        :type pos: int

        :return: The value
        :rtype: bool
        """

        return _getValueFromType(self.manager, value_id, pos)

    def getValueListSelectionStr(self,  value_id):
        """
        Gets value of items from a list value

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The value
        :rtype: str
        """
        return _getValueFromType(self.manager, value_id)

    def getValueListSelectionNum(self,  value_id):
        """
        Gets value of items from a list value

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The value
        :rtype: int
        """
        cdef int32_t type_int
        ret=-1
        if _values_map.find(value_id) != _values_map.end():
            if self.manager.GetValueListSelection(
                _values_map.at(value_id),
                &type_int
            ):
                ret = type_int
        #print "//////// Value Num list item : " ,  ret
        return ret

    def getValueListItems(self, value_id):
        """
        Gets the list of items from a list value

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The list of possible values
        :rtype: list
        """
        cdef vector[string] vect
        cdef string temp
        cdef size_t size
        ret = []

        if _values_map.find(value_id) != _values_map.end():
            if self.manager.GetValueListItems(_values_map.at(value_id), &vect):
                size = vect.size()

                for i in range(size):
                    temp = vect[i]
                    ret += [_str(temp.c_str())]

        return ret

    def getValueListValues(self, value_id):
        """
        Gets the list of values from a list value.

        :param value_id: The ID of a value.
        :type value_id: int

        :return: The list of values
        :rtype: list
        """
        cdef vector[int32_t] vect
        cdef int32_t temp
        cdef size_t size
        ret = []

        if _values_map.find(value_id) != _values_map.end():
            if self.manager.GetValueListValues(_values_map.at(value_id), &vect):
                size = vect.size()

                for i in range(size):
                    temp = vect[i]
                    ret += [temp]

        return ret

    def pressButton(self, value_id):
        """
        Starts an activity in a device.

        Since buttons are write-only values that do not report a state,
        no notification callbacks are sent.

        :param value_id: The ID of an integer value.
        :type value_id: int

        :return: True if the activity was started. Returns false if the
            value is not a ValueID::ValueType_Button. The type can be
            tested with a call to ValueID::GetType.
        :rtype: bool
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.PressButton(_values_map.at(value_id))
        else :
            return False

    def releaseButton(self, value_id):
        """
        Stops an activity in a device.

        Since buttons are write-only values that do not report a state,
        no notification callbacks are sent.

        :param value_id: the ID of an integer value.
        :type value_id: int

        :return: True if the activity was stopped.
            Returns false if the value is not a ValueID::ValueType_Button.
            The type can be tested with a call to ValueID::GetType.
        :rtype: bool
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.ReleaseButton(_values_map.at(value_id))
        else :
            return False

    def getValueFloatPrecision(self, value_id):
        """
        Gets a float value's precision

        :param value_id: The unique identifier of the value.
        :type value_id: int

        :return: a float value's precision.
        :rtype: int, None
        """
        cdef uint8_t precision
        if _values_map.find(value_id) != _values_map.end():
            success = self.manager.GetValueFloatPrecision(
                _values_map.at(value_id),
                &precision
            )
            return precision if success else None
        return None

    def getChangeVerified(self, value_id):
        """
        Determine if value changes upon a refresh should be verified.

        If so, the library will immediately refresh the value a second
        time whenever a change is observed. This helps to filter out
        spurious data reported occasionally by some devices.

        :param value_id:  The unique identifier of the value whose changes
            should or should not be verified.
        :type value_id: int

        :return: `True` if is verified.
        :rtype: bool
        """

        if _values_map.find(value_id) != _values_map.end():
            return self.manager.GetChangeVerified(_values_map.at(value_id))
        return False

    def setChangeVerified(self, value_id, verify):
        """
        Sets a flag indicating whether value changes noted upon a refresh
        should be verified.

        If so, the library will immediately refresh the value a second
        time whenever a change is observed. This helps to filter out
        spurious data reported occasionally by some devices.

        :param value_id: The unique identifier of the value whose changes
            should or should not be verified.
        :type value_id: int

        :param verify: if `True`, verify changes,
            if `False`, don't verify changes
        :type verify: bool

        :rtype: bool
        """

        if _values_map.find(value_id) != _values_map.end():
            self.manager.SetChangeVerified(_values_map.at(value_id), verify)

    # -------------------------------------------------------------------------
    # Climate Control Schedules
    # -------------------------------------------------------------------------
    # Methods for accessing schedule values. All the methods require a
    # ValueID, which will have been provided in the ValueAdded
    # Notification callback when the the value was first discovered by
    # OpenZWave. The ValueType_Schedule is a specialized Value used to
    # simplify access to the switch point schedule information held by a
    # setback thermostat that supports the Climate Control Schedule
    # command class. Each schedule contains up to nine switch points for a
    # single day, consisting of a time in hours and minutes
    # (24 hour clock) and a setback in tenths of a degree Celsius. The
    # setback value can range from -128 (-12.8C) to 120 (12.0C).
    # There are two special setback values - 121 is used to set Frost
    # Protection mode, and 122 is used to set Energy Saving mode. The
    # switch point methods only modify OpenZWave's copy of the schedule
    # information. Once all changes have been made, they are sent to the
    # device by calling SetSchedule.
    #
    def setSwitchPoint(self, value_id, hours, minutes, setback):
        """
        Set a switch point in the schedule.

        :param value_id: The unique identifier of the schedule value.
        :type value_id: int

        :param hours: The hours part of the time when the switch point
            will trigger. The time is set using the 24-hour clock, so this
            value must be between 0 and 23.
        :type hours: int

        :param minutes: The minutes part of the time when the switch point
            will trigger. This value must be between 0 and 59.
        :type minutes: int

        :param setback: The setback in tenths of a degree Celsius. The
            setback value can range from -128 (-12.8C) to 120 (12.0C).
            There are two special setback values - 121 is used to set Frost
            Protection mode, and 122 is used to set Energy Saving mode.
        :type setback: int

        :return: `True` if the switch point is set.
        :rtype: bool
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.SetSwitchPoint(
                _values_map.at(value_id),
                hours,
                minutes,
                setback
            )
        else :
            return False

    def removeSwitchPoint(self, value_id, hours, minutes):
        """
        Remove a switch point from the schedule

        :param value_id: The unique identifier of the schedule value.
        :type value_id: int

        :param hours: The hours part of the time when the switch
            point will trigger. The time is set using the 24-hour clock,
            so this value must be between 0 and 23.
        :type hours: int

        :param minutes: The minutes part of the time when the switch
            point will trigger. This value must be between 0 and 59.
        :type minutes: int

        :return: `True` if the switch point is removed.
        :rtype: bool
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.RemoveSwitchPoint(
                _values_map.at(value_id),
                hours,
                minutes
            )
        else:
            return False

    def clearSwitchPoints(self, value_id):
        """
        Clears all switch points from the schedule

        :param value_id: The unique identifier of the schedule value.
        :type value_id: int

        :return: `True` if all switch points are clear.
        :rtype: bool
        """
        if _values_map.find(value_id) != _values_map.end():
            self.manager.ClearSwitchPoints(_values_map.at(value_id))

    def getSwitchPoint(self, value_id, idx):
        """
        Gets switch point data from the schedule

        :param value_id: The unique identifier of the schedule value.
        :type value_id: int

        :param idx: The index of the switch point, between zero and one
            less than the value returned by GetNumSwitchPoints.
        :type idx: int

        :return: tuple containing (hours, minutes, setback) or `None` if no
            data found

            * house: An integer that will be filled with the hours part
              of the switch point data.
            * minutes: An integer that will be filled with the minutes
              part of the switch point data.
            * setback: An integer that will be filled with the setback
              value. This can range from -128 (-12.8C)to 120 (12.0C). There
              are two special setback values - 121 is used to set Frost
              Protection mode, and 122 is used to set Energy Saving mode.

        :rtype: tuple, optional
        """
        cdef uint8_t ohours
        cdef uint8_t ominutes
        cdef int8_t osetback

        if _values_map.find(value_id) != _values_map.end():
            ret = self.manager.GetSwitchPoint(
                _values_map.at(value_id),
                idx,
                &ohours,
                &ominutes,
                &osetback
            )

            if ret :
                return ohours, ominutes, osetback

    def getNumSwitchPoints(self, value_id):
        """
        Get the number of switch points defined in a schedule

        :param value_id: The unique identifier of the schedule value.
        :type value_id: int

        :return: The number of switch points defined in this schedule.
            Returns zero if the value is not a ValueID::ValueType_Schedule.
            The type can be tested with a call to ValueID::GetType.
        :rtype: int
        """
        if _values_map.find(value_id) != _values_map.end():
            return self.manager.GetNumSwitchPoints(_values_map.at(value_id))
        else :
            return 0

    # -------------------------------------------------------------------------
    # SwitchAll
    # -------------------------------------------------------------------------
    # Methods for switching all devices on or off together. The devices
    # must support the SwitchAll command class. The command is first
    # broadcast to all nodes, and then followed up with individual
    # commands to each node (because broadcasts are not routed, the
    # message might not otherwise reach all the nodes).
    #
    def switchAllOn(self, home_id):
        """
        Switch all devices on.

        All devices that support the SwitchAll command class will be
        turned on.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int
        
        :rtype: None
        """
        self.manager.SwitchAllOn(home_id)

    def switchAllOff(self, home_id):
        """
        Switch all devices off.

        All devices that support the SwitchAll command class will be
        turned off.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int
        
        :rtype: None
        """
        self.manager.SwitchAllOff(home_id)

    # -------------------------------------------------------------------------
    # Configuration Parameters
    # -------------------------------------------------------------------------
    # Methods for accessing device configuration parameters. Configuration
    # parameters are values that are managed by the Configuration command
    # class. The values are device-specific and are not reported by the
    # devices. Information on parameters is provided only in the device
    # user manual.
    #
    # An ongoing task for the OpenZWave project is to create XML files
    # describing the available parameters for every Z-Wave.
    #
    # See the config folder in the project source code for examples.
    #
    def setConfigParam(self, home_id, node_id, param, value, size=2):
        """
        Set the value of a configurable parameter in a device.

        Some devices have various parameters that can be configured to
        control the device behaviour. These are not reported by the device
        over the Z-Wave network but can usually be found in the devices
        user manual. This method returns immediately, without waiting for
        confirmation from the device that the change has been made.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to configure.
        :type node_id: int

        :param param: The index of the parameter.
        :type param: int

        :param value: The value to which the parameter should be set.
        :type value: int

        :param size: Is an optional number of bytes to be sent for the
            parameter value. (default = `2`).
        :type size: int, optional

        :return: True if the message setting the value was sent to
            the device.
        :rtype: bool
        """
        return self.manager.SetConfigParam(
            home_id,
            node_id,
            param,
            value,
            size
        )

    def requestConfigParam(self, home_id, node_id, param):
        """
        Request the value of a configurable parameter from a device.

        Some devices have various parameters that can be configured to
        control the device behaviour. These are not reported by the device
        over the Z-Wave network but can usually be found in the devices
        user manual.

        This method requests the value of a parameter from the device, and
        then returns immediately, without waiting for a response. If the
        parameter index is valid for this device, and the device is awake,
        the value will eventually be reported via a ValueChanged
        notification callback. The ValueID reported in the callback will
        have an index set the same as _param and a command class set to
        the same value as returned by a call to
        Configuration::StaticGetCommandClassId.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to configure.
        :type node_id: int

        :param param: The index of the parameter.
        :type param: int
        
        :rtype: None
        """
        self.manager.RequestConfigParam(home_id, node_id, param)

    def requestAllConfigParams(self, home_id, node_id):
        """
        Request the values of all known configurable parameters
        from a device.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to configure.
        :type node_id: int
        
        :rtype: None
        """
        self.manager.RequestAllConfigParams(home_id, node_id)

    # -------------------------------------------------------------------------
    # Groups (wrappers for the Node methods)
    # -------------------------------------------------------------------------
    # Methods for accessing device association groups.
    #

    def isMultiInstance(self, home_id, node_id, group_idx):
        """
        Get whether the group supports MultiInstance Associations

        :param home_id: The Home ID of the Z-Wave controller that manages
            the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :param group_idx: the index of the group
        :type group_idx: int

        :return: True if the node supports MultiInstance Associations
        :rtype: bool
        """
        return self.manager.IsMultiInstance(home_id, node_id, group_idx)

    def getNumGroups(self, home_id, node_id):
        """
        Gets the number of association groups reported by this node

        In Z-Wave, groups are numbered starting from one. For example,
        if a call to GetNumGroups returns 4, the _groupIdx value to use in
        calls to GetAssociations AddAssociation and RemoveAssociation will
        be a number between 1 and 4.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node whose groups
            we are interested in.
        :type node_id: int

        :return: The number of groups.
        :rtype: int
        """
        return self.manager.GetNumGroups(home_id, node_id)

    def getAssociations(self, home_id, node_id, group_idx):
        """
        Gets the associations for a group

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node whose associations
            we are interested in.
        :type node_id: int

        :param group_idx: one-based index of the group
            (because Z-Wave product manuals use one-based group numbering).
        :type group_idx: int

        :return: A list containing IDs of members of the group
        :rtype: set
        """
        return list(
            x.node_id for x in
            self.getAssociationsInstances(home_id, node_id, group_idx)
            if x.instance == 0x00
        )

    def getAssociationsInstances(self, home_id, node_id, group_idx):
        """
        Gets the associationsInstances for a group

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node whose associations
            we are interested in.
        :type node_id: int

        :param group_idx: one-based index of the group
            (because Z-Wave product manuals use one-based group numbering).
        :type group_idx: int

        :return: A list containing tuples containing the
            node_id and the instance
        :rtype: list
        """
        data = set()
        cdef uint32_t size = self.manager.GetMaxAssociations(home_id, node_id, group_idx)
        #Allocate memory
        cdef struct_associations dbuf = <struct_associations>malloc(sizeof(InstanceAssociation_t) * size)
        # return value is pointer to uint8_t[]
        cdef uint32_t count = self.manager.GetAssociations(home_id, node_id, group_idx, dbuf)
        if count == 0:
            #Don't need to allocate memory.
            free(dbuf)
            return data
        cdef _InstanceAssociationAlloc retassinst = _InstanceAssociationAlloc(count)
        cdef InstanceAssociation_t* p
        cdef uint32_t start = 0
        if count:
            try:
                p = dbuf[0] # p is now pointing at first element of array
                for i in range(start, count):
                    retassinst.data[2*i] = p[0].m_nodeId
                    retassinst.data[2*i+1] = p[0].m_instance
                    data.add((retassinst.data[2*i],retassinst.data[2*i+1]))
                    p += 1
            finally:
                # Free memory
                free(dbuf)
                pass

        res = []
        for item in data:
            assoc = PyInstanceAssociation()
            assoc.node_id = item[0]
            assoc.instance = item[1]
            res += [assoc]

        return res

    def getMaxAssociations(self, home_id, node_id, group_idx):
        """
        Gets the maximum number of associations for a group.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node whose associations
            we are interested in.
        :type node_id: int

        :param group_idx: One-based index of the group
            (because Z-Wave product manuals use one-based group numbering).
        :type group_idx: int

        :return: The maximum number of nodes that can be
            associated into the group.
        :rtype: int
        """
        return self.manager.GetMaxAssociations(home_id, node_id, group_idx)

    def getGroupLabel(self, home_id, node_id, group_idx):
        """
        Returns a label for the particular group of a node.

        This label is populated by the device specific configuration files.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node whose associations
            are to be changed.
        :type node_id: int

        :param group_idx: One-based index of the group
            (because Z-Wave product manuals use one-based group numbering).
        :type group_idx: int

        :return: The label for the particular group of a node.
        :rtype: str
        """
        cdef string c_string = self.manager.GetGroupLabel(
            home_id,
            node_id,
            group_idx
        )
        return _str(c_string.c_str())

    def addAssociation(
        self,
        home_id,
        node_id,
        group_idx,
        target_node_id,
        instance=0x00
    ):
        """
        Adds a node to an association group.

        Due to the possibility of a device being asleep, the command is
        assumed to succeed, and the association data held in this class is
        updated directly. This will be reverted by a future Association
        message from the device if the Z-Wave message actually failed to
        get through. Notification callbacks will be sent in both cases.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node whose associations
            are to be changed.
        :type node_id: int

        :param group_idx: One-based index of the group
            (because Z-Wave product manuals use one-based group numbering).
        :type group_idx: int

        :param target_node_id: Identifier for the node that will be added
            to the association group.
        :type target_node_id: int

        :param instance: Identifier for the instance that will be
            added to the association group. (default = `0x00`)
        :type instance: int, optional
        
        :rtype: bool
        """
        try:
            self.manager.AddAssociation(
                home_id,
                node_id,
                group_idx,
                target_node_id,
                instance
            )
            return True
        except:
            return False

    def removeAssociation(
        self,
        home_id,
        node_id,
        group_idx,
        target_node_id,
        instance=0x00
    ):
        """
        Removes a node from an association group.

        Due to the possibility of a device being asleep, the command is
        assumed to succeed, and the association data held in this class is
        updated directly. This will be reverted by a future Association
        message from the device if the Z-Wave message actually failed to
        get through. Notification callbacks will be sent in both cases.

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node whose associations
            are to be changed.
        :type node_id: int

        :param group_idx: One-based index of the group
            (because Z-Wave product manuals use one-based group numbering).
        :type group_idx: int

        :param target_node_id: Identifier for the node that will be
            removed from the association group.
        :type target_node_id: int

        :param instance: Identifier for the instance that will be added
            to the association group. (default = `0x00`)
        :type instance: int, optional
        
        :rtype: bool
        """

        try:
            self.manager.RemoveAssociation(
                home_id,
                node_id,
                group_idx,
                target_node_id,
                instance
            )
            return True
        except:
            return False


    # -------------------------------------------------------------------------
    # Notifications
    # -------------------------------------------------------------------------
    # For notification of changes to the Z-Wave network or
    # device values and associations.
    #
    def addWatcher(self, python_func):
        """
        Add a notification watcher.

        In OpenZWave, all feedback from the Z-Wave network is sent to the
        application via callbacks.  This method allows the application to
        add a notification callback handler, known as a "watcher" to
        OpenZWave. An application needs only add a single watcher - all
        notifications will be reported to it.

        :param python_func: Watcher pointer to a function that will be
            called by the notification system.
        :type python_func: callable
        
        :rtype: None
        """
        self._watcherCallback = python_func # need to keep a reference to this
        if not self.manager.AddWatcher(_notif_callback, <void*>python_func):
            raise ValueError("call to AddWatcher failed")

    def removeWatcher(self, python_func):
        """
        Remove a notification watcher.

        :param python_func: Watcher pointer to a function
        :type python_func: callable
        
        :rtype: None
        """
        if not self.manager.RemoveWatcher(
            _notif_callback,
            <void*>self._watcherCallback
        ):
            raise ValueError("call to RemoveWatcher failed")
        else:
            self._watcherCallback = None

    # -------------------------------------------------------------------------
    # Controller commands
    # -------------------------------------------------------------------------
    # Commands for Z-Wave network management using the PC Controller.
    #
    def resetController(self, home_id):
        """
        Hard Reset a PC Z-Wave Controller.

        Resets a controller and erases its network configuration settings.
        The controller becomes a primary controller ready to add devices
        to a new network.

        :param home_id: The Home ID of the Z-Wave controller to be reset.
        :type home_id: int
        
        :rtype: None
        """
        _values_map.clear()
        self.manager.ResetController(home_id)

    def softResetController(self, home_id):
        """
        Soft Reset a PC Z-Wave Controller.

        Resets a controller without erasing its network
        configuration settings.

        :param home_id: The Home ID of the Z-Wave controller to be reset.
        :type home_id: int
        
        :rtype: None
        """
        self.manager.SoftReset(home_id)

    def cancelControllerCommand(self, home_id):
        """
        Cancels any in-progress command running on a controller.

        :param home_id: The Home ID of the Z-Wave controller.
        :type home_id: int

        :return: True if a command was running and was cancelled.
        :rtype: bool
        """
        return self.manager.CancelControllerCommand(home_id)

    def createNewPrimary(self, home_id):
        """
        Create a new primary controller when old primary fails.
        Requires SUC.

        This command Creates a new Primary Controller when the Old
        Primary has Failed. Requires a SUC on the network to function.

        Results of the CreateNewPrimary Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.CreateNewPrimary(home_id)

    def transferPrimaryRole(self, home_id):
        """
        Add a new controller to the network and make it the primary.

        The existing primary will become a secondary controller.

        Results of the TransferPrimaryRole Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.TransferPrimaryRole(home_id)

    def receiveConfiguration(self, home_id):
        """
        Receive network configuration information from primary controller.
        Requires secondary.

        This command prepares the controller to receive Network
        Configuration from a Secondary Controller.

        Results of the ReceiveConfiguration Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.ReceiveConfiguration(home_id)

    def addNode(self, home_id, do_decurity):
        """
        Start the Inclusion Process to add a Node to the Network.

        The Status of the Node Inclusion is communicated via Notifications.
        Specifically, you should monitor ControllerCommand Notifications.

        Results of the AddNode Command will be send as a Notification
        with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param do_decurity: Whether to initialize the Network Key on
            the device if it supports the Security CC
        :type do_decurity: bool

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.AddNode(home_id, do_decurity)

    def removeNode(self, home_id, failed_node_id=None):
        """
        Remove a a nmode or a failed node(if specified from the Z-Wave Network

        The Status of the Node Removal is communicated via Notifications.
        Specifically, you should monitor ControllerCommand Notifications.

        Results of the RemoveNode Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        Results of the RemoveFailedNode Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param failed_node_id: The ID of the node that is marked as failed.
        :type failed_node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """

        if failed_node_id is None:
            return self.manager.RemoveNode(home_id)
        else:
            return self.manager.RemoveFailedNode(home_id, failed_node_id)

    def hasNodeFailed(self, home_id, node_id):
        """
        Ask a Node to update its Neighbor Tables

        This command will ask a Node to update its Neighbor Tables.

        Results of the HasNodeFailed Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.HasNodeFailed(home_id, node_id)

    def requestNodeNeighborUpdate(self, home_id, node_id):
        """
        Ask a Node to update its Neighbor Tables

        This command will ask a Node to update its Neighbor Tables.

        Results of the RequestNodeNeighborUpdate Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.RequestNodeNeighborUpdate(home_id, node_id)

    def assignReturnRoute(self, home_id, node_id):
        """
        Ask a Node to update its update its Return Route to the Controller

        This command will ask a Node to update its Return Route to
        the Controller

        Results of the AssignReturnRoute Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.AssignReturnRoute(home_id, node_id)

    def deleteAllReturnRoutes(self, home_id, node_id):
        """
        Ask a Node to delete all Return Route.

        This command will ask a Node to delete all its return routes,
        and will rediscover when needed.

        Results of the DeleteAllReturnRoutes Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.DeleteAllReturnRoutes(home_id, node_id)

    def sendNodeInformation(self, home_id, node_id):
        """
        Create a new primary controller when old primary fails.
        Requires SUC.

        This command Creates a new Primary Controller when the Old Primary
        has Failed. Requires a SUC on the network to function

        Results of the SendNodeInformation Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.SendNodeInformation(home_id, node_id)

    def replaceFailedNode(self, home_id, node_id):
        """
        Replace a failed device with another.

        If the node is not in the controller's failed nodes list, or the
        node responds, this command will fail.

        You can check if a Node is in the Controllers Failed node list by
        using the HasNodeFailed method.

        Results of the ReplaceFailedNode Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.ReplaceFailedNode(home_id, node_id)

    def requestNetworkUpdate(self, home_id, node_id):
        """
        Update the controller with network information from the SUC/SIS.

        Results of the RequestNetworkUpdate Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.RequestNetworkUpdate(home_id, node_id)

    def replicationSend(self, home_id, node_id):
        """
        Send replication command

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.ReplicationSend(home_id, node_id)

    def createButton(self, home_id, node_id, button_id):
        """
        Create a handheld button id.

        Only intended for Bridge Firmware Controllers.

        Results of the CreateButton Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller
            that manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :param button_id: the ID of the Button to query.
        :type button_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.CreateButton(home_id, node_id, button_id)

    def deleteButton(self, home_id, node_id, button_id):
        """
        Delete a handheld button id.

        Only intended for Bridge Firmware Controllers.

        Results of the CreateButton Command will be send as a Notification
        with the Notification type as
        Notification::Type_ControllerCommand

        :param home_id: The Home ID of the Z-Wave controller that
            manages the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :param button_id: the ID of the Button to query.
        :type button_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.DeleteButton(home_id, node_id, button_id)

#-----------------------------------------------------------------------------
# Device file updating
#-----------------------------------------------------------------------------

    def checkLatestConfigFileRevision(self, home_id, node_id):
        """
        Check the Latest Revision of the Config File for this device.

        Optionally update the local database with the latest version Config
        Revisions are exposed on the ManufacturerSpecific CC.
        (both the latest and loaded version)
        Outdated Config Revisions are signaled via Notifications

        :param home_id: The Home ID of the Z-Wave controller that manages the
            node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.checkLatestConfigFileRevision(home_id, node_id)

    def checkLatestMFSRevision(self, home_id):
        """
        Check the Latest Revision of the Manufacturer_Specific.xml file.

        Optionally update to the latest version.
        Outdated Config Revisions are signaled via Notifications

        :param home_id: The Home ID of the Z-Wave controller that manages the
            node.
        :type home_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.checkLatestMFSRevision(home_id)

    def downloadLatestConfigFileRevision(self, home_id, node_id):
        """
        Download the latest Config File Revision.
        The Node will be reloaded depending upon the Option "ReloadAfterUpdate"

        Valid Options include:

            * `"Never"`: Never Reload a Node after updating the Config File.
              Manual Reload is Required.
            * `"Immediate"`: Reload the Node Immediately after downloading the
              latest revision
            * `"Awake"`: Reload Nodes only when they are awake (Always-On
              Nodes will reload immediately, Sleeping Nodes will reload when
              they wake up

            Errors are signaled via Notifications

        :param home_id: The Home ID of the Z-Wave controller that manages the
            node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.downloadLatestConfigFileRevision(home_id, node_id)

    def downloadLatestMFSRevision(self, home_id):
        """
        Download the latest Config File Revision.

        The ManufacturerSpecific File will be updated, and any new Config
        Files will also be downloaded. Existing Config Files will not be
        checked/updated.

        Errors are signaled via Notifications

        :param home_id: The Home ID of the Z-Wave controller that manages the
            node.
        :type home_id: int

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.downloadLatestMFSRevision(home_id)

#-----------------------------------------------------------------------------
# Node metadata
#-----------------------------------------------------------------------------

    def getChangeLog(self, home_id, node_id, revision):
        """
        Gets a nodes changlog information

        :param home_id: The Home ID of the Z-Wave controller that manages the
            node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :param revision: revision of the change log to get
        :type revision: int

        :return: dict
        :rtype: dict
        """
        return self.manager.GetChangeLog(home_id, node_id, revision)

    def getMetaData(self, home_id, node_id, metadata):
        """
        Gets a metadata item for a node

        :param home_id: The Home ID of the Z-Wave controller that manages
            the node.
        :type home_id: int

        :param node_id: The ID of the node to query.
        :type node_id: int

        :param metadata:

            Can be one of the following:

                * `0`: OZW Info page URL
                * `1`: OZW Product page URL
                * `2`: Product picture
                * `3`: Product description
                * `4`: Product manual URL
                * `5`: Product page URL
                * `6`: Inclusion help
                * `7`: Exclusion help
                * `8`: Reset help
                * `9`: Wakeup help
                * `10`: Product support URL
                * `11`: Device frequency
                * `12`: Name
                * `13`: Identifier

        :type metadata: int

        :return: meta data item
        :rtype: str
        """
        return self.manager.GetMetaData(home_id, node_id, metadata)

#-----------------------------------------------------------------------------
# Value instance labels
#-----------------------------------------------------------------------------

    def getInstanceLabel(self, value_id):
        """
        Gets the value instance label

        :param value_id: The ValueId for the instance you want to get the
            label for.
        :type value_id: int
        
        :rtype: str
        """
        cdef string s
        if _values_map.find(value_id) != _values_map.end():
            s = self.manager.GetInstanceLabel(_values_map.at(value_id))
        return _str(s.c_str())

#-----------------------------------------------------------------------------
# Send Raw Data
#-----------------------------------------------------------------------------

    def sendRawData(self, home_id, node_id, log_text, msg_type, send_secure, content, length):
        """
        Send Raw Data

        :param home_id:
        :type home_id: int

        :param node_id:
        :type node_id: int

        :param log_text:
        :type log_text: str

        :param msg_type:
        :type msg_type: int

        :param send_secure:
        :type send_secure: bool

        :param content:
        :type content: str

        :param length:
        :type length: int
        
        :rtype: None
        """

        cdef string l_text = log_text
        cdef uint8_t cont = content
        cdef bool_t secure = send_secure
        cdef uint8_t leng = length
        cdef uint8_t m_type = msg_type

        self.manager.SendRawData(
            home_id,
            node_id,
            l_text,
            msg_type,
            secure,
            &cont,
            leng
        )
