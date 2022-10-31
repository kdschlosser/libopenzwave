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
:synopsis: COMMAND_CLASS_THERMOSTAT_FAN_MODE

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Thermostat Fan Mode Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_FAN_MODE = 0x44


# noinspection PyAbstractClass
class ThermostatFanMode(zwave_cmd_class.ZWaveCommandClass):
    """
    Thermostat Fan Mode Command Class

    symbol: `COMMAND_CLASS_THERMOSTAT_FAN_MODE`
    """

    class_id = COMMAND_CLASS_THERMOSTAT_FAN_MODE
    class_desc = 'COMMAND_CLASS_THERMOSTAT_FAN_MODE'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        thermostat_fan_mode = 0

    @property
    def thermostat_fan_mode(self):
        """
        Get/Set the fan mode.

        :param value: the fan mode, one of
            :py:attr:`thermostat_fan_mode_items`
        :type value: str

        :return: current set fan mode, , one of
            :py:attr:`thermostat_fan_mode_items`
        :rtype: str
        """
        return self.values.thermostat_fan_mode.data

    @thermostat_fan_mode.setter
    def thermostat_fan_mode(self, value):
        self.values.thermostat_fan_mode.data = value

    @property
    def thermostat_fan_mode_items(self):
        """
        Possible Fan Mode Values

        :return: fan modes
        :rtype: List[str]
        """
        return self.values.thermostat_fan_mode.data_items

    @property
    def as_dict(self):
        return dict(
            thermostat_fan_mode=self.thermostat_fan_mode,
            thermostat_fan_mode_items=self.thermostat_fan_mode_items
        )
