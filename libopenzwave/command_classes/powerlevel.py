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
:synopsis: COMMAND_CLASS_POWERLEVEL

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Powerlevel Command Class - Active
# Network-Protocol
COMMAND_CLASS_POWERLEVEL = 0x73


# noinspection PyAbstractClass
class Powerlevel(zwave_cmd_class.ZWaveCommandClass):
    """
    Powerlevel Command Class

    symbol: `COMMAND_CLASS_POWERLEVEL`
    """

    class_id = COMMAND_CLASS_POWERLEVEL
    class_desc = 'COMMAND_CLASS_POWERLEVEL'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        power_level = 0
        power_level_timeout = 1
        power_level_set = 2
        power_level_test_node = 3
        power_level_test_power_level = 4
        power_level_test_frames = 5
        power_level_test = 6
        power_level_report = 7
        power_level_test_status = 8
        power_level_test_ack_frames = 9

    @property
    def power_level(self):
        """
        RF Transmit Power Level

        :param value: one of :py:attr:`power_level_items`
        :type value: str

        :return: one of :py:attr:`power_level_items`
        :rtype: str
        """

        return self.values.power_level.data

    @power_level.setter
    def power_level(self, value):
        self.values.power_level.data = value

    @property
    def power_level_items(self):
        """
        Power Level Items

        :return: list of allowed power level values
        :rtype: List[str]
        """
        return self.values.power_level.data_items

    @property
    def power_level_timeout(self):
        """
        Power Level Timeout

        :param value: timeout
        :type value: int

        :return: timeout
        :rtype: int
        """
        return self.values.power_level_timeout.data

    @power_level_timeout.setter
    def power_level_timeout(self, value):
        self.values.power_level_timeout.data = value

    @property
    def power_level_test_node(self):
        """
        Power Level Test Node

        :param value: node
        :type value: :py:class:`libopenzwave.node.ZWaveNode` instance

        :return: node
        :rtype: :py:class:`libopenzwave.node.ZWaveNode` instance
        """

        node_id = self.values.power_level_test_node.data
        return self.network.nodes[node_id]

    @power_level_test_node.setter
    def power_level_test_node(self, value):
        self.values.power_level_test_node.data = value.id

    @property
    def power_level_test(self):
        """
        Power Level Test

        :param value: one of :py:attr:`power_level_test_items`
        :type value: str

        :return: one of :py:attr:`power_level_test_items`
        :rtype: str
        """
        return self.values.power_level_test_power_level.data

    @power_level_test.setter
    def power_level_test(self, value):
        self.values.power_level_test_power_level.data = value

    @property
    def test_power_level_items(self):
        """
        Test Power Level Items

        :return: list of allowed test power level items
        :rtype: List[str]
        """
        return self.values.power_level_test_power_level.data_items

    @property
    def power_level_frame_count(self):
        """
        Power Level Frame Count

        :return: number of frames
        :rtype: int
        """
        return self.values.power_level_test_frames.data

    @property
    def power_level_acked_frames(self):
        """
        Power Level Acknowledged Frames

        :return: number of frames
        :rtype: int
        """
        return self.values.power_level_test_ack_frames.data

    @property
    def power_level_test_results(self):
        """
        Power Level Test Results

        :return: test status
        :rtype: str
        """
        return self.values.power_level_test_status.data

    def power_level_save(self):
        """
        Power Level Save

        :return: `None`
        :rtype: None
        """
        self.values.power_level_set.data = True

    def power_level_start_test(self):
        """
        Power Level Start Test

        :return: `None`
        :rtype: None
        """

        self.values.power_level_test.data = True

    def power_level_report(self):
        """
        Power Level Report

        :return: `None`
        :rtype: None
        """

        self.values.power_level_report.data = True
