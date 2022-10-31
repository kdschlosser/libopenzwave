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
:synopsis: COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class
from .thermostat_setpoint import ThermostatSetpointSetpoint

# Humidity Control Setpoint Command Class - Active
# Application
COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT = 0x64


# noinspection PyAbstractClass
class HumidityControlSetpoint(zwave_cmd_class.ZWaveCommandClass):
    """
    Humidity Control Setpoint Command Class

    symbol: `COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT`
    """

    class_id = COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT
    class_desc = 'COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        humidifier = 0
        de_humidifier = 1
        auto = 2

    @property
    def humidity_humidifier_setpoint(self):
        """
        Get/Set the target humidity level.

        :param value: new target level
        :type value: float

        :return: current target level
        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self.values.humidifier)

    @humidity_humidifier_setpoint.setter
    def humidity_humidifier_setpoint(self, value):
        self.values.humidifier.data = value

    @property
    def humidity_de_humidifier_setpoint(self):
        """
        Get/Set the target de humidity level.

        :param value: new target level
        :type value: float

        :return: current target level
        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self.values.de_humidifier)

    @humidity_de_humidifier_setpoint.setter
    def humidity_de_humidifier_setpoint(self, value):
        self.values.de_humidifier.data = value

    @property
    def humidity_auto_setpoint(self):
        """
        Get/Set the target auto humidity level.

        :param value: new target level
        :type value: float

        :return: current target level
        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self.values.auto)

    @humidity_auto_setpoint.setter
    def humidity_auto_setpoint(self, value):
        self.values.auto.data = value
