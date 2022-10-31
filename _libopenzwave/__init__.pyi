# encoding: utf-8
# module _libopenzwave
# from C:\Python310\lib\site-packages\libopenzwave-0.5.0-py3.10-win-amd64.egg\_libopenzwave.pyd
# by generator 1.147
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

# imports
import logging as logging
from typing import Union, Optional, List
# Variables with simple values

CWD_CONFIG_DIRECTORY: str

libopenzwave_file: str
libopenzwave_location: str

OZWAVE_CONFIG_DIRECTORY: str

PYLIBRARY: str
PY_OZWAVE_CONFIG_DIRECTORY: str

__version__: str


def _configPath() -> Union[str, None]:  # real signature unknown
    """
    Retrieve the config path. This directory hold the xml files.

        :return: A string containing the library config path or None.
        :rtype: str, None
    """
    pass


# classes

class CommandClassData(object):
    """
    Command Class Data

        Attributes:

        * `commandClassId`: Num type of CommandClass id.
        * `sentCnt`: Number of messages sent from this CommandClass.
        * `receivedCnt`: Number of messages received from this CommandClass
    """

    commandClassId: int
    receivedCnt: int
    sentCnt: int


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

    ACKCnt: int
    ACKWaiting: int
    badChecksum: int
    badroutes: int
    broadcastReadCnt: int
    broadcastWriteCnt: int
    callbacks: int
    CANCnt: int
    dropped: int
    NAKCnt: int
    netbusy: int
    noack: int
    nondelivery: int
    OOFCnt: int
    readAborts: int
    readCnt: int
    retries: int
    routedbusy: int
    SOFCnt: int
    writeCnt: int


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

    def index(self, key: str):  # real signature unknown
        """
        :param key:
        :type key: str
        """
        pass

    def __getattr__(self, item: str):  # real signature unknown
        """
        :param item:
        :type item: str
        """
        pass

    def __getitem__(self, item: Union[int, str]):  # real signature unknown
        """
        :param item:
        :type item: int, str
        """
        pass

    def __init__(self, **kwargs):  # real signature unknown
        """
        :param **kwargs:
        """
        pass

    def __iter__(self):  # real signature unknown
        pass


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

    def set(self, idx: int, doc: str, type_: Optional[int] = None, value: Optional[str] = None) -> EnumItem:  # real signature unknown
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
        pass

    def __call__(self, cls, value):  # real signature unknown
        """
        :param cls:
        :param value:
        """
        pass

    def __int__(self) -> int:  # real signature unknown
        pass

    @classmethod  # known case of __new__
    def __new__(cls, *args, **kwargs):  # real signature unknown
        """
        :param *args:
        :param **kwargs:
        """
        pass

    @property
    def value(self) -> Union[int, str]:
        """
        :rtype: int, str
        """

    doc: str
    idx: int
    type = None
    _value: Union[int, str]


class LibZWaveException(Exception):
    """ Exception class for LibOpenZWave """

    def __init__(self, value):  # real signature unknown
        """
        :param value:
        """
        pass

    def __str__(self) -> str:  # real signature unknown
        pass



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

    ackChannel: int
    averageRequestRTT: int
    averageResponseRTT: int
    ccData: List[CommandClassData]
    hops: int
    lastFailedLinkFrom: int
    lastFailedLinkTo: int
    lastReceivedMessage: List[int]
    lastRequestRTT: int
    lastResponseRTT: int
    lastTxChannel: int
    quality: int
    receivedCnt: int
    receivedDups: int
    receivedTS: str
    receivedUnsolicited: int
    retries: int
    routeScheme: int
    routeSpeed: int
    routeTries: int
    routeUsed: int
    rssi_1: str
    rssi_2: str
    rssi_3: str
    rssi_4: str
    rssi_5: str
    sentCnt: int
    sentFailed: int
    sentTS: str
    txStatusReportSupported: bool
    txTime: int


class NotificationEnum(Enum):
    # no doc
    def __init__(self, **kwargs):  # real signature unknown
        """
        :param **kwargs:
        """
        pass


class NotificationItem(EnumItem):
    # no doc
    def __eq__(self, other: Union[int, str]) -> bool:  # real signature unknown
        """
        :param other:
        :type other: int, str

        :rtype: bool
        """
        pass

    def __hash__(self) -> hash:  # real signature unknown
        """ :rtype: hash """
        pass


    def __int__(self) -> int:  # real signature unknown
        """ :rtype: int """
        pass

    def __ne__(self, other: Union[int, str]) -> bool:  # real signature unknown
        """
        :param other:
        :type other: int, str

        :rtype: bool
        """
        pass

    _handler = None


class PyInstanceAssociation(object):
    # no doc
    def __eq__(self, *args, **kwargs):  # real signature unknown
        pass

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

    def __ne__(self, *args, **kwargs):  # real signature unknown
        pass

    instance: int
    node_id: int


class PyManager(object):
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

    def addAssociation(self, *args, **kwargs):  # real signature unknown
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
        pass

    def addDriver(self, *args, **kwargs):  # real signature unknown
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
                    On Windows this might be something like "\.\COM3",
                    or on Linux "/dev/ttyUSB0".
                :type serial_port: str

                :return: True if a new driver was created
                :rtype: bool
        """
        pass

    def addNode(self, *args, **kwargs):  # real signature unknown
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
        pass

    def addWatcher(self, *args, **kwargs):  # real signature unknown
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
        pass

    def assignReturnRoute(self, *args, **kwargs):  # real signature unknown
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
        pass

    def cancelControllerCommand(self, *args,
                                **kwargs):  # real signature unknown
        """
        Cancels any in-progress command running on a controller.

                :param home_id: The Home ID of the Z-Wave controller.
                :type home_id: int

                :return: True if a command was running and was cancelled.
                :rtype: bool
        """
        pass

    def checkLatestConfigFileRevision(self, *args,
                                      **kwargs):  # real signature unknown
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
        pass

    def checkLatestMFSRevision(self, *args, **kwargs):  # real signature unknown
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
        pass

    def clearSwitchPoints(self, *args, **kwargs):  # real signature unknown
        """
        Clears all switch points from the schedule

                :param value_id: The unique identifier of the schedule value.
                :type value_id: int

                :return: `True` if all switch points are clear.
                :rtype: bool
        """
        pass

    def create(self, *args, **kwargs):  # real signature unknown
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
        pass

    def createButton(self, *args, **kwargs):  # real signature unknown
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
        pass

    def createNewPrimary(self, *args, **kwargs):  # real signature unknown
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
        pass

    def deleteAllReturnRoutes(self, *args, **kwargs):  # real signature unknown
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
        pass

    def deleteButton(self, *args, **kwargs):  # real signature unknown
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
        pass

    def destroy(self, *args, **kwargs):  # real signature unknown
        """
        Deletes the Manager and cleans up any associated objects.

                :rtype: None
        """
        pass

    def disablePoll(self, *args, **kwargs):  # real signature unknown
        """
        Disable polling of a value.

                :param value_id: The ID of the value to disable polling.
                :type value_id: int

                :return: True if polling was disabled.
                :rtype: bool
        """
        pass

    def downloadLatestConfigFileRevision(self, *args,
                                         **kwargs):  # real signature unknown
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
        pass

    def downloadLatestMFSRevision(self, *args,
                                  **kwargs):  # real signature unknown
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
        pass

    def enablePoll(self, *args, **kwargs):  # real signature unknown
        """
        Enable the polling of a device's state.

                :param value_id: The ID of the value to start polling
                :type value_id: int

                :param intensity: The intensity of the poll (default = 1)
                :type intensity: int, optional

                :return: True if polling was enabled.
                :rtype: bool
        """
        pass

    def getAssociations(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getAssociationsInstances(self, *args,
                                 **kwargs):  # real signature unknown
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
        pass

    def getChangeLog(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getChangeVerified(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getControllerInterfaceType(self, *args,
                                   **kwargs):  # real signature unknown
        """
        Retrieve controller interface type, Unknown, Serial, Hid

                :param home_id: The Home ID of the Z-Wave controller.
                :type home_id: int

                :return: The controller interface type
                :rtype: str
        """
        pass

    def getControllerNodeId(self, *args, **kwargs):  # real signature unknown
        """
        Get the node ID of the Z-Wave controller.

                :param home_id: The Home ID of the Z-Wave controller.
                :type home_id: int

                :return: The node ID of the Z-Wave controller
                :rtype: int
        """
        pass

    def getControllerPath(self, *args, **kwargs):  # real signature unknown
        """
        Retrieve controller interface path, name or path used to
                open the controller hardware

                :param home_id: The Home ID of the Z-Wave controller.
                :type home_id: int

                :return: The controller interface type
                :rtype: str
        """
        pass

    def getDriverStatistics(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getGroupLabel(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getInstanceLabel(self, *args, **kwargs):  # real signature unknown
        """
        Gets the value instance label

                :param value_id: The ValueId for the instance you want to get the
                    label for.
                :type value_id: int

                :rtype: str
        """
        pass

    def getLibraryTypeName(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getLibraryVersion(self, *args, **kwargs):  # real signature unknown
        """
        Get the version of the Z-Wave API library used by a controller.

                :param home_id: The Home ID of the Z-Wave controller.
                :type home_id: int

                :return: A string containing the library version. For example,
                    `"Z-Wave 2.48"`.
                :rtype: str
        """
        pass

    def getMaxAssociations(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getMetaData(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeBasic(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeClassInformation(self, *args,
                                **kwargs):  # real signature unknown
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
        pass

    def getNodeDeviceType(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeDeviceTypeString(self, *args,
                                **kwargs):  # real signature unknown
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
        pass

    def getNodeGeneric(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeLocation(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeManufacturerId(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeManufacturerName(self, *args,
                                **kwargs):  # real signature unknown
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
        pass

    def getNodeMaxBaudRate(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeName(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeNeighbors(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodePlusType(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodePlusTypeString(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeProductId(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeProductName(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeProductType(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeQueryStage(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeQueryStageCode(self, *args, **kwargs):  # real signature unknown
        """
        Get code value from a query stage description

                :param query_stage: The query stage description.
                :type query_stage: str

                :return: code value.
                :rtype: int, optional
        """
        pass

    def getNodeRole(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeRoleString(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeSecurity(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeSpecific(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeStatistics(self, *args, **kwargs):  # real signature unknown
        """
        Retrieve statistics per node

                :param home_id: The Home ID of the Z-Wave controller.
                :type home_id: int

                :param node_id: The ID of the node to query.
                :type node_id: int

                :return: A class object containing statistics.
                :rtype: NodeStats
        """
        pass

    def getNodeType(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNodeVersion(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNumGroups(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getNumSwitchPoints(self, *args, **kwargs):  # real signature unknown
        """
        Get the number of switch points defined in a schedule

                :param value_id: The unique identifier of the schedule value.
                :type value_id: int

                :return: The number of switch points defined in this schedule.
                    Returns zero if the value is not a ValueID::ValueType_Schedule.
                    The type can be tested with a call to ValueID::GetType.
                :rtype: int
        """
        pass

    def getOzwLibraryLongVersion(self, *args,
                                 **kwargs):  # real signature unknown
        """
        Get a string containing the openzwave library version.

                :return: A string containing the library type.
                :rtype: str
        """
        pass

    def getOzwLibraryVersion(self, *args, **kwargs):  # real signature unknown
        """
        Get a string containing the openzwave library version.

                :return: A string containing the library type.
                :rtype: str
        """
        pass

    def getOzwLibraryVersionNumber(self, *args,
                                   **kwargs):  # real signature unknown
        """
        Get the openzwave library version number.

                :return: A string containing the library type.
                :rtype: str
        """
        pass

    def getPollIntensity(self, *args, **kwargs):  # real signature unknown
        """
        Get the intensity with which this value is polled
                (0=none, 1=every time through the list, 2-every other time, etc).

                :param value_id: The ID of a value.
                :type value_id: int

                :return: A integer containing the poll intensity
                :rtype: int
        """
        pass

    def getPollInterval(self, *args, **kwargs):  # real signature unknown
        """
        Get the time period between polls of a nodes state

                :return: The number of milliseconds between polls
                :rtype: int
        """
        pass

    def getPythonLibraryFlavor(self, *args, **kwargs):  # real signature unknown
        """
        Get the flavor of the python library.

                :return: A string containing the python library flavor.
                    For example, `"embed"`.
                :rtype: str
        """
        pass

    def getPythonLibraryVersion(self, *args,
                                **kwargs):  # real signature unknown
        """
        Get the version of the python library.

                :return: A string containing the python library version.
                    For example, `"libopenzwave version 0.1"`.
                :rtype: str
        """
        pass

    def getPythonLibraryVersionNumber(self, *args,
                                      **kwargs):  # real signature unknown
        """
        Get the python library version number

                :return: A string containing the python library version.
                    For example, `"0.1"`.
                :rtype: str
        """
        pass

    def getSendQueueCount(self, *args, **kwargs):  # real signature unknown
        """
        Get count of messages in the outgoing send queue.

                :param home_id: The Home ID of the Z-Wave controller.
                :type home_id: int

                :return: Message count
                :rtype: int
        """
        pass

    def getSUCNodeId(self, *args, **kwargs):  # real signature unknown
        """
        Get the node ID of the Static Update Controller.

                :param home_id: The Home ID of the Z-Wave controller.
                :type home_id: int

                :return: the node ID of the Z-Wave controller.
                :rtype: int
        """
        pass

    def getSwitchPoint(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getValue(self, *args, **kwargs):  # real signature unknown
        """
        Gets a value.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: Depending of the type of the valueId, None otherwise
                :rtype: int, str, float, bool
        """
        pass

    def getValueAsBitSet(self, *args, **kwargs):  # real signature unknown
        """
        Gets a value as a bool.

                :param value_id: The ID of a value.
                :type value_id: int

                :param pos: The position of the bit to get LSB first
                :type pos: int

                :return: The value
                :rtype: bool
        """
        pass

    def getValueAsBool(self, *args, **kwargs):  # real signature unknown
        """
        Gets a value as a bool.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The value
                :rtype: bool
        """
        pass

    def getValueAsByte(self, *args, **kwargs):  # real signature unknown
        """
        Gets a value as an 8-bit unsigned integer.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The value
                :rtype: int
        """
        pass

    def getValueAsFloat(self, *args, **kwargs):  # real signature unknown
        """
        Gets a value as a float.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The value
                :rtype: float
        """
        pass

    def getValueAsInt(self, *args, **kwargs):  # real signature unknown
        """
        Gets a value as a 32-bit signed integer.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The value
                :rtype: int
        """
        pass

    def getValueAsRaw(self, *args, **kwargs):  # real signature unknown
        """
        Gets a value as raw.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The value
                :rtype: str
        """
        pass

    def getValueAsShort(self, *args, **kwargs):  # real signature unknown
        """
        Gets a value as a 16-bit signed integer.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The value
                :rtype: int
        """
        pass

    def getValueAsString(self, *args, **kwargs):  # real signature unknown
        """
        Gets a value as a string.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The value
                :rtype: str
        """
        pass

    def getValueCommandClass(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getValueFloatPrecision(self, *args, **kwargs):  # real signature unknown
        """
        Gets a float value's precision

                :param value_id: The unique identifier of the value.
                :type value_id: int

                :return: a float value's precision.
                :rtype: int, None
        """
        pass

    def getValueGenre(self, *args, **kwargs):  # real signature unknown
        """
        Get the genre of the value.

                The genre classifies a value to enable low-level system or
                configuration parameters to be filtered out by the application.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: A string containing the type of the value
                :rtype: str, optional
        """
        pass

    def getValueHelp(self, *args, **kwargs):  # real signature unknown
        """
        Gets a help string describing the value's purpose and usage.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: A string containing the value help text.
                :rtype: str, optional
        """
        pass

    def getValueIndex(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getValueInstance(self, *args, **kwargs):  # real signature unknown
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
        pass

    def getValueLabel(self, *args, **kwargs):  # real signature unknown
        """
        Gets the user-friendly label for the value

                :param value_id: The ID of a value.
                :type value_id: int

                :return: A string containing the user-friendly label of the value
                :rtype: str, optional
        """
        pass

    def getValueListItems(self, *args, **kwargs):  # real signature unknown
        """
        Gets the list of items from a list value

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The list of possible values
                :rtype: list
        """
        pass

    def getValueListSelectionNum(self, *args,
                                 **kwargs):  # real signature unknown
        """
        Gets value of items from a list value

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The value
                :rtype: int
        """
        pass

    def getValueListSelectionStr(self, *args,
                                 **kwargs):  # real signature unknown
        """
        Gets value of items from a list value

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The value
                :rtype: str
        """
        pass

    def getValueListValues(self, *args, **kwargs):  # real signature unknown
        """
        Gets the list of values from a list value.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The list of values
                :rtype: list
        """
        pass

    def getValueMax(self, *args, **kwargs):  # real signature unknown
        """
        Gets the maximum that this value may contain.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The value maximum.
                :rtype: int, optional
        """
        pass

    def getValueMin(self, *args, **kwargs):  # real signature unknown
        """
        Gets the minimum that this value may contain.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: The value minimum.
                :rtype: int, optional
        """
        pass

    def getValueType(self, *args, **kwargs):  # real signature unknown
        """
        Gets the type of the value

                :param value_id: The ID of a value.
                :type value_id: int

                :return: A string containing the type of the value
                :rtype: str, optional
        """
        pass

    def getValueUnits(self, *args, **kwargs):  # real signature unknown
        """
        Gets the units that the value is measured in.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: A string containing the value of the units.
                :rtype: str, optional
        """
        pass

    def hasNodeFailed(self, *args, **kwargs):  # real signature unknown
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
        pass

    def healNetwork(self, *args, **kwargs):  # real signature unknown
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
        pass

    def healNetworkNode(self, *args, **kwargs):  # real signature unknown
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
        pass

    def isBridgeController(self, *args, **kwargs):  # real signature unknown
        """
        Query if the controller is using the bridge controller library.

                A bridge controller is able to create virtual nodes that can be
                associated with other controllers to enable events to be passed on.

                :param home_id: The Home ID of the Z-Wave controller.
                :type home_id: int

                :return: `True` if it is a bridge controller, `False` if not.
                :rtype: bool
        """
        pass

    def isMultiInstance(self, *args, **kwargs):  # real signature unknown
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
        pass

    def isNodeAwake(self, *args, **kwargs):  # real signature unknown
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
        pass

    def isNodeBeamingDevice(self, *args, **kwargs):  # real signature unknown
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
        pass

    def isNodeFailed(self, *args, **kwargs):  # real signature unknown
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
        pass

    def isNodeFrequentListeningDevice(self, *args,
                                      **kwargs):  # real signature unknown
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
        pass

    def isNodeInfoReceived(self, *args, **kwargs):  # real signature unknown
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
        pass

    def isNodeListeningDevice(self, *args, **kwargs):  # real signature unknown
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
        pass

    def isNodeRoutingDevice(self, *args, **kwargs):  # real signature unknown
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
        pass

    def isNodeSecurityDevice(self, *args, **kwargs):  # real signature unknown
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
        pass

    def isNodeZWavePlus(self, *args, **kwargs):  # real signature unknown
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
        pass

    def isPolled(self, *args, **kwargs):  # real signature unknown
        """
        .        Check polling status of a value

                :param value_id: The ID of the value to check polling.
                :type value_id: int

                :return: True if polling is active.
                :rtype: bool
        """
        pass

    def isPrimaryController(self, *args, **kwargs):  # real signature unknown
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
        pass

    def isStaticUpdateController(self, *args,
                                 **kwargs):  # real signature unknown
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
        pass

    def isValuePolled(self, *args, **kwargs):  # real signature unknown
        """
        Test whether the value is currently being polled.

                :param value_id: the ID of a value.
                :type value_id: int

                :return: `True` if the value is being polled, otherwise `False`.
                :rtype: bool, optional
        """
        pass

    def isValueReadOnly(self, *args, **kwargs):  # real signature unknown
        """
        Test whether the value is read-only.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: `True` if the value cannot be changed by the user.
                :rtype: bool, optional
        """
        pass

    def isValueSet(self, *args, **kwargs):  # real signature unknown
        """
        Test whether the value has been set.

                :param value_id: the ID of a value.
                :type value_id: int

                :return: True if the value has actually been set by a status
                    message from the device, rather than simply being the default.
                :rtype: bool, optional
        """
        pass

    def isValueWriteOnly(self, *args, **kwargs):  # real signature unknown
        """
        Test whether the value is write-only.

                :param value_id: The ID of a value.
                :type value_id: int

                :return: `True` if the value can only be written to and not read.
                :rtype: bool, optional
        """
        pass

    def logDriverStatistics(self, *args, **kwargs):  # real signature unknown
        """
        Send current driver statistics to the log file.

                :param home_id: The Home ID of the Z-Wave controller.
                :type home_id: int

                :rtype: None
        """
        pass

    def pressButton(self, *args, **kwargs):  # real signature unknown
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
        pass

    def receiveConfiguration(self, *args, **kwargs):  # real signature unknown
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
        pass

    def refreshNodeInfo(self, *args, **kwargs):  # real signature unknown
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
        pass

    def refreshValue(self, *args, **kwargs):  # real signature unknown
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
        pass

    def releaseButton(self, *args, **kwargs):  # real signature unknown
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
        pass

    def removeAssociation(self, *args, **kwargs):  # real signature unknown
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
        pass

    def removeDriver(self, *args, **kwargs):  # real signature unknown
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
        pass

    def removeNode(self, *args, **kwargs):  # real signature unknown
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
        pass

    def removeSwitchPoint(self, *args, **kwargs):  # real signature unknown
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
        pass

    def removeWatcher(self, *args, **kwargs):  # real signature unknown
        """
        Remove a notification watcher.

                :param python_func: Watcher pointer to a function
                :type python_func: callable

                :rtype: None
        """
        pass

    def replaceFailedNode(self, *args, **kwargs):  # real signature unknown
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
        pass

    def replicationSend(self, *args, **kwargs):  # real signature unknown
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
        pass

    def requestAllConfigParams(self, *args, **kwargs):  # real signature unknown
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
        pass

    def requestConfigParam(self, *args, **kwargs):  # real signature unknown
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
        pass

    def requestNetworkUpdate(self, *args, **kwargs):  # real signature unknown
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
        pass

    def requestNodeDynamic(self, *args, **kwargs):  # real signature unknown
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
        pass

    def requestNodeNeighborUpdate(self, *args,
                                  **kwargs):  # real signature unknown
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
        pass

    def requestNodeState(self, *args, **kwargs):  # real signature unknown
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
        pass

    def resetController(self, *args, **kwargs):  # real signature unknown
        """
        Hard Reset a PC Z-Wave Controller.

                Resets a controller and erases its network configuration settings.
                The controller becomes a primary controller ready to add devices
                to a new network.

                :param home_id: The Home ID of the Z-Wave controller to be reset.
                :type home_id: int

                :rtype: None
        """
        pass

    def sendNodeInformation(self, *args, **kwargs):  # real signature unknown
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
        pass

    def sendRawData(self, *args, **kwargs):  # real signature unknown
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
        pass

    def setChangeVerified(self, *args, **kwargs):  # real signature unknown
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
        pass

    def setConfigParam(self, *args, **kwargs):  # real signature unknown
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
        pass

    def setNodeLevel(self, *args, **kwargs):  # real signature unknown
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
        pass

    def setNodeLocation(self, *args, **kwargs):  # real signature unknown
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
        pass

    def setNodeManufacturerName(self, *args,
                                **kwargs):  # real signature unknown
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
        pass

    def setNodeName(self, *args, **kwargs):  # real signature unknown
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
        pass

    def setNodeOff(self, *args, **kwargs):  # real signature unknown
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
        pass

    def setNodeOn(self, *args, **kwargs):  # real signature unknown
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
        pass

    def setNodeProductName(self, *args, **kwargs):  # real signature unknown
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
        pass

    def setPollIntensity(self, *args, **kwargs):  # real signature unknown
        """
        Set the frequency of polling (0=none, 1=every time through the
                set, 2-every other time, etc)

                :param value_id: The ID of the value whose intensity should be set
                :type value_id: int

                :param intensity: the intensity of the poll
                :type intensity: int

                :rtype: None
        """
        pass

    def setPollInterval(self, *args, **kwargs):  # real signature unknown
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
        pass

    def setSwitchPoint(self, *args, **kwargs):  # real signature unknown
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
        pass

    def setValue(self, *args, **kwargs):  # real signature unknown
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
        pass

    def setValueHelp(self, *args, **kwargs):  # real signature unknown
        """
        Sets a help string describing the value's purpose and usage.

                :param value_id: the ID of a value.
                :type value_id: int

                :param help: The new value of the help text.
                :type help: str

                :rtype: None
        """
        pass

    def setValueLabel(self, *args, **kwargs):  # real signature unknown
        """
        Sets the user-friendly label for the value

                :param value_id: The ID of a value.
                :type value_id: int

                :param label: The label of the value.
                :type label: str

                :rtype: None
        """
        pass

    def setValueUnits(self, *args, **kwargs):  # real signature unknown
        """
        Sets the units that the value is measured in.

                :param value_id: The ID of a value.
                :type value_id: int

                :param unit: The new value of the units.
                :type unit: str

                :rtype: None
        """
        pass

    def softResetController(self, *args, **kwargs):  # real signature unknown
        """
        Soft Reset a PC Z-Wave Controller.

                Resets a controller without erasing its network
                configuration settings.

                :param home_id: The Home ID of the Z-Wave controller to be reset.
                :type home_id: int

                :rtype: None
        """
        pass

    def switchAllOff(self, *args, **kwargs):  # real signature unknown
        """
        Switch all devices off.

                All devices that support the SwitchAll command class will be
                turned off.

                :param home_id: The Home ID of the Z-Wave controller
                    that manages the node.
                :type home_id: int

                :rtype: None
        """
        pass

    def switchAllOn(self, *args, **kwargs):  # real signature unknown
        """
        Switch all devices on.

                All devices that support the SwitchAll command class will be
                turned on.

                :param home_id: The Home ID of the Z-Wave controller
                    that manages the node.
                :type home_id: int

                :rtype: None
        """
        pass

    def testNetwork(self, *args, **kwargs):  # real signature unknown
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
        pass

    def testNetworkNode(self, *args, **kwargs):  # real signature unknown
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
        pass

    def transferPrimaryRole(self, *args, **kwargs):  # real signature unknown
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
        pass

    def writeConfig(self, *args, **kwargs):  # real signature unknown
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
        pass

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

    @staticmethod  # known case of __new__
    def __new__(*args, **kwargs):  # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        pass

    def __reduce__(self, *args, **kwargs):  # real signature unknown
        pass

    def __setstate__(self, *args, **kwargs):  # real signature unknown
        pass

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
        'all nodes queried',
    )
    COMMAND_CLASS_DESC = {
        0: 'COMMAND_CLASS_NO_OPERATION',
        32: 'COMMAND_CLASS_BASIC',
        33: 'COMMAND_CLASS_CONTROLLER_REPLICATION',
        34: 'COMMAND_CLASS_APPLICATION_STATUS',
        35: 'COMMAND_CLASS_ZIP_SERVICES',
        36: 'COMMAND_CLASS_ZIP_SERVER',
        37: 'COMMAND_CLASS_SWITCH_BINARY',
        38: 'COMMAND_CLASS_SWITCH_MULTILEVEL',
        39: 'COMMAND_CLASS_SWITCH_ALL',
        40: 'COMMAND_CLASS_SWITCH_TOGGLE_BINARY',
        41: 'COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL',
        42: 'COMMAND_CLASS_CHIMNEY_FAN',
        43: 'COMMAND_CLASS_SCENE_ACTIVATION',
        44: 'COMMAND_CLASS_SCENE_ACTUATOR_CONF',
        45: 'COMMAND_CLASS_SCENE_CONTROLLER_CONF',
        46: 'COMMAND_CLASS_ZIP_CLIENT',
        47: 'COMMAND_CLASS_ZIP_ADV_SERVICES',
        48: 'COMMAND_CLASS_SENSOR_BINARY',
        49: 'COMMAND_CLASS_SENSOR_MULTILEVEL',
        50: 'COMMAND_CLASS_METER',
        51: 'COMMAND_CLASS_COLOR',
        52: 'COMMAND_CLASS_ZIP_ADV_CLIENT',
        53: 'COMMAND_CLASS_METER_PULSE',
        56: 'COMMAND_CLASS_THERMOSTAT_HEATING',
        60: 'COMMAND_CLASS_METER_TBL_CONFIG',
        61: 'COMMAND_CLASS_METER_TBL_MONITOR',
        62: 'COMMAND_CLASS_METER_TBL_PUSH',
        64: 'COMMAND_CLASS_THERMOSTAT_MODE',
        66: 'COMMAND_CLASS_THERMOSTAT_OPERATING_STATE',
        67: 'COMMAND_CLASS_THERMOSTAT_SETPOINT',
        68: 'COMMAND_CLASS_THERMOSTAT_FAN_MODE',
        69: 'COMMAND_CLASS_THERMOSTAT_FAN_STATE',
        70: 'COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE',
        71: 'COMMAND_CLASS_THERMOSTAT_SETBACK',
        76: 'COMMAND_CLASS_DOOR_LOCK_LOGGING',
        78: 'COMMAND_CLASS_SCHEDULE_ENTRY_LOCK',
        80: 'COMMAND_CLASS_BASIC_WINDOW_COVERING',
        81: 'COMMAND_CLASS_MTP_WINDOW_COVERING',
        86: 'COMMAND_CLASS_CRC_16_ENCAP',
        90: 'COMMAND_CLASS_DEVICE_RESET_LOCALLY',
        91: 'COMMAND_CLASS_CENTRAL_SCENE',
        94: 'COMMAND_CLASS_ZWAVE_PLUS_INFO',
        96: 'COMMAND_CLASS_MULTI_INSTANCE/CHANNEL',
        97: 'COMMAND_CLASS_DISPLAY',
        98: 'COMMAND_CLASS_DOOR_LOCK',
        99: 'COMMAND_CLASS_USER_CODE',
        100: 'COMMAND_CLASS_GARAGE_DOOR',
        102: 'COMMAND_CLASS_BARRIER_OPERATOR',
        112: 'COMMAND_CLASS_CONFIGURATION',
        113: 'COMMAND_CLASS_ALARM',
        114: 'COMMAND_CLASS_MANUFACTURER_SPECIFIC',
        115: 'COMMAND_CLASS_POWERLEVEL',
        117: 'COMMAND_CLASS_PROTECTION',
        118: 'COMMAND_CLASS_LOCK',
        119: 'COMMAND_CLASS_NODE_NAMING',
        120: 'COMMAND_CLASS_ACTUATOR_MULTILEVEL',
        121: 'COMMAND_CLASS_KICK',
        122: 'COMMAND_CLASS_FIRMWARE_UPDATE_MD',
        123: 'COMMAND_CLASS_GROUPING_NAME',
        124: 'COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE',
        125: 'COMMAND_CLASS_REMOTE_ASSOCIATION',
        128: 'COMMAND_CLASS_BATTERY',
        129: 'COMMAND_CLASS_CLOCK',
        130: 'COMMAND_CLASS_HAIL',
        131: 'COMMAND_CLASS_NETWORK_STAT',
        132: 'COMMAND_CLASS_WAKE_UP',
        133: 'COMMAND_CLASS_ASSOCIATION',
        134: 'COMMAND_CLASS_VERSION',
        135: 'COMMAND_CLASS_INDICATOR',
        136: 'COMMAND_CLASS_PROPRIETARY',
        137: 'COMMAND_CLASS_LANGUAGE',
        138: 'COMMAND_CLASS_TIME',
        139: 'COMMAND_CLASS_TIME_PARAMETERS',
        140: 'COMMAND_CLASS_GEOGRAPHIC_LOCATION',
        141: 'COMMAND_CLASS_COMPOSITE',
        142: 'COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION',
        143: 'COMMAND_CLASS_MULTI_CMD',
        144: 'COMMAND_CLASS_ENERGY_PRODUCTION',
        145: 'COMMAND_CLASS_MANUFACTURER_PROPRIETARY',
        146: 'COMMAND_CLASS_SCREEN_MD',
        147: 'COMMAND_CLASS_SCREEN_ATTRIBUTES',
        148: 'COMMAND_CLASS_SIMPLE_AV_CONTROL',
        149: 'COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD',
        150: 'COMMAND_CLASS_AV_RENDERER_STATUS',
        151: 'COMMAND_CLASS_AV_CONTENT_SEARCH_MD',
        152: 'COMMAND_CLASS_SECURITY',
        153: 'COMMAND_CLASS_AV_TAGGING_MD',
        154: 'COMMAND_CLASS_IP_CONFIGURATION',
        155: 'COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION',
        156: 'COMMAND_CLASS_SENSOR_ALARM',
        157: 'COMMAND_CLASS_SILENCE_ALARM',
        158: 'COMMAND_CLASS_SENSOR_CONFIGURATION',
        239: 'COMMAND_CLASS_MARK',
        240: 'COMMAND_CLASS_NON_INTEROPERABLE',
    }


class PyOptions(object):
    """ Manage options manager """

    def addOption(self, name: str, value: Union[bool, int, str]) -> bool:  # real signature unknown
        """
        Add an option.

                :param name: The name of the option.
                :type name: str

                :param value: The value of the option.
                :type value: bool, int, str

                :return: The result of the operation.
                :rtype: bool
        """
        pass

    def addOptionBool(self, name: str, value: bool) -> bool:  # real signature unknown
        """
        Add a boolean option.

                :param name: The name of the option.
                :type name: str

                :param value: The value of the option.
                :type value: bool

                :return: The result of the operation.
                :rtype: bool
        """
        pass

    def addOptionInt(self, name: str, value: int) -> bool:  # real signature unknown
        """
        Add an integer option.

                :param name: The name of the option.
                :type name: str

                :param value: The value of the option.
                :type value: int

                :return: The result of the operation.
                :rtype: bool
        """
        pass

    def addOptionString(self, name: str, value: str, append: bool = False) -> bool:  # real signature unknown
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
        pass

    def areLocked(self) -> bool:  # real signature unknown
        """
        Test whether the options have been locked.

                :return: true if the options have been locked.
                :rtype: bool
        """
        pass

    def create(self) -> bool:  # real signature unknown
        """
        Create an option object used to start the manager

                :rtype: bool
        """
        pass

    def destroy(self) -> bool:  # real signature unknown
        """
        Deletes the Options and cleans up any associated objects.

                The application is responsible for destroying the Options object,
                but this must not be done until after the Manager object has been
                destroyed.

                :return: The result of the operation.
                :rtype: bool
        """
        pass

    def getConfigPath(self,) -> str:  # real signature unknown
        """
        Retrieve the config path. This directory hold the xml files.

                :return: A string containing the library config path or None.
                :rtype: str
        """
        pass

    def getOption(self, name: str) -> Union[bool, int, str, None]:  # real signature unknown
        """
        Retrieve option of a value.

                :param name: The name of the option.
                :type name: str

                :return: The value
                :rtype: bool, int, str, optional
        """
        pass

    def getOptionAsBool(self,  name: str) -> Union[bool, None]:  # real signature unknown
        """
        Retrieve boolean value of an option.

                :param name: The name of the option.
                :type name: str

                :return: The value or None
                :rtype: bool, optional
        """
        pass

    def getOptionAsInt(self,  name: str) -> Union[int, None]:  # real signature unknown
        """
        Retrieve integer value of an option.

                :param name: The name of the option.
                :type name: str

                :return: The value or None
                :rtype: int, optional
        """
        pass

    def getOptionAsString(self,  name: str) -> Union[str, None]:  # real signature unknown
        """
        Retrieve string value of an option.

                :param name: The name of the option.
                :type name: str

                :return: The value or None
                :rtype: str, optional
        """
        pass

    def lock(self) -> bool:  # real signature unknown
        """
        Lock the options.

                Needed to start the manager

                :return: The result of the operation.
                :rtype: bool
        """
        pass

    def __init__(self, config_path: str = '', user_path: str = '', cmd_line: str = ''):  # real signature unknown
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
        pass

    _cmd_line: str
    _config_path: str
    _user_path: str


class StatItem(object):
    # no doc
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

    __weakref__ = property(lambda self: object(), lambda self, v: None,
                           lambda self: None)  # default
    """list of weak references to the object (if defined)"""

    doc = ''
    __dict__ = None  # (!) real value is "mappingproxy({'__module__': '_libopenzwave', 'doc': '', '__dict__': <attribute '__dict__' of 'StatItem' objects>, '__weakref__': <attribute '__weakref__' of 'StatItem' objects>, '__doc__': None})"


class Value(object):
    # no doc
    def __init__(self, id: int):  # real signature unknown
        """
        :param id:
        :type id: int
        """
        pass

    __weakref__ = property(lambda self: object(), lambda self, v: None,
                           lambda self: None)  # default
    """list of weak references to the object (if defined)"""

    command_class: int
    data = None
    genre = None
    id: int
    index: int
    instance: int
    is_read_only: bool
    label: str
    type = None
    units: str


class ZWaveNotification(object):
    # no doc
    def __eq__(self, *args, **kwargs):  # real signature unknown
        """
        :param other:

                :rtype: bool
        """
        pass

    def __init__(self, *args, **kwargs):  # real signature unknown
        """
        :param notification_type:

                :param home_id:

                :param node_id:
        """
        pass

    def __ne__(self, *args, **kwargs):  # real signature unknown
        """
        :param other:

                :rtype: bool
        """
        pass

    def __repr__(self, *args, **kwargs):  # real signature unknown
        pass

    def __str__(self, *args, **kwargs):  # real signature unknown
        pass

    __weakref__ = property(lambda self: object(), lambda self, v: None,
                           lambda self: None)  # default
    """list of weak references to the object (if defined)"""

    button_id: int
    controller_command: int
    controller_error: int
    controller_state: int
    event: int
    group_id: int
    home_id: int
    node_id: int
    notification_code: int
    scene_id: int
    type: int
    user_alert: int
    value: int
    Value = Value


class _bool(int):
    """
    This class is a workaround for a bug found in python by @cgarwood.
        Every data type class in python can be subclassed except for bool. I am not
        sure of the reason why but because we want to add a tooltip/doc attribute
        that is accessable by the user we ned to be able to subclass the data type.

        This class gets used as a parent class to a dynamically created class
        along with StatItem
    """

    def __and__(self, *args, **kwargs):  # real signature unknown
        pass

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

    @staticmethod  # known case of __new__
    def __new__(*args, **kwargs):  # real signature unknown
        pass

    def __or__(self, *args, **kwargs):  # real signature unknown
        pass

    def __rand__(self, *args, **kwargs):  # real signature unknown
        pass

    def __repr__(self, *args, **kwargs):  # real signature unknown
        pass

    def __ror__(self, *args, **kwargs):  # real signature unknown
        pass

    def __rxor__(self, y):  # real signature unknown; restored from __doc__
        """ x.__rxor__(y) <==> y^x """
        pass

    def __str__(self, *args, **kwargs):  # real signature unknown
        pass

    def __xor__(self, *args, **kwargs):  # real signature unknown
        pass

    _value: int

# variables with complex values

logger: logging.Logger  # (!) real value is '<Logger libopenzwave (DEBUG)>'

PyCommandClassData = {
    'commandClassId': 'commandClassId',
    'receivedCnt': 'receivedCnt',
    'sentCnt': 'sentCnt',
}

PyControllerCommand = {
    'AddDevice': 'AddDevice',
    'AssignReturnRoute': 'AssignReturnRoute',
    'CreateButton': 'CreateButton',
    'CreateNewPrimary': 'CreateNewPrimary',
    'DeleteAllReturnRoutes': 'DeleteAllReturnRoutes',
    'DeleteButton': 'DeleteButton',
    'HasNodeFailed': 'HasNodeFailed',
    'None_': 'None',
    'ReceiveConfiguration': 'ReceiveConfiguration',
    'RemoveDevice': 'RemoveDevice',
    'RemoveFailedNode': 'RemoveFailedNode',
    'ReplaceFailedNode': 'ReplaceFailedNode',
    'ReplicationSend': 'ReplicationSend',
    'RequestNetworkUpdate': 'RequestNetworkUpdate',
    'RequestNodeNeighborUpdate': 'RequestNodeNeighborUpdate',
    'SendNodeInformation': 'SendNodeInformation',
    'TransferPrimaryRole': 'TransferPrimaryRole',
}

PyControllerError = {
    'Busy': 'Busy',
    'ButtonNotFound': 'ButtonNotFound',
    'Disabled': 'Disabled',
    'Failed': 'Failed',
    'IsPrimary': 'IsPrimary',
    'NodeNotFound': 'NodeNotFound',
    'None_': 'None',
    'NotBridge': 'NotBridge',
    'NotFound': 'NotFound',
    'NotPrimary': 'NotPrimary',
    'NotSUC': 'NotSUC',
    'NotSecondary': 'NotSecondary',
    'Overflow': 'Overflow',
}

PyControllerInterface = {
    'Hid': 'Hid',
    'Serial': 'Serial',
    'Unknown': 'Unknown',
}

PyControllerState = {
    'Cancel': 'Cancel',
    'Completed': 'Completed',
    'Error': 'Error',
    'Failed': 'Failed',
    'InProgress': 'InProgress',
    'NodeFailed': 'NodeFailed',
    'NodeOK': 'NodeOK',
    'Normal': 'Normal',
    'Sleeping': 'Sleeping',
    'Starting': 'Starting',
    'Waiting': 'Waiting',
}

PyGenres = {
    'Basic': 'Basic',
    'Config': 'Config',
    'System': 'System',
    'User': 'User',
}

PyLogLevels = {
    'Alert': 'Alert',
    'Always': 'Always',
    'Debug': 'Debug',
    'Detail': 'Detail',
    'Error': 'Error',
    'Fatal': 'Fatal',
    'Info': 'Info',
    'Internal': 'Internal',
    'Invalid': 'Invalid',
    'None_': 'None',
    'StreamDetail': 'StreamDetail',
    'Warning': 'Warning',
}

PyNotificationCodes = {
    'Alive': 'Alive',
    'Awake': 'Awake',
    'Dead': 'Dead',
    'MsgComplete': 'MsgComplete',
    'NoOperation': 'NoOperation',
    'Sleep': 'Sleep',
    'Timeout': 'Timeout',
}

PyNotifications = {
    'AllNodesQueried': 'AllNodesQueried',
    'AllNodesQueriedSomeDead': 'AllNodesQueriedSomeDead',
    'AwakeNodesQueried': 'AwakeNodesQueried',
    'ButtonOff': 'ButtonOff',
    'ButtonOn': 'ButtonOn',
    'ControllerCommand': 'ControllerCommand',
    'CreateButton': 'CreateButton',
    'DeleteButton': 'DeleteButton',
    'DriverFailed': 'DriverFailed',
    'DriverReady': 'DriverReady',
    'DriverRemoved': 'DriverRemoved',
    'DriverReset': 'DriverReset',
    'EssentialNodeQueriesComplete': 'EssentialNodeQueriesComplete',
    'Group': 'Group',
    'ManufacturerSpecificDBReady': 'ManufacturerSpecificDBReady',
    'NodeAdded': 'NodeAdded',
    'NodeEvent': 'NodeEvent',
    'NodeNaming': 'NodeNaming',
    'NodeNew': 'NodeNew',
    'NodeProtocolInfo': 'NodeProtocolInfo',
    'NodeQueriesComplete': 'NodeQueriesComplete',
    'NodeRemoved': 'NodeRemoved',
    'NodeReset': 'NodeReset',
    'Notification': 'Notification',
    'PollingDisabled': 'PollingDisabled',
    'PollingEnabled': 'PollingEnabled',
    'SceneEvent': 'SceneEvent',
    'UserAlerts': 'UserAlerts',
    'ValueAdded': 'ValueAdded',
    'ValueChanged': 'ValueChanged',
    'ValueRefreshed': 'ValueRefreshed',
    'ValueRemoved': 'ValueRemoved',
}

PyOptionList = {
    'AppendLogFile': 'AppendLogFile',
    'Associate': 'Associate',
    'AssumeAwake': 'AssumeAwake',
    'ConfigPath': 'ConfigPath',
    'ConsoleOutput': 'ConsoleOutput',
    'CustomSecuredCC': 'CustomSecuredCC',
    'DriverMaxAttempts': 'DriverMaxAttempts',
    'DumpTriggerLevel': 'DumpTriggerLevel',
    'EnableSIS': 'EnableSIS',
    'EnforceSecureReception': 'EnforceSecureReception',
    'Exclude': 'Exclude',
    'Include': 'Include',
    'IncludeInstanceLabel': 'IncludeInstanceLabel',
    'Interface': 'Interface',
    'IntervalBetweenPoll': 'IntervalBetweenPoll',
    'LogFileName': 'LogFileName',
    'Logging': 'Logging',
    'NetworkKey': 'NetworkKey',
    'NotifyOnDriverUnload': 'NotifyOnDriverUnload',
    'NotifyTransactions': 'NotifyTransactions',
    'PerformReturnRoutes': 'PerformReturnRoutes',
    'PollInterval': 'PollInterval',
    'QueueLogLevel': 'QueueLogLevel',
    'RefreshAllUserCodes': 'RefreshAllUserCodes',
    'ReloadAfterUpdate': 'ReloadAfterUpdate',
    'RetryTimeout': 'RetryTimeout',
    'SaveConfiguration': 'SaveConfiguration',
    'SaveLogLevel': 'SaveLogLevel',
    'SecurityStrategy': 'SecurityStrategy',
    'SuppressValueRefresh': 'SuppressValueRefresh',
    'UserPath': 'UserPath',
}

PyOptionType = {
    'Bool': 'Bool',
    'Int': 'Int',
    'Invalid': 'Invalid',
    'String': 'String',
}

PyStatDriver = {
    'ACKCnt': 'ACKCnt',
    'ACKWaiting': 'ACKWaiting',
    'CANCnt': 'CANCnt',
    'NAKCnt': 'NAKCnt',
    'OOFCnt': 'OOFCnt',
    'SOFCnt': 'SOFCnt',
    'badChecksum': 'badChecksum',
    'badroutes': 'badroutes',
    'broadcastReadCnt': 'broadcastReadCnt',
    'broadcastWriteCnt': 'broadcastWriteCnt',
    'callbacks': 'callbacks',
    'dropped': 'dropped',
    'netbusy': 'netbusy',
    'noack': 'noack',
    'nondelivery': 'nondelivery',
    'readAborts': 'readAborts',
    'readCnt': 'readCnt',
    'retries': 'retries',
    'routedbusy': 'routedbusy',
    'writeCnt': 'writeCnt',
}

PyStatNode = {
    'ackChannel': 'ackChannel',
    'averageRequestRTT': 'averageRequestRTT',
    'averageResponseRTT': 'averageResponseRTT',
    'ccData': 'ccData',
    'hops': 'hops',
    'lastFailedLinkFrom': 'lastFailedLinkFrom',
    'lastFailedLinkTo': 'lastFailedLinkTo',
    'lastReceivedMessage': 'lastReceivedMessage',
    'lastRequestRTT': 'lastRequestRTT',
    'lastResponseRTT': 'lastResponseRTT',
    'lastTxChannel': 'lastTxChannel',
    'quality': 'quality',
    'receivedCnt': 'receivedCnt',
    'receivedDups': 'receivedDups',
    'receivedTS': 'receivedTS',
    'receivedUnsolicited': 'receivedUnsolicited',
    'retries': 'retries',
    'routeScheme': 'routeScheme',
    'routeSpeed': 'routeSpeed',
    'routeTries': 'routeTries',
    'routeUsed': 'routeUsed',
    'rssi_1': 'rssi_1',
    'rssi_2': 'rssi_2',
    'rssi_3': 'rssi_3',
    'rssi_4': 'rssi_4',
    'rssi_5': 'rssi_5',
    'sentCnt': 'sentCnt',
    'sentFailed': 'sentFailed',
    'sentTS': 'sentTS',
    'txStatusReportSupported': 'txStatusReportSupported',
    'txTime': 'txTime',
}

PyUserAlerts = {
    'ApplicationStatus_Queued': 'ApplicationStatus_Queued',
    'ApplicationStatus_Rejected': 'ApplicationStatus_Rejected',
    'ApplicationStatus_Retry': 'ApplicationStatus_Retry',
    'ConfigFileDownloadFailed': 'ConfigFileDownloadFailed',
    'ConfigOutOfDate': 'ConfigOutOfDate',
    'DNSError': 'DNSError',
    'MFSOutOfDate': 'MFSOutOfDate',
    'NodeReloadRequired': 'NodeReloadRequired',
    'None_': 'None',
    'UnsupportedController': 'UnsupportedController',
}

PyValueTypes = {
    'BitSet': 'BitSet',
    'Bool': 'Bool',
    'Button': 'Button',
    'Byte': 'Byte',
    'Decimal': 'Decimal',
    'Int': 'Int',
    'List': 'List',
    'Raw': 'Raw',
    'Schedule': 'Schedule',
    'Short': 'Short',
    'String': 'String',
}

