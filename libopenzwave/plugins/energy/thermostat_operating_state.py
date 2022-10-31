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
:synopsis: COMMAND_CLASS_THERMOSTAT_OPERATING_STATE

.. moduleauthor:: Kevin G Schlosser
"""

import datetime

from ...command_classes import (
    ThermostatOperatingState,
    COMMAND_CLASS_THERMOSTAT_OPERATING_STATE
)
from ... import (
    SIGNAL_VALUE_CHANGED,
    SIGNAL_VALUE_ADDED,
    SIGNAL_VALUE_DATASET_LOADED
)

from .xml_handler import EnergyMixin


# noinspection PyAbstractClass
class EnergyThermostatOperatingState(ThermostatOperatingState):

    def __init__(self):
        ThermostatOperatingState.__init__(self)
        self._heat_energy = EnergyMixin(
            self,
            ThermostatOperatingState,
            'heat'
        )
        self._cool_energy = EnergyMixin(
            self,
            ThermostatOperatingState,
            'cool'
        )

        def _changed_callback(value_data, *_, **__):
            data_list = self.values.thermostat_operating_state.data_list
            state = value_data.data
            index = data_list.index(state)

            usage = self.thermostat_heat_use_history
            if len(usage):
                entry = usage[-1]
                if entry.stop is None:
                    entry.stop = datetime.datetime.now()

            usage = self.thermostat_cool_use_history
            if len(usage):
                entry = usage[-1]
                if entry.stop is None:
                    entry.stop = datetime.datetime.now()

            if index in (1, 8):
                usage = self.thermostat_heat_use_history
                energy = self.thermostat_heat_energy_value

                if index == 8:
                    energy *= 0.5

            elif index in (2, 9):
                usage = self.thermostat_cool_use_history
                energy = self.thermostat_cool_energy_value

                if index == 9:
                    energy *= 0.5
            else:
                return

            entry = usage.new()
            entry.start = datetime.datetime.now()
            entry.energy_used = energy

        def _loading_callback(value, *_, **__):
            if (
                value.command_class == COMMAND_CLASS_THERMOSTAT_OPERATING_STATE and
                value.index == self.values.COMMAND_CLASS_THERMOSTAT_OPERATING_STATE.thermostat_operating_state
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
    def thermostat_heat_energy_units(self):
        """
        Get/Set energy use unit of measure for heating.

        This may be different then the colling unit of measure it is quite
        common to have either a gas or an oil fired forced air furnace and
        electric central air conditioning.

        :param value: unit of measure (watts, btus, amps....)
        :type value: str

        :return: set unit of measure
        :rtype: str
        """
        return self._heat_energy.get_energy_units(
            self.values.thermostat_operating_state.instance
        )

    @thermostat_heat_energy_units.setter
    def thermostat_heat_energy_units(self, value):
        self._heat_energy.set_energy_units(
            self.values.thermostat_operating_state.instance,
            value
        )

    @property
    def thermostat_heat_energy_value(self):
        """
        Get/Set maximum energy consumption of heat.

        For gas/oil this is going to be listed as the btu rating of the unit.
        make sure you use the input rating as this is the amount of energy it
        will consume. the output rating is going to be the
        input rating * (EF rating / 100.0)

        If using gas in order to calculate cost of the energy you will nee to
        know the therm conversion for your area. this can be obtained from
        your gas company.

        If using oil to calculate cost you will need to find out how many btu's
        of heat energy is stored per unit of oil. this can be gotten from your
        oil supplier.

        heat pumps should tell you what the electric use is when being used
        in heat mode.

        anything else you will have to use your judgement.

        :param value: the highest amount of energy the fan can consume.
        :type value: int

        :return: the set maximum consumption
        :rtype: int
        """
        return self._heat_energy.get_energy_units(
            self.values.thermostat_operating_state.instance
        )

    @thermostat_heat_energy_value.setter
    def thermostat_heat_energy_value(self, value):
        self._heat_energy.set_energy_value(
            self.values.thermostat_operating_state.instance,
            value
        )

    @property
    def thermostat_heat_use_history(self):
        """
        Use History

        This will return a list like object containing class instances that
        represent each time the heat has changed state.

        Each of the class instances is going to contain these properties.

        * `start`: a datetime.datetime instance of when this state started
        * `stop`: a datetime.datetime instance of when this state stopped
        * `duration`: a time.time instance of how long the device was in this
          state
        * `energy_used`: It is going to be one of the following.
          0, energy_value (stage 1), energy_value * 0.5 (stage 2)
        * `units`: unit of measure

        you have the ability to clear the whole history by calling `clear` on
        the list that has been returned from this property.

        :rtype: list like object
        """
        return self._heat_energy.get_energy_usage(
            self.values.thermostat_operating_state.instance
        )

    @property
    def thermostat_cool_energy_units(self):
        """
        Get/Set energy use unit of measure for cooling.

        This may be different then the heat unit of measure. If you have a gas
        furnace and a split system air conditioner (central air) This is going
        to be the unit of measure for the condenser (the big square outside
        your house).

        :param value: unit of measure (watts, btus, amps....)
        :type value: str

        :return: set unit of measure for cooling
        :rtype: str
        """
        return self._cool_energy.get_energy_units(
            self.values.thermostat_operating_state.instance
        )

    @thermostat_cool_energy_units.setter
    def thermostat_cool_energy_units(self, value):
        self._cool_energy.set_energy_units(
            self.values.thermostat_operating_state.instance,
            value
        )

    @property
    def thermostat_cool_energy_value(self):
        """
        Get/Set maximum energy consumption for cooling.

        If you have a split system air conditioner (central air) you will want
        to set this number to the consumption of the condenser only.
        (the box with the fan in it that is typically outside).

        There should be a label on the condenser that will tell you the running
        watts or amps. You do not want to use the startup rating as this only
        takes place for a split second.

        If the label only shows the amps then you can calculate watts if you
        want by using `volts * amps = watts`

        :param value: the highest amount of energy the cool can consume.
        :type value: int

        :return: the set maximum consumption
        :rtype: int

        :return:
        """
        return self._cool_energy.get_energy_units(
            self.values.thermostat_operating_state.instance
        )

    @thermostat_cool_energy_value.setter
    def thermostat_cool_energy_value(self, value):
        self._cool_energy.set_energy_value(
            self.values.thermostat_operating_state.instance,
            value
        )

    @property
    def thermostat_cool_use_history(self):
        """
        Use History

        This will return a list like object containing class instances that
        represent each time the cool has changed state.

        Each of the class instances is going to contain these properties.

        * `start`: a datetime.datetime instance of when this state started
        * `stop`: a datetime.datetime instance of when this state stopped
        * `duration`: a time.time instance of how long the device was in this
          state
        * `energy_used`: It is going to be one of the following.
          0, energy_value (stage 1), energy_value * 0.5 (stage 2)
        * `units`: unit of measure

        you have the ability to clear the whole history by calling `clear` on
        the list that has been returned from this property.

        :rtype: list like object
        """
        return self._heat_energy.get_energy_usage(
            self.values.thermostat_operating_state.instance
        )
