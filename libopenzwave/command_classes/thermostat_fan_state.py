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
:synopsis: COMMAND_CLASS_THERMOSTAT_FAN_STATE

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Thermostat Fan State Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_FAN_STATE = 0x45


# noinspection PyAbstractClass
class ThermostatFanState(zwave_cmd_class.ZWaveCommandClass):
    """
    Thermostat Fan State Command Class

    symbol: `COMMAND_CLASS_THERMOSTAT_FAN_STATE`
    """

    class_id = COMMAND_CLASS_THERMOSTAT_FAN_STATE
    class_desc = 'COMMAND_CLASS_THERMOSTAT_FAN_STATE'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        thermostat_fan_state = 0

    @property
    def thermostat_fan_state(self):
        """
        Get thermostat fan state.

        :return: onf os :py:attr:`thermostat_fan_state_items`
        :rtype value: str
        """
        return self.values.thermostat_fan_state.data

    @property
    def thermostat_fan_state_items(self):
        """
        Thermostat Fan State Values.

        :return: list of possible fan states
        :rtype value: List[str]
        """
        return self.values.thermostat_fan_state.data_items

    @property
    def as_dict(self):
        return dict(
            thermostat_fan_state=self.thermostat_fan_state,
            thermostat_fan_state_items=self.thermostat_fan_state_items
        )
