# -*- coding: utf-8 -*-
"""
This file is part of **libopenzwave** project

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
from libc.stdint cimport uint32_t, uint8_t
from values cimport ValueID

cdef extern from *:
    ctypedef char* const_notification "OpenZWave::Notification const*"

# noinspection PyPep8Naming
ctypedef void (*pfnOnNotification_t)(const_notification _pNotification, void* _context)

cdef extern from "Notification.h" namespace "OpenZWave::Notification":

    cdef enum NotificationType:
        # A new node value has been added to OpenZWave's list.
        # These notifications occur after a node has been discovered, and
        # details of its command classes have been received. Each command
        # class may generate one or more values depending on the complexity
        # of the item being represented.
        Type_ValueAdded = 0
        # A node value has been removed from OpenZWave's list.
        # This only occurs when a node is removed.
        Type_ValueRemoved = 1
        # A node value has been updated from the Z-Wave network and it is
        # different from the previous value.
        Type_ValueChanged = 2
        # A node value has been updated from the Z-Wave network.
        Type_ValueRefreshed = 3
        # The associations for the node have changed. The application
        # should rebuild any group information it holds about the node.
        Type_Group = 4
        # A new node has been found (not already stored in zwcfg*.xml file)
        Type_NodeNew = 5
        # A new node has been added to OpenZWave's list.
        # This may be due to a device being added to the Z-Wave network, or
        # because the application is initializing itself.
        Type_NodeAdded = 6
        # A node has been removed from OpenZWave's list.
        # This may be due to a device being removed from the Z-Wave network,
        # or because the application is closing.
        Type_NodeRemoved = 7
        # Basic node information has been received, such as whether the node
        # is a listening device, a routing device and its baud rate and basic,
        # generic and specific types. It is after this notification that you
        # can call Manager::GetNodeType to obtain a label containing the
        # device description.
        Type_NodeProtocolInfo = 8
        # One of the node names has changed (name, manufacturer, product).
        Type_NodeNaming = 9
        # A node has triggered an event.  This is commonly caused when a node
        # sends a Basic_Set command to the controller.  The event value is
        # stored in the notification.
        Type_NodeEvent = 10
        # Polling of a node has been successfully turned off by a call to
        # Manager::DisablePoll
        Type_PollingDisabled = 11
        # Polling of a node has been successfully turned on by a call to
        # Manager::EnablePoll
        Type_PollingEnabled = 12
        # Scene Activation Set received
        Type_SceneEvent = 13
        # Handheld controller button event created
        Type_CreateButton = 14
        # Handheld controller button event deleted
        Type_DeleteButton = 15
        # Handheld controller button on pressed event
        Type_ButtonOn = 16
        # Handheld controller button off pressed event
        Type_ButtonOff = 17
        # A driver for a PC Z-Wave controller has been added and is ready to
        # use.  The notification will contain the controller's Home ID,
        # which is needed to call most of the Manager methods.
        Type_DriverReady = 18
        # Driver failed to load
        Type_DriverFailed = 19
        # All nodes and values for this driver have been removed.  This is
        # sent instead of potentially hundreds of individual node and value
        # notifications.
        Type_DriverReset = 20
        # The queries on a node that are essential to its operation have been
        # completed. The node can now handle incoming messages.
        Type_EssentialNodeQueriesComplete = 21
        # All the initialisation queries on a node have been completed.
        Type_NodeQueriesComplete = 22
        # All awake nodes have been queried, so client application can
        # expected complete data for these nodes.
        Type_AwakeNodesQueried = 23
        # All nodes have been queried but some dead nodes found.
        Type_AllNodesQueriedSomeDead = 24
        # All nodes have been queried, so client application can expected
        # complete data.
        Type_AllNodesQueried = 25
        # A manager notification report.
        Type_Notification = 26
        # The Driver is being removed. (either due to Error or by request) Do
        # Not Call Any Driver Related Methods after receiving this call.
        Type_DriverRemoved = 27
        # When Controller Commands are executed, Notifications of
        # Success/Failure etc are communicated via this Notification *
        # Notification::GetEvent returns Driver::ControllerCommand and
        # Notification::GetNotification returns Driver::ControllerState
        Type_ControllerCommand = 28
        # The Device has been reset and thus removed from the NodeList in OZW
        Type_NodeReset = 29
        # Warnings and Notifications Generated by the library that should be
        # displayed to the user (eg, out of date config files)
        Type_UserAlerts = 30
        # The ManufacturerSpecific Database Is Ready
        Type_ManufacturerSpecificDBReady = 31


cdef extern from "Notification.h" namespace "OpenZWave::Notification":

    cdef enum UserAlertNotification:
        # No alert currently present.
        Alert_None = 0
        # A config file is out of date, use GetNodeId to determine which
        # node(s) are effected.
        Alert_ConfigOutOfDate = 1
        # A manufacturer_specific.xml file is out of date.
        Alert_MFSOutOfDate = 2
        # A config file failed to download.
        Alert_ConfigFileDownloadFailed = 3
        # An error occurred performing a DNS Lookup.
        Alert_DNSError = 4
        # A new config file has been discovered for this node, a node reload
        # is required to have the new configuration take affect.
        Alert_NodeReloadRequired = 5
        # The controller is not running a firmware library that is supported
        # by OpenZWave.
        Alert_UnsupportedController = 6
        # The Application Status Command Class returned the message
        # "Retry Later".
        Alert_ApplicationStatus_Retry = 7
        # The command has been queued for later execution.
        Alert_ApplicationStatus_Queued = 8
        # The command was rejected.
        Alert_ApplicationStatus_Rejected = 9

cdef extern from "Notification.h" namespace "OpenZWave::Notification":

    cdef enum NotificationCode:
        # Completed messages.
        Code_MsgComplete = 0
        # Messages that timeout will send a Notification with this code.
        Code_Timeout = 1
        # Report on NoOperation message sent completion.
        Code_NoOperation = 2
        # Report when a sleeping node wakes.
        Code_Awake = 3
        # Report when a node goes to sleep.
        Code_Sleep = 4
        # Report when a node is presumed dead.
        Code_Dead = 5
        # Report when a node is revived.
        Code_Alive = 6


cdef extern from "Notification.h" namespace "OpenZWave":

    # noinspection PyClassicStyleClass,PyMissingOrEmptyDocstring,PyPep8Naming
    cdef cppclass Notification:
        NotificationType GetType() except +
        uint32_t GetHomeId() except +
        uint8_t GetNodeId() except +
        ValueID& GetValueID() except +
        uint8_t GetGroupIdx() except +
        uint8_t GetEvent() except +
        uint8_t GetButtonId() except +
        uint8_t GetSceneId() except +
        uint8_t GetNotification() except +
        uint8_t GetByte() except +
        uint8_t GetCommand() except +
        UserAlertNotification GetUserAlertType() except +
