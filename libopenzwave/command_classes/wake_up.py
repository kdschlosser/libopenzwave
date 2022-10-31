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
:synopsis: COMMAND_CLASS_WAKE_UP

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Wake Up Command Class - Active
# Management
COMMAND_CLASS_WAKE_UP = 0x84


# noinspection PyAbstractClass
class WakeUp(zwave_cmd_class.ZWaveCommandClass):
    """
    Wake Up Command Class

    symbol: `COMMAND_CLASS_WAKE_UP`
    """

    class_id = COMMAND_CLASS_WAKE_UP
    class_desc = 'COMMAND_CLASS_WAKE_UP'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        wakeup_interval = 0
        wakeup_min_interval = 1
        wakeup_max_interval = 2
        wakeup_default_interval = 3
        wakeup_step_interval = 4

    @property
    def wakeup_interval(self):
        """
        Get/Set the Wake Up Interval

        :param value: new wake up interval
        :type value: int

        :return: the current wake up interval
        :rtype: int
        """
        return self.values.wakeup_interval.data

    @wakeup_interval.setter
    def wakeup_interval(self, value):
        step = self.wakeup_interval_step

        while value % step:
            value -= value % step

        value = min(
            self.wakeup_interval_max,
            max(self.wakeup_interval_min, value)
        )

        self.values.wakeup_interval.data = value

    @property
    def wakeup_interval_min(self):
        """
        Minimum Wake Up Interval

        :rtype: int
        """
        return self.values.wakeup_min_interval.data

    @property
    def wakeup_interval_max(self):
        """
        Maximum Wake Up Interval.

        :rtype: int
        """
        return self.values.wakeup_max_interval.data

    @property
    def wakeup_interval_default(self):
        """
        Default Wake Up Interval

        :rtype: int
        """
        return self.values.wakeup_default_interval.data

    @property
    def wakeup_interval_step(self):
        """
        Wake Up interval Step (increment)

        Amount you are allowed to increase or decrease the interval by.

        :rtype: int
        """
        return self.values.wakeup_step_interval.data
