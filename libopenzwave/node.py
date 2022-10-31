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
:synopsis: ZWave node API

.. moduleauthor:: Kevin G Schlosser
"""

import threading
import logging
from .object import ZWaveObject
from .value import ZWaveValues
from . import notification_handler
from . import xml_handler
from .state import State
from .command_classes import COMMAND_CLASSES_  # NOQA
from .node_types import (
    Types,
    SpecificType,
    GenericType,
    BASIC_TYPE_CONTROLLER,
    BASIC_TYPE_SLAVE,
    BASIC_TYPE_STATIC_CONTROLLER
)
from . import signals
from . import utils


import _libopenzwave

PyNotifications = _libopenzwave.PyNotifications

logger = logging.getLogger(__name__)


# the ZWaveNodeInterface class is the starting point of a node creation.
# In the _handle_node_add method in the ZWaveNetwork class I replaced the
# node object ZWaveNode with ZWaveNodeInterface.

# the ZWaveNodeInterface class is a dummy class it is simply a shell to
# redirect the call made to create the instance to ZWaveNodeInterfaceMeta
# I have provided comments in the ZWaveNodeInterfaceMeta class that will walk
# you through what is happening
class ZWaveNodes(dict):

    def __init__(self):
        self.__lock = threading.RLock()
        dict.__init__(self)

    def __iter__(self):
        with self.__lock:
            return dict.__iter__(self)

    def values(self):
        with self.__lock:
            for item in dict.values(self):
                yield item

    def keys(self):
        with self.__lock:
            for item in dict.keys(self):
                yield item

    # noinspection PyMethodOverriding
    def get(self, key, default='^%#*&'):
        """
        :param key:
        :param default:
        """
        try:
            item = self[key]
        except KeyError:
            if default != '^%#*&':
                return default
            raise AttributeError(key)

        return item

    def __getitem__(self, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """
        with self.__lock:
            return dict.__getitem__(self, *args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """
        with self.__lock:
            dict.__setitem__(self, *args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """
        with self.__lock:
            dict.__delitem__(self, *args, **kwargs)

    def __contains__(self, item):
        """
        :param item:

        :rtype: bool
        """
        keys = list(self.keys())[:]
        return item in keys

    def pop(self, key, default='^%#*&'):
        """
        :param key:
        :param default:
        """
        try:
            item = self[key]
        except KeyError:
            if default != '^%#*&':
                return default
            raise AttributeError(key)

        del self[key]

        return item

    def popitem(self):
        with self.__lock:
            return dict.popitem(self)

    def update(self, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """
        with self.__lock:
            dict.update(self, *args, **kwargs)

    def items(self):
        with self.__lock:
            return dict.items(self)

    def clear(self):
        with self.__lock:
            return dict.clear(self)

    def fromkeys(self, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """
        with self.__lock:
            return dict.fromkeys(self, *args, **kwargs)

    def copy(self):
        with self.__lock:
            return dict.copy(self)


class NodeId(str):
    _node_id = 0
    _endpoint_id = 0

    @classmethod
    def __new__(cls, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """
        value = args[1]

        self = super(NodeId, cls).__new__(*args, **kwargs)

        node_id, endpoint_id = value.split('.')
        
        self._node_id = int(node_id)
        self._endpoint_id = int(endpoint_id)
        return self
        
    @property
    def node_id(self):
        """
        :rtype: int
        """
        return self._node_id
    
    @property
    def endpoint_id(self):
        """
        :rtype: int
        """
        return self._endpoint_id


class URLs(object):

    def __init__(self, node, xml_data):
        """
        :param node:
        :type node: "ZWaveNode"

        :param xml_data:
        :type xml_data: xml_handler.XMLElement
        """
        self._xml_handler = xml_data
        self._node = node
        self._network = node.network

    @property
    def node(self):
        """
        :rtype: "ZWaveNode"
        """
        return self._node

    @property
    def network(self):
        """
        :rtype: ZWaveNetwork
        """
        return self._network

    @property
    def xml_handler(self):
        """
        :rtype: xml_handler.XMLElement
        """
        return self._xml_handler

    @property
    def ozw_info(self):
        """
        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getMetaData(
                self._network.home_id,
                self._node.id.node_id,
                0
            )
        else:
            return self._xml_handler.OZWInfo.text

    @property
    def ozw_product(self):
        """
        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getMetaData(
                self._network.home_id,
                self._node.id.node_id,
                1
            )
        else:
            return self._xml_handler.OZWProduct.text

    @property
    def product_image(self):
        """
        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getMetaData(
                self._network.home_id,
                self._node.id.node_id,
                2
            )
        else:
            return self._xml_handler.ProuctImage.text

    @property
    def product_manual(self):
        """
        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getMetaData(
                self._network.home_id,
                self._node.id.node_id,
                4
            )
        else:
            return self._xml_handler.ProductManual.text

    @property
    def product(self):
        """
        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getMetaData(
                self._network.home_id,
                self._node.id.node_id,
                5
            )
        else:
            return self._xml_handler.Product.text

    @property
    def product_support(self):
        """
        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getMetaData(
                self._network.home_id,
                self._node.id.node_id,
                10
            )
        else:
            return self._xml_handler.ProductSupport.text

    def _update_dataset(self):
        if self._xml_handler is None:
            handler = xml_handler.XMLElement('URLs')
            self._node.xml_handler.URLs = handler
        else:
            handler = self._xml_handler

        manager = self._network.manager
        home_id = self._network.home_id
        node_id = self._node.id.node_id

        handler.OZWInfo = xml_handler.XMLElement('OZWInfo')
        ozw_info = manager.getMetaData(home_id, node_id, 0)
        if ozw_info.strip():
            handler.OZWInfo.text = ozw_info

        handler.OZWProduct = xml_handler.XMLElement('OZWProduct')
        ozw_product = manager.getMetaData(home_id, node_id, 1)
        if ozw_product.strip():
            handler.OZWProduct.text = ozw_product

        handler.ProductImage = xml_handler.XMLElement('ProductImage')
        product_image = manager.getMetaData(home_id, node_id, 2)
        if product_image.strip():
            handler.ProductImage.text = product_image

        handler.ProductManual = xml_handler.XMLElement('ProductManual')
        product_manual = manager.getMetaData(home_id, node_id, 4)
        if product_manual.strip():
            handler.ProductManual.text = product_manual

        handler.Product = xml_handler.XMLElement('Product')
        product = manager.getMetaData(home_id, node_id, 5)
        if product.strip():
            handler.Product.text = product

        handler.ProductSupport = xml_handler.XMLElement('ProductSupport')
        product_support = manager.getMetaData(home_id, node_id, 10)
        if product_support.strip():
            handler.ProductSupport.text = product_support

        self._xml_handler = handler


class Help(object):

    def __init__(self, node, xml_data):
        """
        :param node:
        :type node: "ZWaveNode"
        :param xml_data: xml_handler.XMLElement
        """
        self._xml_handler = xml_data
        self._node = node
        self._network = node.network

    @property
    def node(self):
        """
        :rtype: "ZWaveNode"
        """
        return self._node

    @property
    def network(self):
        """
        :rtype: ZWaveNetwork
        """
        return self._network

    @property
    def xml_handler(self):
        """
        :rtype: xml_handler.XMLElement
        """
        return self._xml_handler

    @property
    def inclusion(self):
        """
        :param value:
        :type value: str

        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getMetaData(
                self._network.home_id,
                self._node.id.node_id,
                6
            )
        else:
            return self._xml_handler.Inclusion.text

    @inclusion.setter
    def inclusion(self, value):
        if self._xml_handler is not None:
            self._xml_handler.Inclusion.text = value

    @property
    def exclusion(self):
        """
        :param value:
        :type value: str

        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getMetaData(
                self._network.home_id,
                self._node.id.node_id,
                7
            )
        else:
            return self._xml_handler.Exclusion.text

    @exclusion.setter
    def exclusion(self, value):
        if self._xml_handler is not None:
            self._xml_handler.Exclusion.text = value

    @property
    def reset(self):
        """
        :param value:
        :type value: str

        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getMetaData(
                self._network.home_id,
                self._node.id.node_id,
                8
            )
        else:
            return self._xml_handler.Reset.text

    @reset.setter
    def reset(self, value):
        if self._xml_handler is not None:
            self._xml_handler.Reset.text = value

    @property
    def wakeup(self):
        """
        :param value:
        :type value: str

        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getMetaData(
                self._network.home_id,
                self._node.id.node_id,
                9
            )
        else:
            return self._xml_handler.Wakeup.text

    @wakeup.setter
    def wakeup(self, value):
        if self._xml_handler is not None:
            self._xml_handler.Wakeup.text = value

    def _update_dataset(self):
        if self._xml_handler is None:
            handler = xml_handler.XMLElement('Help')
            self._node.xml_handler.Help = handler

            manager = self._network.manager
            home_id = self._network.home_id
            node_id = self._node.id.node_id

            handler.Inclusion = xml_handler.XMLElement('Inclusion')
            inclusion = manager.getMetaData(home_id, node_id, 6)
            if inclusion.strip():
                handler.Inclusion.text = inclusion

            handler.Exclusion = xml_handler.XMLElement('Exclusion')
            exclusion = manager.getMetaData(home_id, node_id, 7)
            if exclusion.strip():
                handler.Exclusion.text = exclusion

            handler.Reset = xml_handler.XMLElement('Reset')
            reset = manager.getMetaData(home_id, node_id, 8)
            if reset.strip():
                handler.Reset.text = reset

            handler.Wakeup = xml_handler.XMLElement('Wakeup')

            wakeup = manager.getMetaData(home_id, node_id, 9)
            if wakeup.strip():
                handler.Wakeup.text = wakeup

            self._xml_handler = handler

    
class ZWaveNode(ZWaveObject):
    """
    Represents a single Node within the Z-Wave Network.
    """

    def __init__(
        self,
        node_id,
        network,
        xml_data=None,
        parent_node=None,
        *_,
        **__
    ):
        """
        Initialize Z-Wave node

        :param node_id: ID of the node
        :type node_id: int

        :param network: The network object to access the manager
        :type network: ZWaveNetwork

        :param xml_data:
        :type xml_data: xml_handler.XMLElement, optional

        :param parent_node:
        :type parent_node: "ZWaveNode", optional

        :param *_:
        :param **__:
        """
        
        node_id = NodeId(node_id)
        
        logger.debug("Create object node (node_id:%s)", node_id)
        ZWaveObject.__init__(self, node_id, network, xml_data)
        self._command_state = None
        self._parent_node = parent_node
        self._is_ready = False
        # No cache management for values in nodes
        self.values = ZWaveValues(self)
        self._value_lock = threading.Lock()
        self._xml_lock = threading.Lock()
        self._endpoint_values = {}

        self._groups_loaded = set()
        self._endpoints_loaded = set()
        self._multi_channel_groups_loaded = set()

        if parent_node is None:
            self._notification_handler = (
                notification_handler.NotificationHandler(self)
            )
            self._notification_handler.start()

        else:
            self._notification_handler = parent_node._notification_handler

        if xml_data is None:
            if parent_node is None:
                self._tmp_xml_handler = xml_handler.XMLElement('Node')
            else:
                self._tmp_xml_handler = xml_handler.XMLElement('VirtualNode')

            self._tmp_xml_handler.Values = xml_handler.XMLElement('Values')

            def do():
                if parent_node is None:
                    signals.SIGNAL_NODE_ADDED.send(
                        sender=network,
                        network=network,
                        node=self
                    )
                else:
                    signals.SIGNAL_VIRTUAL_NODE_ADDED.send(
                        sender=parent_node,
                        network=network,
                        node=self
                    )
        else:
            self._tmp_xml_handler = None

            if hasattr(xml_data, 'Values'):
                from . import value as _value

                with self._value_lock:
                    for value in xml_data.Values:
                        value_id = _value.new_value_id()

                        self.values[value_id] = _value.ZWaveValue(
                            value_id,
                            network,
                            self,
                            value
                        )

            def do():
                if parent_node is None:
                    signals.SIGNAL_NODE_DATASET_LOADED.send(
                        sender=network,
                        network=network,
                        node=self
                    )
                else:
                    signals.SIGNAL_VIRTUAL_NODE_DATASET_LOADED.send(
                        sender=parent_node,
                        network=network,
                        node=self
                    )

        self._notification_handler.add(do)

    @property
    def is_endpoint(self):
        """
        :rtype: bool
        """
        return self._parent_node is not None

    @property
    def xml_handler(self):
        """
        :rtype: xml_handler.XMLElement
        """
        if self._xml_handler is None:
            return self._tmp_xml_handler
        else:
            return self._xml_handler

    @property
    def urls(self):
        """
        :rtype: URLs
        """
        if self._xml_handler is None:
            url_xml = None
        else:
            url_xml = self._xml_handler.URLs

        return URLs(self, url_xml)

    @property
    def help(self):
        """
        :rtype: Help
        """
        if self._xml_handler is None:
            help_xml = None
        else:
            help_xml = self._xml_handler.Help

        return Help(self, help_xml)

    @property
    def id(self):
        """
        Gets the node id.

        :return: the node id
        :rtype: NodeId
        """

        return self._object_id

    def _update_dataset(self):
        if self._xml_handler is None:
            if self._parent_node is None:
                handler = xml_handler.XMLElement('Node')
            else:
                handler = xml_handler.XMLElement('VirtualNode')

            handler.Description = xml_handler.XMLElement('Description')
            handler.Description.text = (
                self._network.manager.getMetaData(self.home_id, self.id.node_id, 3)
            )

            self.network.xml_handler.Nodes.append(handler)

            handler['id'] = self.id
            handler['name'] = (
                self._manager.getNodeName(self.home_id, self.id.node_id)
            )
            handler['location'] = (
                self._manager.getNodeLocation(self.home_id, self.id.node_id)
            )
            handler['product_name'] = (
                self._manager.getNodeProductName(self.home_id, self.id.node_id)
            )
            handler['product_type'] = (
                self._manager.getNodeProductType(self.home_id, self.id.node_id)
            )
            handler['product_id'] = (
                self._manager.getNodeProductId(self.home_id, self.id.node_id)
            )
            handler['manufacturer_id'] = (
                self._manager.getNodeManufacturerId(self.home_id, self.id.node_id)
            )
            handler['manufacturer_name'] = (
                self._manager.getNodeManufacturerName(self.home_id, self.id.node_id)
            )
            handler['version'] = (
                self._manager.getNodeVersion(self.home_id, self.id.node_id)
            )
            handler['max_baud_rate'] = (
                self._manager.getNodeMaxBaudRate(self.home_id, self.id.node_id)
            )
            handler['zwave_frequency'] = (
                self._manager.getMetaData(self.home_id, self.id.node_id, 11)
            )
            handler['security'] = (
                self._manager.getNodeSecurity(self.home_id, self.id.node_id)
            )
            handler['listening_device'] = (
                self._manager.isNodeListeningDevice(self.home_id, self.id.node_id)
            )
            handler['beaming_device'] = (
                self._manager.isNodeBeamingDevice(self.home_id, self.id.node_id)
            )
            handler['security_device'] = (
                self._manager.isNodeSecurityDevice(self.home_id, self.id.node_id)
            )
            handler['routing_device'] = (
                self._manager.isNodeRoutingDevice(self.home_id, self.id.node_id)
            )
            handler['controller_type'] = "0x{0:04X}".format(
                self._manager.getNodeBasic(self.home_id, self.id.node_id)
            )
            handler['role_type'] = "0x{0:04X}".format(
                self._manager.getNodeRole(self.home_id, self.id.node_id)
            )
            handler['device_type'] = "0x{0:04X}".format(
                self._manager.getNodeDeviceType(self.home_id, self.id.node_id)
            )
            handler['basic_type'] = "0x{0:04X}".format(
                self._manager.getNodeBasic(self.home_id, self.id.node_id)
            )
            handler['generic_type'] = "0x{0:04X}".format(
                self._manager.getNodeGeneric(self.home_id, self.id.node_id)
            )
            handler['specific_type'] = "0x{0:04X}".format(
                self._manager.getNodeSpecific(self.home_id, self.id.node_id)
            )
            handler['node_type'] = (
                self._manager.getNodeType(self.home_id, self.id.node_id)
            )
            handler['frequent_listening_device'] = (
                self._manager.isNodeFrequentListeningDevice(
                    self.home_id,
                    self.id.node_id
                )
            )

            from .command_classes import COMMAND_CLASSES

            command_classes = xml_handler.XMLElement('CommandClasses')

            if self._parent_node is not None:
                for value in self.values.values():
                    cc = value.command_class

                    command_class = xml_handler.XMLElement('CommandClass')
                    command_class['id'] = "0x{0:04X}".format(cc.class_id)
                    command_class['symbol'] = cc.class_desc
                    command_classes.append(command_class)

            else:
                for cc_id in sorted(self._command_classes):
                    cc = COMMAND_CLASSES[cc_id]

                    command_class = xml_handler.XMLElement('CommandClass')
                    command_class['id'] = "0x{0:04X}".format(cc_id)
                    command_class['symbol'] = cc.class_desc
                    command_classes.append(command_class)

            handler.insert(0, command_classes)

            for element in self._tmp_xml_handler:
                handler.append(element)

            self._tmp_xml_handler = None
        else:
            handler = self._xml_handler

        handler.Neighbors = xml_handler.XMLElement('Neighbors')
        neighbors = self._manager.getNodeNeighbors(self.home_id, self.id.node_id)

        for neighbor_id in sorted(neighbors):
            neighbor = xml_handler.XMLElement('Neighbor')
            neighbor['id'] = str(neighbor_id) + '.1'
            handler.Neighbors.append(neighbor)

        self._xml_handler = handler

        urls = URLs(self, None)
        urls._update_dataset()

        help = Help(self, None)
        help._update_dataset()

        from .command_classes import (
            COMMAND_CLASS_ASSOCIATION,
            COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION
        )

        if (
            self._parent_node is None and
            (
                self == COMMAND_CLASS_ASSOCIATION or
                self == COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION
            )
        ):
            handler.AssociationGroups = xml_handler.XMLElement('AssociationGroups')

            for group in self.association_groups:
                group._update_dataset()

        for value in self:
            value._update_dataset()

    def __iter__(self):
        for value in sorted(list(self.values.values()), key=lambda x: x.id):
            yield value

    @property
    def is_ready(self):
        """
        :rtype: bool
        """
        return self._is_ready

    @property
    def description(self):
        """
        :param value:
        :type value: str

        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getMetaData(self.home_id, self.id.node_id, 3)
        else:
            return self._xml_handler.Description.text

    @description.setter
    def description(self, value):
        if self._xml_handler is not None:
            self._xml_handler.Description.text = value

    @utils.logit
    def destroy(self):
        self._update_dataset()

        logger.debug('Node {0}: destroying'.format(self.id.node_id))

        if len(self._groups_loaded):
            logger.debug(str(self.id.node_id) + ' - destroying association groups')
            for group in self._groups_loaded:
                group.destroy()

            self._groups_loaded.clear()

        logger.debug(str(self.id.node_id) + ' - destroying values')
        for value in self:
            value.destroy()

        if self._notification_handler.is_owner_object(self):
            logger.debug(
                'Node {0}: Stopping Notification Handler'.format(self.id.node_id)
            )
            self._notification_handler.stop()

        logger.debug('Node {0}: destroyed'.format(self.id.node_id))

    @property
    def is_associated_to(self):
        """
        Gets all the association groups this node is a member of.

        :return: list of
            :py:class:`libopenzwave.association_group.ZWaveAssociationGroup`
            instances

        :rtype: List[ZWaveAssociationGroup]
        """

        res = []
        for node in list(self.network.nodes.values())[:]:
            if node == self:
                continue

            for group in node.association_groups:
                if self in group:
                    res += [group]

        return res

    @property
    def association_groups(self):
        """
        Get the association groups reported by this node

        :return: list of
            :py:class:`association_group.ZWaveAssociationGroup`
            instances
        :rtype: List[ZWaveAssociationGroup]
        """
        from .association_group import ZWaveAssociationGroup

        from .command_classes import (
            COMMAND_CLASS_ASSOCIATION,
            COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION
        )

        if (
            self._parent_node is not None or
            (
                self != COMMAND_CLASS_ASSOCIATION and
                self != COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION
            )
        ):
            return []

        groups = []

        if self._is_ready:
            groups_added = 0
            group_id = 1
            manager = self.network.manager
            num_groups = manager.getNumGroups(self.home_id, self.id.node_id)

            while groups_added < num_groups and group_id < 256:
                if manager.getMaxAssociations(self.home_id, self.id.node_id, group_id) > 0:
                    for xml_group in self._xml_handler.AssociationGroups:
                        if xml_group['id'] == group_id:
                            break
                    else:
                        xml_group = None

                    group = ZWaveAssociationGroup(self, group_id, xml_group)
                    self._groups_loaded.add(group)
                    groups += [group]
                    groups_added += 1

                group_id += 1

        elif hasattr(self._xml_handler, 'AssociationGroups'):
            for xml_group in self._xml_handler.AssociationGroups:
                group = ZWaveAssociationGroup(self, xml_group['id'], xml_group)
                self._groups_loaded.add(group)
                groups += [group]

        return groups

    @property
    def command_classes(self):
        """
        :rtype: List[COMMAND_CLASSES_]
        """
        from .command_classes import COMMAND_CLASSES
        res = []

        for cc_id in self._command_classes:
            res += [COMMAND_CLASSES.str_wrapper(cc_id)]

        return res

    @property
    def command_state(self):
        """
        If a command to a node has been given this will return the state
        of that command.

        The returned value is a :py:class:`libopenzwave.state.State` instance.
        This object has 4 attributes which are using in an application.

        * `label`: label that can be used to display to the user. (EN)
        * `error`: one of :py:data:`_libopenzwave.PyControllerError`
        * `command`: one of :py:data:`_libopenzwave.PyControllerCommand`
        * `state`: one of :py:data:`_libopenzwave.PyControllerState`


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
    def _handle_notification(self, notif):
        if notif.value is not None:
            self._handle_value(notif)

        elif notif == PyNotifications.Notification:
            def _do(c):
                signals.SIGNAL_NOTIFICATION.send(
                    sender=self,
                    network=self.network,
                    controller=self.network.controller,
                    node=self,
                    notification_code=c
                )

            self._notification_handler.add(_do, notif.notification_code)

        elif notif == PyNotifications.NodeRemoved:
            def _do():
                if self._parent_node is None:
                    for node in list(self.network.nodes.values())[:]:
                        if node == self:
                            continue

                        if node.id.node_id == self.id.node_id:
                            node._handle_notification(notif)

                del self.network.nodes[self.id]

                self._xml_handler.parent.remove(self._xml_handler)

                if self._parent_node is None:

                    signals.SIGNAL_NODE_REMOVED.send(
                        sender=self.network,
                        network=self.network,
                        controller=self.network.controller,
                        node=self
                    )
                else:
                    signals.SIGNAL_VIRTUAL_NODE_REMOVED.send(
                        sender=self.network,
                        network=self.network,
                        controller=self.network.controller,
                        node=self
                    )

            self._notification_handler.add(_do)

        elif notif == PyNotifications.UserAlerts:
            def _do(alert):
                if alert.idx != 0:
                    signals.SIGNAL_USER_ALERTS.send(
                        sender=self,
                        network=self.network,
                        controller=self.network.controller,
                        node=self,
                        user_alert=alert
                    )
                    for signal in (
                        signals.SIGNAL_ALERT_CONFIG_OUT_OF_DATE,
                        signals.SIGNAL_ALERT_MFS_OUT_OF_DATE,
                        signals.SIGNAL_ALERT_CONFIG_FILE_DOWNLOAD_FAILED,
                        signals.SIGNAL_ALERT_RELOAD_REQUIRED
                    ):
                        if signal == alert:
                            signal.send(
                                sender=self,
                                network=self.network,
                                controller=self.network.controller,
                                node=self
                            )
                            break

            self._notification_handler.add(_do, notif.user_alerts)

        elif notif == PyNotifications.NodeQueriesComplete:
            def _do():
                with self._value_lock:
                    self._is_cache = False
                    self._is_ready = True
                    self._update_dataset()

                    for value in self:
                        if not value.is_ready:
                            value._is_ready = True

                            signals.SIGNAL_VALUE_READY.send(
                                sender=self,
                                network=self.network,
                                controller=self.network.controller,
                                node=self,
                                value=value,
                                value_data=value.data
                            )

                if self._parent_node is None:
                    for node in list(self.network.nodes.values())[:]:
                        if node == self:
                            continue

                        if node.id.node_id == self.id.node_id:
                            node._handle_notification(notif)

                    signals.SIGNAL_NODE_READY.send(
                        sender=self,
                        network=self.network,
                        controller=self.network.controller,
                        node=self
                    )
                else:
                    if self._xml_handler is None:
                        self._update_dataset()
                        del self._instances[self.__instance_key__]
                        del self.network.nodes[self.id]

                        node = ZWaveNode(self.id, self.network, self._xml_handler, self._parent)
                        node._is_ready = True

                        for value_id in node.values.keys()[:]:
                            del node.values[value_id]

                        for value in self.values.values():
                            node.values[value.id] = value
                            value._parent = node
                            value._xml_handler.parent = node.xml_handler

                            self._xml_handler.parent.remove(self._xml_handler)

                    signals.SIGNAL_VIRTUAL_NODE_READY.send(
                        sender=self,
                        network=self.network,
                        controller=self.network.controller,
                        node=self
                    )

            if not self._is_ready:
                self._notification_handler.add(_do)

        elif notif == PyNotifications.Group:
            def _do(g_id):

                for group in self.association_groups:
                    if group.id == g_id:
                        break
                else:
                    return

                signals.SIGNAL_NODE_ASSOCIATION_GROUP.send(
                    sender=self,
                    network=self.network,
                    controller=self.network.controller,
                    node=self,
                    group=group
                )

            self._notification_handler.add(_do, notif.group_id)

        elif notif == PyNotifications.NodeNaming:
            def _do():
                signals.SIGNAL_NODE_NAMING.send(
                    sender=self,
                    network=self.network,
                    controller=self.network.controller,
                    node=self
                )

            self._notification_handler.add(_do)

        elif notif == PyNotifications.NodeProtocolInfo:
            def _do():
                signals.SIGNAL_NODE_PROTOCOL_INFO.send(
                    sender=self,
                    network=self.network,
                    controller=self.network.controller,
                    node=self
                )

            self._notification_handler.add(_do)

        elif notif == PyNotifications.PollingDisabled:
            def _do():
                signals.SIGNAL_NODE_POLLING_DISABLED.send(
                    sender=self,
                    network=self.network,
                    controller=self.network.controller,
                    node=self
                )

            self._notification_handler.add(_do)

        elif notif == PyNotifications.PollingEnabled:
            def _do():
                signals.SIGNAL_NODE_POLLING_ENABLED.send(
                    sender=self,
                    network=self.network,
                    controller=self.network.controller,
                    node=self
                )

            self._notification_handler.add(_do)

        elif notif == PyNotifications.CreateButton:
            def _do():
                signals.SIGNAL_NODE_CREATE_BUTTON.send(
                    sender=self,
                    network=self.network,
                    controller=self.network.controller,
                    node=self
                )

            self._notification_handler.add(_do)

        elif notif == PyNotifications.DeleteButton:
            def _do():
                signals.SIGNAL_NODE_DELETE_BUTTON.send(
                    sender=self,
                    network=self.network,
                    controller=self.network.controller,
                    node=self
                )

            self._notification_handler.add(_do)

        elif notif == PyNotifications.ButtonOn:

            def _do():
                signals.SIGNAL_NODE_BUTTON_ON.send(
                    sender=self,
                    network=self.network,
                    controller=self.network.controller,
                    node=self
                )

            self._notification_handler.add(_do)

        elif notif == PyNotifications.ButtonOff:

            def _do():
                signals.SIGNAL_NODE_BUTTON_OFF.send(
                    sender=self,
                    network=self.network,
                    controller=self.network.controller,
                    node=self
                )

            self._notification_handler.add(_do)

        elif notif == PyNotifications.NodeEvent:

            def _do(event):
                signals.SIGNAL_NODE_EVENT.send(
                    sender=self,
                    network=self.network,
                    controller=self.network.controller,
                    node=self,
                    event=event
                )

            self._notification_handler.add(_do, notif.event)

    @utils.logit
    def _handle_value(self, notif):
        def _do(n):
            for value_id, value in list(self.values.items())[:]:
                if value_id == n.value.id:
                    break

                if value_id > -1:
                    continue

                cc_id = value.command_class.class_id

                if (
                    cc_id == n.value.command_class and
                    value.index == n.value.index and
                    value.instance == n.value.instance
                ):
                    value._id = n.value.id
                    self.values[n.value.id] = self.values.pop(value_id)
                    value._update_dataset()
                    break
            else:
                value = None

            if n == PyNotifications.ValueAdded and value is None:
                from .value import ZWaveValue

                self.values[n.value.id] = (
                    ZWaveValue(
                        n.value.id,
                        self.network,
                        self,
                        None
                    )
                )

            elif notif == PyNotifications.ValueRemoved:
                if value is None:
                    logger.warning(
                        'Z-Wave Notification ValueRemoved for an '
                        'unknown value (%s) on node %s',
                        n.value.id,
                        self.id.node_id
                    )

                    signals.SIGNAL_VALUE_REMOVED.send(
                        sender=self,
                        network=self.network,
                        controller=self.network.controller,
                        node=self,
                        value=None,
                        value_data=n.value
                    )
                else:
                    del self.values[n.value.id]
                    value._handle_notification(n)

            elif notif in (
                PyNotifications.ValueChanged,
                PyNotifications.ValueRefreshed
            ):
                if value is None:
                    from .value import ZWaveValue

                    value = self.values[n.value.id] = (
                        ZWaveValue(
                            n.value.id,
                            self.network,
                            self,
                            None
                        )
                    )
                
                value._handle_notification(n)

        node_id = str(notif.node_id) + '.' + str(notif.value.instance)

        if node_id == self.id:
            self._notification_handler.add(_do, notif)
        else:
            if node_id not in self.network.nodes:
                self.network.nodes[node_id] = ZWaveNode(node_id, self.network, None, self)

            self.network.nodes[node_id]._handle_value(notif)

    @property
    def _manager(self):
        """
        :rtype: ZWaveManager
        """
        return self._network._manager

    @property
    def name(self):
        """
        Get/Set the name of the node.

        :param value:  node name
        :type value: str

        :rtype: str
        """
        if self._xml_handler is not None:
            name = self._xml_handler['name']
        else:
            name = self._manager.getNodeName(self.home_id, self.id.node_id)

        if not name:
            manufacturer_name = self.manufacturer_name
            product_name = self.product_name

            if manufacturer_name is None and product_name is None:
                name = ''
            elif None not in (manufacturer_name, product_name):
                name = manufacturer_name + ' - ' + product_name

            elif manufacturer_name is not None:
                name = manufacturer_name
            else:
                name = product_name

        return name

    @name.setter
    @utils.logit
    def name(self, value):
        if self._xml_handler is not None:
            self._xml_handler['name'] = value

        self._manager.setNodeName(self.home_id, self.id.node_id, value)

    @property
    def location(self):
        """
        Get/Set the location (room) of the node.

        :param value: node location
        :type value: str
        :rtype: str
        """
        if self._xml_handler is not None:
            location = self._xml_handler['location']
        else:
            location = self._manager.getNodeLocation(self.home_id, self.id.node_id)

        if not location:
            location = 'No Location'

        return location

    @location.setter
    @utils.logit
    def location(self, value):
        if self._xml_handler is not None:
            self._xml_handler['location'] = value

        self._manager.setNodeLocation(self.home_id, self.id.node_id, value)

    @property
    def product_name(self):
        """
        Get/Set the product name of the node.

        :param value: product name
        :type value: str

        :rtype: str
        """
        if self._xml_handler is not None:
            return self._xml_handler['product_name']
        else:
            return self._manager.getNodeProductName(self.home_id, self.id.node_id)

    @product_name.setter
    @utils.logit
    def product_name(self, value):
        if self._xml_handler is not None:
            self._xml_handler['product_name'] = value

        self._manager.setNodeProductName(self.home_id, self.id.node_id, value)

    @property
    def product_type(self):
        """
        The product type of the node.

        :rtype: str
        """
        if self._xml_handler is not None:
            return self._xml_handler['product_type']
        else:
            return self._manager.getNodeProductType(self.home_id, self.id.node_id)

    @property
    def product_id(self):
        """
        The product Id of the node.

        :rtype: str
        """
        if self._xml_handler is not None:
            return self._xml_handler['product_id']
        else:
            return self._manager.getNodeProductId(self.home_id, self.id.node_id)

    @property
    def manufacturer_id(self):
        """
        The manufacturer id of the node.

        :rtype: str
        """
        if self._xml_handler is not None:
            return self._xml_handler['manufacturer_id']
        else:
            return self._manager.getNodeManufacturerId(self.home_id, self.id.node_id)

    @property
    def manufacturer_name(self):
        """
        Get/Set the manufacturer name of the node.

        :param value: manufacturer name.
        :type value: str

        :rtype: str
        """

        if self._xml_handler is not None:
            return self._xml_handler['manufacturer_name']
        else:
            return self._manager.getNodeManufacturerName(self.home_id, self.id.node_id)

    @manufacturer_name.setter
    @utils.logit
    def manufacturer_name(self, value):
        if self._xml_handler is not None:
            self._xml_handler['manufacturer_name'] = value

        self._manager.setNodeManufacturerName(self.home_id, self.id.node_id, value)

    @property
    def version(self):
        """
        Gets the version of the node.

        :rtype: int
        """

        if self._xml_handler is not None:
            return self._xml_handler['version']
        else:
            return self._manager.getNodeVersion(self.home_id, self.id.node_id)

    @property
    def types(self):
        """
        The various type classifications for the node.

        :rtype: Types
        """
        return Types(self)

    @property
    def max_baud_rate(self):
        """
        Get the maximum baud rate of a node

        :rtype: int
        """
        if self._xml_handler is not None:
            return self._xml_handler['max_baud_rate']
        else:
            return self._manager.getNodeMaxBaudRate(self.home_id, self.id.node_id)

    @property
    def security(self):
        """
        The security type of the node.

        :rtype: int
        """

        if self._xml_handler is not None:
            return self._xml_handler['security']
        else:
            return self._manager.getNodeSecurity(self.home_id, self.id.node_id)

    @property
    def neighbors(self):
        """
        Node neighbors.

        :return: a list of node id's that this node can send packets to and
            receive packets from.
        :rtype: List["ZWaveNode"]
        """

        if self._xml_handler is None:
            neighbors = self._manager.getNodeNeighbors(self.home_id, self.id.node_id)
        else:
            neighbors = []
            for neighbor in self._xml_handler.Neighbors:
                neighbors += [int(neighbor['id'], 16)]

        res = []
        for neighbor_id in neighbors:
            res += [self.network.nodes[neighbor_id]]
        return res

    @property
    def category(self):
        """
        The nodes category.

        :return: category
        :rtype: GenericType
        """
        return self.types.generic

    @property
    def sub_category(self):
        """
        The nodes sub category.

        :return: sub category
        :rtype: SpecificType
        """
        return self.types.specific

    @property
    def is_openzwave_controller(self):
        """
        Check if the node is the USB Stick controller.

        :return: `True`/`False`
        :rtype: bool
        """
        from .controller import ZWaveController
        return isinstance(self, ZWaveController)

    @property
    def is_static_controller(self):
        """
        Check if the node is a static controller node.

        :return: `True`/`False`
        :rtype: bool
        """
        if self._xml_handler is not None:
            code =  int(self._xml_handler['basic_type'], 16)
        else:
            code = self._manager.getNodeBasic(self.home_id, self.id.node_id)

        return code == BASIC_TYPE_STATIC_CONTROLLER

    @property
    def is_slave_controller(self):
        """
        Check if the node is a slave controller node.

        :return: `True`/`False`
        :rtype: bool
        """

        if self._xml_handler is not None:
            code =  int(self._xml_handler['basic_type'], 16)
        else:
            code = self._manager.getNodeBasic(self.home_id, self.id.node_id)

        return code == BASIC_TYPE_SLAVE

    @property
    def is_portable_controller(self):
        """
        Check if the node is a portable controller node.

        :return: `True`/`False`
        :rtype: bool
        """

        if self._xml_handler is not None:
            code =  int(self._xml_handler['basic_type'], 16)
        else:
            code = self._manager.getNodeBasic(self.home_id, self.id.node_id)

        return code == BASIC_TYPE_CONTROLLER

    @property
    def is_listening_device(self):
        """
        Is node a listening device.

        :rtype: bool
        """
        if self._xml_handler is not None:
            return self._xml_handler['listening_device']
        else:
            return self._manager.isNodeListeningDevice(self.home_id, self.id.node_id)

    @property
    def is_beaming_device(self):
        """
        Is node a beaming device.

        :rtype: bool
        """

        if self._xml_handler is not None:
            return self._xml_handler['beaming_device']
        else:
            return self._manager.isNodeBeamingDevice(self.home_id, self.id.node_id)

    @property
    def is_frequent_listening_device(self):
        """
        Is node a frequent listening device.

        :rtype: bool
        """
        if self._xml_handler is not None:
            return self._xml_handler['frequent_listening_device']
        else:
            return self._manager.isNodeFrequentListeningDevice(
                self.home_id,
                self.id.node_id
            )

    @property
    def is_security_device(self):
        """
        Is node a security device.

        :rtype: bool
        """

        if self._xml_handler is not None:
            return self._xml_handler['security_device']
        else:
            return self._manager.isNodeSecurityDevice(self.home_id, self.id.node_id)

    @property
    def is_routing_device(self):
        """
        Is node a routing device.

        :rtype: bool
        """
        if self._xml_handler is not None:
            return self._xml_handler['routing_device']
        else:
            return self._manager.isNodeRoutingDevice(self.home_id, self.id.node_id)

    @property
    def is_sleeping(self):
        """
        Is node sleeping.

        :rtype: bool
        """

        if self.home_id in (None, 0):
            return None

        return not self.is_awake

    @property
    def is_awake(self):
        """
        Is node awake.

        :rtype: bool
        """

        if self.home_id in (None, 0):
            return None

        return self._manager.isNodeAwake(self.home_id, self.id.node_id)

    @property
    def is_failed(self):
        """
        Has node failed (presumed)

        :rtype: bool
        """
        logger.debug(
            'Send controller command : has_node_failed, : node : %s',
            self.id.node_id
        )
        if self.home_id in (None, 0):
            return None

        return self._manager.isNodeFailed(self.home_id, self.id.node_id)

    @property
    def zwave_frequency(self):
        """
        :rtype: str
        """
        if self._xml_handler is None:
            return self._manager.getMetaData(self.home_id, self.id.node_id, 11)
        else:
            return self._xml_handler['zwave_frequency']

    @utils.logit
    def update_neighbors(self):
        """
        Ask a Node to update its Neighbor Tables

        This command will ask a Node to update its Neighbor Tables.

        :rtype: bool
        """
        logger.debug(
            'Send controller command : '
            'request_node_neighbor_update, : node : %s',
            self.id.node_id
        )

        return self._manager.requestNodeNeighborUpdate(self.home_id, self.id.node_id)

    @utils.logit
    def create_button(self, button_id):
        """
        Create a handheld button id.

        Only intended for Bridge Firmware Controllers.

        :param button_id: the ID of the Button to query.
        :type button_id: int

        :rtype: bool
        """
        if self._controller.is_bridge_controller:
            logger.debug(
                'Send controller command : create_button, : '
                'node : %s, button : %s',
                self.id.node_id,
                button_id
            )

            return self._manager.createButton(self.home_id, self.id.node_id, button_id)

        return False

    @utils.logit
    def delete_button(self, button_id):
        """
        Delete a handheld button id.

        Only intended for Bridge Firmware Controllers.

        :param button_id: the ID of the Button to query.
        :type button_id: int

        :rtype: bool
        """
        if self._controller.is_bridge_controller:
            logger.debug(
                'Send controller command : delete_button, : '
                'node : %s, button : %s',
                self.id.node_id,
                button_id
            )

            return self._manager.deleteButton(self.home_id, self.id.node_id, button_id)
        return False

    @property
    def query_stage(self):
        """
        Node query stage.

        :return:
            One of the following items:

                * `"None"`
                * `"ProtocolInfo"`
                * `"Probe"`
                * `"WakeUp"`
                * `"ManufacturerSpecific1"`
                * `"NodeInfo"`
                * `"NodePlusInfo"`
                * `"SecurityReport"`
                * `"ManufacturerSpecific2"`
                * `"Versions"`
                * `"Instances"`
                * `"Static"`
                * `"CacheLoad"`
                * `"Associations"`
                * `"Neighbors"`
                * `"Session"`
                * `"Dynamic"`
                * `"Configuration"`
                * `"Complete"`

        :rtype: str
        """
        if self.home_id in (None, 0):
            return None

        return self._manager.getNodeQueryStage(self.home_id, self.id.node_id)

    @property
    def is_info_received(self):
        """
        Get whether the node information has been received.

        :return: if the node information has been received yet `True`/`False`
        :rtype: bool
        """

        if self._manager is None:
            return None

        return self._manager.isNodeInfoReceived(self.home_id, self.id.node_id)

    @utils.logit
    def heal(self, update_routes=False):
        """
        Heal network node by requesting the node rediscover their neighbors.

        :param update_routes: Optional Whether to perform return routes
            initialization. (default = False).
        :type update_routes: bool, optional

        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        if self.is_awake is False:
            logger.warning('Node state must a minimum set to awake')
            return False
        self._manager.healNetworkNode(self.home_id, self.id.node_id, update_routes)
        return True

    @utils.logit
    def test(self, count=1):
        """
        Send a number of test messages to node and record results.

        :param count: The number of test messages to send. (default = 1)
        :type count: int, optional
        """
        self._manager.testNetworkNode(self.home_id, self.id.node_id, count)

    @utils.logit
    def update_return_route(self):
        """
        Ask a Node to update its Return Route to the Controller

        This command will ask a Node to update its Return Route to the
        Controller

        :rtype: bool
        """
        logger.debug(
            'Send controller command : assign_return_route, : node : %s',
            self.id.node_id
        )

        return self._manager.assignReturnRoute(self.home_id, self.id.node_id)

    @utils.logit
    def refresh_node(self):
        """
        Trigger the fetching of fixed data about a node.

        Causes the nodes data to be obtained from the Z-Wave network in
        the same way as if it had just been added.  This method would
        normally be called automatically by OpenZWave, but if you know that
        a node has been changed, calling this method will force a refresh of
        the data held by the library. This can be especially useful for
        devices that were asleep when the application was first run.

        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        logger.debug('refresh_info for node [%s]', self.id.node_id)
        return self._manager.refreshNodeInfo(self.home_id, self.id.node_id)

    @utils.logit
    def refresh_node_values(self):
        """
        Trigger the fetching of just the dynamic value data for a node.

        Causes the node's values to be requested from the Z-Wave network.
        This is the same as the query state starting from the dynamic state.

        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        logger.debug('request_state for node [%s]', self.id.node_id)
        return self._manager.requestNodeState(self.home_id, self.id.node_id)

    @utils.logit
    def delete_return_routes(self):
        """
        Ask a Node to delete all Return Route.

        This command will ask a Node to delete all its return routes, and will
        rediscover when needed.

        :rtype: bool
        """
        logger.debug(
            'Send controller command : '
            'delete_all_return_routes, : node : %s',
            self.id.node_id
        )

        return self._manager.deleteAllReturnRoutes(self.home_id, self.id.node_id)

    @utils.logit
    def send_information(self):
        """
        Send a NIF frame from the Controller to a Node.

        :rtype: bool
        """
        logger.debug(
            'Send controller command : send_node_information, : node : %s',
            self.id.node_id
        )
        return self._manager.sendNodeInformation(self.home_id, self.id.node_id)

    @utils.logit
    def network_update(self):
        """
        Update the controller with network information from the SUC/SIS.

        :rtype: bool
        """
        logger.debug(
            'Send controller command : request_network_update, : '
            'node : %s',
            self.id.node_id
        )
        return self._manager.requestNetworkUpdate(self.home_id, self.id.node_id)

    @utils.logit
    def request_config_params(self):
        """
        Request the values of all known configurable parameters from a device.
        """
        logger.debug('Requesting config params for node [%s]', self.id.node_id)
        self._manager.requestAllConfigParams(self.home_id, self.id.node_id)

    @utils.logit
    def request_config_param(self, param):
        """
        Request the value of a configurable parameter from a device.

        Some devices have various parameters that can be configured to control
        the device behaviour. These are not reported by the device over the
        Z-Wave network but can usually be found in the devices user manual.
        This method requests the value of a parameter from the device, and then
        returns immediately, without waiting for a response. If the parameter
        index is valid for this device, and the device is awake, the value will
        eventually be reported via a ValueChanged notification callback. The
        ValueID reported in the callback will have an index set the same as
        _param and a command class set to the same value as returned by a call
        to Configuration::StaticGetCommandClassId.

        :param param: The param id of the node.
        :type param: int

        :return: value of the param
        :rtype: Any
        """
        logger.debug(
            'Requesting config param %s for node [%s]',
            param,
            self.id.node_id
        )
        self._manager.requestConfigParam(self.home_id, self.id.node_id, param)

    @utils.logit
    def set_config_param(self, param, value, size=2):
        """
        Set the value of a configurable parameter in a device.

        Some devices have various parameters that can be configured to control
        the device behaviour. These are not reported by the device over the
        Z-Wave network but can usually be found in the devices user manual.
        This method returns immediately, without waiting for confirmation from
        the device that the change has been made.

        :param param: The param id of the node.
        :type param: int

        :param value: The value of the param.
        :type value: Any

        :param size: Number if bytes to send as the value. (default = 2).
        :type size: int, optional

        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        logger.debug('Set config param %s for node [%s]', param, self.id.node_id)
        return self._manager.setConfigParam(
            self.home_id,
            self.id.node_id,
            param,
            value,
            size
        )

    @property
    def stats(self):
        """
        Retrieve statistics for node.

        :return: A class object containing statistics.

        Attributes:

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

        :rtype: _libopenzwave.NodeStats
        """
        return self._manager.getNodeStatistics(self.home_id, self.id.node_id)

    @property
    def as_dict(self):
        """
        Dictionary representation of a node.

        :rtype: dict
        """
        ret = dict(
            name=self.name,
            location=self.location,
            product_name=self.product_name,
            product_type=self.product_type,
            product_id=self.product_id,
            manufacturer_name=self.manufacturer_name,
            manufacturer_id=self.manufacturer_id,
            version=self.version,
            types=self.types.as_dict,
            max_baud_rate=self.max_baud_rate,
            security=self.security,
            id=self.id.node_id,
            is_controller=self.is_controller,
            is_listening_device=self.is_listening_device,
            is_beaming_device=self.is_beaming_device,
            is_frequent_listening_device=self.is_frequent_listening_device,
            is_security_device=self.is_security_device,
            is_routing_device=self.is_routing_device,
            is_failed=self.is_failed,
            values=list(value.as_dict for value in self.values.values()),
            neighbors=list(neighbor.id for neighbor in self.neighbors),
            stats=self.stats.as_dict
        )

        for cls in self._bases:
            ret.update(cls.__dict__['as_dict'].fget(self))

        return ret

    def __eq__(self, other):
        """
        :param other:
        :type other: "ZWaveNode", int

        :rtype: bool
        """
        if isinstance(other, ZWaveNode):
            return self.id.node_id == other.id
        if isinstance(other, int):
            for cls in self._bases:
                if cls.class_id == other:
                    return True
            return False
        try:
            for cls in self._bases:
                if cls.class_id == other.class_id:
                    return True
            return False
        except AttributeError:
            return False

    def __ne__(self, other):
        """
        :param other:
        :type other: "ZWaveNode", int

        :rtype: bool
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        :rtype: hash
        """
        return hash(repr(self))
