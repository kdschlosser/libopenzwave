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
:synopsis: COMMAND_CLASS_BARRIER_OPERATOR

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Barrier Operator Command Class - Active
# Application
COMMAND_CLASS_BARRIER_OPERATOR = 0x66


# noinspection PyAbstractClass
class BarrierOperator(zwave_cmd_class.ZWaveCommandClass):
    """
    Barrier Operator Command Class

    symbol: `COMMAND_CLASS_BARRIER_OPERATOR`
    """

    class_id = COMMAND_CLASS_BARRIER_OPERATOR
    class_desc = 'COMMAND_CLASS_BARRIER_OPERATOR'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        barrier_command = 0
        barrier_state = 1
        supported_signals = 2
        audible_signal = 3
        visual_signal = 4

    @property
    def barrier_state(self):
        """
        Get/Set The barrier state

        :param value: new state,
            one of :py:attr:`BarrierOperatorbarrier_state_items`
        :type value: str

        :return: The state of the barrier,
            one of :py:attr:`BarrierOperator.barrier_state_items`
        :rtype: str
        """
        return self.values.barrier_state.data

    @barrier_state.setter
    def barrier_state(self, value):
        """
        :type value: str
        """
        self.values.barrier_state.data = value

    @property
    def barrier_state_items(self):
        """
        Barrier state items.

        This returns a list of allowed barrier states to be set.

        :return: Allowed barrier states
        :rtype: list
        """
        return self.values.barrier_state.data_list

    @property
    def is_barrier_audible_supported(self):
        """
        Checks to see if the barrier supports audible signals.

        :return: `True`/`False`
        :rtype: bool
        """
        value = self.values.supported_signals.data
        items = self.values.supported_signals.data.data_items

        return items.index(value) in (1, 3)

    @property
    def barrier_audible_notification(self):
        """
        Get/Set (turn on and off) the barriers audible signal.

        :param value:
            Allowed values:

                * `True`: Turn signal on
                * `False` Turn signal off

        :type value: bool

        :return:

            Possible returned values:

                * `True`: Signal is on
                * `False` Signal is off
                * `None`: Not supported.

        :rtype: bool, optional
        """
        if not self.is_barrier_audible_supported:
            return None

        return self.values.audible_signal.data

    @barrier_audible_notification.setter
    def barrier_audible_notification(self, value):
        """
        :type value: bool
        """
        if self.is_barrier_audible_supported:
            self.values.audible_signal.data = value

    def toggle_barrier_audible_notification(self):
        """
        Toggles the barrier audible signal on and off.

        :return: The new audible state or `None` if not supported
        :rtype: bool, optional
        """
        state = self.barrier_audible_notification

        if state is None:
            return None

        self.barrier_audible_notification = not state

        return not state

    @property
    def is_barrier_visual_supported(self):
        """
        Checks to see if the barrier supports visual signals.

        :return: `True`/`False`
        :rtype: bool
        """
        value = self.values.supported_signals.data
        items = self.values.supported_signals.data.data_items

        return items.index(value) in (2, 3)

    @property
    def barrier_visual_notification(self):
        """
        Get/Set (turn on and off) the barriers visual signal.

        :param value:
            Allowed values:

                * `True`: Turn signal on
                * `False` Turn signal off

        :type value: bool

        :return:
            Possible returned values:

                * `True`: Signal is on
                * `False` Signal is off
                * `None`: Not supported.

        :rtype: bool, optional
        """
        if not self.is_barrier_visual_supported:
            return None

        return self.values.visual_signal.data

    @barrier_visual_notification.setter
    def barrier_visual_notification(self, value):
        """
        :type value: bool
        """
        if self.is_barrier_visual_supported:
            self.values.visual_signal.data = value

    def toggle_barrier_visual_notification(self):
        """
        Toggles the barrier visual signal on and off.

        :return: The new visual state or `None` if not supported
        :rtype: bool, optional
        """
        state = self.barrier_visual_notification

        if state is None:
            return None

        self.barrier_visual_notification = not state

        return not state
