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
:synopsis: ZWave node types API

.. moduleauthor:: Kevin G Schlosser
"""


class DeviceType(int):
    value = 0
    doc = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        value = args[1]

        self = super(DeviceType, cls).__new__(*args, **kwargs)
        setattr(self, 'value', value)
        return self

    def set_doc(self, value):
        """
        :param value:
        :type value: str

        :rtype: "DeviceType"
        """
        if self.doc is None:
            self.doc = value
            self.__doc__ = value

        return self

    def __int__(self):
        return self.value

    def __str__(self):
        return self.doc

    def __eq__(self, other):
        """
        :param other:
        :type other: int, "DeviceType"

        :rtype: "DeviceType"
        """
        if isinstance(other, int):
            return int(self) == other

        return object.__eq__(self, other)

    def __ne__(self, other):
        """
        :param other:
        :type other: int, "DeviceType"

        :rtype: "DeviceType"
        """
        return not self.__eq__(other)


DEVICE_TYPE_UNKNOWN = DeviceType(-1).set_doc('Type Unknown')
DEVICE_TYPE_CENTRAL_CONTROLLER = (
    DeviceType(0x0100).set_doc('Central Controller')
)
DEVICE_TYPE_DISPLAY_SIMPLE = (
    DeviceType(0x0200).set_doc('Display (simple)')
)
DEVICE_TYPE_DOOR_LOCK_KEYPAD = (
    DeviceType(0x0300).set_doc('Door Lock Keypad')
)
DEVICE_TYPE_SWITCH_FAN = (
    DeviceType(0x0400).set_doc('Fan Switch')
)
DEVICE_TYPE_GATEWAY = (
    DeviceType(0x0500).set_doc('Gateway')
)
DEVICE_TYPE_SWITCH_MULTILEVEL = (
    DeviceType(0x0600).set_doc('Light Dimmer Switch')
)
DEVICE_TYPE_SWITCH_BINARY = (
    DeviceType(0x0700).set_doc('On/Off Power Switch')
)
DEVICE_TYPE_POWER_STRIP = (
    DeviceType(0x0800).set_doc('Power Strip')
)
DEVICE_TYPE_REMOTE_CONTROL_AV = (
    DeviceType(0x0900).set_doc('Remote Control (AV)')
)
DEVICE_TYPE_REMOTE_CONTROL_MULTI_PURPOSE = (
    DeviceType(0x0A00).set_doc('Remote Control (multi purpose)')
)
DEVICE_TYPE_REMOTE_CONTROL_SIMPLE = (
    DeviceType(0x0B00).set_doc('Remote Control (simple)')
)
DEVICE_TYPE_KEY_FOB = (
    DeviceType(0x0B01).set_doc('Key Fob')
)
DEVICE_TYPE_SENSOR_NOTIFICATION = (
    DeviceType(0x0C00).set_doc('Sensor (notification)')
)
DEVICE_TYPE_SENSOR_SMOKE_ALARM = (
    DeviceType(0x0C01).set_doc('Sensor (smoke alarm)')
)
DEVICE_TYPE_SENSOR_CO_ALARM = (
    DeviceType(0x0C02).set_doc('Sensor (CO)')
)
DEVICE_TYPE_SENSOR_CO2_ALARM = (
    DeviceType(0x0C03).set_doc('Sensor (CO2)')
)
DEVICE_TYPE_SENSOR_HEAT_ALARM = (
    DeviceType(0x0C04).set_doc('Sensor (heat)')
)
DEVICE_TYPE_SENSOR_WATER_ALARM = (
    DeviceType(0x0C05).set_doc('Sensor (water)')
)
DEVICE_TYPE_SENSOR_ACCESS_CONTROL = (
    DeviceType(0x0C06).set_doc('Sensor (access control)')
)
DEVICE_TYPE_SENSOR_HOME_SECURITY = (
    DeviceType(0x0C07).set_doc('Sensor (security)')
)
DEVICE_TYPE_SENSOR_POWER_MANAGEMENT = (
    DeviceType(0x0C08).set_doc('Sensor (power management)')
)
DEVICE_TYPE_SENSOR_SYSTEM = (
    DeviceType(0x0C09).set_doc('Sensor (system)')
)
DEVICE_TYPE_SENSOR_EMERGENCY_ALARM = (
    DeviceType(0x0C0A).set_doc('Sensor (emergency)')
)
DEVICE_TYPE_SENSOR_CLOCK = (
    DeviceType(0x0C0B).set_doc('Sensor (clock)')
)
DEVICE_TYPE_SENSOR_MULTIDEVICE_1 = (
    DeviceType(0x0CFF).set_doc('Sensor (multi device 1)')
)
DEVICE_TYPE_SENSOR_MULTILEVEL = (
    DeviceType(0x0D00).set_doc('Sensor (multi level)')
)
DEVICE_TYPE_SENSOR_AIR_TEMPERATURE = (
    DeviceType(0x0D01).set_doc('Sensor (air)')
)
DEVICE_TYPE_SENSOR_GENERAL_PURPOSE = (
    DeviceType(0x0D02).set_doc('Sensor (general)')
)
DEVICE_TYPE_SENSOR_LUMINANCE = (
    DeviceType(0x0D03).set_doc('Sensor (luminance)')
)
DEVICE_TYPE_SENSOR_POWER = (
    DeviceType(0x0D04).set_doc('Sensor (power)')
)
DEVICE_TYPE_SENSOR_HUMIDITY = (
    DeviceType(0x0D05).set_doc('Sensor (humidity)')
)
DEVICE_TYPE_SENSOR_VELOCITY = (
    DeviceType(0x0D06).set_doc('Sensor (velocity)')
)
DEVICE_TYPE_SENSOR_DIRECTION = (
    DeviceType(0x0D07).set_doc('Sensor (direction)')
)
DEVICE_TYPE_SENSOR_ATMOSPHERIC_PRESSURE = (
    DeviceType(0x0D08).set_doc('Sensor (atmospheric pressure)')
)
DEVICE_TYPE_SENSOR_BAROMETRIC_PRESSURE = (
    DeviceType(0x0D09).set_doc('Sensor (barometric pressure)')
)
DEVICE_TYPE_SENSOR_SOLAR_RADIATION = (
    DeviceType(0x0D0A).set_doc('Sensor (solar radiation)')
)
DEVICE_TYPE_SENSOR_DEW_POINT = (
    DeviceType(0x0D0B).set_doc('Sensor (dew point)')
)
DEVICE_TYPE_SENSOR_RAIN_RATE = (
    DeviceType(0x0D0C).set_doc('Sensor (rain rate)')
)
DEVICE_TYPE_SENSOR_TIDE_LEVEL = (
    DeviceType(0x0D0D).set_doc('Sensor (tide level)')
)
DEVICE_TYPE_SENSOR_WEIGHT = (
    DeviceType(0x0D0E).set_doc('Sensor (weight)')
)
DEVICE_TYPE_SENSOR_VOLTAGE = (
    DeviceType(0x0D0F).set_doc('Sensor (voltage)')
)
DEVICE_TYPE_SENSOR_CURRENT = (
    DeviceType(0x0D10).set_doc('Sensor (current)')
)
DEVICE_TYPE_SENSOR_CO2_LEVEL = (
    DeviceType(0x0D11).set_doc('Sensor (CO2 level)')
)
DEVICE_TYPE_SENSOR_AIR_FLOW = (
    DeviceType(0x0D12).set_doc('Sensor (air flow)')
)
DEVICE_TYPE_SENSOR_TANK_CAPACITY = (
    DeviceType(0x0D13).set_doc('Sensor (tank capacity)')
)
DEVICE_TYPE_SENSOR_DISTANCE = (
    DeviceType(0x0D14).set_doc('Sensor (distance)')
)
DEVICE_TYPE_SENSOR_ANGLE_POSTITION = (
    DeviceType(0x0D15).set_doc('Sensor (angle position)')
)
DEVICE_TYPE_SENSOR_ROTATION = (
    DeviceType(0x0D16).set_doc('Sensor (rotation)')
)
DEVICE_TYPE_SENSOR_WATER_TEMPERATURE = (
    DeviceType(0x0D17).set_doc('Sensor (H2O temperature)')
)
DEVICE_TYPE_SENSOR_SOIL_TEMPERATURE = (
    DeviceType(0x0D18).set_doc('Sensor (soil temperature)')
)
DEVICE_TYPE_SENSOR_SEISMIC_INTENSITY = (
    DeviceType(0x0D19).set_doc('Sensor (seismic intensity)')
)
DEVICE_TYPE_SENSOR_SEISMIC_MAGNITUDE = (
    DeviceType(0x0D1A).set_doc('Sensor (seismic magnatitude)')
)
DEVICE_TYPE_SENSOR_ULTRAVIOLET = (
    DeviceType(0x0D1B).set_doc('Sensor (ultraviolet)')
)
DEVICE_TYPE_SENSOR_ELECTRICAL_RESISTIVITY = (
    DeviceType(0x0D1C).set_doc('Sensor (electrical resistivity)')
)
DEVICE_TYPE_SENSOR_ELECTRICAL_CONDUCTIVITY = (
    DeviceType(0x0B1D).set_doc('Sensor (electrical conductivity)')
)
DEVICE_TYPE_SENSOR_LOUDNESS = (
    DeviceType(0x0B1E).set_doc('Sensor (loudness)')
)
DEVICE_TYPE_SENSOR_MOISTURE = (
    DeviceType(0x0B1F).set_doc('Sensor (moisture)')
)
DEVICE_TYPE_SENSOR_FREQUENCY = (
    DeviceType(0x0B20).set_doc('Sensor (frequency)')
)
DEVICE_TYPE_SENSOR_TIME = (
    DeviceType(0x0B21).set_doc('Sensor (time)')
)
DEVICE_TYPE_SENSOR_TARGET_TEMPERATURE = (
    DeviceType(0x0B22).set_doc('Sensot (target temperature)')
)
DEVICE_TYPE_SENSOR_MULTIDEVICE_2 = (
    DeviceType(0x0BFF).set_doc('Sensor (multi device 2)')
)
DEVICE_TYPE_SET_TOP_BOX = (
    DeviceType(0x0E00).set_doc('Set Top Box')
)
DEVICE_TYPE_SIREN = (
    DeviceType(0x0F00).set_doc('Siren')
)
DEVICE_TYPE_SUB_ENERGY_METER = (
    DeviceType(0x1000).set_doc('Sub Energy Meter')
)
DEVICE_TYPE_SUB_SYSTEM_CONTROLLER = (
    DeviceType(0x1100).set_doc('Sub System Controller')
)
DEVICE_TYPE_THERMOSTAT_HVAC = (
    DeviceType(0x1200).set_doc('Thermostat HVAC')
)
DEVICE_TYPE_THERMOSTAT_SETBACK = (
    DeviceType(0x1300).set_doc('Thermostat Setback')
)
DEVICE_TYPE_TV = (
    DeviceType(0x1400).set_doc('TV')
)
DEVICE_TYPE_VALVE_OPEN_CLOSE = (
    DeviceType(0x1500).set_doc('Valve (open/close)')
)
DEVICE_TYPE_WALL_CONTROLLER = (
    DeviceType(0x1600).set_doc('Wall Controller')
)
DEVICE_TYPE_WHOLE_HOME_METER_SIMPLE = (
    DeviceType(0x1700).set_doc('Whole Home Meter (simple)')
)
DEVICE_TYPE_WINDOW_COVERING_NO_POSITION_ENDPOINT = (
    DeviceType(0x1800).set_doc('Window Covering (no position endpoint)')
)
DEVICE_TYPE_WINDOW_COVERING_ENDPOINT_AWARE = (
    DeviceType(0x1900).set_doc('Window Covering (endpoint aware)')
)
DEVICE_TYPE_WINDOW_COVERING_POSITION_ENDPOINT_AWARE = (
    DeviceType(0x1A00).set_doc('Window Covering (position endpoint aware)')
)


DEVICE_TYPES = [
    DEVICE_TYPE_UNKNOWN,
    DEVICE_TYPE_CENTRAL_CONTROLLER,
    DEVICE_TYPE_DISPLAY_SIMPLE,
    DEVICE_TYPE_DOOR_LOCK_KEYPAD,
    DEVICE_TYPE_SWITCH_FAN,
    DEVICE_TYPE_GATEWAY,
    DEVICE_TYPE_SWITCH_MULTILEVEL,
    DEVICE_TYPE_SWITCH_BINARY,
    DEVICE_TYPE_POWER_STRIP,
    DEVICE_TYPE_REMOTE_CONTROL_AV,
    DEVICE_TYPE_REMOTE_CONTROL_MULTI_PURPOSE,
    DEVICE_TYPE_REMOTE_CONTROL_SIMPLE,
    DEVICE_TYPE_KEY_FOB,
    DEVICE_TYPE_SENSOR_NOTIFICATION,
    DEVICE_TYPE_SENSOR_SMOKE_ALARM,
    DEVICE_TYPE_SENSOR_CO_ALARM,
    DEVICE_TYPE_SENSOR_CO2_ALARM,
    DEVICE_TYPE_SENSOR_HEAT_ALARM,
    DEVICE_TYPE_SENSOR_WATER_ALARM,
    DEVICE_TYPE_SENSOR_ACCESS_CONTROL,
    DEVICE_TYPE_SENSOR_HOME_SECURITY,
    DEVICE_TYPE_SENSOR_POWER_MANAGEMENT,
    DEVICE_TYPE_SENSOR_SYSTEM,
    DEVICE_TYPE_SENSOR_EMERGENCY_ALARM,
    DEVICE_TYPE_SENSOR_CLOCK,
    DEVICE_TYPE_SENSOR_MULTIDEVICE_1,
    DEVICE_TYPE_SENSOR_MULTILEVEL,
    DEVICE_TYPE_SENSOR_AIR_TEMPERATURE,
    DEVICE_TYPE_SENSOR_GENERAL_PURPOSE,
    DEVICE_TYPE_SENSOR_LUMINANCE,
    DEVICE_TYPE_SENSOR_POWER,
    DEVICE_TYPE_SENSOR_HUMIDITY,
    DEVICE_TYPE_SENSOR_VELOCITY,
    DEVICE_TYPE_SENSOR_DIRECTION,
    DEVICE_TYPE_SENSOR_ATMOSPHERIC_PRESSURE,
    DEVICE_TYPE_SENSOR_BAROMETRIC_PRESSURE,
    DEVICE_TYPE_SENSOR_SOLAR_RADIATION,
    DEVICE_TYPE_SENSOR_DEW_POINT,
    DEVICE_TYPE_SENSOR_RAIN_RATE,
    DEVICE_TYPE_SENSOR_TIDE_LEVEL,
    DEVICE_TYPE_SENSOR_WEIGHT,
    DEVICE_TYPE_SENSOR_VOLTAGE,
    DEVICE_TYPE_SENSOR_CURRENT,
    DEVICE_TYPE_SENSOR_CO2_LEVEL,
    DEVICE_TYPE_SENSOR_AIR_FLOW,
    DEVICE_TYPE_SENSOR_TANK_CAPACITY,
    DEVICE_TYPE_SENSOR_DISTANCE,
    DEVICE_TYPE_SENSOR_ANGLE_POSTITION,
    DEVICE_TYPE_SENSOR_ROTATION,
    DEVICE_TYPE_SENSOR_WATER_TEMPERATURE,
    DEVICE_TYPE_SENSOR_SOIL_TEMPERATURE,
    DEVICE_TYPE_SENSOR_SEISMIC_INTENSITY,
    DEVICE_TYPE_SENSOR_SEISMIC_MAGNITUDE,
    DEVICE_TYPE_SENSOR_ULTRAVIOLET,
    DEVICE_TYPE_SENSOR_ELECTRICAL_RESISTIVITY,
    DEVICE_TYPE_SENSOR_ELECTRICAL_CONDUCTIVITY,
    DEVICE_TYPE_SENSOR_LOUDNESS,
    DEVICE_TYPE_SENSOR_MOISTURE,
    DEVICE_TYPE_SENSOR_FREQUENCY,
    DEVICE_TYPE_SENSOR_TIME,
    DEVICE_TYPE_SENSOR_TARGET_TEMPERATURE,
    DEVICE_TYPE_SENSOR_MULTIDEVICE_2,
    DEVICE_TYPE_SET_TOP_BOX,
    DEVICE_TYPE_SIREN,
    DEVICE_TYPE_SUB_ENERGY_METER,
    DEVICE_TYPE_SUB_SYSTEM_CONTROLLER,
    DEVICE_TYPE_THERMOSTAT_HVAC,
    DEVICE_TYPE_THERMOSTAT_SETBACK,
    DEVICE_TYPE_TV,
    DEVICE_TYPE_VALVE_OPEN_CLOSE,
    DEVICE_TYPE_WALL_CONTROLLER,
    DEVICE_TYPE_WHOLE_HOME_METER_SIMPLE,
    DEVICE_TYPE_WINDOW_COVERING_NO_POSITION_ENDPOINT,
    DEVICE_TYPE_WINDOW_COVERING_ENDPOINT_AWARE,
    DEVICE_TYPE_WINDOW_COVERING_POSITION_ENDPOINT_AWARE
]


# **** Generic and Specific Device Class identifiers *****

class SpecificType(int):
    value = 0
    doc = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        value = args[1]

        self = super(SpecificType, cls).__new__(*args, **kwargs)
        setattr(self, 'value', value)
        return self

    def set_doc(self, value):
        """
        :param value:
        :type value: str

        :rtype: "SpecificType"
        """
        if self.doc is None:
            self.doc = value
            self.__doc__ = value

        return self

    def __int__(self):
        return self.value

    def __str__(self):
        return self.doc

    def __eq__(self, other):
        """
        :param other:
        :type other: int, "SpecificType"

        :rtype: bool
        """
        if isinstance(other, int):
            return int(self) == other

        return object.__eq__(self, other)

    def __ne__(self, other):
        """
        :param other:
        :type other: int, "SpecificType"

        :rtype: bool
        """
        return not self.__eq__(other)


class GenericType(int):
    value = 0
    specific_types = None
    doc = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        value = args[1]

        self = super(GenericType, cls).__new__(*args, **kwargs)
        setattr(self, 'value', value)
        setattr(self, 'specific_types', [])
        return self

    def set_doc(self, value):
        """
        :param value:
        :type value: str

        :rtype: "GenericType"
        """
        if self.doc is None:
            self.doc = value
            self.__doc__ = value

        return self

    def __int__(self):
        return self.value

    def __str__(self):
        return self.doc

    def __contains__(self, item):
        """
        :param item:
        :type item: int, SpecificType

        :rtype: bool
        """
        for specific_type in self.specific_types:
            if specific_type == item:
                return True
        return False

    def __getitem__(self, item):
        """
        :param item:
        :type item: int, SpecificType

        :rtype: SpecificType
        """
        for specific_type in self.specific_types:
            if specific_type == item:
                return specific_type

        return SPECIFIC_TYPE_UNKNOWN

    def __iadd__(self, other):
        """
        :param other:
        :type other: List[SpecificType]

        :rtype: "GenericType"
        """
        self.specific_types += other
        return self

    def __eq__(self, other):
        """
        :param other:
        :type other: int, "GenericType"

        :rtype: bool
        """
        if isinstance(other, int):
            return int(self) == other

        return object.__eq__(self, other)

    def __ne__(self, other):
        """
        :param other:
        :type other: int, "GenericType"

        :rtype: bool
        """
        return not self.__eq__(other)


GENERIC_TYPE_UNKNOWN = GenericType(-1).set_doc('Generic Type Unknown')
SPECIFIC_TYPE_UNKNOWN = SpecificType(-1).set_doc('Specific Type Unknown')

#  Device class Av Control Point
GENERIC_TYPE_AV_CONTROL_POINT = GenericType(0x03).set_doc('AV Control Point')
SPECIFIC_TYPE_DOORBELL = SpecificType(0x12).set_doc('Doorbell')
SPECIFIC_TYPE_SATELLITE_RECEIVER = (
    SpecificType(0x04).set_doc('Satellite Receiver')
)
SPECIFIC_TYPE_SATELLITE_RECEIVER_V2 = (
    SpecificType(0x11).set_doc('Satellite Receiver V2')
)
SPECIFIC_TYPE_SOUND_SWITCH = SpecificType(0x01).set_doc('Sound Switch')

GENERIC_TYPE_AV_CONTROL_POINT += [
    SPECIFIC_TYPE_DOORBELL,
    SPECIFIC_TYPE_SATELLITE_RECEIVER,
    SPECIFIC_TYPE_SATELLITE_RECEIVER_V2,
    SPECIFIC_TYPE_SOUND_SWITCH
]

#  Device class Display
GENERIC_TYPE_DISPLAY = GenericType(0x04).set_doc('Display')
SPECIFIC_TYPE_SIMPLE_DISPLAY = SpecificType(0x01).set_doc('Display (simple)')

GENERIC_TYPE_DISPLAY += [SPECIFIC_TYPE_SIMPLE_DISPLAY]


#  Device class Entry Control
GENERIC_TYPE_ENTRY_CONTROL = GenericType(0x40).set_doc('Entry Control')
SPECIFIC_TYPE_DOOR_LOCK = SpecificType(0x01).set_doc('Door Lock')
SPECIFIC_TYPE_ADVANCED_DOOR_LOCK = (
    SpecificType(0x02).set_doc('Advanced Door Lock')
)
SPECIFIC_TYPE_SECURE_KEYPAD_DOOR_LOCK = (
    SpecificType(0x03).set_doc('Door Lock (keypad lever)')
)
SPECIFIC_TYPE_SECURE_KEYPAD_DOOR_LOCK_DEADBOLT = (
    SpecificType(0x04).set_doc('Door Lock (keypad deadbolt)')
)
SPECIFIC_TYPE_SECURE_DOOR = SpecificType(0x05).set_doc('Secure Door')
SPECIFIC_TYPE_SECURE_GATE = SpecificType(0x06).set_doc('Secure Gate')
SPECIFIC_TYPE_SECURE_BARRIER_ADDON = (
    SpecificType(0x07).set_doc('Barrier Addon')
)
SPECIFIC_TYPE_SECURE_BARRIER_OPEN_ONLY = (
    SpecificType(0x08).set_doc('Barrier Open Only')
)
SPECIFIC_TYPE_SECURE_BARRIER_CLOSE_ONLY = (
    SpecificType(0x09).set_doc('Barrier Close Only')
)
SPECIFIC_TYPE_SECURE_LOCKBOX = SpecificType(0x0A).set_doc('Lock Box')
SPECIFIC_TYPE_SECURE_KEYPAD = SpecificType(0x0B).set_doc('Keypad')

GENERIC_TYPE_ENTRY_CONTROL += [
    SPECIFIC_TYPE_DOOR_LOCK,
    SPECIFIC_TYPE_ADVANCED_DOOR_LOCK,
    SPECIFIC_TYPE_SECURE_KEYPAD_DOOR_LOCK,
    SPECIFIC_TYPE_SECURE_KEYPAD_DOOR_LOCK_DEADBOLT,
    SPECIFIC_TYPE_SECURE_DOOR,
    SPECIFIC_TYPE_SECURE_GATE,
    SPECIFIC_TYPE_SECURE_BARRIER_ADDON,
    SPECIFIC_TYPE_SECURE_BARRIER_OPEN_ONLY,
    SPECIFIC_TYPE_SECURE_BARRIER_CLOSE_ONLY,
    SPECIFIC_TYPE_SECURE_LOCKBOX,
    SPECIFIC_TYPE_SECURE_KEYPAD,
]

#  Device class Generic Controller
GENERIC_TYPE_GENERIC_CONTROLLER = (
    GenericType(0x01).set_doc('Remote Controller')
)
SPECIFIC_TYPE_PORTABLE_REMOTE_CONTROLLER = (
    SpecificType(0x01).set_doc('Remote Control (Multi Purpose)')
)
SPECIFIC_TYPE_PORTABLE_SCENE_CONTROLLER = (
    SpecificType(0x02).set_doc('Portable Scene Controller')
)
SPECIFIC_TYPE_PORTABLE_INSTALLER_TOOL = (
    SpecificType(0x03).set_doc('Installer Tool')
)
SPECIFIC_TYPE_REMOTE_CONTROL_AV = (
    SpecificType(0x04).set_doc('Remote Control (AV)')
)
SPECIFIC_TYPE_REMOTE_CONTROL_SIMPLE = (
    SpecificType(0x06).set_doc('Remote Control (Simple)')
)

GENERIC_TYPE_GENERIC_CONTROLLER += [
    SPECIFIC_TYPE_PORTABLE_REMOTE_CONTROLLER,
    SPECIFIC_TYPE_PORTABLE_SCENE_CONTROLLER,
    SPECIFIC_TYPE_PORTABLE_INSTALLER_TOOL,
    SPECIFIC_TYPE_REMOTE_CONTROL_AV,
    SPECIFIC_TYPE_REMOTE_CONTROL_SIMPLE,
]


#  Device class Meter
GENERIC_TYPE_METER = GenericType(0x31).set_doc('Meter')
SPECIFIC_TYPE_SIMPLE_METER = (
    SpecificType(0x01).set_doc('Sub Energy Meter')
)
SPECIFIC_TYPE_ADV_ENERGY_CONTROL = (
    SpecificType(0x02).set_doc('Whole Home Energy Meter (Advanced)')
)
SPECIFIC_TYPE_WHOLE_HOME_METER_SIMPLE = (
    SpecificType(0x03).set_doc('Whole Home Meter (Simple)')
)

GENERIC_TYPE_METER += [
    SPECIFIC_TYPE_SIMPLE_METER,
    SPECIFIC_TYPE_ADV_ENERGY_CONTROL,
    SPECIFIC_TYPE_WHOLE_HOME_METER_SIMPLE,
]


#  Device class Meter Pulse
GENERIC_TYPE_METER_PULSE = GenericType(0x30).set_doc('Pulse Meter')

#  Device class Non Interoperable
GENERIC_TYPE_NON_INTEROPERABLE = GenericType(0xFF).set_doc('Non interoperable')

#  Device class Repeater Slave
GENERIC_TYPE_REPEATER_SLAVE = GenericType(0x0F).set_doc('Repeater Slave')
SPECIFIC_TYPE_REPEATER_SLAVE = (
    SpecificType(0x01).set_doc('Basic Repeater Slave')
)
SPECIFIC_TYPE_VIRTUAL_NODE = SpecificType(0x02).set_doc('Virtual Node')

GENERIC_TYPE_REPEATER_SLAVE += [
    SPECIFIC_TYPE_REPEATER_SLAVE,
    SPECIFIC_TYPE_VIRTUAL_NODE
]


#  Device class Security Panel
GENERIC_TYPE_SECURITY_PANEL = GenericType(0x17).set_doc('Security Panel')
SPECIFIC_TYPE_ZONED_SECURITY_PANEL = (
    SpecificType(0x01).set_doc('Zoned Security Panel')
)

GENERIC_TYPE_SECURITY_PANEL += [SPECIFIC_TYPE_ZONED_SECURITY_PANEL]


#  Device class Semi Interoperable
GENERIC_TYPE_SEMI_INTEROPERABLE = (
    GenericType(0x50).set_doc('Semi Interoperable')
)
SPECIFIC_TYPE_ENERGY_PRODUCTION = (
    SpecificType(0x01).set_doc('Energy Production')
)

GENERIC_TYPE_SEMI_INTEROPERABLE += [SPECIFIC_TYPE_ENERGY_PRODUCTION]


#  Device class Sensor Alarm
GENERIC_TYPE_SENSOR_ALARM = GenericType(0xA1).set_doc('Sensor Alarm')
SPECIFIC_TYPE_ADV_ZENSOR_NET_ALARM_SENSOR = (
    SpecificType(0x05).set_doc('Zensor Net Alarm (advanced) Sensor')
)
SPECIFIC_TYPE_ADV_ZENSOR_NET_SMOKE_SENSOR = (
    SpecificType(0x0A).set_doc('Zensor Net Smoke (advanced) Sensor')
)
SPECIFIC_TYPE_BASIC_ROUTING_ALARM_SENSOR = (
    SpecificType(0x01).set_doc('Routing Alarm (basic) Sensor')
)
SPECIFIC_TYPE_BASIC_ROUTING_SMOKE_SENSOR = (
    SpecificType(0x06).set_doc('Routing Smoke (basic) Sensor')
)
SPECIFIC_TYPE_BASIC_ZENSOR_NET_ALARM_SENSOR = (
    SpecificType(0x03).set_doc('Zensor Net Alarm (basic) Sensor')
)
SPECIFIC_TYPE_BASIC_ZENSOR_NET_SMOKE_SENSOR = (
    SpecificType(0x08).set_doc('Zensor Net Smoke (basic) Sensor')
)
SPECIFIC_TYPE_ROUTING_ALARM_SENSOR = (
    SpecificType(0x02).set_doc('Routing Alarm Sensor')
)
SPECIFIC_TYPE_ROUTING_SMOKE_SENSOR = (
    SpecificType(0x07).set_doc('Routing Smoke Sensor')
)
SPECIFIC_TYPE_ZENSOR_NET_ALARM_SENSOR = (
    SpecificType(0x04).set_doc('Zensor Net Alarm Sensor')
)
SPECIFIC_TYPE_ZENSOR_NET_SMOKE_SENSOR = (
    SpecificType(0x09).set_doc('Zensor Net Smoke Sensor')
)
SPECIFIC_TYPE_ALARM_SENSOR = SpecificType(0x0B).set_doc('Sensor (Alarm)')

GENERIC_TYPE_SENSOR_ALARM += [
    SPECIFIC_TYPE_ADV_ZENSOR_NET_ALARM_SENSOR,
    SPECIFIC_TYPE_ADV_ZENSOR_NET_SMOKE_SENSOR,
    SPECIFIC_TYPE_BASIC_ROUTING_ALARM_SENSOR,
    SPECIFIC_TYPE_BASIC_ROUTING_SMOKE_SENSOR,
    SPECIFIC_TYPE_BASIC_ZENSOR_NET_ALARM_SENSOR,
    SPECIFIC_TYPE_BASIC_ZENSOR_NET_SMOKE_SENSOR,
    SPECIFIC_TYPE_ROUTING_ALARM_SENSOR,
    SPECIFIC_TYPE_ROUTING_SMOKE_SENSOR,
    SPECIFIC_TYPE_ZENSOR_NET_ALARM_SENSOR,
    SPECIFIC_TYPE_ZENSOR_NET_SMOKE_SENSOR,
    SPECIFIC_TYPE_ALARM_SENSOR,
]


#  Device class Sensor Binary
GENERIC_TYPE_SENSOR_BINARY = GenericType(0x20).set_doc('Binary Sensor')
SPECIFIC_TYPE_ROUTING_SENSOR_BINARY = (
    SpecificType(0x01).set_doc('Routing Binary Sensor')
)

GENERIC_TYPE_SENSOR_BINARY += [SPECIFIC_TYPE_ROUTING_SENSOR_BINARY]

#  Device class Sensor Multilevel
GENERIC_TYPE_SENSOR_MULTILEVEL = GenericType(0x21).set_doc('Multilevel Sensor')
SPECIFIC_TYPE_ROUTING_SENSOR_MULTILEVEL = (
    SpecificType(0x01).set_doc('Sensor (Multilevel)')
)
SPECIFIC_TYPE_CHIMNEY_FAN = SpecificType(0x02).set_doc('Chimney Fan')

GENERIC_TYPE_SENSOR_MULTILEVEL += [
    SPECIFIC_TYPE_ROUTING_SENSOR_MULTILEVEL,
    SPECIFIC_TYPE_CHIMNEY_FAN
]


#  Device class Static Controller
GENERIC_TYPE_STATIC_CONTROLLER = GenericType(0x02).set_doc('Static Controller')
SPECIFIC_TYPE_PC_CONTROLLER = SpecificType(0x01).set_doc('Central Controller')
SPECIFIC_TYPE_SCENE_CONTROLLER = SpecificType(0x02).set_doc('Scene Controller')
SPECIFIC_TYPE_STATIC_INSTALLER_TOOL = (
    SpecificType(0x03).set_doc('Installer Tool')
)
SPECIFIC_TYPE_SET_TOP_BOX = SpecificType(0x04).set_doc('Set Top Box')
SPECIFIC_TYPE_SUB_SYSTEM_CONTROLLER = (
    SpecificType(0x05).set_doc('Sub System Controller')
)
SPECIFIC_TYPE_TV = SpecificType(0x06).set_doc('TV')
SPECIFIC_TYPE_GATEWAY = SpecificType(0x07).set_doc('Gateway')

GENERIC_TYPE_STATIC_CONTROLLER += [
    SPECIFIC_TYPE_PC_CONTROLLER,
    SPECIFIC_TYPE_SCENE_CONTROLLER,
    SPECIFIC_TYPE_STATIC_INSTALLER_TOOL,
    SPECIFIC_TYPE_SET_TOP_BOX,
    SPECIFIC_TYPE_SUB_SYSTEM_CONTROLLER,
    SPECIFIC_TYPE_TV,
    SPECIFIC_TYPE_GATEWAY
]


#  Device class Switch Binary
GENERIC_TYPE_SWITCH_BINARY = GenericType(0x10).set_doc('Binary Switch')
SPECIFIC_TYPE_POWER_SWITCH_BINARY = (
    SpecificType(0x01).set_doc('On/Off Power Switch')
)
SPECIFIC_TYPE_SCENE_SWITCH_BINARY = (
    SpecificType(0x03).set_doc('Binary Scene Switch')
)
SPECIFIC_TYPE_POWER_STRIP = SpecificType(0x04).set_doc('Power Strip')
SPECIFIC_TYPE_SIREN = SpecificType(0x05).set_doc('Siren')
SPECIFIC_TYPE_VALVE_OPEN_CLOSE = (
    SpecificType(0x06).set_doc('Valve (open/close)')
)
SPECIFIC_TYPE_COLOR_TUNABLE_BINARY = (
    SpecificType(0x02).set_doc('Turnable Switch')
)
SPECIFIC_TYPE_IRRIGATION_CONTROLLER = SpecificType(0x07).set_doc('Irrigation')

GENERIC_TYPE_SWITCH_BINARY += [
    SPECIFIC_TYPE_POWER_SWITCH_BINARY,
    SPECIFIC_TYPE_SCENE_SWITCH_BINARY,
    SPECIFIC_TYPE_POWER_STRIP,
    SPECIFIC_TYPE_SIREN,
    SPECIFIC_TYPE_VALVE_OPEN_CLOSE,
    SPECIFIC_TYPE_COLOR_TUNABLE_BINARY,
    SPECIFIC_TYPE_IRRIGATION_CONTROLLER
]


#  Device class Switch Multilevel
GENERIC_TYPE_SWITCH_MULTILEVEL = GenericType(0x11).set_doc('Multilevel Switch')
SPECIFIC_TYPE_CLASS_A_MOTOR_CONTROL = (
    SpecificType(0x05).set_doc('Window Covering No Position/Endpoint')
)
SPECIFIC_TYPE_CLASS_B_MOTOR_CONTROL = (
    SpecificType(0x06).set_doc('Window Covering Endpoint Aware')
)
SPECIFIC_TYPE_CLASS_C_MOTOR_CONTROL = (
    SpecificType(0x07).set_doc('Window Covering Position/Endpoint Aware')
)
SPECIFIC_TYPE_MOTOR_MULTIPOSITION = (
    SpecificType(0x03).set_doc('Multiposition Motor')
)
SPECIFIC_TYPE_POWER_SWITCH_MULTILEVEL = (
    SpecificType(0x01).set_doc('Light Dimmer Switch')
)
SPECIFIC_TYPE_SCENE_SWITCH_MULTILEVEL = (
    SpecificType(0x04).set_doc('Multilevel Scene Switch')
)
SPECIFIC_TYPE_FAN_SWITCH = SpecificType(0x08).set_doc('Fan Switch')
SPECIFIC_TYPE_COLOR_TUNABLE_MULTILEVEL = (
    SpecificType(0x02).set_doc('Turnable (multilevel) Switch')
)

GENERIC_TYPE_SWITCH_MULTILEVEL += [
    SPECIFIC_TYPE_CLASS_A_MOTOR_CONTROL,
    SPECIFIC_TYPE_CLASS_B_MOTOR_CONTROL,
    SPECIFIC_TYPE_CLASS_C_MOTOR_CONTROL,
    SPECIFIC_TYPE_MOTOR_MULTIPOSITION,
    SPECIFIC_TYPE_POWER_SWITCH_MULTILEVEL,
    SPECIFIC_TYPE_SCENE_SWITCH_MULTILEVEL,
    SPECIFIC_TYPE_FAN_SWITCH,
    SPECIFIC_TYPE_COLOR_TUNABLE_MULTILEVEL
]


#  Device class Switch Remote
GENERIC_TYPE_SWITCH_REMOTE = GenericType(0x12).set_doc('Remote Switch')
SPECIFIC_TYPE_SWITCH_REMOTE_BINARY = (
    SpecificType(0x01).set_doc('Binary Remote Switch')
)
SPECIFIC_TYPE_SWITCH_REMOTE_MULTILEVEL = (
    SpecificType(0x02).set_doc('Multilevel Remote Switch')
)
SPECIFIC_TYPE_SWITCH_REMOTE_TOGGLE_BINARY = (
    SpecificType(0x03).set_doc('Binary Toggle Remote Switch')
)
SPECIFIC_TYPE_SWITCH_REMOTE_TOGGLE_MULTILEVEL = (
    SpecificType(0x04).set_doc('Multilevel Toggle Remote Switch')
)

GENERIC_TYPE_SWITCH_REMOTE += [
    SPECIFIC_TYPE_SWITCH_REMOTE_BINARY,
    SPECIFIC_TYPE_SWITCH_REMOTE_MULTILEVEL,
    SPECIFIC_TYPE_SWITCH_REMOTE_TOGGLE_BINARY,
    SPECIFIC_TYPE_SWITCH_REMOTE_TOGGLE_MULTILEVEL
]


#  Device class Switch Toggle
GENERIC_TYPE_SWITCH_TOGGLE = GenericType(0x13).set_doc('Toggle Switch')
SPECIFIC_TYPE_SWITCH_TOGGLE_BINARY = (
    SpecificType(0x01).set_doc('Binary Toggle Switch')
)
SPECIFIC_TYPE_SWITCH_TOGGLE_MULTILEVEL = (
    SpecificType(0x02).set_doc('Multilevel Toggle Switch')
)

GENERIC_TYPE_SWITCH_TOGGLE += [
    SPECIFIC_TYPE_SWITCH_TOGGLE_BINARY,
    SPECIFIC_TYPE_SWITCH_TOGGLE_MULTILEVEL
]


#  Device class Thermostat
GENERIC_TYPE_THERMOSTAT = GenericType(0x08).set_doc('Thermostat')
SPECIFIC_TYPE_SETBACK_SCHEDULE_THERMOSTAT = (
    SpecificType(0x03).set_doc('Setback Schedule Thermostat')
)
SPECIFIC_TYPE_SETBACK_THERMOSTAT = (
    SpecificType(0x05).set_doc('Thermostat Setback')
)
SPECIFIC_TYPE_SETPOINT_THERMOSTAT = (
    SpecificType(0x04).set_doc('Thermostat Setpoint')
)
SPECIFIC_TYPE_THERMOSTAT_GENERAL = (
    SpecificType(0x02).set_doc('Thermostat General')
)
SPECIFIC_TYPE_THERMOSTAT_GENERAL_V2 = (
    SpecificType(0x06).set_doc('Thermostat HVAC')
)
SPECIFIC_TYPE_THERMOSTAT_HEATING = (
    SpecificType(0x01).set_doc('Thermostat Heating')
)

GENERIC_TYPE_THERMOSTAT += [
    SPECIFIC_TYPE_SETBACK_SCHEDULE_THERMOSTAT,
    SPECIFIC_TYPE_SETBACK_THERMOSTAT,
    SPECIFIC_TYPE_SETPOINT_THERMOSTAT,
    SPECIFIC_TYPE_THERMOSTAT_GENERAL,
    SPECIFIC_TYPE_THERMOSTAT_GENERAL_V2,
    SPECIFIC_TYPE_THERMOSTAT_HEATING
]

#  Device class Ventilation
GENERIC_TYPE_VENTILATION = GenericType(0x16).set_doc('Ventilation')
SPECIFIC_TYPE_RESIDENTIAL_HRV = SpecificType(0x01).set_doc('Residential HRV')

GENERIC_TYPE_VENTILATION += [SPECIFIC_TYPE_RESIDENTIAL_HRV]


#  Device class Window Covering
GENERIC_TYPE_WINDOW_COVERING = GenericType(0x09).set_doc('Window Covering')
SPECIFIC_TYPE_SIMPLE_WINDOW_COVERING = (
    SpecificType(0x01).set_doc('Simple Window Covering Control')
)

GENERIC_TYPE_WINDOW_COVERING += [SPECIFIC_TYPE_SIMPLE_WINDOW_COVERING]


#  Device class Zip Node
GENERIC_TYPE_ZIP_NODE = GenericType(0x15).set_doc('ZIP')
SPECIFIC_TYPE_ZIP_ADV_NODE = SpecificType(0x02).set_doc('ZIP (adv)')
SPECIFIC_TYPE_ZIP_TUN_NODE = SpecificType(0x01).set_doc('ZIP (tun)')

GENERIC_TYPE_ZIP_NODE += [
    SPECIFIC_TYPE_ZIP_ADV_NODE,
    SPECIFIC_TYPE_ZIP_TUN_NODE
]


#  Device class Wall Controller
GENERIC_TYPE_WALL_CONTROLLER = GenericType(0x18).set_doc('Wall Controller')
SPECIFIC_TYPE_BASIC_WALL_CONTROLLER = (
    SpecificType(0x01).set_doc('Wall Controller')
)

GENERIC_TYPE_WALL_CONTROLLER += [SPECIFIC_TYPE_BASIC_WALL_CONTROLLER]


#  Device class Network Extender
GENERIC_TYPE_NETWORK_EXTENDER = GenericType(0x05).set_doc('Network Extender')
SPECIFIC_TYPE_SECURE_EXTENDER = SpecificType(0x01).set_doc('Secure Extender')

GENERIC_TYPE_NETWORK_EXTENDER += [SPECIFIC_TYPE_SECURE_EXTENDER]


#  Device class Appliance
GENERIC_TYPE_APPLIANCE = GenericType(0x06).set_doc('Appliance')
SPECIFIC_TYPE_GENERAL_APPLIANCE = (
    SpecificType(0x01).set_doc('General Appliance')
)
SPECIFIC_TYPE_KITCHEN_APPLIANCE = (
    SpecificType(0x02).set_doc('Kitchen Appliance')
)
SPECIFIC_TYPE_LAUNDRY_APPLIANCE = (
    SpecificType(0x03).set_doc('Laundry Appliance')
)

GENERIC_TYPE_APPLIANCE += [
    SPECIFIC_TYPE_GENERAL_APPLIANCE,
    SPECIFIC_TYPE_KITCHEN_APPLIANCE,
    SPECIFIC_TYPE_LAUNDRY_APPLIANCE
]


# Device class Sensor Notification
GENERIC_TYPE_SENSOR_NOTIFICATION = (
    GenericType(0x07).set_doc('Sensor (notification)')
)
SPECIFIC_TYPE_NOTIFICATION_SENSOR = (
    SpecificType(0x01).set_doc('Notification Sensor')
)


# Device class Z/IP Gateway
GENERIC_TYPE_ZIP_GATEWAY = GenericType(0x14).set_doc('ZIP Gateway')
SPECIFIC_TYPE_ZIP_TUN_GATEWAY = (
    SpecificType(0x01).set_doc('ZIP Gateway (tunneling)')
)
SPECIFIC_TYPE_ZIP_ADV_GATEWAY = (
    SpecificType(0x02).set_doc('ZIP Gateway (advanced)')
)

GENERIC_TYPES = [
    GENERIC_TYPE_UNKNOWN,
    GENERIC_TYPE_GENERIC_CONTROLLER,  # 0x01
    GENERIC_TYPE_STATIC_CONTROLLER,  # 0x02
    GENERIC_TYPE_AV_CONTROL_POINT,  # 0x03
    GENERIC_TYPE_DISPLAY,  # 0x04
    GENERIC_TYPE_NETWORK_EXTENDER,  # 0x05
    GENERIC_TYPE_APPLIANCE,  # 0x06
    GENERIC_TYPE_SENSOR_NOTIFICATION,  # 0x07
    GENERIC_TYPE_THERMOSTAT,  # 0x08
    GENERIC_TYPE_WINDOW_COVERING,  # 0x09
    GENERIC_TYPE_REPEATER_SLAVE,  # 0x0F
    GENERIC_TYPE_SWITCH_BINARY,  # 0x10
    GENERIC_TYPE_SWITCH_MULTILEVEL,  # 0x11
    GENERIC_TYPE_SWITCH_REMOTE,  # 0x12
    GENERIC_TYPE_SWITCH_TOGGLE,  # 0x13
    GENERIC_TYPE_ZIP_GATEWAY,  # 0x14
    GENERIC_TYPE_ZIP_NODE,  # 0x15
    GENERIC_TYPE_VENTILATION,  # 0x16
    GENERIC_TYPE_SECURITY_PANEL,  # 0x17
    GENERIC_TYPE_WALL_CONTROLLER,  # 0x18
    GENERIC_TYPE_SENSOR_BINARY,  # 0x20
    GENERIC_TYPE_SENSOR_MULTILEVEL,  # 0x21
    GENERIC_TYPE_METER_PULSE,  # 0x30
    GENERIC_TYPE_METER,  # 0x31
    GENERIC_TYPE_ENTRY_CONTROL,  # 0x40
    GENERIC_TYPE_SEMI_INTEROPERABLE,  # 0x50
    GENERIC_TYPE_SENSOR_ALARM,  # 0xA1
    GENERIC_TYPE_NON_INTEROPERABLE  # 0xFF
]


# ************ Z-Wave+ Role Type identifiers *************
class RoleType(int):
    value = 0
    doc = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        value = args[1]

        self = super(RoleType, cls).__new__(*args, **kwargs)
        setattr(self, 'value', value)
        return self

    def set_doc(self, value):
        """
        :param value:
        :type value: str

        :rtype: "RoleType"
        """
        if self.doc is None:
            self.doc = value
            self.__doc__ = value

        return self

    def __int__(self):
        return self.value

    def __str__(self):
        return self.doc

    def __eq__(self, other):
        """
        :param other:
        :type other: int, "RoleType"

        :rtype: bool
        """
        if isinstance(other, int):
            return int(self) == other

        return object.__eq__(self, other)

    def __ne__(self, other):
        """
        :param other:
        :type other: int, "RoleType"

        :rtype: bool
        """
        return not self.__eq__(other)


ROLE_TYPE_UNKNOWN = (
    RoleType(-1).set_doc('Role Type Unknown')
)
ROLE_TYPE_CONTROLLER_CENTRAL_STATIC = (
    RoleType(0x00).set_doc('Central Static Controller (CSC)')
)
ROLE_TYPE_CONTROLLER_SUB_STATIC = (
    RoleType(0x01).set_doc('Sub Static Controller (SSC)')
)
ROLE_TYPE_CONTROLLER_PORTABLE = (
    RoleType(0x02).set_doc('Portable Controller (PC)')
)
ROLE_TYPE_CONTROLLER_PORTABLE_REPORTING = (
    RoleType(0x03).set_doc('Reporting Portable Controller (RPC)')
)
ROLE_TYPE_SLAVE_PORTABLE = (
    RoleType(0x04).set_doc('Portable Slave (PS)')
)
ROLE_TYPE_SLAVE_ALWAYS_ON = (
    RoleType(0x05).set_doc('Always On Slave (AOS)')
)
ROLE_TYPE_SLAVE_SLEEPING_REPORTING = (
    RoleType(0x06).set_doc('Reporting Sleeping Slave (RSS)')
)
ROLE_TYPE_SLAVE_SLEEPING_LISTENING = (
    RoleType(0x07).set_doc('Listening Sleeping Slave (LSS)')
)
ROLE_TYPE_SLAVE_NETWORK_AWARE = (
    RoleType(0x08).set_doc('Network Aware Slave (NAS)')
)

ROLE_TYPES = [
    ROLE_TYPE_UNKNOWN,
    ROLE_TYPE_CONTROLLER_CENTRAL_STATIC,
    ROLE_TYPE_CONTROLLER_SUB_STATIC,
    ROLE_TYPE_CONTROLLER_PORTABLE,
    ROLE_TYPE_CONTROLLER_PORTABLE_REPORTING,
    ROLE_TYPE_SLAVE_PORTABLE,
    ROLE_TYPE_SLAVE_ALWAYS_ON,
    ROLE_TYPE_SLAVE_SLEEPING_REPORTING,
    ROLE_TYPE_SLAVE_SLEEPING_LISTENING,
    ROLE_TYPE_SLAVE_NETWORK_AWARE,
]


# *********** Basic Device Class identifiers *************
class BasicType(int):
    value = 0
    doc = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        value = args[1]

        self = super(BasicType, cls).__new__(*args, **kwargs)
        setattr(self, 'value', value)
        return self

    def set_doc(self, value):
        """
        :param value:
        :type value: str

        :rtype: "BasicType"
        """
        if self.doc is None:
            self.doc = value
            self.__doc__ = value

        return self

    def __int__(self):
        return self.value

    def __str__(self):
        return self.doc

    def __eq__(self, other):
        """
        :param other:
        :type other: int, "BasicType"

        :rtype: bool
        """
        if isinstance(other, int):
            return int(self) == other

        return object.__eq__(self, other)

    def __ne__(self, other):
        """
        :param other:
        :type other: int, "BasicType"

        :rtype: bool
        """
        return not self.__eq__(other)


BASIC_TYPE_UNKNOWN = BasicType(-1).set_doc('Basic Type Unknown')
BASIC_TYPE_CONTROLLER = BasicType(0x01).set_doc('Portable Controller')
BASIC_TYPE_ROUTING_SLAVE = BasicType(0x04).set_doc('Routing Slave')
BASIC_TYPE_SLAVE = BasicType(0x03).set_doc('Slave')
BASIC_TYPE_STATIC_CONTROLLER = BasicType(0x02).set_doc('Static Controller')


BASIC_TYPES = [
    BASIC_TYPE_UNKNOWN,
    BASIC_TYPE_CONTROLLER,
    BASIC_TYPE_ROUTING_SLAVE,
    BASIC_TYPE_SLAVE,
    BASIC_TYPE_STATIC_CONTROLLER
]


# *********** Node Type identifiers *************
class NodeType(int):
    value = 0
    doc = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        value = args[1]

        self = super(NodeType, cls).__new__(*args, **kwargs)
        setattr(self, 'value', value)
        return self

    def set_doc(self, value):
        """
        :param value:
        :type value: str

        :rtype: "NodeType"
        """
        if self.doc is None:
            self.doc = value
            self.__doc__ = value

        return self

    def __int__(self):
        return self.value

    def __str__(self):
        return self.doc

    def __eq__(self, other):
        """
        :param other:
        :type other: int, "NodeType"

        :rtype: bool
        """
        if isinstance(other, int):
            return int(self) == other

        return object.__eq__(self, other)

    def __ne__(self, other):
        """
        :param other:
        :type other: int, "NodeType"

        :rtype: bool
        """
        return not self.__eq__(other)


NODE_TYPE_UNKNOWN = NodeType(-1).set_doc('Node Type Unknown')
NODE_TYPE_ZWAVEPLUS_NODE = (
    NodeType(0x00).set_doc('Z-Wave+ Node')
)
NODE_TYPE_ZWAVEPLUS_FOR_IP_ROUTER = (
    NodeType(0x01).set_doc('Z-Wave+ IP Router')
)
NODE_TYPE_ZWAVEPLUS_FOR_IP_GATEWAY = (
    NodeType(0x02).set_doc('Z-Wave+ IP Gateway')
)
NODE_TYPE_ZWAVEPLUS_FOR_IP_CLIENT_IP_NODE = (
    NodeType(0x03).set_doc('Z-Wave+ IP Client and IP Node')
)
NODE_TYPE_ZWAVEPLUS_FOR_IP_CLIENT_ZWAVE_NODE = (
    NodeType(0x04).set_doc('Z-Wave+ IP Client and Z-Wave Node')
)

NODE_TYPES = [
    NODE_TYPE_UNKNOWN,
    NODE_TYPE_ZWAVEPLUS_NODE,
    NODE_TYPE_ZWAVEPLUS_FOR_IP_ROUTER,
    NODE_TYPE_ZWAVEPLUS_FOR_IP_GATEWAY,
    NODE_TYPE_ZWAVEPLUS_FOR_IP_CLIENT_IP_NODE,
    NODE_TYPE_ZWAVEPLUS_FOR_IP_CLIENT_ZWAVE_NODE
]


# ************* Types class *************
class Types(object):
    """
    Various "type" Labels

    There are several "type" labels that a node is placed into.

    * role type
    * device type
    * basic type
    * generic type (category)
    * specific type (sub category)
    * node type
    """

    def __init__(self, node):
        """
        :param node:
        :type node: ZWaveNode
        """
        self._node = node

    @property
    def network(self):
        """
        The Network object
        """
        return self._node.network

    @property
    def _manager(self):
        """
        :rtype: ZWaveManager
        """
        return self._node.network.manager

    @property
    def home_id(self):
        """
        The Home Id

        :rtype: int
        """
        return self.network.home_id

    @property
    def node_id(self):
        """
        The Node Id

        :rtype: NodeId
        """
        return self._node.id

    @property
    def role(self):
        """
        The Role Type

        :rtype: RoleType
        """
        if 'role_type' in self._node.xml_handler:
            code = int(self._node.xml_handler['role_type'], 16)
        else:
            code = self._manager.getNodeRole(
                self.home_id,
                self._node.id.node_id
            )

        for role_type in ROLE_TYPES:
            if role_type == code:
                return role_type

        return ROLE_TYPE_UNKNOWN

    @property
    def device(self):
        """
        The Device Type

        :rtype: DeviceType
        """
        if 'device_type' in self._node.xml_handler:
            code = int(self._node.xml_handler['device_type'], 16)
        else:
            code = self._manager.getNodeDeviceType(
                self.home_id,
                self._node.id.node_id
            )

        for device_type in DEVICE_TYPES:
            if device_type == code:
                return device_type

        return DEVICE_TYPE_UNKNOWN

    @property
    def basic(self):
        """
        The Basic Type

        :rtype: BasicType
        """
        if 'basic_type' in self._node.xml_handler:
            code = int(self._node.xml_handler['basic_type'], 16)
        else:
            code = self._manager.getNodeBasic(
                self.home_id,
                self._node.id.node_id
            )

        for basic_type in BASIC_TYPES:
            if basic_type == code:
                return basic_type

        return BASIC_TYPE_UNKNOWN

    @property
    def generic(self):
        """
        The Generic Type

        :rtype: GenericType
        """
        if 'generic_type' in self._node.xml_handler:
            code = int(self._node.xml_handler['generic_type'], 16)
        else:
            code = self._manager.getNodeGeneric(
                self.home_id,
                self._node.id.node_id
            )

        for generic_type in GENERIC_TYPES:
            if generic_type == code:
                return generic_type

        return GENERIC_TYPE_UNKNOWN

    @property
    def specific(self):
        """
        The Specific Type

        :rtype: SpecificType
        """
        generic = self.generic

        if 'specific_type' in self._node.xml_handler:
            code = int(self._node._xml_handler['specific_type'], 16)  # NOQA
        else:
            code = self._manager.getNodeSpecific(
                self.home_id,
                self._node.id.node_id
            )

        return generic[code]

    @property
    def node(self):
        """
        The Node Type

        :rtype: NodeType
        """
        if 'node_type' in self._node._xml_handler:  # NOQA
            return self._node._xml_handler['node_type']  # NOQA
        else:
            return self._manager.getNodeType(
                self.home_id,
                self._node.id.node_id
            )

    @property
    def as_dict(self):
        """
        A dictionary representation of the node types

        :rtype: dict
        """
        return dict(
            role=dict(
                id=int(self.role),
                doc=self.role.doc
            ),
            basic=dict(
                id=int(self.basic),
                doc=self.basic.doc
            ),
            generic=dict(
                id=int(self.generic),
                doc=self.generic.doc
            ),
            specific=dict(
                id=int(self.specific),
                doc=self.specific.doc
            ),
            device=dict(
                id=int(self.device),
                doc=self.device.doc
            ),
            node=dict(
                id=int(self.node),
                doc=self.node.doc
            )
        )
