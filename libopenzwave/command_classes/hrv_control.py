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
:synopsis: COMMAND_CLASS_HRV_CONTROL

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# HRV Control Command Class - Active
# Application
COMMAND_CLASS_HRV_CONTROL = 0x39


# noinspection PyAbstractClass
class HRVControl(zwave_cmd_class.ZWaveCommandClass):
    """
    Heat Recovery Ventilation Command Class

    symbol: `COMMAND_CLASS_HRV_CONTROL`
    """

    class_id = COMMAND_CLASS_HRV_CONTROL
    class_desc = 'COMMAND_CLASS_HRV_CONTROL'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        mode = 0
        bypass = 1
        ventilation_rate = 2

    @property
    def hrv_mode(self):
        """
        Get/Set the mode.

        :param value: the mode, one of
            :py:attr:`hrv_mode_items`
        :type value: str

        :return: current set mode, one of
            :py:attr:`hrv_mode_items`
        :rtype: str
        """
        return self.values.mode.data

    @hrv_mode.setter
    def hrv_mode(self, value):
        self.values.mode.data = value

    @property
    def hrv_mode_items(self):
        """
        Possible Mode Values

        :rtype: List[str]
        """
        return self.values.mode.data_items

    @property
    def hrv_bypass(self):
        """
        Get/Set the bypass

        :param value: new bypass
        :type value: Any

        :rtype: Any
        """
        return self.values.bypass.data

    @hrv_bypass.setter
    def hrv_bypass(self, value):
        self.values.bypass.data = value

    @property
    def hrv_ventilation_rate(self):
        """
        Get/Set the ventilation rate

        :param value: new ventilation rate
        :type value: Any

        :rtype: Any
        """
        return self.values.ventilation_rate.data

    @hrv_ventilation_rate.setter
    def hrv_ventilation_rate(self, value):
        self.values.ventilation_rate.data = value
