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
:synopsis: Energy COMMAND_CLASS_SWITCH_BINARY

.. moduleauthor:: Kevin G Schlosser
"""

import datetime
from ...command_classes import SwitchBinary, COMMAND_CLASS_SWITCH_BINARY
from ... import (
    SIGNAL_VALUE_CHANGED,
    SIGNAL_VALUE_ADDED,
    SIGNAL_VALUE_DATASET_LOADED
)
from .xml_handler import EnergyMixin


# noinspection PyAbstractClass
class EnergySwitchBinary(SwitchBinary):

    def __init__(self):
        SwitchBinary.__init__(self)

        if hasattr(self, '_switch_energy'):
            self._switch_energy = getattr(self, '_switch_energy')
        else:
            self._switch_energy = EnergyMixin(
                self,
                SwitchBinary,
                'switch binary'
            )

            def _changed_callback(value_data, *_, **__):
                usage = self.switch_use_history
                state = value_data

                if len(usage):
                    entry = usage[-1]
                    if entry.stop is None:
                        entry.stop = datetime.datetime.now()

                if state:
                    entry = usage.new()
                    entry.start = datetime.datetime.now()
                    entry.energy_used = self.switch_energy_value

            def _loading_callback(value, *_, **__):
                if (
                    value.command_class == COMMAND_CLASS_SWITCH_BINARY and
                    value.index == self.values.COMMAND_CLASS_SWITCH_BINARY.switch_binary_state
                ):
                    SIGNAL_VALUE_ADDED.unregister(
                        _loading_callback,
                        self
                    )
                    SIGNAL_VALUE_DATASET_LOADED.unregister(
                        _loading_callback,
                        self
                    )

                    SIGNAL_VALUE_CHANGED.register(
                        _changed_callback,
                        value
                    )

            SIGNAL_VALUE_ADDED.register(_loading_callback, self)
            SIGNAL_VALUE_DATASET_LOADED.register(_loading_callback, self)

    @property
    def switch_energy_units(self):
        """
        Get/Set energy use unit of measure.

        :param value: unit of measure (watts, btus, amps....)
        :type value: str

        :return: set unit of measure
        :rtype: str
        """
        return self._switch_energy.get_energy_units(
            self.values.switch_binary_state.instance
        )

    @switch_energy_units.setter
    def switch_energy_units(self, value):
        self._switch_energy.set_energy_units(
            self.values.switch_binary_state.instance,
            value
        )

    @property
    def switch_energy_value(self):
        """
        Get/Set maximum energy consumption of device.

        :param value: the highest amount of energy the device can consume.
            So if you have a 100 watt light bulb set this to 100.
        :type value: int

        :return: the set maximum consumption
        :rtype: int
        """
        return self._switch_energy.get_energy_value(
            self.values.switch_binary_state.instance
        )

    @switch_energy_value.setter
    def switch_energy_value(self, value):
        self._switch_energy.set_energy_value(
            self.values.switch_binary_state.instance,
            value
        )

    @property
    def switch_use_history(self):
        """
        Use History

        This will return a list like object containing class instances that
        represent each time the device has changed state.

        Each of the class instances is going to contain these properties.

        * `start`: a datetime.datetime instance of when this state started
        * `stop`: a datetime.datetime instance of when this state stopped
        * `duration`: a time.time instance of how long the device was in this
          state
        * `energy_used`: It is going to be one of the following.
          0, energy_value or energy_value * state / 100.0
        * `units`: unit of measure

        you have the ability to clear the whole history by calling `clear` on
        the list that has been returned from this property.

        :rtype: list like object
        """
        return self._switch_energy.get_energy_usage(
            self.values.switch_binary_state.instance
        )
