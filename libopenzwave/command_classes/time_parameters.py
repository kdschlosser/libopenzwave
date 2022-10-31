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
:synopsis: COMMAND_CLASS_TIME_PARAMETERS

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Time Parameters Command Class - Active
# Application
COMMAND_CLASS_TIME_PARAMETERS = 0x8B


# noinspection PyAbstractClass
class TimeParameters(zwave_cmd_class.ZWaveCommandClass):
    """
    Time Parameters Command Class

    symbol: `COMMAND_CLASS_TIME_PARAMETERS`
    """

    class_id = COMMAND_CLASS_TIME_PARAMETERS
    class_desc = 'COMMAND_CLASS_TIME_PARAMETERS'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        time_params_date = 0
        time_params_time = 1
        time_params_set = 2
        time_params_refresh = 3

    @property
    def time_params_date(self):
        """
        Gets the current set date.

        :rtype: str
        """
        return self.values.time_params_date.data

    @property
    def time_params_time(self):
        """
        Gets the current set time.

        :rtype: str
        """
        return self.values.time_params_time.data

    def time_params_set(self):
        """
        Sets the devices date/time to to the system clock running this API

        :rtype: None
        """
        self.values.time_params_set.data = True

    def time_params_refresh(self):
        """
        Refreshes the date and time

        :rtype: None
        """
        self.values.time_params_refresh.data = True
