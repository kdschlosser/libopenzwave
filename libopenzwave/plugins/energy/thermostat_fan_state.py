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
:synopsis: Energy COMMAND_CLASS_THERMOSTAT_FAN_STATE

.. moduleauthor:: Kevin G Schlosser
"""

import datetime


from ...command_classes import (
    ThermostatFanState,
    COMMAND_CLASS_THERMOSTAT_FAN_STATE
)

from ... import (
    SIGNAL_VALUE_CHANGED,
    SIGNAL_VALUE_ADDED,
    SIGNAL_VALUE_DATASET_LOADED
)


from .xml_handler import EnergyMixin


# noinspection PyAbstractClass
class EnergyThermostatFanState(ThermostatFanState):

    def __init__(self):
        ThermostatFanState.__init__(self)
        self._fan_energy = EnergyMixin(self, ThermostatFanState, 'fan')

        def _changed_callback(value_data, *_, **__):
            usage = self.thermostat_fan_use_history
            energy = self.thermostat_fan_energy_value

            state = value_data

            if len(usage):
                entry = usage[-1]
                if entry.stop is None:
                    entry.stop = datetime.datetime.now()

            if state == 'Idle':
                return

            if state == 'Running Low':
                energy *= 0.33
            elif state == 'Running Medium':
                energy *= 0.66

            entry = usage.new()
            entry.start = datetime.datetime.now()
            entry.energy_used = energy

        def _loading_callback(value, *_, **__):
            if (
                value.command_class == COMMAND_CLASS_THERMOSTAT_FAN_STATE and
                value.index == self.values.COMMAND_CLASS_THERMOSTAT_FAN_STATE.thermostat_fan_state
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
    def thermostat_fan_energy_units(self):
        """
        Get/Set energy use unit of measure.

        :param value: unit of measure (watts, btus, amps....)
        :type value: str

        :return: set unit of measure
        :rtype: str
        """
        return self._fan_energy.get_energy_units(
            self.values.thermostat_fan_state.instance
        )

    @thermostat_fan_energy_units.setter
    def thermostat_fan_energy_units(self, value):
        self._fan_energy.set_energy_units(
            self.values.thermostat_fan_state.instance,
            value
        )

    @property
    def thermostat_fan_energy_value(self):
        """
        Get/Set maximum energy consumption of device.

        You want to set this value to what the fan in the device consumes.
        Not the whole unit. This might be listed on the device label, and if
        it is not then it will be on the motor for the fan.

        If the label only shows the amps then you can calculate watts if you
        want by using `volts * amps = watts`

        :param value: the highest amount of energy the fan can consume.
        :type value: int

        :return: the set maximum consumption
        :rtype: int
        """
        return self._fan_energy.get_energy_units(
            self.values.thermostat_fan_state.instance
        )

    @thermostat_fan_energy_value.setter
    def thermostat_fan_energy_value(self, value):
        self._fan_energy.set_energy_value(
            self.values.thermostat_fan_state.instance,
            value
        )

    @property
    def thermostat_fan_use_history(self):
        """
        Use History

        This will return a list like object containing class instances that
        represent each time the fan has changed state.

        Each of the class instances is going to contain these properties.

        * `start`: a datetime.datetime instance of when this state started
        * `stop`: a datetime.datetime instance of when this state stopped
        * `duration`: a time.time instance of how long the device was in this
          state
        * `energy_used`: It is going to be one of the following.
          0, energy_value (high), energy_value * 0.33(low) or
          energy_value * 0.66 (medium)
        * `units`: unit of measure

        you have the ability to clear the whole history by calling `clear` on
        the list that has been returned from this property.

        :rtype: list like object
        """
        return self._fan_energy.get_energy_usage(
            self.values.thermostat_fan_state.instance
        )
