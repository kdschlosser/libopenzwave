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
:synopsis: COMMAND_CLASS_CONTROLLER_REPLICATION

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Controller Replication Command Class - Active
# Application
COMMAND_CLASS_CONTROLLER_REPLICATION = 0x21


# noinspection PyAbstractClass
class ControllerReplication(zwave_cmd_class.ZWaveCommandClass):
    """
    Controller Replication Command Class

    symbol: `COMMAND_CLASS_CONTROLLER_REPLICATION`
    """

    class_id = COMMAND_CLASS_CONTROLLER_REPLICATION
    class_desc = 'COMMAND_CLASS_CONTROLLER_REPLICATION'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        replication_node_id = 0
        replication_function = 1
        replication_replicate = 2

    @property
    def replication_node_id(self):
        """
        Get/Set Replication Node

        :param value: node
        :type value: :py:class:`libopenzwave.node.ZWaveNode` instance

        :return: node
        :rtype: :py:class:`libopenzwave.node.ZWaveNode` instance
        """
        id_ = self.values.replication_node_id.data
        return self.network.nodes[id_]

    @replication_node_id.setter
    def replication_node_id(self, value):
        self.values.replication_node_id.data = value.id

    @property
    def replication_function(self):
        """
        Get/Set Replication Function

        :param value: one of the values returned from
            :py:attr:`replication_function_items`
        :type value: str

        :return: one of the values returned from
            :py:attr:`replication_function_items`
        :rtype: str, Optional
        """
        return self.values.replication_function.data

    @replication_function.setter
    def replication_function(self, value):
        self.values.replication_function.data = value

    @property
    def replication_function_items(self):
        """
        Allowed Replication Function values

        :return: list of allowed values
        :rtype: List[Any]
        """
        return self.values.replication_function.data_items

    def replicate(self):
        """
        Replicate

        starts the replication process.

        :return: if command was successful `True`/`False`
        :rtype: bool
        """

        self.values.replication_replicate.data = True
