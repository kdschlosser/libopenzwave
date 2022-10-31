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
:synopsis: COMMAND_CLASS_SIMPLE_AV_CONTROL

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Simple AV Control Command Class - Active
# Application
COMMAND_CLASS_SIMPLE_AV_CONTROL = 0x94


# noinspection PyAbstractClass
class SimpleAVControl(zwave_cmd_class.ZWaveCommandClass):
    """
    Simple AV Control Command Class

    symbol: `COMMAND_CLASS_SIMPLE_AV_CONTROL`
    """

    class_id = COMMAND_CLASS_SIMPLE_AV_CONTROL
    class_desc = 'COMMAND_CLASS_SIMPLE_AV_CONTROL'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        command = 0

    def av_control_send(self, command):
        """
        Send AV command

        :param command: one of :py:attr:`av_commands`
        :type command: str

        :return: `None`
        :rtype: None
        """

        self.values.command.data = command

    @property
    def av_control_items(self):
        """
        AV Commands

        :return: list of available AV commands
        :rtype: List[str]
        """

        return self.values.command.data_items

    @property
    def as_dict(self):
        return dict(
            av_control_items=self.av_control_items,
        )
