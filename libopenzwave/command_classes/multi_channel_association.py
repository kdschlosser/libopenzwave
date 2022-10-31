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
:synopsis: COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION

.. moduleauthor:: Kevin G Schlosser
"""


import logging

from . import zwave_cmd_class
from .. import xml_handler

logger = logging.getLogger(__name__)

# Multi Channel Association Command Class - Active
# Management
COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION = 0x8E


# noinspection PyAbstractClass
class MultiChannelAssociation(zwave_cmd_class.ZWaveCommandClass):
    """
    Multi Channel Association Command Class

    symbol: `COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION`
    """

    class_id = COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION
    class_desc = 'COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        pass

    def __init__(self):
        self._multi_channel_groups_loaded = getattr(
            self,
            '_multi_channel_groups_loaded'
        )
        self._xml_handler = getattr(self, '_xml_handler')
        self._is_ready = getattr(self, '_is_ready')
        zwave_cmd_class.ZWaveCommandClass.__init__(self)

    def _update_association_dataset(self):
        if not hasattr(self._xml_handler, 'AssociationGroups'):
            self._xml_handler.AssociationGroups = (
                xml_handler.XMLElement('AssociationGroups')
            )

        for group in self.association_groups:
            group._update_dataset()  # NOQA

    @property
    def is_associated_to(self):
        """
        Gets all the association groups this node is a member of.

        :return: list of
            :py:class:`libopenzwave.association_group.AssociationGroup` instances

        :rtype: List[:py:class:`libopenzwave.association_group.AssociationGroup`]
        """
        from . import COMMAND_CLASS_ASSOCIATION

        res = []
        for node in self.network.nodes.values():
            if node == self or node != COMMAND_CLASS_ASSOCIATION:
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
        :rtype: List[ :py:class:`association_group.ZWaveAssociationGroup`]
        """

        from ..association_group import ZWaveAssociationGroup

        groups = []

        if self._is_ready:
            groups_added = 0
            group_id = 1
            manager = self.network.manager
            num_groups = manager.getNumGroups(self.home_id, self.id)

            while groups_added < num_groups and group_id < 256:
                if (
                    manager.getMaxAssociations(self.home_id, self.id, group_id)
                    > 0
                ):
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
