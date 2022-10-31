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
:synopsis: ZWave Controller node API

.. moduleauthor:: Kevin G Schlosser
"""

import os
import logging
import zipfile
import tempfile
import threading
import shutil
import time
from urllib.request import urlopen


from . import singleton
from .node import ZWaveNode
from . import utils
from . import xml_handler  # NOQA
import _libopenzwave


logger = logging.getLogger(__name__)


class ZWaveController(ZWaveNode, metaclass=singleton.InstanceSingleton):
    """
    The controller manager.

    Allows to retrieve information about the library, statistics, ...
    Also used to send commands to the controller

    Commands :

        * ControllerCommand_AddController: Add a new secondary controller to
          the Z-Wave network.
        * ControllerCommand_AddDevice: Add a new device (but not a controller)
          to the Z-Wave network.
        * ControllerCommand_CreateNewPrimary: (Not yet implemented)
        * ControllerCommand_ReceiveConfiguration:
        * ControllerCommand_RemoveController: remove a controller from the
          Z-Wave network.
        * ControllerCommand_RemoveDevice: remove a device (but not a
          controller) from the Z-Wave network.
        * ControllerCommand_RemoveFailedNode: move a node to the controller's
          list of failed nodes. The node must actually have failed or have
          been disabled since the command will fail if it responds. A node
          must be in the controller's failed nodes list or
          ControllerCommand_ReplaceFailedNode to work.
        * ControllerCommand_HasNodeFailed: Check whether a node is in the
          controller's failed nodes list.
        * ControllerCommand_ReplaceFailedNode: replace a failed device with
          another. If the node is not in the controller's failed nodes list,
          or the node responds, this command will fail.
        * ControllerCommand_TransferPrimaryRole: (Not yet implemented) - Add a
          new controller to the network and make it the primary. The existing
          primary will become a secondary controller.
        * ControllerCommand_RequestNetworkUpdate: Update the controller with
          network information from the SUC/SIS.
        * ControllerCommand_RequestNodeNeighborUpdate: Get a node to rebuild
          its neighbour list. This method also does
          ControllerCommand_RequestNodeNeighbors afterwards.
        * ControllerCommand_AssignReturnRoute: Assign a network return route
          to a device.
        * ControllerCommand_DeleteAllReturnRoutes: Delete all network return
          routes from a device.
        * ControllerCommand_CreateButton: Create a handheld button id.
        * ControllerCommand_DeleteButton: Delete a handheld button id.

    Callbacks :

        * ControllerState_Waiting: The controller is waiting for a user
          action. A notice should be displayed to the user at this point,
          telling them what to do next. For the add, remove, replace and
          transfer primary role commands, the user needs to be told to press
          the inclusion button on the device that is going to be added or
          removed. For ControllerCommand_ReceiveConfiguration, they must set
          their other controller to send its data, and for
          ControllerCommand_CreateNewPrimary, set the other controller to
          learn new data.
        * ControllerState_InProgress: the controller is in the process of
          adding or removing the chosen node. It is now too late to cancel the
          command.
        * ControllerState_Complete: the controller has finished adding or
          removing the node, and the command is complete.
        * ControllerState_Failed: will be sent if the command fails for any
          reason.
    """
    STATE_NORMAL = _libopenzwave.EnumItem('Normal').set(0, 'Normal')
    STATE_STARTING = _libopenzwave.EnumItem('Starting').set(1, 'Starting')
    STATE_CANCEL = _libopenzwave.EnumItem('Cancel').set(2, 'Cancel')
    STATE_ERROR = _libopenzwave.EnumItem('Error').set(3, 'Error')
    STATE_WAITING = _libopenzwave.EnumItem('Waiting').set(4, 'Waiting')
    STATE_SLEEPING = _libopenzwave.EnumItem('Sleeping').set(5, 'Sleeping')
    STATE_INPROGRESS = _libopenzwave.EnumItem(
        'InProgress'
    ).set(6, 'In Progress')
    STATE_COMPLETED = _libopenzwave.EnumItem('Completed').set(7, 'Completed')
    STATE_FAILED = _libopenzwave.EnumItem('Failed').set(8, 'Failed')
    STATE_NODEOK = _libopenzwave.EnumItem('NodeOK').set(9, 'Node OK')
    STATE_NODEFAILED = _libopenzwave.EnumItem(
        'NodeFailed'
    ).set(10, 'Node Failed')

    ERROR_NONE = _libopenzwave.PyControllerError.None_
    ERROR_BUTTON_NOT_FOUND = _libopenzwave.PyControllerError.ButtonNotFound
    ERROR_NODE_NOT_FOUND = _libopenzwave.PyControllerError.NodeNotFound
    ERROR_NOT_BRIDGE = _libopenzwave.PyControllerError.NotBridge
    ERROR_NOT_SUC = _libopenzwave.PyControllerError.NotSUC
    ERROR_NOT_SECONDARY = _libopenzwave.PyControllerError.NotSecondary
    ERROR_NOT_PRIMARY = _libopenzwave.PyControllerError.NotPrimary
    ERROR_IS_PRIMARY = _libopenzwave.PyControllerError.IsPrimary
    ERROR_NOT_FOUND = _libopenzwave.PyControllerError.NotFound
    ERROR_BUSY = _libopenzwave.PyControllerError.Busy
    ERROR_FAILED = _libopenzwave.PyControllerError.Failed
    ERROR_DISABLED = _libopenzwave.PyControllerError.Disabled
    ERROR_OVERFLOW = _libopenzwave.PyControllerError.Overflow
    ERROR_LOCKED = _libopenzwave.EnumItem(
        'Locked'
    ).set(13, "Controller is busy")

    SIGNAL_CONTROLLER_STATS = (
        _libopenzwave.NotificationItem(
            'ControllerStats'
        ).set(0, 'Controller Stats')
    )

    def __init__(
        self,
        id_,
        network=None,
        xml_data=None,
        parent_node=None,
        *_,
        **__
    ):
        """
        Initialize controller object
        
        :param id_:
        :type id_: int
        
        :param network:
        :type network: ZWaveNetwork, optional
        
        :param xml_data:
        :type xml_data: xml_handler.XMLElement, optional
        
        :param parent_node:
        :type parent_node: ZWaveNode, optional
        
        :param *_:

        :param **__:
        """

        ZWaveNode.__init__(
            self,
            id_,
            network,
            xml_data=xml_data,
            parent_node=parent_node
        )

        self._options = network.options
        self._library_type_name = None
        self._library_version = None
        self._python_library_version = None
        self._timer_statistics = None
        self._interval_statistics = 0.0
        self._ctrl_lock = threading.Lock()
        # self._manager_last = None
        self._ctrl_last_state = self.STATE_NORMAL
        self._ctrl_last_message = ""
        self.STATES_LOCKED = [
            self.STATE_STARTING,
            self.STATE_WAITING,
            self.STATE_SLEEPING,
            self.STATE_INPROGRESS
        ]
        self.STATES_UNLOCKED = [
            self.STATE_NORMAL,
            self.STATE_CANCEL,
            self.STATE_ERROR,
            self.STATE_COMPLETED,
            self.STATE_FAILED,
            self.STATE_NODEOK,
            self.STATE_NODEFAILED
        ]

    def _update_dataset(self):

        self.network.xml_handler['library_type_name'] = (
            self._manager.getLibraryTypeName(self.home_id)
        )
        self.network.xml_handler['library_version'] = (
            self._manager.getLibraryVersion(self.home_id)
        )
        self.network.xml_handler['python_library_flavor'] = (
            self._manager.getPythonLibraryFlavor()
        )
        self.network.xml_handler['python_library_version'] = (
            self._manager.getPythonLibraryVersionNumber()
        )
        self.network.xml_handler['python_library_config_version'] = (
            self._get_config_version()
        )
        self.network.xml_handler['ozw_library_version'] = (
            self._manager.getOzwLibraryVersion()
        )

        handler = self._xml_handler

        if handler is None:
            ZWaveNode._update_dataset(self)
            handler = self._xml_handler
            handler.parent.remove(handler)
            handler.tag = 'Controller'
            self.network.xml_handler.insert(0, handler)

            handler['primary_controller'] = (
                self._manager.isPrimaryController(self.home_id)
            )
            handler['static_update_controller'] = (
                self._manager.isStaticUpdateController(self.home_id)
            )
            handler['bridge_controller'] = (
                self._manager.isBridgeController(self.home_id)
            )

            self._xml_handler = handler

    @utils.logit
    def destroy(self):
        self._update_dataset()

        logger.debug('destroying controller')

        logger.debug('destroying controller values')
        for value in self:
            value.destroy()

        if self._notification_handler.is_owner_object(self):
            logger.debug(
                'Node {0}: Stopping Notification Handler'.format(self.id)
            )
            self._notification_handler.stop()

        logger.debug('controller destroyed')

    @property
    def id(self):
        """
        The id of the controller on the network.

        :return: The node id of the controller on the network
        :rtype: NodeId
        """
        return self._object_id

    @property
    def library_type_name(self):
        """
        The name of the library.

        :return: The cpp library name
        :rtype: str
        """
        if 'library_type_name' in self.network.xml_handler:
            return self.network.xml_handler['library_type_name']
        else:
            return self._manager.getLibraryTypeName(self.home_id)

    @property
    def library_description(self):
        """
        The description of the library.

        :return: The library description (name and version)
        :rtype: str
        """
        return (
            '{0} version {1}'.format(
                self.library_type_name,
                self.library_version
            )
        )

    @property
    def library_version(self):
        """
        The version of the library.

        :return: The cpp library version
        :rtype: str
        """
        if 'library_version' in self.network.xml_handler:
            return self.network.xml_handler['library_version']
        else:
            return self._manager.getLibraryVersion(self.home_id)

    @property
    def python_library_flavor(self):
        """
        The flavor of the python library.

        :return: The python library flavor
        :rtype: str
        """
        if 'python_library_flavor' in self.network.xml_handler:
            return self.network.xml_handler['python_library_flavor']
        else:
            return self._manager.getPythonLibraryFlavor()

    @property
    def python_library_version(self):
        """
        The version of the python library.

        :return: The python library version
        :rtype: str
        """
        if 'python_library_version' in self.network.xml_handler:
            return self.network.xml_handler['python_library_version']
        else:
            return self._manager.getPythonLibraryVersionNumber()

    @property
    def python_library_config_version(self):
        """
        The version of the config for python library.

        :return: The python library config version
        :rtype: str
        """

        if 'python_library_config_version' in self.network.xml_handler:
            return self.network.xml_handler['python_library_config_version']
        else:
            return self._get_config_version()

    def _get_config_version(self):
        tversion = "Original {0}".format(self.library_version)
        fversion = os.path.join(
            self.library_config_path,
            'pyozw_config.version'
        )
        if os.path.isfile(fversion):
            with open(fversion) as f:
                val = f.read()
            tversion = "Git %s" % val
        return tversion

    @property
    def ozw_library_version(self):
        """
        The version of the openzwave library.

        :return: The openzwave library version
        :rtype: str
        """
        if 'ozw_library_version' in self.network.xml_handler:
            return self.network.xml_handler['ozw_library_version']
        else:
            return self._manager.getOzwLibraryVersion()

    @property
    def library_config_path(self):
        """
        The library Config path.

        :return: The library config directory
        :rtype: str
        """
        if self._options is not None:
            return self._options.config_path
        else:
            return None

    @property
    def library_user_path(self):
        """
        The library User path.

        :return: The user directory to store user configuration
        :rtype: str
        """
        if self._options is not None:
            return self._options.user_path
        else:
            return None

    @property
    def device(self):
        """
        The device path.

        :return: The device (ie /dev/zwave)
        :rtype: str
        """
        if self._options is not None:
            return self._options.device
        else:
            return None

    @property
    def options(self):
        """
        The starting options of the manager.

        :return: The options used to start the manager
        :rtype: ZWaveOption
        """
        return self._options

    @property
    def stats(self):
        """
        Retrieve statistics from driver.

        :return: A class object containing statistics.

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
            * `sentCnt`: Number of messages sent from this node.
            * `sentFailed`: Number of sent messages failed.
            * `retries`: Number of message retries.
            * `receivedCnt`: Number of messages received from this node.
            * `receivedDups`: Number of duplicated messages received.
            * `receivedUnsolicited`: Number of messages received
              unsolicited.
            * `sentTS`: Last message sent time.
            * `receivedTS`: Last message received time.
            * `lastRequestRTT`: Last message request RTT.
            * `averageRequestRTT`: Average Request Round Trip Time (ms).
            * `lastResponseRTT`: Last message response RTT.
            * `averageResponseRTT`: Average response round trip time.
            * `quality`: Node quality measure.
            * `lastReceivedMessage`: Place to hold last received message.

        :rtype: _libopenzwave.DriverStats
        """
        if self.home_id in (None, 0):
            return None

        driver_stats = self._manager.getDriverStatistics(self.home_id)
        # noinspection PyArgumentList
        node_stats = ZWaveNode.stats.fget(self)

        for key, value in node_stats.__dict__.items():
            if key.startswith('_'):
                continue

            driver_stats.__dict__[key] = value

        return driver_stats

    @utils.logit
    def do_poll_statistics(self):
        """
        Timer based polling system for statistics
        """
        self._timer_statistics = None
        stats = self.stats
        self.SIGNAL_CONTROLLER_STATS.send(
            sender=self,
            controller=self,
            stats=stats
        )

        self._timer_statistics = threading.Timer(
            self._interval_statistics,
            self.do_poll_statistics
        )
        self._timer_statistics.start()

    @property
    @utils.logit
    def poll_stats(self):
        """
        Get/Set the interval for polling statistics

        :param value: The interval in seconds
        :type value: float

        :return: The interval in seconds
        :rtype: float
        """
        return self._interval_statistics

    @poll_stats.setter
    @utils.logit
    def poll_stats(self, value):
        if value != self._interval_statistics:
            if self._timer_statistics is not None:
                self._timer_statistics.cancel()
            if value != 0:
                self._interval_statistics = value
                self._timer_statistics = threading.Timer(
                    self._interval_statistics,
                    self.do_poll_statistics
                )
                self._timer_statistics.start()

    @property
    def is_primary_controller(self):
        """
        Is this node a primary controller of the network.

        :return: `True`/`False`
        :rtype: bool
        """
        return self._manager.isPrimaryController(self.home_id)

    @property
    def is_static_update_controller(self):
        """
        Is this controller a static update controller (SUC).

        :return: `True`/`False`
        :rtype: bool
        """
        return self._manager.isStaticUpdateController(self.home_id)

    @property
    def is_bridge_controller(self):
        """
        Is this controller using the bridge controller library.

        :return: `True`/`False`
        :rtype: bool
        """
        return self._manager.isBridgeController(self.home_id)

    @property
    def send_queue_count(self):
        """
        Get count of messages in the outgoing send queue.

        :return: The count of messages in the outgoing send queue.
        :rtype: int
        """
        if self.home_id is not None:
            return self._manager.getSendQueueCount(self.home_id)
        return -1

    @utils.logit
    def hard_reset(self):
        """
        Hard Reset a PC Z-Wave Controller.

        Resets a controller and erases its network configuration settings.
        The controller becomes a primary controller ready to add devices to a
        new network.

        This command fires a lot of signals.

        :return: `True` if the command was executed
        :rtype: bool
        """
        self._network.state = self._network.STATE_RESET
        self._network.SIGNAL_NETWORK_RESET.send(
            sender=self,
            network=self._network
        )
        return self._manager.resetController(self.home_id)

    @utils.logit
    def soft_reset(self):
        """
        Soft Reset a PC Z-Wave Controller.

        Resets a controller without erasing its network configuration settings.

        :return: `True` if the command was executed
        :rtype: bool
        """
        return self._manager.softResetController(self.home_id)

    @utils.logit
    def create_new_primary(self):
        """
        Create a new primary controller when old primary fails.

        Requires SUC.

        This command creates a new Primary Controller when the Old Primary has
        Failed. Requires a SUC on the network to function.

        :return: `True` if the command was executed
        :rtype: bool
        """
        logger.debug('Send controller command : create_new_primary')

        return self._manager.createNewPrimary(self.home_id)

    @utils.logit
    def transfer_primary_role(self):
        """
        Add a new controller to the network and make it the primary.

        The existing primary will become a secondary controller.

        :return: `True` if the command was executed
        :rtype: bool
        """
        logger.debug('Send controller command : transfer_primary_role')

        return self._manager.transferPrimaryRole(self.home_id)

    @utils.logit
    def replication_send(self, node_):
        """
        Send information from primary to secondary

        :param node_: The secondary controller to send to
        :type node_: node.ZWaveNode

        :return: `True` if the command was executed
        :rtype: bool
        """
        logger.debug(
            'Send controller command : replication_send, : node : %s', '',
            node_.id
        )

        return self._network.manager.replicationSend(
            self.home_id,
            node_.id.node_id
        )

    @utils.logit
    def receive_configuration(self):
        """
        Receive network configuration information from primary controller.

        Requires secondary.

        This command prepares the controller to receive Network Configuration
        from a Secondary Controller.

        Results of the ReceiveConfiguration Command will be send as a
        Notification with the Notification type as
        Notification::Type_ControllerCommand

        :return: True if the request was sent successfully.
        :rtype: bool
        """
        logger.debug('Send controller command : receive_configuration')
        return self._manager.receiveConfiguration(self.home_id)

    @utils.logit
    def cancel_command(self):
        """
        Cancels any in-progress command running on a controller.

        :return: `True` if the command was executed
        :rtype: bool
        """

        if self.home_id is not None:
            return self._network.manager.cancelControllerCommand(self.home_id)

        return False

    @property
    def as_dict(self):
        """Return a dict representation of the controller.

        :returns: A dict
        :rtype: dict
        """

        # noinspection PyArgumentList
        ret = ZWaveNode.as_dict.fget(self)
        ret['capabilities'] = self.capabilities
        ret['library_version'] = self.library_version
        ret['library_description'] = self.library_description
        ret['library_type_name'] = self.library_type_name
        ret['library_user_path'] = self.library_user_path
        ret['library_config_path'] = self.library_config_path
        ret['ozw_library_version'] = self.ozw_library_version
        ret['python_library_config_version'] = (
            self.python_library_config_version
        )
        ret['python_library_version'] = self.python_library_version
        ret['device'] = self.device
        ret['is_primary_controller'] = self.is_primary_controller
        ret['is_static_update_controller'] = self.is_static_update_controller
        ret['is_bridge_controller'] = self.is_bridge_controller

        return ret

    @utils.logit
    def update_ozw_config(self):
        """
        Update the openzwave config from github.

        Not available for shared flavor as we don't want to update the config
        of the precompiled config.
        """
        if self.python_library_flavor in ['shared']:
            logger.warning(
                "Can't update_ozw_config for this flavor (%s).",
                self.python_library_flavor
            )
            return

        logger.info('Update_ozw_config from github.')

        dest = tempfile.mkdtemp()
        dest_file = os.path.join(dest, 'open-zwave.zip')

        try:
            req = urlopen(
                'https://codeload.github.com/OpenZWave/open-zwave/zip/master'
            )
            with open(dest_file, 'wb') as f:
                f.write(req.read())

            zip_ref = zipfile.ZipFile(dest_file)
            zip_ref.extractall(dest)
            zip_ref.close()

        except Exception:  # NOQA
            logger.exception("Can't get zip from github. Cancelling")
            try:
                shutil.rmtree(dest)
            except OSError:
                pass

        if os.path.isdir(self.library_config_path):
            # Try to remove old config
            try:
                shutil.rmtree(self.library_config_path)
            except OSError:
                logger.exception("Can't remove old config directory")

        try:
            shutil.copytree(
                os.path.join(dest, 'open-zwave-master', 'config'),
                self.library_config_path
            )
        except OSError:
            logger.exception("Can't copy to %s", self.library_config_path)

        version_path = os.path.join(
            self.library_config_path,
            'pyozw_config.version'
        )
        try:

            with open(version_path, 'w') as f:
                f.write(time.strftime("%Y-%m-%d %H:%M"))

        except OSError:
            logger.exception("Can't update %s", version_path)
        shutil.rmtree(dest)
