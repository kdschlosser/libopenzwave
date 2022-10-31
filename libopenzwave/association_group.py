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

.. moduleauthor:: Kevin G Schlosser
"""

import logging

from . import singleton
from . import utils
from . import xml_handler


logger = logging.getLogger(__name__)


class _AssociationText(int):
    long = ''
    short = ''
    value = 0

    @staticmethod
    def __new__(cls, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """
        args = list(args)
        args[1] = cls.value

        return super(_AssociationText, cls).__new__(*args, **kwargs)

    @property
    def short_description(self):
        """
        :rtype: str
        """
        return self.short

    @property
    def long_description(self):
        """
        :rtype: str
        """
        return self.long

    def __str__(self):
        """
        :rtype: str
        """
        return self.short

    def __and__(self, other):
        """
        Return self & value.

        :param other:
        :type other: int

        :rtype: int
        """
        return self.value & other

    def __or__(self, other):
        """
        Return self | value.

        :param other:
        :type other: int

        :rtype: int
        """
        return self.value | other

    def __rand__(self, other):
        """
        Return value & self.

        :param other:
        :type other: int

        :rtype: int
        """
        return other & self.value

    def __ror__(self, other):
        """
        Return value | self.

        :param other:
        :type other: int

        :rtype: int
        """
        return other | self.value

    def __rxor__(self, other):
        """
        Return value ^ self.

        :param other:
        :type other: int

        :rtype: int
        """
        return other ^ self.value

    def __xor__(self, other):
        """
        Return self ^ value.

        :param other:
        :type other: int

        :rtype: int
        """
        return self.value ^ other

    def __eq__(self, other):
        """
        :param other:
        :type other:  bool, str

        :rtype: bool
        """
        if isinstance(other, bool):
            return other == self.value
        return other == self.short

    def __ne__(self, other):
        """
        :param other:
        :type other:  bool, str

        :rtype: bool
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        :rtype: hash
        """
        return hash(repr(self))


class SuccessAdd(_AssociationText):
    short = 'Success.'
    long = 'Node/Endpoint has been added to this group successfully.'
    value = True


class SuccessRemove(_AssociationText):
    short = 'Success.'
    long = 'Node/Endpoint has been removed from this group successfully.'
    value = True


class MaxAssociationsReached(_AssociationText):
    short = 'Max associations reached.'
    long = (
        'The number of associations permitted for this group has been reached.'
    )
    value = False


class AssociationAlreadyExists(_AssociationText):
    short = 'Node/Endpoint already in group.'
    long = (
        'The node or endpoint has already been added to this association group.'
    )
    value = False


class EndpointsNotSupported(_AssociationText):
    short = 'Endpoints not supported.'
    long = 'This association group does not support multichannel endpoints'
    value = False


class NoAssociationFound(_AssociationText):
    short = 'Association not found.'
    long = 'No association exists for this node/endpoint.'
    value = False


class UnknownError(_AssociationText):
    short = 'An unknown error occured'
    long = 'Unknown error - most likely an endpoint id mapping issue.'
    value = False


class ZWaveAssociationGroup(object, metaclass=singleton.InstanceSingleton):
    """
    Representation of an association group.

    Association groups (if supported by the device) allow a device to
    communicate directly with another device. The purpose for being able to
    do this is to be able to control other devices while reducing network
    traffic.

    Example: You have 2 outside lights and the switch for each of the lights
    is at 2 different entries to your house. You want to be able to turn on
    both lights from a single switch. Using association groups allows you to
    do this.

    ZWave+ devices may also have multi-tap features and that multi-tap function
    may be attached to an association group. If it is then pressing the switch
    multiple times will trigger different association groups to run.

    Example: Same scenario as above. Except when you double press the switch
    on or off it will turn both lights on or off. Again this is done with
    association groups.

    There is a limit to the number of associated devices that can be applied
    to a single group.

    Please refer to the documentation for your device to see if it supports
    association groups and what those groups may be attached to in terms of
    function.

    NOTE: This class can be iterated over like a list to get the associations.
    I also added the left hand operands + and -. + adds a node(s) or
    endpoint(s) and - removes

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

    @utils.logit
    def __init__(self, node, id_, xml_data, *_, **__):
        """
        :param node:
        :type node: ZWaveNode

        :param id_:
        :type id_: int

        :param xml_data:
        :type xml_data: xml_handler.XMLElement

        :param *_:
        :param **__:
        """
        self._node = node
        self._id = id_
        self._xml_handler = xml_data

    @property
    def xml_handler(self):
        """
        :rtype: xml_handler.XMLElement
        """
        return self._xml_handler

    def _update_dataset(self):
        if self._xml_handler is None:
            handler = xml_handler.XMLElement('AssociationGroup')
            self._node.xml_handler.AssociationGroups.append(handler)
            handler['id'] = self.id
            handler['max_associations'] = (
                self.network.manager.getMaxAssociations(
                    self.home_id,
                    self._node.id.node_id,
                    self.id
                )
            )
            handler['name'] = (
                self.network.manager.getGroupLabel(
                    self.home_id,
                    self._node.id.node_id,
                    self.id
                )
            )
            handler['multi_instance'] = (
                self.network.manager.isMultiInstance(
                    self.network.home_id,
                    self._node.id.node_id,
                    self.id
                )
            )

        else:
            handler = self._xml_handler

        handler.clear()

        associations = self.network.manager.getAssociationsInstances(
            self.home_id,
            self._node.id.node_id,
            self.id
        )

        for assoc in associations:
            assoc_element = xml_handler.XMLElement('Association')
            assoc_element['node_id'] = '0x{0:04X}'.format(assoc.node_id)
            assoc_element['endpoint'] = assoc.instance
            handler.append(assoc_element)

        self._xml_handler = handler

    def destroy(self):
        """
        Internal use.

        removes this instance from the instance singleton list.

        :return: None
        """
        self._update_dataset()
        logger.debug(str(self.id) + ' - destroyed')

    @property
    def parent_node(self):
        """
        The parent node of this group.

        :return: parent node
        :rtype: ZWaveNode
        """
        return self._node

    @property
    def id(self):
        """
        The association group id (index)

        :return: group id
        :rtype: int
        """
        return self._id

    @property
    def home_id(self):
        """
        Home id of the network the group belongs to.

        :return: home id
        :rtype: int
        """
        return self._node.network.home_id

    @property
    def network(self):
        """
        Reference to the ZWaveNetwork object instance.

        :return: ZWaveNetwork instance
        :rtype: ZWaveNetwork
        """
        return self._node.network

    @property
    @utils.logit
    def max_associations(self):
        """
        The maximum number of associated nodes in this group.

        :return: Max associations
        :rtype: int
        """
        if self._xml_handler is None:
            return self.network.manager.getMaxAssociations(
                self.home_id,
                self._node.id.node_id,
                self.id
            )
        else:
            return self._xml_handler['max_associations']

    @property
    def name(self):
        """
        The name of the group.

        :param value:
        :type value: str

        :return: Name
        :rtype: str
        """
        if self._xml_handler is None:
            return self.network.manager.getGroupLabel(
                self.home_id,
                self._node.id.node_id,
                self.id
            )
        else:
            return self._xml_handler['name']

    @name.setter
    def name(self, value):
        if self._xml_handler is not None:
            self._xml_handler['name'] = value

    def __iter__(self):
        for association in self.associations:
            yield association

    def __contains__(self, item):
        return item in list(self)

    def __iadd__(self, other):
        if isinstance(other, (list, tuple)):
            for item in other:
                self.add(item)
        else:
            self.add(other)

        return self

    def __isub__(self, other):
        if isinstance(other, (list, tuple)):
            for item in other:
                self.remove(item)
        else:
            self.remove(other)

        return self

    @property
    def is_multi_channel(self):
        """
        Is Multi Instance

        Does this group support multiple instances

        :return: `True`/`False`
        :rtype: bool
        """

        if self._xml_handler is None:
            return self.network.manager.isMultiInstance(
                self.network.home_id,
                self._node.id.node_id,
                self.id
            )
        else:
            return self._xml_handler['multi_instance']

    @property
    @utils.logit
    def associations(self):
        """
        The associations.

        :return: list that contains
            :py:class:`libopenzwave.node.ZWaveNode` instance(s)

        :rtype: List[ZWaveNode]
        """

        associations = self.network.manager.getAssociationsInstances(
            self.home_id,
            self._node.id.node_id,
            self.id
        )

        res = set()

        for assoc in associations:
            node_id = assoc.node_id
            instance_id = assoc.instance
            endpoint_id = str(node_id) + '.' + str(instance_id + 1)

            nde = self.network.nodes[endpoint_id]
            res.add(nde)

        return res

    @utils.logit
    def add(self, association):
        """
        Adds a node to an association group.

        Due to the possibility of a device being asleep, the command is
        assumed to complete with success, and the association data held in
        this class is updated directly. This will be reverted by a future
        Association message from the device if the Z-Wave message actually
        failed to get through. Notification callbacks will be sent in both
        cases.

        :param association: The association to be added.
        :type association: ZWaveNode

        :return: `False` if the association cannot be added, `True` if it can
        :rtype: bool
        """

        if not self.is_multi_channel and association.is_endpoint:
            return EndpointsNotSupported()

        if len(self.associations) == self.max_associations:
            return MaxAssociationsReached()

        if association in self.associations:
            return NoAssociationFound()

        res = self.network.manager.addAssociation(
            self.home_id,
            self._node.id.node_id,
            self.id,
            association.id.node_id,
            association.id.endpoint_id - 1
        )

        if res is True:
            return SuccessAdd()
        else:
            return UnknownError()

    @utils.logit
    def remove(self, association):
        """
        Removes a node from an association group.

        Due to the possibility of a device being asleep, the command is
        assumed to succeed, and the association data held in this class is
        updated directly. This will be reverted by a future Association
        message from the device if the Z-Wave message actually failed to get
        through. Notification callbacks will be sent in both cases.

        :param association: The association to be removed.
        :type association: ZWaveNode

        :return: `True` if there is an association, `False` if not.
        :rtype: bool
        """

        if not self.is_multi_channel and association.is_endpoint:
            return EndpointsNotSupported()

        if association not in self.associations:
            return NoAssociationFound()

        res = self.network.manager.removeAssociation(
            self.home_id,
            self._node.id.node_id,
            self.id,
            association.id.node_id,
            association.id.endpoint_id - 1
        )

        if res is True:
            return SuccessRemove()
        else:
            return UnknownError()

    @property
    def as_dict(self):
        """
        Dictionary representation of an association group

        :return: A dictionary

            Example layout:

            .. code-block:: python

                {
                    "id": 0,
                    "name": "some name",
                    "home_id": 1,
                    "parent_node": 6,
                    "max_associations": 5,
                    "associations": {
                        1: [0],
                        2: [1, 2, 3]
                    }
                }

            where "associations" is a dict where the keys are the id of the
            associated node and the value is the instance id of that node.
            if there is no instance id then a 0 will be in the list.
        :rtype: dict
        """

        associations = {}
        for association in self.associations:
            if association.id.node_id not in associations:
                associations[association.id.node_id] = []

            associations[association.id.node_id] += [association.id.endpoint_id]

        return dict(
            id=self.id,
            parent_node=self.parent_node.id,
            home_id=self.home_id,
            max_associations=self.max_associations,
            name=self.name,
            associations=associations
        )


