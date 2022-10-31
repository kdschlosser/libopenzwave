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
:synopsis: COMMAND_CLASS_THERMOSTAT_MODE

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Thermostat Mode Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_MODE = 0x40


# noinspection PyAbstractClass
class ThermostatMode(zwave_cmd_class.ZWaveCommandClass):
    """
    Thermostat Mode Command Class

    symbol: `COMMAND_CLASS_THERMOSTAT_MODE`
    """

    class_id = COMMAND_CLASS_THERMOSTAT_MODE
    class_desc = 'COMMAND_CLASS_THERMOSTAT_MODE'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        thermostat_mode = 0

    @property
    def thermostat_operating_mode(self):
        """
        Get/Set the operating mode.

        :param value: the mode,
            one of :py:attr:`ThermostatMode.thermostat_operating_mode_items`
        :type value: str

        :return: current set mode,
            one of :py:attr:`ThermostatMode.thermostat_operating_mode_items`
        :rtype: str
        """
        return self.values.thermostat_mode.data

    @thermostat_operating_mode.setter
    def thermostat_operating_mode(self, value):
        self.values.thermostat_mode.data = value

    @property
    def thermostat_operating_mode_items(self):
        """
        Thermostat Operating Modes

        :return: list of possible thermostat operating modes
        :rtype: List[str]
        """
        return self.values.thermostat_mode.data_items

    @property
    def as_dict(self):
        return dict(
            thermostat_operating_mode=self.thermostat_operating_mode,
            thermostat_operating_mode_items=(
                self.thermostat_operating_mode_items
            )
        )
