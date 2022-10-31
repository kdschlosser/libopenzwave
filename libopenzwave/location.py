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
:synopsis: ZWave API

.. moduleauthor:: Kevin G Schlosser
"""

import logging

from . import singleton
from . import utils
from . import xml_handler

logger = logging.getLogger(__name__)


class ZWaveLocation(object, metaclass=singleton.InstanceSingleton):
    """
    This class represents a collection of nodes/endpoints at a location.

    This class is also an InstanceSingleton. There can only be one instance
    of this class in existence. if you change the location of a node then you
    will also have to refresh any node lists that were obtained from
    this class.

    Endpoint locations are not supported by openzwave. I am doing this through
    a manipulation of the label for the endpoint values. I did want to mention
    That is if see a strange label by some chance please report it to me and
    I will correct the value label problem. Here is an example as to why i did
    this.

    I personally own a landscape lighting controller. that controller has
    6 zones. Each zone is an endpoint. I also have a bunch of exterior lights.
    so instead of having a single location called outside with 14 nodes listed
    in it i wanted to narrow down the choices a bit more. I wanted to have
    outside zones "back deck", "side deck" "front yard" and "back yard".
    because the landscape lighting controller has lights in all of these areas
    only being able to set a single location was not going to do the job.
    With being able to set locations for the individual endpoints (zones) i
    can now set locations for each fo them and then set the location of where
    the controller is located as well.

    NOTE: This class can be iterated over like a list to get the nodes in
    the location. you can also check if a node is in the location.

    ..code-block:: python

        if node in location:
            # do your code here
            pass

    I also added the left hand operands + and -. + adds a node(s) or
    endpoint(s) and - removes

    removing a node or endpoint from a location will set the location to
    "No Location".

    ..code-block:: python

        association_group += node
        # or
        association_group += endpoint

    or if you want to add more then a single node

    ..code-block:: python

        association_group += [node1, endpoint1, node3]
        # or
        association_group += (node1, endpoint1, node2)

    """
    _location_id_count = 0
    _instances = {}

    @utils.logit
    def __init__(self, name, network_, xml_data, *_, **__):
        """
        :param name: name of the location
        :type name: str

        :param network: network object
        :type network: ZWaveNetwork

        :param xml_data:
        :type xml_data: xml_handler.XMLElement

        :param *_:

        :param **__:
        """

        if xml_data is None:
            self._id = network_.xml_handler.Locations['next_id']
            network_.xml_handler.Locations['next_id'] = self._id + 1
        else:
            self._id = int(xml_data['id'], 16)

        self._network = network_
        self._name = name
        self._xml_handler = xml_data

    @property
    def xml_handler(self):
        """
        :rtype: xml_handler.XMLElement
        """
        return self._xml_handler

    def _update_dataset(self):
        nodes = self.nodes
        endpoints = self.endpoints

        if not nodes and not endpoints and self._xml_handler is not None:
            self._network.xml_handler.Locations.remove(self._xml_handler)

        if self._xml_handler is None:
            handler = xml_handler.XMLElement('Location')
            self._network.xml_handler.Locations.append(handler)

            handler.Nodes = xml_handler.XMLElement('Nodes')
            handler.Endpoints = xml_handler.XMLElement('Endpoints')

            handler['name'] = self._name
            handler['id'] = '0x{0:04X}'.format(self._id)

        else:
            handler = self._xml_handler

        handler.Nodes.clear()
        handler.Endpoints.clear()

        for node_ in self.nodes:
            node_element = xml_handler.XMLElement('Node')
            node_element['id'] = '{0:04X}'.format(node_.id)
            handler.Nodes.append(node_element)

        for endpoint in self.endpoints:
            endpoint_element = xml_handler.XMLElement('Endpoint')
            endpoint_element['id'] = '{0:04X}'.format(endpoint.id)
            endpoint_element['endpoint'] = endpoint.instance_id - 1
            handler.Endpoints.append(endpoint_element)

    def destroy(self):
        """
        Internal use.

        removes this instance from the instance singleton list.
        """
        self._update_dataset()
        logger.debug(self.name + ' - destroyed')

    @property
    @utils.logit
    def name(self):
        """
        Get/Set the Location Name

        If you change the name of this location it will also change the
        location name for every node that is contained within this location.

        :param value: the new location name
        :type value: str

        :return: the location name
        :rtype: str
        """
        return self._name

    @name.setter
    @utils.logit
    def name(self, value):
        for node_ in self._network:
            if node_.location == self._name:
                node_.location = value

        del ZWaveLocation._instances[self._name]

        if value in ZWaveLocation._instances:
            location = ZWaveLocation._instances[value]
            self.__dict__.update(location.__dict__)

        else:
            ZWaveLocation._instances[value] = self
            self._name = value

        self._xml_handler['name'] = value

    @property
    def id(self):
        """
        The id of the location

        :return: id
        :rtype: int
        """
        return self._id

    @property
    def network(self):
        """
        The Network object this location belongs to.

        :return: network object
        :rtype: ZWaveNetwork
        """
        return self._network

    @property
    def nodes(self):
        """
        The nodes that at this location

        :return: list of nodes
        :rtype: List[ZWaveNode]
        """

        nodes = []
        for node in self._network:
            if node.location == self._name:
                nodes.append(node)

        return list(sorted(nodes, key=lambda x: x.id))

    @property
    def endpoints(self):
        """
        :rtype: List[ZWaveNode]
        """
        from .command_classes import COMMAND_CLASS_MULTI_CHANNEL

        endpoints = []
        for node in self._network:
            if node != COMMAND_CLASS_MULTI_CHANNEL:
                continue

            for endpoint in node.endpoints:
                if endpoint.location == self._name:
                    endpoints += [endpoint]

        return endpoints

    def __iter__(self):
        res = self.nodes[:] + self.endpoints[:]
        return iter(res)

    def __contains__(self, item):
        """
        :param item:
        :type item: int, NodeId

        :rtype: bool
        """
        if isinstance(item, int):
            for node in self:
                if node.id == item:
                    return True
        else:
            for node in self:
                if item == node:
                    return True
        return False

    def add(self, node):
        """
        :param node:
        :type node: ZWaveNode

        :rtype: bool
        """
        if node in list(self):
            return False

        node.location = self._name
        return True

    def remove(self, node):
        """
        :param node:
        :type node: ZWaveNode

        :rtype: bool
        """
        if node not in list(self):
            return False

        node.location = ''
        return True

    def __iadd__(self, other):
        """
        :param other:
        :type other: List[ZWaveNode], ZWaveNode
        """
        if isinstance(other, (list, tuple)):
            for node_ in other:
                self.add(node_)
        else:
            self.add(other)

        return self

    def __isub__(self, other):
        """
        :param other:
        :type other: List[ZWaveNode], ZWaveNode
        """
        if isinstance(other, (list, tuple)):
            for node_ in other:
                self.remove(node_)
        else:
            self.remove(other)

        return self
