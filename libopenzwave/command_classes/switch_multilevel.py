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


# this is a simple function that remaps a value into a new range.
# this is sued to provide a pad to the duration of the ramping.. the lower
# the diference between level changes the
# higher the returned value. this has to deal with network latencies and such.

def re_map(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    return (((value - old_min) * new_range) / old_range) + new_min


# TODO: Bug Test the ramping and the GE switch level property
class SwitchRamping(object):

    """
    Adjustable ramping of a dimmer level.

    This class is the meat and potatoes of being able to ramp a dimmer up and
    down.
    You have several parameters that are used in this process and by using the
    class in different waysyou are able to achieve different lighting effects.

    An example of a lighting effect would be in a home theater. so you can have
    the lights dim slowly when a movie starts playing and raise the lights
    slowly when it stops. This will work independantly from setting the level
    directly using ZWave and also using the switch manually.


    This class operates in 2 ways. as a context using the `with` statement and
    calling start inside of the context or by calling the start and optionally
    the stop methods outside of a context the range of levels that the light
    will be able to achieve is 1 to 99.

    There are 3 parameters that will need to be passed to the start method.
    They are all optional depending on what you are trying to achieve and also
    if the node supports the various parameters.

    These are the parameters and what they do.

    * target_level: if you supply the target level this is used to determine
      the duration that the program should run for in order to achieve that
      level. This is only possible if the node also supports having the
      duration set.
    * step_duration: This is the amount of time to wait between level changes.
      It is sued to calculate how long the program should run for. If this is
      does not get set and the node supports it then it will use the factory
      ramp duration.
    * start_level: Most time this is going to get left unset. If this does get
      set then this is the level at which the ramping will start at.

    If you use the class in the context manner using `with` it sets the program
    up to be blocking. what this means is that if you pass a target level of 00
    and the start level is 0 and you put in place step duration of 100
    milliseconds You will end up with 100 level changes at 100 ms for each
    change. so (100 * 100) = 10000 milliseconds. so 10000 / 1000 = 10 seconds.

    If you use the class by calling the start method without using `with` this
    will set up the program to be non blocking.

    Thease are the scenarios on how the stop method gets called.

    If you supply a target level and a step duration the program is going to
    call stop for you this is done if you use `with` or do not use it.

    If you only supply the target level and not the step duration you need to
    be sure that the node supports having the duration set. It will use the set
    duration to calculate the total runtime of the program. If the node does not
    support the duration then you will be responsible for calling stop as there
    is no way for the program to determine when to stop.

    If you wish to control the stop yourself simply do not provide a target
    level and do not run the ramp using `with`
    """

    def __init__(self, node, direction_value, skip_ge_step_size=False):
        self.stop_event = threading.Event()
        self._node = node
        self._direction_value = direction_value
        self._ignore_start_level = (
            node.values.switch_multilevel_ignore_start_level
        )
        self._start_level = node.values.switch_multilevel_start_level
        self._duration = node.values.switch_multilevel_duration
        self._skip_ge_step_size = skip_ge_step_size

        self._entered = False

    def __call__(self):
        return self

    def __enter__(self):
        self._entered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def stop(self):
        if self.stop_event.is_set():
            return

        self.stop_event.set()
        self._direction_value.data = False

    def start(self, target_level=None, step_duration=None, start_level=None):
        """
        Starts the program

        :param target_level: 1 - 99, the level you want to have the program
          stop at. to determine when exactly to stop the step_duration
          parameter will also need to be set as well.
        :type target_level: optional, int

        :param step_duration: The length of time to wait between level changes
          in milliseconds. 0 - 2550
        :type step_duration: optional, int

        :param start_level: the level you wish the program to start at..
          most times you will not set this, 0 - 99
        :type start_level: optional, int

        :rtype: None
        """
        if self.stop_event.is_set():
            logger.error(
                'Reuse of a dimmer switch ramping object is not permitted.'
            )
            return

        if step_duration is None:
            full_duration = 0xFF
        elif step_duration > 0:
            full_duration = int((step_duration * 100) / 1000)

            if full_duration > 127 * 60:
                full_duration = 127
        else:
            full_duration = step_duration

        self._duration.data = full_duration

        if start_level is None:
            self._ignore_start_level.data = True
            start_level = self._node.switch_level
        else:
            self._ignore_start_level.data = False
            self._start_level.data = start_level

        if target_level is None:
            if (
                self._direction_value ==
                self._node.values.switch_multilevel_bright
            ):
                target_level = 99
            else:
                target_level = 0

        if target_level < 0:
            target_level = 0
        elif target_level > 99:
            target_level = 99

        level_diff = target_level - start_level

        if level_diff < 0:
            level_diff = -level_diff

        dur_data = self._duration.data

        if dur_data is not None:
            duration = ((dur_data / 100.0) * level_diff) / 1000
        elif step_duration is not None:
            duration = (level_diff * step_duration) / 1000
        else:
            duration = None

        def do(dur, step, lvl_dif):
            self._direction_value.data = True

            if (
                self._node.manufacturer_id == '0x0063' and
                step is not None and
                self._duration.data is None
            ):
                config_step = self._node.values.parameter_7
                config_duration = self._node.values.parameter_8
                saved_step = config_step.data

                if saved_step is not None:
                    if self._skip_ge_step_size:
                        step_size = saved_step
                    else:
                        config_step.data = 1
                        step_size = 1
                else:
                    step_size = 1

                saved_duration = config_duration.data

                if saved_duration is not None:
                    if step == 0:
                        step = 10

                    if int(step / 10) > 255:
                        step = 2550

                    config_duration.data = int(step / 10)
                    step = int(step / 10) * 10
                else:
                    config_step = None
                    config_duration = None
                    saved_step = None
                    saved_duration = None

                num_steps = lvl_dif / step_size
                dur = (num_steps * step) / 1000

                import time

                start = time.time()
                while (
                    time.time() - start < dur and
                    not self.stop_event.is_set()
                ):
                    self.stop_event.wait(step / 1000)

                if saved_step is not None:
                    config_step.data = saved_step

                if saved_duration is not None:
                    config_duration.data = saved_duration

            elif dur is not None:
                self.stop_event.wait(dur)

            if not self._entered and dur is not None:
                self.stop()

            if target_level == 0:
                self._node.switch_level = 0

        if (
            (duration and self._entered) or
            (duration is None and not self._entered)
        ):
            do(duration, step_duration, level_diff)
        elif duration:
            t = threading.Thread(
                target=do,
                args=(duration, step_duration, level_diff)
            )
            t.daemon = True
            t.start()
        else:
            self._direction_value.data = True


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

    def __init__(self):
        self._running_bright_dim = None
        self._bright_dim_lock = threading.Lock()
        zwave_cmd_class.ZWaveCommandClass.__init__(self)

        from . import COMMAND_CLASS_ZWAVEPLUS_INFO

        self._is_plus = self == COMMAND_CLASS_ZWAVEPLUS_INFO

    @property
    def switch_ramp_up(self):
        """
        Ramps up a multi level light.

        This returns an object that is a context based object. it is designed
        to be used in the same manner you would using a file and the "with"
        statement. It allows you to set the start level and the duration each
        step should take in milliseconds. while in the "with" statement you
        call start on the returned object with the duration of time you want to
        hold the switch button for. the maximum allowable hold time is going
        to be `step duration * (99 - start_level)` if a start level is supplied
        or `step_duration * (99 - current_level)` otherwise. if duration is set
        to `None` then the button will simply be "pressed" and the application
        is now going to be responsible for handling how long to wait. the
        button gets released when the "with" statement exits.

        Not all Switched support the ramping speed being sent in this command.
        However, some switches do support having the ramp increments and speed
        set. Use case is some GE switches. in this cause you will want to pass

        :rtype: SwitchRamping
        """
        with self._bright_dim_lock:
            if self._running_bright_dim is not None:
                self._running_bright_dim.stop_event.set()

            self._running_bright_dim = (
                SwitchRamping(self, self.values.switch_multilevel_bright)
            )

            return self._running_bright_dim

    @property
    def switch_ramp_down(self):
        """
        :rtype: SwitchRamping
        """
        with self._bright_dim_lock:
            if self._running_bright_dim is not None:
                self._running_bright_dim.stop_event.set()

            self._running_bright_dim = (
                SwitchRamping(self, self.values.switch_multilevel_dim)
            )

            return self._running_bright_dim

    @property
    def switch_target_level(self):
        """
        Target Level

        This is the value that the dimmer will stop at. This may not be
        the same number as :py:attr:`level`

        :return: target level, if not supported `None`
        :rtype: int, optional
        """
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

    def switch_ge_jasco_level(self, value):
        if self.manufacturer_id == '0x0063':
            if value > 99:
                value = 99
            elif value < 0:
                value = 0

            step_duration = self.values.parameter_8.data

            if step_duration is None:
                logger.warning(
                    'This device does not have the proper '
                    'config variables to use the switch_ge_jasco_level '
                    'set property ({0})'.format(self.id)
                )

            else:
                with self._bright_dim_lock:
                    if self._running_bright_dim is not None:
                        self._running_bright_dim.stop_event.set()

                    if value < self.switch_level:
                        ramp_value = self.values.switch_multilevel_dim
                    else:
                        ramp_value = self.values.switch_multilevel_bright

                    ramp = self._running_bright_dim = (
                        SwitchRamping(self, ramp_value, skip_ge_step_size=True)
                    )

                    ramp.start(
                        target_level=value,
                        step_duration=step_duration * 10,
                        start_level=None
                    )
        else:
            logger.warning(
                'the switch_ce_jasco_level set property can '
                'only be used on GE or Jasco dimmer switches'
            )

    switch_ge_jasco_level = property(fset=switch_ge_jasco_level)

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

        with self._bright_dim_lock:
            if self._running_bright_dim is not None:
                self._running_bright_dim.stop_event.set()

            self._running_bright_dim = None

        self.values.switch_multilevel_level.data = value

    @property
    def as_dict(self):
        return dict(
            switch_level=self.switch_level,
            switch_target_level=self.switch_target_level,
        )
