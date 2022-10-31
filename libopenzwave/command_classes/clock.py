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
:synopsis: COMMAND_CLASS_CLOCK

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Clock Command Class - Active
# Application
COMMAND_CLASS_CLOCK = 0x81


# noinspection PyAbstractClass
class Clock(zwave_cmd_class.ZWaveCommandClass):
    """
    Clock Command Class

    symbol: `COMMAND_CLASS_CLOCK`
    """

    class_id = COMMAND_CLASS_CLOCK
    class_desc = 'COMMAND_CLASS_CLOCK'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        clock_day = 0
        clock_hour = 1
        clock_minute = 2

    @property
    def clock_hour(self):
        """
        Get/Set Clock Hour

        24 hour clock 0-23

        :param value: new clock hour
        :type value: int

        :return: hour the node is set to
        :rtype: int
        """
        return self.values.clock_hour.data

    @clock_hour.setter
    def clock_hour(self, value):
        """
        :type value: int
        """
        self.values.clock_hour.data = value

    @property
    def clock_day(self):
        """
        Get/Set Clock Day

        :param value: one of the days in :py:attr:`clock_day_items`
        :type value: str

        :return:  day the node is set to
        :rtype: str
        """
        return self.values.clock_day.data

    @clock_day.setter
    def clock_day(self, value):
        """
        :type value: str
        """
        self.values.clock_day.data = value

    @property
    def clock_day_items(self):
        """
        Allowed days

        :return: list of allowed days
        :rtype: List[str]
        """
        return self.values.clock_day.data_list

    @property
    def clock_minute(self):
        """
        Get/Set Clock Minute

        0 - 59

        :param value: new clock minute
        :type value: int

        :return: minute the node is set to
        :rtype: int
        """
        return self.values.clock_minute.data

    @clock_minute.setter
    def clock_minute(self, value):
        """
        :type value: int
        """
        self.values.clock_minute.data = value
