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
:synopsis: COMMAND_CLASS_HRV_STATUS

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# HRV Status Command Class - Active
# Application
COMMAND_CLASS_HRV_STATUS = 0x37


# noinspection PyAbstractClass
class HRVStatus(zwave_cmd_class.ZWaveCommandClass):
    """
    Heat Recovery Ventilation Status Command Class

    symbol: `COMMAND_CLASS_HRV_STATUS`
    """

    class_id = COMMAND_CLASS_HRV_STATUS
    class_desc = 'COMMAND_CLASS_HRV_STATUS'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        outdoor_air_temperature = 0
        supply_air_temperature = 1
        exhaust_air_temperature = 2
        discharge_air_temperature = 3
        room_air_temperature = 4
        room_relative_humidity = 5
        remaining_filter_life = 6

    @property
    def hrv_outdoor_air_temperature(self):
        """
        The Outdoor Air Temperature

        :rtype: float
        """
        return self.values.outdoor_air_temperature.data

    @property
    def hrv_supply_air_temperature(self):
        """
        The Supply Air Temperature

        :rtype: float
        """
        return self.values.supply_air_temperature.data

    @property
    def hrv_exhaust_air_temperature(self):
        """
        The Exhaust Air Temperature

        :rtype: float
        """
        return self.values.exhaust_air_temperature.data

    @property
    def hrv_discharge_air_temperature(self):
        """
        The Discharge Air Temperature

        :rtype: float
        """
        return self.values.discharge_air_temperature.data

    @property
    def hrv_room_air_temperature(self):
        """
        The Room Air Temperature

        :rtype: float
        """
        return self.values.room_air_temperature.data

    @property
    def hrv_room_relative_humidity(self):
        """
        The Room Relative Humidity

        :rtype: float
        """
        return self.values.room_relative_humidity.data

    @property
    def hrv_remaining_filter_life(self):
        """
        The Remaining Filter Life

        :rtype: int
        """
        return self.values.remaining_filter_life.data
