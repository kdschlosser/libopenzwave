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
:synopsis: COMMAND_CLASS_METER

.. moduleauthor:: Kevin G Schlosser
"""

import math
from . import zwave_cmd_class

# Meter Command Class - Active
# Application
COMMAND_CLASS_METER = 0x32


class MeterBase(object):
    """
    Base Meter Class
    """
    def __init__(self, node):
        self._node = node

    @property
    def node(self):
        """
        Node that contains the meter readings.

        :rtype: :py:class:`libopenzwave.node.ZWaveNode`
        """
        return self._node

    def __getitem__(self, item):
        meters = {
            ElectricMeter: 'electric',
            GasMeter: 'gas',
            WaterMeter: 'water',
            HeatMeter: 'heating',
            CoolMeter: 'cooling'
        }

        for cls, meter in meters.items():
            if isinstance(self, cls):
                break
        else:
            return None

        value = getattr(
            self._node.values,
            'meter_' + meter + '_unknown_' + str(item)
        )

        if value is None:
            return None

        return value.data


class ElectricMeter(MeterBase):
    """
    Electric Meter
    """

    @property
    def watts(self):
        """
        Watts

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_electric_w.data

    @property
    def amps(self):
        """
        Amps

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_electric_a.data

    @property
    def volts(self):
        """
        Volts

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_electric_v.data

    @property
    def power_factor(self):
        """
        Power Factor

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_electric_powerfactor.data

    @property
    def kilowatt_hour(self):
        """
        Kilowatt Hour (kWh)

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_electric_kwh.data

    @property
    def kilovolt_amp_hour(self):
        """
        Kilovolt Amp Hour (kVAh)

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_electric_kvah.data

    @property
    def pulses(self):
        """
        Meter Pulse Count

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_electric_pulse.data

    @property
    def kilovolt_amp_reactive(self):
        """
        Watts

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_electric_kvar.data

    @property
    def kilovolt_amp_reactive_hour(self):
        """
        Watts

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_electric_kvarh.data


class GasMeter(MeterBase):
    """
    Gas Meter
    """

    @property
    def cubic_meters(self):
        """
        Cubic Meters

        :returns: meter reading
        :rtype: int
        """
        data = self._node.values.meter_gas_cubic_meters.data

        if data is None:
            data = self._node.values.meter_gas_cubic_feet.data
            data /= 35.3147

        return int(round(data))

    @property
    def cubic_feet(self):
        """
        Cubic Feet

        :returns: meter reading
        :rtype: int
        """
        data = self._node.values.meter_gas_cubic_feet.data

        if data is None:
            data = self._node.values.meter_gas_cubic_meters.data
            data *= 35.3147

        return int(round(data))

    @property
    def pulses(self):
        """
        Meter Pulse Count

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_gas_pulse.data


class WaterMeter(MeterBase):
    """
    Water Meter
    """

    @property
    def cubic_meters(self):
        """
        Cubic Meters

        :returns: meter reading
        :rtype: int
        """
        data = self._node.values.meter_water_cubic_meters.data

        if data is None:
            data = self._node.values.meter_water_cubic_feet.data

            if data is None:
                data = self._node.values.meter_water_us_gallons.data
                data /= 264.172
            else:
                data /= 35.3147

        return int(round(data))

    @property
    def cubic_feet(self):
        """
        Cubic Feet

        :returns: meter reading
        :rtype: int
        """
        data = self._node.values.meter_water_cubic_feet.data

        if data is None:
            data = self._node.values.meter_water_cubic_meters.data

            if data is None:
                data = self._node.values.meter_water_us_gallons.data
                data /= 7.48052
            else:
                data *= 35.3147

        return int(round(data))

    @property
    def gallons(self):
        """
        Gallons

        :returns: meter reading
        :rtype: int
        """
        data = self._node.values.meter_water_us_gallons.data

        if data is None:
            data = self._node.values.meter_water_cubic_meters.data

            if data is None:
                data = self._node.values.meter_water_cubic_feet.data
                data *= 7.48052

            else:
                data *= 264.172

        return int(round(data))

    @property
    def pulses(self):
        """
        Meter Pulse Count

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_water_pulse.data


class HeatMeter(MeterBase):
    """
    Heating Meter
    """

    @property
    def kilowatt_hour(self):
        """
        Kilowatt Hour (kWh)

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_heating_kwh.data


class CoolMeter(MeterBase):
    """
    Cooling Meter
    """

    @property
    def kilowatt_hour(self):
        """
        Kilowatt Hour (kWh)

        :returns: meter reading or `None` if not supported
        :rtype: int, Optional
        """
        return self._node.values.meter_cooling_kwh.data


# noinspection PyAbstractClass
class Meter(zwave_cmd_class.ZWaveCommandClass):
    """
    Meter Command Class

    symbol: `COMMAND_CLASS_METER`
    """

    class_id = COMMAND_CLASS_METER
    class_desc = 'COMMAND_CLASS_METER'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        meter_electric_kwh = 0
        meter_electric_kvah = 1  # Kilo Volt Ampere Hours
        meter_electric_w = 2
        meter_electric_pulse = 3
        meter_electric_v = 4
        meter_electric_a = 5
        meter_electric_powerfactor = 6
        meter_electric_unknown_1 = 7
        meter_electric_kvar = 8  # Kilovolt-Ampere Reactive
        meter_electric_kvarh = 9  # Kilovolt-Ampere Reactive hours
        meter_electric_unknown_2 = 10
        meter_electric_unknown_3 = 11
        meter_electric_unknown_4 = 12
        meter_electric_unknown_5 = 13
        meter_electric_unknown_6 = 14
        meter_electric_unknown_7 = 15
        meter_gas_cubic_meters = 16
        meter_gas_cubic_feet = 17
        meter_gas_unknown_1 = 18
        meter_gas_pulse = 19
        meter_gas_unknown_2 = 20
        meter_gas_unknown_3 = 21
        meter_gas_unknown_4 = 22
        meter_gas_unknown_5 = 23
        meter_gas_unknown_6 = 24
        meter_gas_unknown_7 = 25
        meter_gas_unknown_8 = 26
        meter_gas_unknown_9 = 27
        meter_gas_unknown_10 = 28
        meter_gas_unknown_11 = 29
        meter_gas_unknown_12 = 30
        meter_gas_unknown_13 = 31
        meter_water_cubic_meters = 32
        meter_water_cubic_feet = 33
        meter_water_us_gallons = 34
        meter_water_pulse = 35
        meter_water_unknown_1 = 36
        meter_water_unknown_2 = 37
        meter_water_unknown_3 = 38
        meter_water_unknown_4 = 39
        meter_water_unknown_5 = 40
        meter_water_unknown_6 = 41
        meter_water_unknown_7 = 42
        meter_water_unknown_8 = 43
        meter_water_unknown_9 = 44
        meter_water_unknown_10 = 45
        meter_water_unknown_11 = 46
        meter_water_unknown_12 = 47
        meter_heating_kwh = 48
        meter_heating_unknown_1 = 49
        meter_heating_unknown_2 = 50
        meter_heating_unknown_3 = 51
        meter_heating_unknown_4 = 52
        meter_heating_unknown_5 = 53
        meter_heating_unknown_6 = 54
        meter_heating_unknown_7 = 55
        meter_heating_unknown_8 = 56
        meter_heating_unknown_9 = 57
        meter_heating_unknown_10 = 58
        meter_heating_unknown_11 = 59
        meter_heating_unknown_12 = 60
        meter_heating_unknown_13 = 61
        meter_heating_unknown_14 = 62
        meter_heating_unknown_15 = 63
        meter_cooling_kwh = 64
        meter_cooling_unknown_1 = 65
        meter_cooling_unknown_2 = 66
        meter_cooling_unknown_3 = 67
        meter_cooling_unknown_4 = 68
        meter_cooling_unknown_5 = 69
        meter_cooling_unknown_6 = 70
        meter_cooling_unknown_7 = 71
        meter_cooling_unknown_8 = 72
        meter_cooling_unknown_9 = 73
        meter_cooling_unknown_10 = 74
        meter_cooling_unknown_11 = 75
        meter_cooling_unknown_12 = 76
        meter_cooling_unknown_13 = 77
        meter_cooling_unknown_14 = 78
        meter_cooling_unknown_15 = 79
        meter_exporting = 256
        meter_reset = 257

    def meter_reset(self):
        """
        Reset Meter

        :rtype: None
        """
        self.values.meter_reset.data = True

    @property
    def meter(self):
        """
        Gets the meter associated to this node.

        :rtype: ElectricMeter, GasMeter, WaterMeter, HeatMeter, CoolMeter
        """
        for value in self.values:
            index = value.index

            if 0 <= index <= 15 and value.data is not None:  # electric
                cls = ElectricMeter
                break

            elif 16 <= index <= 31 and value.data is not None:  # gas
                cls = GasMeter
                break

            elif 32 <= index <= 47 and value.data is not None:  # water
                cls = WaterMeter
                break

            elif 48 <= index <= 63 and value.data is not None:  # heat
                cls = HeatMeter
                break

            elif 64 <= index <= 79 and value.data is not None:  # cool
                cls = CoolMeter
                break

            else:
                continue
        else:
            return None

        return cls(self)

    @property
    def is_water_meter(self):
        """
        If the meter is a water meter.

        :return: `True`/`False`
        :rtype: bool
        """
        return isinstance(self.meter, WaterMeter)

    @property
    def is_gas_meter(self):
        """
        If the meter is a gas meter.

        :return: `True`/`False`
        :rtype: bool
        """
        return isinstance(self.meter, GasMeter)

    @property
    def is_electric_meter(self):
        """
        If the meter is an electric meter.

        :return: `True`/`False`
        :rtype: bool
        """
        return isinstance(self.meter, ElectricMeter)

    @property
    def is_heating_meter(self):
        """
        If the meter is a heating meter.

        :return: `True`/`False`
        :rtype: bool
        """
        return isinstance(self.meter, HeatMeter)

    @property
    def is_cooling_meter(self):
        """
        If the meter is a cooling meter.

        :return: `True`/`False`
        :rtype: bool
        """
        return isinstance(self.meter, CoolMeter)
