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
:synopsis: COMMAND_CLASS_SWITCH_BINARY

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Binary Switch Command Class - Active
# Application
COMMAND_CLASS_SWITCH_BINARY = 0x25


# noinspection PyAbstractClass
class SwitchBinary(zwave_cmd_class.ZWaveCommandClass):
    """
    Switch Binary Command Class

    symbol: `COMMAND_CLASS_SWITCH_BINARY`
    """

    class_id = COMMAND_CLASS_SWITCH_BINARY
    class_desc = 'COMMAND_CLASS_SWITCH_BINARY'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        switch_binary_state = 0
        switch_binary_target_state = 1
        switch_binary_duration = 2

    @property
    def switch_duration(self):
        """
        Get/Set the switch duration

        :param value: duration
        :type value: int

        :return: The duration
        :rtype: int
        """
        return self.values.switch_binary_duration.data

    @switch_duration.setter
    def switch_duration(self, value):
        self.values.switch_binary_duration.data = value

    @property
    def switch_state(self):
        """
        Get/Set the state of a switch or a dimmer.

        :param value: The state you want to set to `True`/`False`
        :type value: bool

        :return: The state of the value
        :rtype: bool
        """
        return self.values.switch_binary_state.data

    @switch_state.setter
    def switch_state(self, value):
        self.values.switch_binary_state.data = value

    @property
    def switch_target_state(self):
        """
        Actual Switch State

        :return: actual switch state, or `None` if not supported
        :rtype: bool, optional
        """
        return self.values.switch_binary_target_state.data

    @property
    def as_dict(self):
        return dict(
            switch_state=self.switch_state,
            switch_target_state=self.switch_target_state,
        )
