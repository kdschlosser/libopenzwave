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
:synopsis: COMMAND_CLASS_ENERGY_PRODUCTION

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Energy Production Command Class - Active
# Application
COMMAND_CLASS_ENERGY_PRODUCTION = 0x90


# noinspection PyAbstractClass
class EnergyProduction(zwave_cmd_class.ZWaveCommandClass):
    """
    Energy Production Command Class

    symbol: `COMMAND_CLASS_ENERGY_PRODUCTION`
    """

    class_id = COMMAND_CLASS_ENERGY_PRODUCTION
    class_desc = 'COMMAND_CLASS_ENERGY_PRODUCTION'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        e_production_instant = 0
        e_production_total = 1
        e_production_today = 2
        e_production_time = 3

    @property
    def energy_production_current(self):
        """
        Current Energy Production

        :return: current production
        :rtype: int
        """
        return self.values.e_production_instant.data

    @property
    def energy_production_total(self):
        """
        Total Energy Production

        :return: total production
        :rtype: int
        """
        return self.values.e_production_total.data

    @property
    def energy_production_today(self):
        """
        Energy Production Today

        :return: energy production
        :rtype: int
        """
        return self.values.e_production_today.data

    @property
    def energy_production_total_time(self):
        """
        Total Energy Production Time

        :return: total time in seconds
        :rtype: int
        """
        return self.values.e_production_time.data
