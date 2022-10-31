Data documentation
-------------------

The common data structures and definitions.

all data containers are an instance of the class below.

.. toctree::
    :maxdepth: 2

.. autoclass:: _libopenzwave.Enum
    :show-inheritance:

---------------
PyNotifications
---------------
.. py:data:: _libopenzwave.PyNotifications

* `PyNotifications.ValueAdded`:

    * `ValueAdded.doc`: A new node value has been added to OpenZWave's set. These notifications occur after a node has been discovered, and details of its command classes have been received. Each command class may generate one or more values depending on the complexity of the item being represented.

* `PyNotifications.ValueRemoved`:

    * `ValueRemoved.doc`: A node value has been removed from OpenZWave's set. This only occurs when a node is removed.

* `PyNotifications.ValueChanged`:

    * `ValueChanged.doc`: A node value has been updated from the Z-Wave network and it is different from the previous value.

* `PyNotifications.ValueRefreshed`:

    * `ValueRefreshed.doc`: A node value has been updated from the Z-Wave network.

* `PyNotifications.Group`:

    * `Group.doc`: The associations for the node have changed. The application should rebuild any group information it holds about the node.

* `PyNotifications.NodeNew`:

    * `NodeNew.doc`: A new node has been found (not already stored in zwcfg*.xml file).

* `PyNotifications.NodeAdded`:

    * `NodeAdded.doc`: A new node has been added to OpenZWave's set. This may be due to a device being added to the Z-Wave network, or because the application is initializing itself.

* `PyNotifications.NodeRemoved`:

    * `NodeRemoved.doc`: A node has been removed from OpenZWave's set. This may be due to a device being removed from the Z-Wave network, or because the application is closing.

* `PyNotifications.NodeProtocolInfo`:

    * `NodeProtocolInfo.doc`: Basic node information has been received, such as whether the node is a listening device, a routing device and its baud rate and basic, generic and specific types. It is after this notification that you can call Manager::GetNodeType to obtain a label containing the device description.

* `PyNotifications.NodeNaming`:

    * `NodeNaming.doc`: One of the node names has changed (name, manufacturer, product).

* `PyNotifications.NodeEvent`:

    * `NodeEvent.doc`: A node has triggered an event. This is commonly caused when a node sends a Basic_Set command to the controller. The event value is stored in the notification.

* `PyNotifications.PollingDisabled`:

    * `PollingDisabled.doc`: Polling of a node has been successfully turned off by a call to Manager::DisablePoll.

* `PyNotifications.PollingEnabled`:

    * `PollingEnabled.doc`: Polling of a node has been successfully turned on by a call to Manager::EnablePoll.

* `PyNotifications.SceneEvent`:

    * `SceneEvent.doc`: Scene Activation Set received.

* `PyNotifications.CreateButton`:

    * `CreateButton.doc`: Handheld controller button event created.

* `PyNotifications.DeleteButton`:

    * `DeleteButton.doc`: Handheld controller button event deleted.

* `PyNotifications.ButtonOn`:

    * `ButtonOn.doc`: Handheld controller button on pressed event.

* `PyNotifications.ButtonOff`:

    * `ButtonOff.doc`: Handheld controller button off pressed event.

* `PyNotifications.DriverReady`:

    * `DriverReady.doc`: A driver for a PC Z-Wave controller has been added and is ready to use. The notification will contain the controller's Home ID, which is needed to call most of the Manager methods.

* `PyNotifications.DriverFailed`:

    * `DriverFailed.doc`: Driver failed to load.

* `PyNotifications.DriverReset`:

    * `DriverReset.doc`: All nodes and values for this driver have been removed. This is sent instead of potentially hundreds of individual node and value notifications.

* `PyNotifications.EssentialNodeQueriesComplete`:

    * `EssentialNodeQueriesComplete.doc`: The queries on a node that are essential to its operation have been completed. The node can now handle incoming messages.

* `PyNotifications.NodeQueriesComplete`:

    * `NodeQueriesComplete.doc`: All the initialisation queries on a node have been completed.

* `PyNotifications.AwakeNodesQueried`:

    * `AwakeNodesQueried.doc`: All awake nodes have been queried, so client application can expected complete data for these nodes.

* `PyNotifications.AllNodesQueriedSomeDead`:

    * `AllNodesQueriedSomeDead.doc`: All nodes have been queried but some dead nodes found.

* `PyNotifications.AllNodesQueried`:

    * `AllNodesQueried.doc`: All nodes have been queried, so client application can expected complete data.

* `PyNotifications.Notification`:

    * `Notification.doc`: A manager notification report.

* `PyNotifications.DriverRemoved`:

    * `DriverRemoved.doc`: The Driver is being removed.

* `PyNotifications.ControllerCommand`:

    * `ControllerCommand.doc`: When Controller Commands are executed, Notifications of Success/Failure etc are communicated via this Notification.

* `PyNotifications.NodeReset`:

    * `NodeReset.doc`: A node has been reset from OpenZWave's set. The Device has been reset and thus removed from the NodeList in OZW.

* `PyNotifications.UserAlerts`:

    * `UserAlerts.doc`: Warnings and Notifications Generated by the library that should be displayed to the user (eg, out of date config files)

* `PyNotifications.ManufacturerSpecificDBReady`:

    * `ManufacturerSpecificDBReady.doc`: The ManufacturerSpecific Database Is Ready

--------
PyGenres
--------
.. py:data:: _libopenzwave.PyGenres

* `PyGenres.Basic`:

    * `Basic.doc`: The 'level' as controlled by basic commands. Usually duplicated by another command class.

* `PyGenres.User`:

    * `User.doc`: Basic values an ordinary user would be interested in.

* `PyGenres.Config`:

    * `Config.doc`: Device-specific configuration parameters. These cannot be automatically discovered via Z-Wave, and are usually described in the user manual instead.

* `PyGenres.System`:

    * `System.doc`: Values of significance only to users who understand the Z-Wave protocol

------------
PyValueTypes
------------
.. py:data:: _libopenzwave.PyValueTypes

* `PyValueTypes.Bool`:

    * `Bool.doc`: Boolean, true or false

* `PyValueTypes.Byte`:

    * `Byte.doc`: 8-bit unsigned value

* `PyValueTypes.Decimal`:

    * `Decimal.doc`: Represents a non-integer value as a string, to avoid floating point accuracy issues.

* `PyValueTypes.Int`:

    * `Int.doc`: 32-bit signed value

* `PyValueTypes.List`:

    * `List.doc`: List from which one item can be selected

* `PyValueTypes.Schedule`:

    * `Schedule.doc`: Complex type used with the Climate Control Schedule command class

* `PyValueTypes.Short`:

    * `Short.doc`: 16-bit signed value

* `PyValueTypes.String`:

    * `String.doc`: Text string

* `PyValueTypes.Button`:

    * `Button.doc`: A write-only value that is the equivalent of pressing a button to send a command to a device

* `PyValueTypes.Raw`:

    * `Raw.doc`: Raw byte values

* `PyValueTypes.BitSet`:

    * `BitSet.doc`: Group of boolean values

-------------------
PyControllerCommand
-------------------
.. py:data:: _libopenzwave.PyControllerCommand


* `PyControllerCommand.None_`:

    * `None_.doc`: No command.

* `PyControllerCommand.AddDevice`:

    * `AddDevice.doc`: Add a new device (but not a controller) to the Z-Wave network.

* `PyControllerCommand.CreateNewPrimary`:

    * `CreateNewPrimary.doc`: Add a new controller to the Z-Wave network. The new controller will be the primary, and the current primary will become a secondary controller.

* `PyControllerCommand.ReceiveConfiguration`:

    * `ReceiveConfiguration.doc`: Receive Z-Wave network configuration information from another controller.

* `PyControllerCommand.RemoveDevice`:

    * `RemoveDevice.doc`: Remove a new device (but not a controller) from the Z-Wave network.

* `PyControllerCommand.RemoveFailedNode`:

    * `RemoveFailedNode.doc`: Move a node to the controller's failed nodes list. This command will only work if the node cannot respond.

* `PyControllerCommand.HasNodeFailed`:

    * `HasNodeFailed.doc`: Check whether a node is in the controller's failed nodes list.

* `PyControllerCommand.ReplaceFailedNode`:

    * `ReplaceFailedNode.doc`: Replace a non-responding node with another. The node must be in the controller's list of failed nodes for this command to succeed.

* `PyControllerCommand.TransferPrimaryRole`:

    * `TransferPrimaryRole.doc`: Make a different controller the primary.

* `PyControllerCommand.RequestNetworkUpdate`:

    * `RequestNetworkUpdate.doc`: Request network information from the SUC/SIS.

* `PyControllerCommand.RequestNodeNeighborUpdate`:

    * `RequestNodeNeighborUpdate.doc`: Get a node to rebuild its neighbour list. This method also does ControllerCommand_RequestNodeNeighbors.

* `PyControllerCommand.AssignReturnRoute`:

    * `AssignReturnRoute.doc`: Assign a network return routes to a device.

* `PyControllerCommand.DeleteAllReturnRoutes`:

    * `DeleteAllReturnRoutes.doc`: Delete all return routes from a device.

* `PyControllerCommand.SendNodeInformation`:

    * `SendNodeInformation.doc`: Send a node information frame.

* `PyControllerCommand.ReplicationSend`:

    * `ReplicationSend.doc`: Send information from primary to secondary.

* `PyControllerCommand.CreateButton`:

    * `CreateButton.doc`: Create an id that tracks handheld button presses.

* `PyControllerCommand.DeleteButton`:

    * `DeleteButton.doc`: Delete id that tracks handheld button presses.

-----------------
PyControllerError
-----------------
.. py:data:: _libopenzwave.PyControllerError


* `PyControllerError.None_`:

    * `None_.doc`: None.

* `PyControllerError.ButtonNotFound`:

    * `ButtonNotFound.doc`: Button.

* `PyControllerError.NodeNotFound`:

    * `NodeNotFound.doc`: Button.

* `PyControllerError.NotBridge`:

    * `NotBridge.doc`: Button.

* `PyControllerError.NotSUC`:

    * `NotSUC.doc`: CreateNewPrimary.

* `PyControllerError.NotSecondary`:

    * `NotSecondary.doc`: CreateNewPrimary.

* `PyControllerError.NotPrimary`:

    * `NotPrimary.doc`: RemoveFailedNode, AddNodeToNetwork.

* `PyControllerError.IsPrimary`:

    * `IsPrimary.doc`: ReceiveConfiguration.

* `PyControllerError.NotFound`:

    * `NotFound.doc`: RemoveFailedNode.

* `PyControllerError.Busy`:

    * `Busy.doc`: RemoveFailedNode, RequestNetworkUpdate.

* `PyControllerError.Failed`:

    * `Failed].doc`: RemoveFailedNode, RequestNetworkUpdate.

* `PyControllerError.Disabled`:

    * `Disabled.doc`: RequestNetworkUpdate error.

* `PyControllerError.Overflow`:

    * `Overflow.doc`: RequestNetworkUpdate error.

-----------------
PyControllerState
-----------------
.. py:data:: _libopenzwave.PyControllerState


* `PyControllerState.Normal`:

    * `Normal.doc`: No command in progress.

* `PyControllerState.Starting`:

    * `Starting.doc`: The command is starting.

* `PyControllerState.Cancel`:

    * `Cancel.doc`: The command was cancelled.

* `PyControllerState.Error`:

    * `Error.doc`: Command invocation had error(s) and was aborted.

* `PyControllerState.Waiting`:

    * `Waiting.doc`: Controller is waiting for a user action.

* `PyControllerState.Sleeping`:

    * `Sleeping.doc`: Controller command is on a sleep queue wait for device.

* `PyControllerState.InProgress`:

    * `InProgress.doc`: The controller is communicating with the other device to carry out the command.

* `PyControllerState.Completed`:

    * `Completed.doc`: The command has completed successfully.

* `PyControllerState.Failed`:

    * `Failed.doc`: The command has failed.

* `PyControllerState.NodeOK`:

    * `NodeOK.doc`: Used only with ControllerCommand_HasNodeFailed to indicate that the controller thinks the node is OK.

* `PyControllerState.NodeFailed`:

    * `NodeFailed.doc`: Used only with ControllerCommand_HasNodeFailed to indicate that the controller thinks the node has failed.

------------
PyUserAlerts
------------
.. py:data:: _libopenzwave.PyUserAlerts


* `PyUserAlerts.None_`:

    * `None_.doc`: No alert currently present.

* `PyUserAlerts.ConfigOutOfDate`:

    * `ConfigOutOfDate.doc`: A config file is out of date, use GetNodeId to determine which node(s) are effected.

* `PyUserAlerts.MFSOutOfDate`:

    * `MFSOutOfDate.doc`: A manufacturer_specific.xml file is out of date.

* `PyUserAlerts.ConfigFileDownloadFailed`:

    * `ConfigFileDownloadFailed.doc`: A config file failed to download.

* `PyUserAlerts.DNSError`:

    * `DNSError.doc`: An error occurred performing a DNS Lookup.

* `PyUserAlerts.NodeReloadRequired`:

    * `NodeReloadRequired.doc`: A new config file has been discovered for this node, a node reload is required to have the new configuration take affect.

* `PyUserAlerts.UnsupportedController`:

    * `UnsupportedController.doc`: The controller is not running a firmware library that is supported by OpenZWave.

* `PyUserAlerts.ApplicationStatus_Retry`:

    * `ApplicationStatus_Retry.doc`: The Application Status Command Class returned the message "Retry Later".

* `PyUserAlerts.ApplicationStatus_Queued`:

    * `ApplicationStatus_Queued.doc`: The command has been queued for later execution.

* `PyUserAlerts.ApplicationStatus_Rejected`:

    * `ApplicationStatus_Rejected.doc`: The command was rejected.

-------------------
PyNotificationCodes
-------------------
.. py:data:: _libopenzwave.PyNotificationCodes


* `PyNotificationCodes.MsgComplete`:

    * `MsgComplete.doc`: Completed messages.

* `PyNotificationCodes.Timeout`:

    * `Timeout.doc`: Messages that timeout will send a Notification with this code.

* `PyNotificationCodes.NoOperation`:

    * `NoOperation.doc`: Report on NoOperation message sent completion.

* `PyNotificationCodes.Awake`:

    * `Awake.doc`: Report when a sleeping node wakes.

* `PyNotificationCodes.Sleep`:

    * `Sleep.doc`: Report when a node goes to sleep.

* `PyNotificationCodes.Dead`:

    * `Dead.doc`: Report when a node is presumed dead.

* `PyNotificationCodes.Alive`:

    * `Alive.doc`: Report when a node is revived.

---------------------
PyControllerInterface
---------------------
.. py:data:: _libopenzwave.PyControllerInterface


* `PyControllerInterface.Unknown`:

    * `Unknown.doc`: Controller interface use unknown protocol.

* `PyControllerInterface.Serial`:

    * `Serial.doc`: Controller interface use serial protocol.

* `PyControllerInterface.Hid`:

    * `Hid.doc`: Controller interface use human interface device protocol.

------------
PyOptionType
------------
.. py:data:: _libopenzwave.PyOptionType


* `PyOptionType.Invalid`:

    * `Invalid.doc`: Invalid type.

* `PyOptionType.Bool`:

    * `Bool.doc`: Boolean.

* `PyOptionType.Int`:

    * `Int.doc`: Integer.

* `PyOptionType.String`:

    * `String.doc`: String.


-----------
PyLogLevels
-----------
.. py:data:: _libopenzwave.PyLogLevels


* `PyLogLevels.Info`:

    * `Info.doc`: Everything's working fine...these messages provide streamlined feedback on each message

* `PyLogLevels.None_`:

    * `None_.doc`: Disable all logging

* `PyLogLevels.Always`:

    * `Always.doc`: These messages should always be shown

* `PyLogLevels.Detail`:

    * `Detail.doc`: Detailed information on the progress of each message

* `PyLogLevels.Invalid`:

    * `Invalid.doc`: Invalid Log Status

* `PyLogLevels.Internal`:

    * `Internal.doc`: Used only within the log class (uses existing timestamp, etc

* `PyLogLevels.Error`:

    * `Error.doc`: A serious issue with the library or the network

* `PyLogLevels.Debug`:

    * `Debug.doc`: Very detailed information on progress that will create a huge log file quickly but this level (as others) can be queued and sent to the log only on an error or warning

* `PyLogLevels.Fatal`:

    * `Fatal.doc`: A likely fatal issue in the library

* `PyLogLevels.StreamDetail`:

    * `StreamDetail.doc`: Will include low-level byte transfers from controller to buffer to application and back

* `PyLogLevels.Alert`:

    * `Alert.doc`: Something unexpected by the library about which the controlling application should be aware

* `PyLogLevels.Warning`:

    * `Warning.doc`: A minor issue from which the library should be able to recover

------------
PyOptionList
------------
.. py:data:: _libopenzwave.PyOptionList


* `PyOptionList.SaveLogLevel`:

    * `SaveLogLevel.doc`: Save (to file) log messages equal to or above LogLevel_Detail.
    * `SaveLogLevel.type`: Int

* `PyOptionList.AppendLogFile`:

    * `AppendLogFile.doc`: Append new session logs to existing log file (false - overwrite).
    * `AppendLogFile.type`: Bool

* `PyOptionList.LogFileName`:

    * `LogFileName.doc`: Name of the log file (can be changed via Log::SetLogFileName).
    * `LogFileName.type`: String

* `PyOptionList.ConfigPath`:

    * `ConfigPath.doc`: Path to the OpenZWave config folder.
    * `ConfigPath.type`: String

* `PyOptionList.DumpTriggerLevel`:

    * `DumpTriggerLevel.doc`: Default is to never dump RAM-stored log messages.
    * `DumpTriggerLevel.type`: Int

* `PyOptionList.UserPath`:

    * `UserPath.doc`: Path to the user's data folder.
    * `UserPath.type`: String

* `PyOptionList.Include`:

    * `Include.doc`: Only handle the specified command classes. The Exclude option is ignored if anything is listed here.
    * `Include.type`: String

* `PyOptionList.IntervalBetweenPolls`:

    * `IntervalBetweenPolls.doc`: If false, try to execute the entire poll list within the PollInterval time frame. If true, wait for PollInterval milliseconds between polls.
    * `IntervalBetweenPolls.type`: Bool

* `PyOptionList.Associate`:

    * `Associate.doc`: Enable automatic association of the controller with group one of every device.
    * `Associate.type`: Bool

* `PyOptionList.ReloadAfterUpdate`:

    * `ReloadAfterUpdate.doc`: Changes the node reloading after downloading a new device config file
    * `ReloadAfterUpdate.type`: String

* `PyOptionList.EnableSIS`:

    * `EnableSIS.doc`: Automatically become a SUC if there is no SUC on the network.
    * `EnableSIS.type`: Bool

* `PyOptionList.NetworkKey`:

    * `NetworkKey.doc`: Key used to negotiate and communicate with devices that support Security Command Class
    * `NetworkKey.type`: String

* `PyOptionList.QueueLogLevel`:

    * `QueueLogLevel.doc`: Save (in RAM) log messages equal to or above LogLevel_Debug.
    * `QueueLogLevel.type`: Int

* `PyOptionList.SaveConfiguration`:

    * `SaveConfiguration.doc`: Save the XML configuration upon driver close.
    * `SaveConfiguration.type`: Bool

* `PyOptionList.DriverMaxAttempts`:

    * `DriverMaxAttempts.doc`: .
    * `DriverMaxAttempts.type`: Int

* `PyOptionList.PollInterval`:

    * `PollInterval.doc`: 30 seconds (can easily poll 30 values in this time; ~120 values is the effective limit for 30 seconds).
    * `PollInterval.type`: Int

* `PyOptionList.Logging`:

    * `Logging.doc`: Enable logging of library activity.
    * `Logging.type`: Bool

* `PyOptionList.AssumeAwake`:

    * `AssumeAwake.doc`: Assume Devices that Support the Wakeup CC are awake when we first query them ...
    * `AssumeAwake.type`: Bool

* `PyOptionList.IncludeInstanceLabel`:

    * `IncludeInstanceLabel.doc`: Should we include the Instance Label in Value Labels on MultiInstance Devices
    * `IncludeInstanceLabel.type`: Bool

* `PyOptionList.PerformReturnRoutes`:

    * `PerformReturnRoutes.doc`: If true, return routes will be updated.
    * `PerformReturnRoutes.type`: Bool

* `PyOptionList.Interface`:

    * `Interface.doc`: Identify the serial port to be accessed (TODO: change the code so more than one serial port can be specified and HID).
    * `Interface.type`: String

* `PyOptionList.SuppressValueRefresh`:

    * `SuppressValueRefresh.doc`: If true, notifications for refreshed (but unchanged) values will not be sent.
    * `SuppressValueRefresh.type`: Bool

* `PyOptionList.SecurityStrategy`:

    * `SecurityStrategy.doc`: Should we encrypt CC's that are available via both clear text and Security CC?.
    * `SecurityStrategy.type`: String
    * `SecurityStrategy.value`: SUPPORTED

* `PyOptionList.RefreshAllUserCodes`:

    * `RefreshAllUserCodes.doc`: If true, during startup, we refresh all the UserCodes the device reports it supports. If False, we stop after we get the first "Available" slot (Some devices have 250+ usercode slots! - That makes our Session Stage Very Long ).
    * `RefreshAllUserCodes.type`: Bool

* `PyOptionList.CustomSecuredCC`:

    * `CustomSecuredCC.doc`: What List of Custom CC should we always encrypt if SecurityStrategy is CUSTOM.
    * `CustomSecuredCC.type`: String
    * `CustomSecuredCC.value`: 0x62,0x4c,0x63

* `PyOptionList.EnforceSecureReception`:

    * `EnforceSecureReception.doc`: If we recieve a clear text message for a CC that is Secured, should we drop the message
    * `EnforceSecureReception.type`: Bool

* `PyOptionList.NotifyOnDriverUnload`:

    * `NotifyOnDriverUnload.doc`: Should we send the Node/Value Notifications on Driver Unloading - Read comments in Driver::~Driver() method about possible race conditions.
    * `NotifyOnDriverUnload.type`: Bool

* `PyOptionList.NotifyTransactions`:

    * `NotifyTransactions.doc`: Notifications when transaction complete is reported.
    * `NotifyTransactions.type`: Bool

* `PyOptionList.Exclude`:

    * `Exclude.doc`: Remove support for the listed command classes.
    * `Exclude.type`: String

* `PyOptionList.RetryTimeout`:

    * `RetryTimeout.doc`: How long do we wait to timeout messages sent.
    * `RetryTimeout.type`: Int

* `PyOptionList.ConsoleOutput`:

    * `ConsoleOutput.doc`: Display log information on console (as well as save to disk).
    * `ConsoleOutput.type`: Bool

------------
PyStatDriver
------------
.. py:data:: _libopenzwave.PyStatDriver

* `PyStatDriver.retries`:

    * `retries.doc`: Number of messages retransmitted

* `PyStatDriver.readCnt`:

    * `readCnt.doc`: Number of messages successfully read

* `PyStatDriver.readAborts`:

    * `readAborts.doc`: Number of times read were aborted due to timeouts

* `PyStatDriver.routedbusy`:

    * `routedbusy.doc`: Number of messages received with routed busy status

* `PyStatDriver.ACKCnt`:

    * `ACKCnt.doc`: Number of ACK bytes received

* `PyStatDriver.OOFCnt`:

    * `OOFCnt.doc`: Number of bytes out of framing

* `PyStatDriver.noack`:

    * `noack.doc`: Number of no ACK returned errors

* `PyStatDriver.broadcastWriteCnt`:

    * `broadcastWriteCnt.doc`: Number of broadcasts sent

* `PyStatDriver.callbacks`:

    * `callbacks.doc`: Number of unexpected callbacks

* `PyStatDriver.writeCnt`:

    * `writeCnt.doc`: Number of messages successfully sent

* `PyStatDriver.badChecksum`:

    * `badChecksum.doc`: Number of bad checksums

* `PyStatDriver.nondelivery`:

    * `nondelivery.doc`: Number of messages not delivered to network

* `PyStatDriver.CANCnt`:

    * `CANCnt.doc`: Number of CAN bytes received

* `PyStatDriver.NAKCnt`:

    * `NAKCnt.doc`: Number of NAK bytes received

* `PyStatDriver.netbusy`:

    * `netbusy.doc`: Number of network busy/failure messages

* `PyStatDriver.SOFCnt`:

    * `SOFCnt.doc`: Number of SOF bytes received

* `PyStatDriver.broadcastReadCnt`:

    * `broadcastReadCnt.doc`: Number of broadcasts read

* `PyStatDriver.badroutes`:

    * `badroutes.doc`: Number of failed messages due to bad route response

* `PyStatDriver.ACKWaiting`:

    * `ACKWaiting.doc`: Number of unsolicited messages while waiting for an ACK

* `PyStatDriver.dropped`:

    * `dropped.doc`: Number of messages dropped & not delivered


----------
PyStatNode
----------
.. py:data:: _libopenzwave.PyStatNode

* `PyStatNode.receivedDups`:

    * `receivedDups.doc`: Number of duplicated messages received

* `PyStatNode.sentCnt`:

    * `sentCnt.doc`: Number of messages sent from this node

* `PyStatNode.receivedTS`:

    * `receivedTS.doc`: Last message received time

* `PyStatNode.quality`:

    * `quality.doc`: Node quality measure

* `PyStatNode.lastRequestRTT`:

    * `lastRequestRTT.doc`: Last message request RTT

* `PyStatNode.sentFailed`:

    * `sentFailed.doc`: Number of sent messages failed

* `PyStatNode.retries`:

    * `retries.doc`: Number of message retries

* `PyStatNode.lastResponseRTT`:

    * `lastResponseRTT.doc`: Last message response RTT

* `PyStatNode.errors`:

    * `errors.doc`: Count errors for dead node detection

* `PyStatNode.averageRequestRTT`:

    * `averageRequestRTT.doc`: Average Request round trip time

* `PyStatNode.receivedCnt`:

    * `receivedCnt.doc`: Number of messages received from this node

* `PyStatNode.averageResponseRTT`:

    * `averageResponseRTT.doc`: Average Response round trip time

* `PyStatNode.lastReceivedMessage`:

    * `lastReceivedMessage.doc`: Place to hold last received message

* `PyStatNode.receivedUnsolicited`:

    * `receivedUnsolicited.doc`: Number of messages received unsolicited

* `PyStatNode.sentTS`:

    * `sentTS.doc`: Last message sent time
