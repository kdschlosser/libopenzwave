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
:synopsis: COMMAND_CLASS_THERMOSTAT_SETPOINT

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Thermostat Setpoint Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_SETPOINT = 0x43


class ThermostatSetpointSetpoint(object):
    """
    Base Setpoint Class

    This class acts like an integer with a few extras.
    """

    def __init__(self, value):
        self.__value = value

    @property
    def as_dict(self):
        """
        Dictionary representation of this class instance.

        :rtype: dict
        """
        return dict(
            unit=self.units,
            setpoint=self.__value.data
        )

    @property
    def units(self):
        """
        Get/Set Unit of measure

        :param value: new unit of measure
        :type value: str

        :rtype: str
        """
        return self.__value.units

    @units.setter
    def units(self, value):
        self.__value.units = value

    def __int__(self):
        data = self.__value.data

        if data is None:
            return 0

        return int(round(data))

    def __float__(self):
        data = self.__value.data
        if data is None:
            return 0.00

        return data

    def __str__(self):
        data = self.__value.data

        if data is None:
            return 'None'

        return '{0:0.2f}'.format(data)

    def __iadd__(self, other):
        value = self.__value.data
        if value is None:
            return self

        value += other
        self.__value.data = value
        return self

    def __isub__(self, other):
        value = self.__value.data

        if value is None:
            return self

        value -= other
        self.__value.data = value
        return self

    def __imul__(self, other):
        value = self.__value.data

        if value is None:
            return self

        value *= other
        self.__value.data = value
        return self

    def __idiv__(self, other):
        value = self.__value.data

        if value is None:
            return self

        value /= other
        self.__value.data = value
        return self

    def __radd__(self, other):
        value = self.__value.data

        if value is None:
            return other

        return other + value

    def __rsub__(self, other):
        value = self.__value.data

        if value is None:
            return other

        return other - value

    def __rmul__(self, other):
        value = self.__value.data

        if value is None:
            return other

        return other * value

    def __rdiv__(self, other):
        value = self.__value.data
        return other / value

    def __add__(self, other):
        value = self.__value.data

        if value is None:
            return other

        return value + other

    def __sub__(self, other):
        value = self.__value.data

        if value is None:
            return other

        return value - other

    def __mul__(self, other):
        value = self.__value.data

        if value is None:
            return other

        return value * other

    def __truediv__(self, other):
        value = self.__value.data

        if value is None:
            return other

        return value / other


class HeatingSetpoint(ThermostatSetpointSetpoint):

    def __init__(self, node):
        self._node = node
        ThermostatSetpointSetpoint.__init__(self, node.values.thermostat_heating)

    @property
    def stage1(self):
        """
        Get/Set Stage 1 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_heating_stage_1)

    @stage1.setter
    def stage1(self, value):
        self._node.values.thermostat_heating_stage_1.data = value

    @property
    def stage2(self):
        """
        Get/Set Stage 2 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_heating_stage_2)

    @stage2.setter
    def stage2(self, value):
        self._node.values.thermostat_heating_stage_2.data = value

    @property
    def as_dict(self):
        res = dict(
            stage1=self.stage1.as_dict,
            stage2=self.stage2.as_dict
        )

        # noinspection PyArgumentList
        res.update(ThermostatSetpointSetpoint.as_dict.fget(self))
        return res


class CoolingSetpoint(ThermostatSetpointSetpoint):

    def __init__(self, node):
        self._node = node
        ThermostatSetpointSetpoint.__init__(self, node.values.thermostat_cooling)

    @property
    def stage1(self):
        """
        Get/Set Stage 1 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_cooling_stage_1)

    @stage1.setter
    def stage1(self, value):
        self._node.values.thermostat_cooling_stage_1.data = value

    @property
    def stage2(self):
        """
        Get/Set Stage 2 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_cooling_stage_2)

    @stage2.setter
    def stage2(self, value):
        self._node.values.thermostat_cooling_stage_2.data = value

    @property
    def as_dict(self):
        res = dict(
            stage1=self.stage1.as_dict,
            stage2=self.stage2.as_dict
        )

        # noinspection PyArgumentList
        res.update(ThermostatSetpointSetpoint.as_dict.fget(self))
        return res


class DryAirSetpoint(ThermostatSetpointSetpoint):

    def __init__(self, node):
        self._node = node
        ThermostatSetpointSetpoint.__init__(self, node.values.thermostat_dry_air)

    @property
    def stage1(self):
        """
        Get/Set Stage 1 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint`
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_dry_air_stage_1)

    @stage1.setter
    def stage1(self, value):
        self._node.values.thermostat_dry_air_stage_1.data = value

    @property
    def stage2(self):
        """
        Get/Set Stage 2 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_dry_air_stage_2)

    @stage2.setter
    def stage2(self, value):
        self._node.values.thermostat_dry_air_stage_2.data = value

    @property
    def as_dict(self):
        res = dict(
            stage1=self.stage1.as_dict,
            stage2=self.stage2.as_dict
        )

        # noinspection PyArgumentList
        res.update(ThermostatSetpointSetpoint.as_dict.fget(self))
        return res


class FurnaceSetpoint(ThermostatSetpointSetpoint):

    def __init__(self, node):
        self._node = node
        ThermostatSetpointSetpoint.__init__(self, node.values.thermostat_furnace)

    @property
    def stage1(self):
        """
        Get/Set Stage 1 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_furnace_stage_1)

    @stage1.setter
    def stage1(self, value):
        self._node.values.thermostat_furnace_stage_1.data = value

    @property
    def stage2(self):
        """
        Get/Set Stage 2 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_furnace_stage_2)

    @stage2.setter
    def stage2(self, value):
        self._node.values.thermostat_furnace_stage_2.data = value

    @property
    def as_dict(self):
        res = dict(
            stage1=self.stage1.as_dict,
            stage2=self.stage2.as_dict
        )

        # noinspection PyArgumentList
        res.update(ThermostatSetpointSetpoint.as_dict.fget(self))
        return res


class AutoChangeoverSetpoint(ThermostatSetpointSetpoint):

    def __init__(self, node):
        self._node = node
        ThermostatSetpointSetpoint.__init__(self, node.values.thermostat_auto_changeover)

    @property
    def stage1(self):
        """
        Get/Set Stage 1 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_auto_changeover_stage_1)

    @stage1.setter
    def stage1(self, value):
        self._node.values.thermostat_auto_changeover_stage_1.data = value

    @property
    def stage2(self):
        """
        Get/Set Stage 2 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_auto_changeover_stage_2)

    @stage2.setter
    def stage2(self, value):
        self._node.values.thermostat_auto_changeover_stage_2.data = value

    @property
    def as_dict(self):
        res = dict(
            stage1=self.stage1.as_dict,
            stage2=self.stage2.as_dict
        )

        # noinspection PyArgumentList
        res.update(ThermostatSetpointSetpoint.as_dict.fget(self))
        return res


class MoistAirSetpoint(ThermostatSetpointSetpoint):

    def __init__(self, node):
        self._node = node
        ThermostatSetpointSetpoint.__init__(self, node.values.thermostat_moist_air)

    @property
    def stage1(self):
        """
        Get/Set Stage 1 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_moist_air_stage_1)

    @stage1.setter
    def stage1(self, value):
        self._node.values.thermostat_moist_air_stage_1.data = value

    @property
    def stage2(self):
        """
        Get/Set Stage 2 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_moist_air_stage_2)

    @stage2.setter
    def stage2(self, value):
        self._node.values.thermostat_moist_air_stage_2.data = value

    @property
    def as_dict(self):
        res = dict(
            stage1=self.stage1.as_dict,
            stage2=self.stage2.as_dict
        )

        # noinspection PyArgumentList
        res.update(ThermostatSetpointSetpoint.as_dict.fget(self))
        return res


class HeatingEconSetpoint(ThermostatSetpointSetpoint):

    def __init__(self, node):
        self._node = node
        ThermostatSetpointSetpoint.__init__(self, node.values.thermostat_heating_econ)

    @property
    def stage1(self):
        """
        Get/Set Stage 1 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_heating_econ_stage_1)

    @stage1.setter
    def stage1(self, value):
        self._node.values.thermostat_heating_econ_stage_1.data = value

    @property
    def stage2(self):
        """
        Get/Set Stage 2 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_heating_econ_stage_2)

    @stage2.setter
    def stage2(self, value):
        self._node.values.thermostat_heating_econ_stage_2.data = value

    @property
    def as_dict(self):
        res = dict(
            stage1=self.stage1.as_dict,
            stage2=self.stage2.as_dict
        )

        # noinspection PyArgumentList
        res.update(ThermostatSetpointSetpoint.as_dict.fget(self))
        return res


class CoolingEconSetpoint(ThermostatSetpointSetpoint):

    def __init__(self, node):
        self._node = node
        ThermostatSetpointSetpoint.__init__(self, node.values.thermostat_cooling_econ)

    @property
    def stage1(self):
        """
        Get/Set Stage 1 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_cooling_econ_stage_1)

    @stage1.setter
    def stage1(self, value):
        self._node.values.thermostat_cooling_econ_stage_1.data = value

    @property
    def stage2(self):
        """
        Get/Set Stage 2 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_cooling_econ_stage_2)

    @stage2.setter
    def stage2(self, value):
        self._node.values.thermostat_cooling_econ_stage_2.data = value

    @property
    def as_dict(self):
        res = dict(
            stage1=self.stage1.as_dict,
            stage2=self.stage2.as_dict
        )

        # noinspection PyArgumentList
        res.update(ThermostatSetpointSetpoint.as_dict.fget(self))
        return res


class AwayHeatingSetpoint(ThermostatSetpointSetpoint):

    def __init__(self, node):
        self._node = node
        ThermostatSetpointSetpoint.__init__(self, node.values.thermostat_away_heating)

    @property
    def stage1(self):
        """
        Get/Set Stage 1 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_away_heating_stage_1)

    @stage1.setter
    def stage1(self, value):
        self._node.values.thermostat_away_heating_stage_1.data = value

    @property
    def stage2(self):
        """
        Get/Set Stage 2 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_away_heating_stage_2)

    @stage2.setter
    def stage2(self, value):
        self._node.values.thermostat_away_heating_stage_2.data = value

    @property
    def as_dict(self):
        res = dict(
            stage1=self.stage1.as_dict,
            stage2=self.stage2.as_dict
        )

        # noinspection PyArgumentList
        res.update(ThermostatSetpointSetpoint.as_dict.fget(self))
        return res


class AwayCoolingSetpoint(ThermostatSetpointSetpoint):

    def __init__(self, node):
        self._node = node
        ThermostatSetpointSetpoint.__init__(self, node.values.thermostat_away_cooling)

    @property
    def stage1(self):
        """
        Get/Set Stage 1 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_away_cooling_stage_1)

    @stage1.setter
    def stage1(self, value):
        self._node.values.thermostat_away_cooling_stage_1.data = value

    @property
    def stage2(self):
        """
        Get/Set Stage 2 of a multi stage thermostat

        :param value: new setpoint
        :type value: float

        :rtype: ThermostatSetpointSetpoint
        """
        return ThermostatSetpointSetpoint(self._node.values.thermostat_away_cooling_stage_2)

    @stage2.setter
    def stage2(self, value):
        self._node.values.thermostat_away_cooling_stage_2.data = value

    @property
    def as_dict(self):
        res = dict(
            stage1=self.stage1.as_dict,
            stage2=self.stage2.as_dict
        )

        # noinspection PyArgumentList
        res.update(ThermostatSetpointSetpoint.as_dict.fget(self))
        return res


# noinspection PyAbstractClass
class ThermostatSetpoint(zwave_cmd_class.ZWaveCommandClass):
    """
    Thermostat Setpoint Command Class

    symbol: `COMMAND_CLASS_THERMOSTAT_SETPOINT`
    """

    class_id = COMMAND_CLASS_THERMOSTAT_SETPOINT
    class_desc = 'COMMAND_CLASS_THERMOSTAT_SETPOINT'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        thermostat_unused_0 = 0
        thermostat_heating = 1
        thermostat_cooling = 2
        thermostat_unused_3 = 3
        thermostat_unused_4 = 4
        thermostat_unused_5 = 5
        thermostat_unused_6 = 6
        thermostat_furnace = 7
        thermostat_dry_air = 8
        thermostat_moist_air = 9
        thermostat_auto_changeover = 10
        thermostat_heating_econ = 11
        thermostat_cooling_econ = 12
        thermostat_away_heating = 13
        thermostat_away_cooling = 14
        thermostat_unused_0_stage_1 = 100
        thermostat_heating_stage_1 = 101
        thermostat_cooling_stage_1 = 102
        thermostat_unused_3_stage_1 = 103
        thermostat_unused_4_stage_1 = 104
        thermostat_unused_5_stage_1 = 105
        thermostat_unused_6_stage_1 = 106
        thermostat_furnace_stage_1 = 107
        thermostat_dry_air_stage_1 = 108
        thermostat_moist_air_stage_1 = 109
        thermostat_auto_change_over_stage_1 = 110
        thermostat_heating_econ_stage_1 = 111
        thermostat_cooling_econ_stage_1 = 112
        thermostat_away_heating_stage_1 = 113
        thermostat_away_cooling_stage_1 = 114
        thermostat_unused_0_stage_2 = 200
        thermostat_heating_stage_2 = 201
        thermostat_cooling_stage_2 = 202
        thermostat_unused_3_stage_2 = 203
        thermostat_unused_4_stage_2 = 204
        thermostat_unused_5_stage_2 = 205
        thermostat_unused_6_stage_2 = 206
        thermostat_furnace_stage_2 = 207
        thermostat_dry_air_stage_2 = 208
        thermostat_moist_air_stage_2 = 209
        thermostat_auto_change_over_stage_2 = 210
        thermostat_heating_econ_stage_2 = 211
        thermostat_cooling_econ_stage_2 = 212
        thermostat_away_heating_stage_2 = 213
        thermostat_away_cooling_stage_2 = 214

    @property
    def thermostat_heat_setpoint(self):
        """
        Get/Set the target heat temperature.

        :param value: new target temperature
        :type value: float

        :return: current target temperature
        :rtype: HeatingSetpoint
        """
        return HeatingSetpoint(self)

    @thermostat_heat_setpoint.setter
    def thermostat_heat_setpoint(self, value):
        self.values.thermostat_heating.data = value

    @property
    def thermostat_economy_heat_setpoint(self):
        """
        Get/Set the target economy heat temperature.

        :param value: new target temperature
        :type value: float

        :return: current target temperature
        :rtype: HeatingEconSetpoint
        """
        return HeatingEconSetpoint(self)

    @thermostat_economy_heat_setpoint.setter
    def thermostat_economy_heat_setpoint(self, value):
        self.values.thermostat_economy_heating.data = value

    @property
    def thermostat_away_heat_setpoint(self):
        """
        Get/Set the target away heat temperature.

        :param value: new target temperature
        :type value: float

        :return: current target temperature
        :rtype: AwayHeatingSetpoint
        """
        return AwayHeatingSetpoint(self)

    @thermostat_away_heat_setpoint.setter
    def thermostat_away_heat_setpoint(self, value):
        self.values.thermostat_away_heating.data = value

    @property
    def thermostat_cool_setpoint(self):
        """
        Get/Set the target cool temperature.

        :param value: new target temperature
        :type value: float

        :return: current target temperature
        :rtype: CoolingSetpoint
        """
        return CoolingSetpoint(self)

    @thermostat_cool_setpoint.setter
    def thermostat_cool_setpoint(self, value):
        self.values.thermostat_cooling.data = value

    @property
    def thermostat_economy_cool_setpoint(self):
        """
        Get/Set the target economy cool temperature.

        :param value: new target temperature
        :type value: float

        :return: current target temperature
        :rtype: CoolingEconSetpoint
        """
        return CoolingEconSetpoint(self)

    @thermostat_economy_cool_setpoint.setter
    def thermostat_economy_cool_setpoint(self, value):
        self.values.thermostat_economy_cooling.data = value

    @property
    def thermostat_away_cool_setpoint(self):
        """
        Get/Set the target away cool temperature.

        :param value: new target temperature
        :type value: float

        :return: current target temperature
        :rtype: AwayCoolingSetpoint
        """
        return AwayCoolingSetpoint(self)

    @thermostat_away_cool_setpoint.setter
    def thermostat_away_cool_setpoint(self, value):
        self.values.thermostat_away_cooling.data = value

    @property
    def thermostat_auto_changeover_setpoint(self):
        """
        Get/Set the target auto changeover temperature.

        :param value: new target temperature
        :type value: float

        :return: current target temperature
        :rtype: AutoChangeoverSetpoint
        """
        return AutoChangeoverSetpoint(self)

    @thermostat_auto_changeover_setpoint.setter
    def thermostat_auto_changeover_setpoint(self, value):
        self.values.thermostat_auto_changeover.data = value

    @property
    def thermostat_moist_air_setpoint(self):
        """
        Get/Set the target moist air temperature.

        :param value: new target temperature
        :type value: float

        :return: current target temperature
        :rtype: MoistAirSetpoint
        """
        return MoistAirSetpoint(self)

    @thermostat_moist_air_setpoint.setter
    def thermostat_moist_air_setpoint(self, value):
        self.values.thermostat_moist_air.data = value

    @property
    def thermostat_dry_air_setpoint(self):
        """
        Get/Set the target dry air temperature.

        :param value: new target temperature
        :type value: float

        :return: current target temperature
        :rtype: DryAirSetpoint
        """
        return DryAirSetpoint(self)

    @thermostat_dry_air_setpoint.setter
    def thermostat_dry_air_setpoint(self, value):
        self.values.thermostat_dry_air.data = value

    @property
    def as_dict(self):
        return dict(
            thermostat_heat_setpoint=(
                self.thermostat_heat_setpoint.as_dict
            ),
            thermostat_economy_heat_setpoint=(
                self.thermostat_economy_heat_setpoint.as_dict
            ),
            thermostat_away_heat_setpoint=(
                self.thermostat_away_heat_setpoint.as_dict
            ),
            thermostat_cool_setpoint=(
                self.thermostat_cool_setpoint.as_dict
            ),
            thermostat_economy_cool_setpoint=(
                self.thermostat_economy_cool_setpoint.as_dict
            ),
            thermostat_away_cool_setpoint=(
                self.thermostat_away_cool_setpoint.as_dict
            ),
            thermostat_auto_changeover_setpoint=(
                self.thermostat_auto_changeover_setpoint.as_dict
            ),
            thermostat_moist_air_setpoint=(
                self.thermostat_moist_air_setpoint.as_dict
            ),
            thermostat_dry_air_setpoint=(
                self.thermostat_dry_air_setpoint.as_dict
            )
        )
