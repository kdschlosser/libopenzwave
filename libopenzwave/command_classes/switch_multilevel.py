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
:synopsis: COMMAND_CLASS_SWITCH_MULTILEVEL

.. moduleauthor:: Kevin G Schlosser
"""

import threading
import logging
from . import zwave_cmd_class

logger = logging.getLogger(__name__)


# Multilevel Switch Command Class - Active
# Application
COMMAND_CLASS_SWITCH_MULTILEVEL = 0x26


class _RampTimer(threading.Thread):

    def __init__(self, button, wait, reset_running_ramp):
        self.button = button
        self.wait = wait
        self.reset_running_ramp = reset_running_ramp
        self.event = threading.Event()
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        self.button.data = True
        self.event.wait(self.wait)
        self.button.data = False
        self.reset_running_ramp()

    def stop(self):
        if not self.event.is_set():
            self.event.set()
            self.event.clear()
            self.event.wait(0.005)


# noinspection PyAbstractClass
class SwitchMultilevel(zwave_cmd_class.ZWaveCommandClass):
    """
    Switch Multilevel Command Class

    symbol: `COMMAND_CLASS_SWITCH_MULTILEVEL`
    """

    class_id = COMMAND_CLASS_SWITCH_MULTILEVEL
    class_desc = 'COMMAND_CLASS_SWITCH_MULTILEVEL'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        switch_multilevel_level = 0
        switch_multilevel_bright = 1
        switch_multilevel_dim = 2
        switch_multilevel_ignore_start_level = 3
        switch_multilevel_start_level = 4
        switch_multilevel_duration = 5
        switch_multilevel_step = 6
        switch_multilevel_inc = 7
        switch_multilevel_dec = 8
        switch_multilevel_target_level = 9
        switch_multilevel_target_duration = 10

    def __init__(self):
        self._running_bright_dim = None
        self._bright_dim_lock = threading.Lock()
        zwave_cmd_class.ZWaveCommandClass.__init__(self)

        from . import COMMAND_CLASS_ZWAVEPLUS_INFO

        self._is_plus = self == COMMAND_CLASS_ZWAVEPLUS_INFO
        self._running_ramp = None

    @property
    def switch_duration(self):
        """
        This is a funk value because it does 2 things. With devices that support
        version 4 of the SWITCH_MULTILEVEL command clas this value can change
        as the device reoprts its current level. This would be the amount of
        time left to reach the target value. OR it can be how long you want it
        to take to get to the new level. It woud be wise to check if the target
        level and the current level are the same before setting this value.
        If they are not it could spontaniously change if the device is in the
        middle of a transition which would screw up how fast the lamp
        transitions.

        I put a bug report in for this problem
        https://github.com/OpenZWave/open-zwave/issues/2645

        :rtype: int, None
        """
        if self.switch_command_class_version >= 2:
            return self.values.switch_multilevel_duration.data

    @switch_duration.setter
    def switch_duration(self, value):
        if self.switch_command_class_version >= 2:
            self.values.switch_multilevel_duration.data = value

    @property
    def switch_target_duration(self):
        """
        Not implimented yet see switch duration docstring

        :rtype: int
        """
        if self.switch_command_class_version >= 4:
            return self.values.switch_multilevel_target_duration.data

    @property
    def switch_target_level(self):
        """
        Target Level

        This is the value that the dimmer will stop at. This may not be
        the same number as :py:attr:`level`

        :return: target level, if not supported `None`
        :rtype: int, optional
        """
        if self.switch_command_class_version >= 4:
            return self.values.switch_multilevel_target_level.data

    @property
    def switch_state(self):
        """
        :type value: bool
        :rtype: bool
        """
        return self.switch_level > 0

    @switch_state.setter
    def switch_state(self, value):
        if value:
            self.switch_level = 255
        else:
            self.switch_level = 0

    def switch_ramp(
        self,
        stop_level,
        duration,
        start_level=None,
        step=None
    ):
        """
        Ramps at a given duration.

        This is a nice feature to have for a movie theater where you want the
        light to dim up and down really slow.

        If you set the level or start a new ramp and the lamps are still in the
        middle of the transition the transition will stop and the level will
        change using either the new ramp values or the new level value.

        :param stop_level: 0 - 99
        :type stop_level: int

        :param duration: number of seconds to sweep from 0 to 99. calculations
          are done internally to change the value base on the current level or
          the supplied start_value. Maximum duration is 7619 seconds
          2 hours, 6 minutes and 59 seconds
        :type duration: int

        :param start_level: what level do you want to start off at (0-99) or
          `None` for the current level
        :type start_level: int, None, optional

        :param step: how many increments to take at one go. This only applys to
          motors and actuators and not lights..
        :type step: int, None, optional

        :return: `True` if sucessful, `False` if unsucessful
        :rtype: bool
        """

        if self._running_ramp is not None:
            self._running_ramp.stop()

        if start_level is None:
            self.values.switch_multilevel_ignore_start_level.data = True
            start_level = self.values.switch_multilevel_level.data
            self.values.switch_multilevel_start_level.data = start_level

        else:
            self.values.switch_multilevel_ignore_start_level.data = False
            self.values.switch_multilevel_start_level.data = start_level

        self.values.switch_multilevel_duration.data = duration

        if self.switch_command_class_version >= 3:
            if step is None:
                self.values.switch_multilevel_step.data = 0

                if start_level > stop_level:
                    button = self.values.switch_multilevel_dim
                elif start_level < stop_level:
                    button = self.values.switch_multilevel_bright
                else:
                    return False
            else:
                self.values.switch_multilevel_step.data = step
                if start_level > stop_level:
                    button = self.values.switch_multilevel_dec
                elif start_level < stop_level:
                    button = self.values.switch_multilevel_inc
                else:
                    return False
        else:
            if start_level > stop_level:
                button = self.values.switch_multilevel_dec
            elif start_level < stop_level:
                button = self.values.switch_multilevel_inc
            else:
                return False

        def _reset_running_ramp():
            self.values.switch_multilevel_ignore_start_level.data = True
            self.values.switch_multilevel_duration.data = 7621

            if self.switch_command_class_version >= 3:
                self.values.switch_multilevel_step.data = 0

            self.values.switch_multilevel_start_level.data = 0
            self._running_ramp = None

        step_dur = int(duration / 99)
        num_steps = abs(start_level - stop_level)
        wait = num_steps * step_dur

        self._running_ramp = _RampTimer(button, wait, _reset_running_ramp)
        self._running_ramp.start()

        return True

    @property
    def switch_command_class_version(self):
        """
        The command class version.

        :rtype: int
        """
        cc_data = self.network.manager.getNodeClassInformation(
            self.home_id,
            self.id.node_id,
            COMMAND_CLASS_SWITCH_MULTILEVEL
        )

        return cc_data.version

    @property
    def switch_in_transition(self):
        """
        :rtype: bool
        """
        return self._running_ramp is not None

    @property
    def switch_level(self):
        """
        Get/Set the level of a dimmer.

        :param value: The level a value between 0-99 or 255. 255 set the
            level to the last value. 0 turn the dimmer off.
        :type value: int

        :return: The level a value between 0-99
        :rtype: int
        """

        if not self._is_plus:
            self.values.switch_multilevel_level.refresh()

        return self.values.switch_multilevel_level.data

    @switch_level.setter
    def switch_level(self, value):
        if 99 < value < 255:
            value = 99
        elif value < 0:
            value = 0

        if self._running_ramp is not None:
            self._running_ramp.stop()

        self.values.switch_multilevel_level.data = value

    @property
    def as_dict(self):
        return dict(
            switch_level=self.switch_level,
            switch_target_level=self.switch_target_level,
            switch_target_duration=self.switch_target_duration
        )
