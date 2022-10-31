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
:synopsis: ZWave network API

.. moduleauthor:: Kevin G Schlosser
"""

import os
import logging
import threading

from _libopenzwave import PyNotifications
from .object import ZWaveObject
from .exception import ZWaveException  # NOQA

from . import state
from . import notification_handler
from . import signals
from . import utils
from . import xml_handler


logger = logging.getLogger(__name__)


class ZWaveNetwork(ZWaveObject):
    """
    The ZWaveNetwork class is the entry point to controlling a ZWave network.

    *IMPORTANT PLEASE READ*

    The ZWave network was designed to be as lightweight as possible. This was
    done so that a device would be able to run on batteries and also to be as
    energy efficient as possible.. The RF (radio frequency) used in the
    communications is a low frequency low power signal. In order to get the
    maximum range while using a lower transmitting power the low frequency is
    what is used to achieve this. With the use of low frequencies you have
    low speeds. So a ZWave network is not fast. It also has one other
    limitation besides speed, and that is the lack of "dual band" or
    a "broadband" type of connection. ZWave in it's current form is only able
    to have a single packet in the air at any given time. What this means is
    that only a single command is sent at a time, and the controller
    (USB Stick) will wait for a response to that command and do nothing else
    while this is happening.

    There is a "queue" for outgoing commands/requests, Si if you issue a
    command or a request it can take a while before it gets carried out.
    How long is up the the user and the application developer. The busier a
    network is and the more requests and commands that are being transmitted
    the slower it is going to appear to be. Excessive polling of nodes and a
    nodes values incorrectly is what causes the most latencies. So use some
    judgement when setting the polling.

    Here is a great example of how to manage polling of nodes and values.

    If you have 30 light switches and you 10 motion sensors and a handful of
    door/window sensors (for security) polling the light switches would be
    pointless if the motion sensors are "armed" and having the motion sensors
    polled if they are not armed would not need to be done either.

    Another example. polling lights that are outside may not be something that
    you would want to do if the local time is not between 30 minutes after
    sunset and 30 minutes before sunrise.

    So there are some very simple things that can be done to help reduce ZWave
    network traffic. As an application developer you may decide to assist a
    user in handling the polling by offering an "automatic" option or you may
    decide to let the user handle it on their own. No matter what you decide
    to do PLEASE at least add a monitor that will produce a warning the user
    can see if the user is excessively polling. Another good idea is to add a
    tooltip or some form of a narrative informing the user of what excessive
    polling does.

    With the release of ZWave+ devices they have tried to get the polling
    situation under control by having the devices report state changes without
    having to be asked. While this is not a 100% guarantee that the new state
    will actually get reported it at least will help. setting timers that will
    automatically request the new state at random intervals when the network
    use is low is a good idea. and if a device reports in on it's own then
    reset the timer.

    TIP: Only ask for updates to the values that matter.

    Since we do not want to have an application getting stalled waiting for a
    response we have designed a series of "signals" or "notifications" that
    you can pass a callback function to. This callback function will get called
    when a command has completed. These signals are also used to inform an
    application when a change in the network occurs or a value for a node has
    changed/updated.


    SIGNAL_AWAKE_NODES_QUERIED
    SIGNAL_NETWORK_AWAKE

    SIGNAL_DRIVER_FAILED
    SIGNAL_NETWORK_FAILED


    SIGNAL_ALL_NODES_QUERIED
    SIGNAL_ALL_NODES_QUERIED_SOME_DEAD
    SIGNAL_NETWORK_READY


    SIGNAL_DRIVER_RESET
    SIGNAL_NETWORK_RESET


    SIGNAL_DRIVER_READY
    SIGNAL_NETWORK_STARTED


    SIGNAL_DRIVER_REMOVED
    SIGNAL_NETWORK_STOPPED

    SIGNAL_USER_ALERTS

    SIGNAL_USER_ALERT_CONFIG_OUT_OF_DATE
    SIGNAL_USER_ALERT_MFS_OUT_OF_DATE
    SIGNAL_USER_ALERT_CONFIG_FILE_DOWNLOAD_FAILED
    SIGNAL_USER_ALERT_DNS_ERROR
    SIGNAL_USER_ALERT_NODE_RELOAD_REQUIRED
    SIGNAL_USER_ALERT_UNSUPPORTED_CONTROLLER
    SIGNAL_USER_ALERT_APPLICATION_STATUS_RETRY
    SIGNAL_USER_ALERT_APPLICATION_STATUS_QUEUED
    SIGNAL_USER_ALERT_APPLICATION_STATUS_REJECTED


SIGNAL_CONTROLLER_COMMAND


    SIGNAL_BUTTON_OFF
    SIGNAL_BUTTON_ON

    SIGNAL_CREATE_BUTTON
    SIGNAL_DELETE_BUTTON

    SIGNAL_GROUP

    SIGNAL_NODE_NEW

    SIGNAL_NODE_ADDED
    SIGNAL_NODE_CACHE_LOADED
    SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE
    SIGNAL_NODE_EVENT
    SIGNAL_NODE_NAMING
    SIGNAL_NODE_PROTOCOL_INFO
    SIGNAL_NODE_REMOVED

    SIGNAL_NODE_RESET

    SIGNAL_POLLING_DISABLED
    SIGNAL_POLLING_ENABLED


    SIGNAL_NODE_QUERIES_COMPLETE
    SIGNAL_NODE_READY


    SIGNAL_NOTIFICATION


    SIGNAL_VALUE_ADDED
    SIGNAL_VALUE_CHANGED
    SIGNAL_VALUE_REFRESHED
    SIGNAL_VALUE_REMOVED


    SIGNAL_MANUFACTURER_SPECIFIC_DB_READY

    SIGNAL_CONTROLLER_WAITING
    SIGNAL_MSG_COMPLETE


    Signals:

        * SIGNAL_NETWORK_FAILED: `"NetworkFailed"`
        * SIGNAL_NETWORK_STARTED: `"NetworkStarted"`
        * SIGNAL_NETWORK_READY: `"NetworkReady"`
        * SIGNAL_NETWORK_STOPPED: `"NetworkStopped"`
        * SIGNAL_NETWORK_RESET: `"DriverResetted"`
        * SIGNAL_NETWORK_AWAKE: `"DriverAwaked"`
        * SIGNAL_DRIVER_FAILED:`"DriverFailed"`
        * SIGNAL_DRIVER_READY: `"DriverReady"`
        * SIGNAL_DRIVER_RESET: `"DriverReset"`
        * SIGNAL_DRIVER_REMOVED: `"DriverRemoved"`
        * SIGNAL_NODE_ADDED: `"NodeAdded"`
        * SIGNAL_NODE_EVENT: `"NodeEvent"`
        * SIGNAL_NODE_NAMING: `"NodeNaming"`
        * SIGNAL_NODE_NEW: `"NodeNew"`
        * SIGNAL_NODE_PROTOCOL_INFO: `"NodeProtocolInfo"`
        * SIGNAL_NODE_READY: `"NodeReady"`
        * SIGNAL_NODE_REMOVED: `"NodeRemoved"`
        * SIGNAL_SCENE_EVENT: `"SceneEvent"`
        * SIGNAL_VALUE_ADDED: `"ValueAdded"`
        * SIGNAL_VALUE_CHANGED: `"ValueChanged"`
        * SIGNAL_VALUE_REFRESHED: `"ValueRefreshed"`
        * SIGNAL_VALUE_REMOVED: `"ValueRemoved"`
        * SIGNAL_POLLING_ENABLED: `"PollingEnabled"`
        * SIGNAL_POLLING_DISABLED: `"PollingDisabled"`
        * SIGNAL_CREATE_BUTTON: `"CreateButton"`
        * SIGNAL_DELETE_BUTTON: `"DeleteButton"`
        * SIGNAL_BUTTON_ON: `"ButtonOn"`
        * SIGNAL_BUTTON_OFF: `"ButtonOff"`
        * SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE:
          `"EssentialNodeQueriesComplete"`
        * SIGNAL_NODE_QUERIES_COMPLETE: `"NodeQueriesComplete"`
        * SIGNAL_AWAKE_NODES_QUERIED: `"AwakeNodesQueried"`
        * SIGNAL_ALL_NODES_QUERIED: `"AllNodesQueried"`
        * SIGNAL_ALL_NODES_QUERIED_SOME_DEAD: `"AllNodesQueriedSomeDead"`
        * SIGNAL_MSG_COMPLETE: `"MsgComplete"`
        * SIGNAL_ERROR: `"Error"`
        * SIGNAL_NOTIFICATION: `"Notification"`
        * SIGNAL_CONTROLLER_COMMAND: `"ControllerCommand"`
        * SIGNAL_CONTROLLER_WAITING: `"ControllerWaiting`"

    The table presented below sets notifications in the order they might
    typically be received, and grouped into a few logically related
    categories. Of course, given the variety of ZWave controllers, devices and
    network configurations the actual sequence will vary (somewhat). The
    descriptions below the notification name (in square brackets) identify
    whether the notification is always sent (unless there’s a significant
    error in the network or software) or potentially sent during the execution
    sequence.

    Driver Initialization Notification

    The notification below is sent when OpenZWave has successfully connected
    to a physical ZWave controller.

    * DriverReady: [always sent]

    Sent when the driver (representing a connection between OpenZWave and a
    Z-Wave controller attached to the specified serial (or HID) port) has been
    initialized. At the time this notification is sent, only certain
    information about the controller itself is known.

        * Controller Z-Wave version
        * Network HomeID
        * Controller capabilities
        * Controller Application Version & Manufacturer/Product ID
        * Nodes included in the network

    * DriverRemoved: [always sent (either due to Error or by request)]

    The Driver is being removed. Do Not Call Any Driver Related Methods after
    receiving this.

    Node Initialization Notifications

    As OpenZWave starts, it identifies and reads information about each node
    in the network. The following notifications may be sent during the
    initialization process.

    * NodeNew: [potentially sent]

    Sent when a new node has been identified as part of the Z-Wave network. It
    is not sent if the node was identified in a prior execution of the
    OpenZWave library and stored in the zwcfg*.xml file.

    At the time this notification is sent, very little is known about the node
    itself... Only that it is new to OpenZWave. This message is sent once for
    each new node identified.

    * NodeAdded: [always sent (for each node associated with the controller)]

    Sent when a node has been added to OpenZWave’s set of nodes.  It can be
    triggered either as the zwcfg*.xml file is being read, when a new node
    is found on startup (see NodeNew notification above), or if a new node
    is included in the network while OpenZWave is running.

    As with NodeNew, very little is known about the node at the time the
    notification is sent…just the fact that a new node has been identified
    and its assigned NodeID.

    * NodeProtocolInfo: [potentially sent]

    Sent after a node’s protocol information has been successfully read from
    the controller.

    At the time this notification is sent, only certain information about
    the node is known.

        * Whether it is a “listening” or “sleeping” device
        * Whether the node is capable of routing messages
        * Maximum baud rate for communication
        * Version number
        * Security byte

    * NodeNaming: [potentially sent]

    Sent when a node’s name has been set or changed (although it may be “set”
    to “” or NULL).

    * ValueAdded: [potentially sent]

    Sent when a new value has been associated with the node. At the time this
    notification is sent, the new value may or may not have “live” data
    associated with it. It may be populated, but it may alternatively just be
    a placeholder for a value that has not been read at the time the
    notification is sent.

    * NodeQueriesComplete: [always sent (for each node associated with the
      controller that has been successfully queried)]

    Sent when a node’s values and attributes have been fully queried. At the
    time this notification is sent, the node’s information has been fully read
    at least once. So this notification might trigger “full” display of the
    node’s information, values, etc. If this notification is not sent, it
    indicates that there has been a problem initializing the device.

    The most common issue is that the node is a “sleeping” device. The
    NodeQueriesComplete notification will be sent when the node wakes up and
    the query process completes.

    **Initialization Complete Notifications**

    As indicated above, when OpenZWave starts it reads certain information
    from a file, from the controller and from the network.  The following
    notifications identify when this initialization/querying process is
    complete.

    * AwakeNodesQueried: [always sent]

    Sent when all “listening” -always-on-devices have been queried
    successfully.  It also indicates, by implication, that there are some
    “sleeping” nodes that will not complete their queries until they wake up.
    This notification should be sent relatively quickly after start-up. (Of
    course, it depends on the number of devices on the ZWave network and
    whether there are any messages that “time out” without a proper response.)

    * AllNodesQueried: [potentially sent]

    Sent when all nodes have been successfully queried.

    This notification should be sent relatively quickly if there are
    no “sleeping” nodes. But it might be sent quite a while after start-up
    if there are sleeping nodes and at least one of these nodes has a long
    “wake-up” interval.

    Other Notifications

    In addition to the notifications described above, which are primarily
    “initialization” notifications that are sent during program start-up,
    the following notifications may be sent as a result of user actions,
    external program control, etc.

    * ValueChanged

    Sent when a value associated with a node has changed. Receipt of this
    notification indicates that it may be a good time to read the new value
    and display or otherwise process it accordingly.

    * ValueRemoved

    Sent when a value associated with a node has been removed.

    * Group

    Sent when a node’s group association has changed.

    * NodeRemoved

    Sent when a node has been removed from the ZWave network.

    * NodeEvent

    Sent when a node sends a Basic_Set command to the controller.

    This notification can be generated by certain sensors, for example, motion
    detectors, to indicate that an event has been sensed.

    * PollingEnabled

    Sent when node/value polling has been enabled.

    * PollingDisabled

    Sent when node/value polling has been disabled.

    * DriverReset

    Sent to indicate when a controller has been reset.

    This notification is intended to replace the potentially hundreds of
    notifications representing each value and node removed from the network.

    About the use of louie signals :
    For network, python-openzwave send the following louie signal :

        * SIGNAL_NETWORK_FAILED: The driver has failed to start.
        * SIGNAL_NETWORK_STARTED: The driver is ready, but network is not
          available.
        * SIGNAL_NETWORK_AWAKE: All awake nodes are queried. Some sleeping
          nodes may be missing.
        * SIGNAL_NETWORK_READY: All nodes are queried. Network is fully
          functional.
        * SIGNAL_NETWORK_RESET: The network has been reset. It will start
          again.
        * SIGNAL_NETWORK_STOPPED: The network has been stopped.

    Deprecated : SIGNAL_DRIVER_* shouldn't be used anymore.
    """

    STATE_STOPPED = state.STATE_STOPPED
    STATE_FAILED = state.STATE_FAILED
    STATE_RESET = state.STATE_RESET
    STATE_STARTED = state.STATE_STARTED
    STATE_AWAKE = state.STATE_AWAKE
    STATE_READY = state.STATE_READY

    ignoreSubsequent = True

    def __init__(self, options, auto_start=True):
        """
        Initialize zwave network

        :param options: Options to use with manager
        :type options: ZWaveOption

        :param auto_start: should we start the network.
        :type auto_start: bool
        """

        from .node import ZWaveNodes

        xml_file = os.path.join(
            options.user_path,
            'PyOZW_NetworkData.xml'
        )

        if os.path.exists(xml_file):
            try:
                handler = (
                    xml_handler.XMLRootElement.handle_file(xml_file)
                )
                if 'home_id' in handler.attrib:
                    home_id = int(handler['home_id'], 16)
                else:
                    handler['home_id'] = '0x00'
                    home_id = None
            except:  # NOQA
                import traceback
                traceback.print_exc()
                raise RuntimeError(
                    'database load failure ({0})'.format(xml_file)
                )

        else:
            logger.info('network database not found, creating new database...')

            handler = xml_handler.XMLRootElement('Network')
            handler['home_id'] = '0x00'
            handler.xml_file = xml_file

            handler.Nodes = xml_handler.XMLElement('Nodes')
            handler.Locations = xml_handler.XMLElement('Locations')
            handler.Locations['next_id'] = 1
            home_id = None

        ZWaveObject.__init__(self, home_id, self, handler)
        logger.debug("Create network object.")
        self._options = options
        self._controller = None
        self._command_state = None
        self._state = self.STATE_STOPPED
        self._nodes = ZWaveNodes()
        self._notification_handler = None
        self._id_separator = '.'
        self.network_event = threading.Event()
        self._started = False
        self._active_notifs = []
        self._pending_node_addition = {}
        self._auto_start = auto_start
        self._manager = None
        self._locations_loaded = set()

    def __iter__(self):
        for node in sorted(
            list(self.nodes.values()),
            key=lambda x: (x.id.node_id, x.id.endpoint_id)
        ):
            yield node

    @property
    def options(self):
        """
        :rtype: ZWaveOption
        """
        return self._options

    @property
    def command_state(self):
        """
        If a command on the network has been given this will return the state
        of that command.

        The returned value is a :py:class:`libopenzwave.network.State` instance.
        This object has 4 attributes which are using in an application.

        * `label`: label that can be used to display to the user. (EN)
        * `error`: one of :py:data:`libopenzwave.PyControllerError`
        * `command`: one of :py:data:`libopenzwave.PyControllerCommand`
        * `state`: one of :py:data:`libopenzwave.PyControllerState`


        the error, command and state attributes have an additional attribute
        to them that provides a brief description of the item.

        .. code-block :: python

            print(network.controller_state.error.doc)
            print(network.controller_state.command.doc)
            print(network.controller_state.state.doc)

        :return: command state
        :rtype: state.State
        """
        return self._command_state

    @utils.logit
    def start(self):
        """
        Start the network object :
            - add a watcher
            - add a driver

        """
        from .controller import ZWaveController  # NOQA
        from .node import ZWaveNode
        from .manager import ZWaveManager

        if self._started is True:
            return

        logger.info("starting Z-Wave network.")

        self._notification_handler = (
            notification_handler.NotificationHandler(self)
        )
        self._notification_handler.start()

        if hasattr(self._xml_handler, 'Controller'):
            id_ = self._xml_handler.Controller['id']

            self._controller = ZWaveController(
                id_,
                self,
                self._xml_handler.Controller,
                None
            )

            self.nodes[id_] = self._controller

            waiting_for_parents = {}
            for node in self._xml_handler.Nodes:
                if node['id'].endswith('.1'):
                    self.nodes[node['id']] = ZWaveNode(
                        node['id'],
                        self,
                        node,
                        None
                    )

                    for child in waiting_for_parents.pop(node['id'], []):
                        self.nodes[child['id']] = ZWaveNode(
                            child['id'],
                            self, child,
                            self.nodes[node['id']]
                        )
                else:
                    parent_id = node['id'].split('.')[0] + '.1'
                    if parent_id in self.nodes:
                        self.nodes[node['id']] = ZWaveNode(
                            node['id'],
                            self,
                            node,
                            self.nodes[parent_id]
                        )
                    else:
                        if parent_id not in waiting_for_parents:
                            waiting_for_parents[parent_id] = []

                        waiting_for_parents[parent_id] += [node]

            def _do():
                signals.SIGNAL_NETWORK_DATASET_LOADED.send(
                    sender=self,
                    network=self,
                    controller=self._controller
                )

            self._notification_handler.add(_do)

        if self._manager is None:
            self._manager = ZWaveManager(self)
            self._manager.create()

        self._started = True
        self._manager.addWatcher(self._zwcallback)
        self._manager.addDriver(self._options.device)

    @utils.logit
    def stop(self):
        """
        Stop the network object.

            * remove the watcher
            * remove the driver
            * clear the nodes
        """

        if not self._started:
            return

        def _do():
            logger.info("shutting down Z-Wave network.")

            # self.write_config()

            logger.debug('destroying locations')

            for location in self.locations:
                location.destroy()

            self._locations_loaded.clear()

            logger.debug('destroying nodes')
            for node in list(self)[:]:
                if not node.is_openzwave_controller:
                    node.destroy()

                del self.nodes[node.id]

            if self._controller is not None:
                event = threading.Event()

                logger.debug('stopping controller')
                if self._controller._timer_statistics is not None:  # NOQA
                    self._controller._timer_statistics.cancel()  # NOQA

                logger.debug('canceling controller commands')
                self._controller.cancel_command()

                logger.info(
                    'waiting for send queue to empty, '
                    'this can take up to 60 seconds'
                )

                num_queued = self._controller.send_queue_count
                last_num_queued = 0

                count = 0

                while num_queued > 0 and count < 60:

                    if num_queued != last_num_queued:
                        last_num_queued = num_queued
                        logger.info(
                            'Send queue has %s items remaining.',
                            num_queued
                        )
                    event.wait(1.0)
                    count += 1

                    num_queued = self._controller.send_queue_count

                if count == 60 and num_queued:
                    logger.info(
                        'send queue did not empty %s items remaining.',
                        num_queued
                    )
                else:
                    logger.info('send queue empty')

                logger.debug('controller stopped')

                self._controller.destroy()
                self._controller = None
            else:
                logger.debug('controller was already stopped')

            logger.debug('removing watcher')
            self._manager.removeWatcher(self._zwcallback)
            logger.debug('watcher removed')

            logger.debug('removing driver')
            self._manager.removeDriver(self._options.device)
            logger.debug('driver removed')

            self._started = False
            self._state = self.STATE_STOPPED

            signals.SIGNAL_NETWORK_STOPPED.send(
                sender=self,
                network=self,
            )

            logger.debug('stopping network notification handler')
            self._notification_handler.stop()
            logger.debug('network notification handler stopped')
            self._notification_handler = None

            logger.info("shutdown complete.")

        self._notification_handler.add(_do)

    @property
    def driver_stats(self):
        """
        Retrieve statistics from driver.

        Statistics:

            * SOFCnt: Number of SOF bytes received
            * ACKWaiting: Number of unsolicited messages while waiting for
              an ACK
            * readAborts: Number of times read were aborted due to timeouts
            * badChecksum: Number of bad check sums
            * readCnt: Number of messages successfully read
            * writeCnt: Number of messages successfully sent
            * CANCnt: Number of CAN bytes received
            * NAKCnt: Number of NAK bytes received
            * ACKCnt: Number of ACK bytes received
            * OOFCnt: Number of bytes out of framing
            * dropped: Number of messages dropped & not delivered
            * retries: Number of messages retransmitted
            * controllerReadCnt: Number of controller messages read
            * controllerWriteCnt: Number of controller messages sent

        :return: Statistics of the controller
        :rtype: _libopenzwave.DriverStats
        """
        return self._manager.getDriverStatistics(self.home_id)

    @utils.logit
    def destroy(self):
        """
        Destroy the network and all related stuff.
        """

        self._manager.destroy()
        self._options.destroy()
        self._manager = None
        self._options = None

    @property
    def home_id(self):
        """
        Gets the home_id of the network.

        :rtype: int
        """

        if self._object_id is None:
            return 0
        return self._object_id

    @property
    def home_id_str(self):
        """
        The home_id of the network as string.

        :rtype: str
        """
        return "0x%0.8X" % self.home_id

    @property
    def locations(self):
        """
        The locations that are in the network.

        This property iterates over all of the nodes in the network getting
        the location name assigned to each node. it then yields a
        :py:class:`libopenzwave.location.Location` instance for each unique name.

        You have the ability to iterate over the location instance to get the
        nodes that are in that location.

        This is a very handy property for any applications that provide a UI
        that displays rooms and then in the rooms the nodes in that room.

        :return: `list` of :py:class:`libopenzwave.location.ZWaveLocation` instances
        :rtype: List[ZWaveLocation]
        """

        from .location import ZWaveLocation  # NOQA

        for loc_xml in self._xml_handler.Locations:
            if loc_xml['name'] == 'No Location':
                break
        else:
            loc_xml = None

        no_location = ZWaveLocation('No Location', self, loc_xml)

        self._locations_loaded.add(no_location)

        locations = set()

        for node in self:
            locations.add(node.location)
        res = []

        for location in sorted(loc for loc in locations):
            for loc_xml in self._xml_handler.Locations:
                if loc_xml['name'] == location:
                    break
            else:
                loc_xml = None

            location = ZWaveLocation(location, self, loc_xml)
            self._locations_loaded.add(location)
            res += [location]

        return res

    @property
    def is_ready(self):
        """
        Says if the network is ready for operations.

        :rtype: bool
        """
        return self._state >= self.STATE_READY

    @property
    def state(self):
        """
        Gets the state of the network.

        Values may be changed in the future, only order is important.
        You can safely ask node information when state >= STATE_READY

        * STATE_STOPPED: `0`
        * STATE_FAILED: `1`
        * STATE_RESET: `3`
        * STATE_STARTED: `5`
        * STATE_AWAKE: `7`
        * STATE_READY: `10`

        :rtype: state.StateItem
        """
        return self._state

    @utils.logit
    def add_node(self, do_security=False):
        """
        Start the Inclusion Process to add a Node to the Network.

        The Status of the Node Inclusion is communicated via Notifications.
        Specifically, you should monitor ControllerCommand Notifications.

        Results of the AddNode Command will be send as a Notification with the
        Notification type as Notification::Type_ControllerCommand

        :param do_security: Whether to initialize the Network Key on the device
            if it supports the Security CC
        :type do_security: bool

        :rtype: bool
        """
        logger.debug(
            'Send controller command : add_node, : secure : %s',
            do_security
        )
        return self.manager.addNode(self.home_id, do_security)

    @utils.logit
    def replace_failed_node(self, node):
        """
        Replace a failed device with another.

        If the node is not in the controller's failed nodes list, or the node
        responds, this command will fail.

        :param node: The node to replace.
        :type node: ZWaveNode

        :rtype: bool
        """
        logger.debug(
            'Send controller command : replace_failed_node, : node : %s',
            node.id
        )

        return self.manager.replaceFailedNode(self.home_id, node.id.node_id)

    @utils.logit
    def remove_node(self, node=None):
        """
        Remove a Device from the Z-Wave Network

        :param node: If a node is supplied then the node is going to be
            checked to see if it has failed. The Node should be on the
            Controllers Failed Node List, otherwise this command will fail.
            You can use the :py:attr:`libopenzwave.node.ZWaveNode.is_failed`
            property to test if the Controller believes the Node has Failed.

            If no node is supplied then the
            network will be set into exclusion mode.

        :type node: optional, ZWaveNode

        """

        if node is None:
            logger.debug('Send controller command : remove_node')
            return self.manager.removeNode(self.home_id)
        else:
            logger.debug(
                'Send controller command : remove_failed_node, : node : %s',
                node.id
            )

            return self.manager.removeFailedNode(self.home_id, node.id.node_id)

    @property
    def manager(self):
        """
        The manager to use to communicate with the lib c++.

        :rtype: ZWaveManager
        """
        if self._manager is not None:
            return self._manager
        else:
            raise ZWaveException("Manager not initialised")

    @property
    def controller(self):
        """
        The controller of the network.

        :return: The controller of the network
        :rtype: ZWaveController
        """
        return self._controller

    @property
    def nodes(self):
        """
        The nodes of the network.

        :rtype: dict
        """
        return self._nodes

    @property
    def as_dict(self):
        """
        Return a dict representation of the network.

        :returns: A dict
        :rtype: dict

        """
        res = dict(
            state=dict(id=int(self.state), doc=self.state.doc),
            home_id=self.home_id,
            home_id_str=self.home_id_str,
            nodes_count=self.nodes_count,
            nodes=list(node.as_dict for node in self.nodes.values())
        )
        return res

    @utils.logit
    def test(self, count=1):
        """
        Send a number of test messages to every node and record results.

        :param count: The number of test messages to send.
        :type count: int
        """
        self.manager.testNetwork(self.home_id, count)

    @utils.logit
    def heal(self, update_return_routes=False):
        """
        Heal network by requesting nodes rediscover their neighbors.
        Sends a ControllerCommand_RequestNodeNeighborUpdate to every node.
        Can take a while on larger networks.

        :param update_return_routes: Whether to perform return routes
            initialization.
            (default = False).
        :type update_return_routes: bool, optional

        :return: `True` is the ControllerCommand ins sent. `False` otherwise
        :rtype: bool
        """
        if self.network.state < self.network.STATE_AWAKE:
            logger.warning('Network must be awake')
            return False

        self.manager.healNetwork(self.home_id, update_return_routes)
        return True

    @property
    def id_separator(self):
        """
        Gets/Sets the separator in id representation.

        :param value: The new separator
        :type value: chr

        :rtype: chr
        """
        return self._id_separator

    @id_separator.setter
    def id_separator(self, value):
        self._id_separator = value

    @property
    def nodes_count(self):
        """
        The nodes count of the network.

        :rtype: int
        """
        return len(self.nodes)

    @property
    def sleeping_nodes_count(self):
        """
        The count of sleeping nodes on the network.

        :rtype: int
        """
        result = 0
        for node in self.nodes.values():
            if node.is_sleeping:
                result += 1
        return result

    @utils.logit
    def get_poll_interval(self):
        """
        Get the time period between polls of a nodes state

        :return: The number of milliseconds between polls
        :rtype: int
        """
        return self.manager.getPollInterval()

    @utils.logit
    def set_poll_interval(self, milliseconds=500, interval_between_polls=True):
        """
        Set the time period between polls of a nodes state.

        Due to patent concerns, some devices do not report state changes
        automatically to the controller. These devices need to have their
        state polled at regular intervals. The length of the interval is the
        same for all devices. To even out the Z-Wave network traffic generated
        by polling, OpenZWave divides the polling interval by the number of
        devices that have polling enabled, and polls each in turn. It is
        recommended that if possible, the interval should not be set shorter
        than the number of polled devices in seconds (so that the network
        does not have to cope with more than one poll per second).

        :param milliseconds: The length of the polling interval in
            milliseconds.
        :type milliseconds: int

        :param interval_between_polls: If set to `True` (via SetPollInterval),
            the pollInterval will be interspersed between each poll
            (so a much smaller m_pollInterval like 100, 500, or 1,000 may be
            appropriate). If `False`, the library attempts to complete all
            polls within m_pollInterval.
        :type interval_between_polls: bool
        """
        self.manager.setPollInterval(milliseconds, interval_between_polls)

    @utils.logit
    def _zwcallback(self, notif):
        # noinspection PyPep8
        """
        The Callback Handler used with the libopenzwave.
        """
        logger.debug('zwcallback notif=%s', notif)

        if notif == PyNotifications.DriverFailed:
            def _do():
                for n in self._nodes.values():
                    n.destroy()

                self._nodes.clear()
                self._manager = None
                self._state = self.STATE_FAILED

                signals.SIGNAL_NETWORK_FAILED.send(
                    sender=self,
                    network=self
                )
                self._controller = None

            self._notification_handler.add(_do)
            self._notification_handler.stop()

        elif notif == PyNotifications.DriverReady:

            from .controller import ZWaveController

            id_ = notif.home_id
            if id_ != self._object_id:
                self._xml_handler['home_id'] = '0x{0:X}'.format(id_)

            self._object_id = id_

            if self._controller is None:
                node_id = str(notif.node_id) + '.1'
                self._controller = self.nodes[node_id] = (
                    ZWaveController(node_id, self, None, None)
                 )

            self._state = self.STATE_STARTED

            logger.info(
                'home_id 0x%0.8x, controller node id is %d',
                self.home_id,
                notif.node_id
            )
            logger.info(
                'connected to Z-Wave network using library %s',
                self._controller.library_description
            )

            signals.SIGNAL_NETWORK_STARTED.send(
                sender=self,
                network=self,
                controller=self._controller
            )

        elif notif == PyNotifications.DriverReset:
            event = threading.Event()

            def _do():
                for n in self._nodes:
                    n.destroy()

                self._nodes.clear()
                self._state = self.STATE_RESET

                signals.SIGNAL_NETWORK_RESET.send(
                    sender=self,
                    network=self,
                    controller=self._controller
                )
                logger.debug(
                    'Z-Wave network driver has been reset. resetting nodes.'
                )
                event.set()

            self._notification_handler.add(_do)
            event.wait()

        elif notif == PyNotifications.DriverRemoved:
            event = threading.Event()

            def _do():
                for n in self._nodes:
                    n.destroy()

                self.nodes.clear()
                self._state = self.STATE_STOPPED
                self._manager = None
                self._controller = None

                signals.SIGNAL_NETWORK_STOPPED.send(sender=self, network=self)
                event.set()

            self._notification_handler.add(_do)
            event.wait()

        elif notif == PyNotifications.ManufacturerSpecificDBReady:
            def _do(n):
                signals.SIGNAL_NETWORK_MANUFACTURER_DB_READY.send(
                    sender=self,
                    network=self,
                    notif=n
                )

            self._notification_handler.add(_do, notif)

        elif notif in (
            PyNotifications.AllNodesQueriedSomeDead,
            PyNotifications.AwakeNodesQueried,
            PyNotifications.AllNodesQueried
        ):
            import time
            handlers = notification_handler.NotificationHandler.node_handlers
            while True:
                for handler in handlers:
                    if handler.is_busy:
                        time.sleep(0.01)
                        break
                else:
                    break

            if notif == PyNotifications.AllNodesQueried:

                def _do():
                    self._state = self.STATE_READY

                    dead = []
                    sleeping = []
                    awake = []

                    for nd in self.nodes.values():
                        if nd.is_failed:
                            dead += [nd]
                        elif nd.is_awake:
                            awake += [nd]
                        else:
                            sleeping += [nd]

                    signals.SIGNAL_NODES_LOADED.send(
                        sender=self,
                        network=self,
                        controller=self._controller,
                        sleeping=sleeping,
                        dead=dead,
                        awake=awake

                    )
                    signals.SIGNAL_NODES_LOADED_ALL.send(
                        sender=self,
                        network=self,
                        controller=self._controller
                    )
                    signals.SIGNAL_NETWORK_READY.send(
                        sender=self,
                        network=self
                    )

                self._notification_handler.add(_do)

            elif notif == PyNotifications.AwakeNodesQueried:

                def _do(home_id):
                    self._object_id = home_id
                    if self._state < self.STATE_AWAKE:
                        self._state = self.STATE_AWAKE

                    dead = []
                    sleeping = []
                    awake = []

                    for nd in self.nodes.values():
                        if nd.is_failed:
                            dead += [nd]
                        elif nd.is_awake:
                            awake += [nd]
                        else:
                            sleeping += [nd]

                    signals.SIGNAL_NODES_LOADED.send(
                        sender=self,
                        network=self,
                        controller=self._controller,
                        sleeping=sleeping,
                        dead=dead,
                        awake=awake

                    )
                    signals.SIGNAL_NODES_LOADED_AWAKE.send(
                        sender=self,
                        network=self,
                        controller=self._controller,
                        sleeping=sleeping
                    )
                    signals.SIGNAL_NETWORK_READY.send(
                        sender=self,
                        network=self
                    )

                self._notification_handler.add(_do, notif.home_id)

            elif notif == PyNotifications.AllNodesQueriedSomeDead:

                def _do(home_id):
                    self._object_id = home_id
                    self._state = self.STATE_READY

                    dead = []
                    sleeping = []
                    awake = []

                    for nd in self.nodes.values():
                        if nd.is_failed:
                            dead += [nd]
                        elif nd.is_awake:
                            awake += [nd]
                        else:
                            sleeping += [nd]

                    signals.SIGNAL_NODES_LOADED.send(
                        sender=self,
                        network=self,
                        controller=self._controller,
                        sleeping=sleeping,
                        dead=dead,
                        awake=awake

                    )
                    signals.SIGNAL_NODES_LOADED_SOME_DEAD.send(
                        sender=self,
                        network=self,
                        controller=self._controller,
                        dead=dead
                    )
                    signals.SIGNAL_NETWORK_READY.send(
                        sender=self,
                        network=self
                    )

                self._notification_handler.add(_do, notif.home_id)

        # elif notif == PyNotifications.MsgComplete:
        #     self._notification_handler.add(
        #         signals.SIGNAL_MSG_COMPLETE.send,
        #         sender=self,
        #         network=self,
        #     )

        elif notif == PyNotifications.ControllerCommand:
            self._handle_controller_command(notif)

        elif notif == PyNotifications.NodeAdded:
            if str(notif.node_id) + '.1' not in list(self.nodes.keys()):
                self._pending_node_addition[notif.node_id] = []

        elif notif == PyNotifications.EssentialNodeQueriesComplete:
            def _do(node_id_):
                n_id = str(node_id_) + '.1'

                if n_id in list(self.nodes.keys()):
                    nd = self.nodes[n_id]
                else:
                    from .node import ZWaveNode

                    nd = self.nodes[n_id] = ZWaveNode(n_id, self, None, None)

                nd._update_dataset()  # NOQA

                signals.SIGNAL_NODE_LOADING_ESSENTIAL.send(
                    sender=self,
                    network=self.network,
                    controller=self.network.controller,
                    node=nd
                )
                pending_notifications = (
                    self._pending_node_addition.pop(node_id_, [])
                )

                for item in pending_notifications:
                    self._zwcallback(item)

            self._notification_handler.add(_do, notif.node_id)

        elif notif.node_id != 0:
            if notif == PyNotifications.NodeNew:
                def _do(node_id_):
                    signals.SIGNAL_NODE_NEW.send(
                        sender=self,
                        network=self,
                        controller=self._controller,
                        node_id=node_id_
                    )

                self._notification_handler.add(_do, notif.node_id)

            else:
                if notif.node_id in self._pending_node_addition:
                    self._pending_node_addition[notif.node_id] += [notif]
                else:
                    node = self.nodes[str(notif.node_id) + '.1']
                    node._handle_notification(notif)  # NOQA

        elif notif == PyNotifications.Notification:
            def _do(code):
                signals.SIGNAL_NOTIFICATION.send(
                    sender=self,
                    network=self,
                    controller=self._controller,
                    notification_code=code,
                )

            self._notification_handler.add(_do, notif.notification_code)

        elif notif == PyNotifications.UserAlerts:
            def _do(alert):
                if alert == signals.SIGNAL_ALERT_DNS_ERROR:
                    signals.SIGNAL_ALERT_DNS_ERROR.send(
                        sender=self,
                        network=self,
                    )
                elif alert == signals.SIGNAL_ALERT_UNSUPPORTED_CONTROLLER:
                    signals.SIGNAL_ALERT_UNSUPPORTED_CONTROLLER.send(
                        sender=self,
                        network=self,
                    )
                elif alert == signals.SIGNAL_ALERT_APPLICATION_STATUS_RETRY:
                    signals.SIGNAL_ALERT_APPLICATION_STATUS_RETRY.send(
                        sender=self,
                        network=self,
                    )
                elif alert == signals.SIGNAL_ALERT_APPLICATION_STATUS_QUEUED:
                    signals.SIGNAL_ALERT_APPLICATION_STATUS_QUEUED.send(
                        sender=self,
                        network=self,
                    )

                elif alert == signals.SIGNAL_ALERT_APPLICATION_STATUS_REJECTED:
                    signals.SIGNAL_ALERT_APPLICATION_STATUS_REJECTED.send(
                        sender=self,
                        network=self,
                    )

            self._notification_handler.add(_do, notif.user_alert)

        # elif notif_type == self.SIGNAL_NODE_READY:
        #     self._handleNodeReady,
        else:
            logger.warning('Skipping unhandled notification [%s]', notif)

    @utils.logit
    def _handle_controller_command(self, notif):
        """
        Called when a message from controller is sent.

        :param notif: data sent by the notification
        """
        logger.debug('Z-Wave ControllerCommand : %s', notif)

        controller_state = notif.controller_state
        error = notif.controller_error
        command = notif.controller_command
        node_id = notif.node_id

        if node_id != 0 and node_id in self.nodes:
            sender = self.nodes[node_id]
        else:
            sender = self

        stat = state.State(
            sender,
            command=command,
            state=controller_state,
            error=error
        )

        def _do(st):
            st.node._command_state = st

            if st.node == self:
                signals.SIGNAL_NETWORK_CONTROLLER_COMMAND.send(
                    sender=st.node,
                    network=self,
                    controller=self._controller,
                    state=st
                )

            else:
                signals.SIGNAL_NODE_CONTROLLER_COMMAND.send(
                    sender=st.node,
                    network=self,
                    controller=self._controller,
                    node=st.node,
                    state=st
                )
            # SIGNAL_NODE_RESET = signals.SIGNAL_NODE_RESET

        self._notification_handler.add(_do, stat)

    @utils.logit
    def check_latest_mfs_revision(self):
        """
        Check the Latest Revision of the Manufacturer_Specific.xml file.

        optionally update to the latest version.
        Outdated Config Revisions are signaled via Notifications

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self._network.manager.checkLatestMFSRevision(self.home_id)

    @utils.logit
    def download_latest_mfs_revision(self):
        """
        Download the latest Config File Revision.

        The ManufacturerSpecific File will be updated, and any new Config
        Files will also be downloaded. Existing Config Files will not be
        checked/updated.

        Errors are signaled via Notifications

        :return: `True` if the request was sent successfully.
        :rtype: bool
        """
        return self.manager.downloadLatestMFSRevision(self.home_id)
