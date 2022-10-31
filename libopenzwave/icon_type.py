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
:synopsis: python-openzwave exception classes

.. moduleauthor:: Kevin G Schlosser
"""

# MUST NOT be used by any product
ICON_TYPE_UNASSIGNED = 0x0000

# Central Controller Device Type
ICON_TYPE_GENERIC_CENTRAL_CONTROLLER = 0x0100

# Display Simple Device Type
ICON_TYPE_GENERIC_DISPLAY_SIMPLE = 0x0200

# Door Lock Keypad  Device Type
ICON_TYPE_GENERIC_DOOR_LOCK_KEYPAD = 0x0300

# Fan Switch  Device Type
ICON_TYPE_GENERIC_FAN_SWITCH = 0x0400

# Gateway  Device Type
ICON_TYPE_GENERIC_GATEWAY = 0x0500

# Light Dimmer Switch  Device Type
ICON_TYPE_GENERIC_LIGHT_DIMMER_SWITCH = 0x0600
# Light Dimmer, implemented as a plugin device
ICON_TYPE_SPECIFIC_LIGHT_DIMMER_SWITCH_PLUGIN = 0x0601
# Light Dimmer, implemented as a wall outlet
ICON_TYPE_SPECIFIC_LIGHT_DIMMER_SWITCH_WALL_OUTLET = 0x0602
# Light Dimmer, implemented as a ceiling outlet
ICON_TYPE_SPECIFIC_LIGHT_DIMMER_SWITCH_CEILING_OUTLET = 0x0603
# Relay device, implemented as a wall mounted lamp
ICON_TYPE_SPECIFIC_LIGHT_DIMMER_SWITCH_WALL_LAMP = 0x0604
# Relay device, implemented as a ceiling outlet
ICON_TYPE_SPECIFIC_LIGHT_DIMMER_SWITCH_LAMP_POST_HIGH = 0x0605
# Relay device, implemented as a ceiling outlet
ICON_TYPE_SPECIFIC_LIGHT_DIMMER_SWITCH_LAMP_POST_LOW = 0x0606

# On/Off Power Switch  Device Type
ICON_TYPE_GENERIC_ON_OFF_POWER_SWITCH = 0x0700
# Relay device, implemented as a plugin device
ICON_TYPE_SPECIFIC_ON_OFF_POWER_SWITCH_PLUGIN = 0x0701
# Relay device, implemented as a wall outlet
ICON_TYPE_SPECIFIC_ON_OFF_POWER_SWITCH_WALL_OUTLET = 0x0702
# Relay device, implemented as a ceiling outlet
ICON_TYPE_SPECIFIC_ON_OFF_POWER_SWITCH_CEILING_OUTLET = 0x0703
# Relay device, implemented as a wall mounted lamp
ICON_TYPE_SPECIFIC_ON_OFF_POWER_SWITCH_WALL_LAMP = 0x0704
# Relay device, implemented as a ceiling outlet
ICON_TYPE_SPECIFIC_ON_OFF_POWER_SWITCH_LAMP_POST_HIGH = 0x0705
# Relay device, implemented as a ceiling outlet
ICON_TYPE_SPECIFIC_ON_OFF_POWER_SWITCH_LAMP_POST_LOW = 0x0706

# Power Strip  Device Type
ICON_TYPE_GENERIC_POWER_STRIP = 0x0800
# Individual outlet of a power strip for showing outlets in exploded view
ICON_TYPE_SPECIFIC_POWER_STRIP_INDIVIDUAL_OUTLET = 0x08

# Remote Control AV  Device Type
ICON_TYPE_GENERIC_REMOTE_CONTROL_AV = 0x0900

# Remote Control Multi Purpose Device Type
ICON_TYPE_GENERIC_REMOTE_CONTROL_MULTI_PURPOSE = 0x0A00

# Remote Control Simple Device Type
ICON_TYPE_GENERIC_REMOTE_CONTROL_SIMPLE = 0x0B00
# Remote Control Simple Device Type (Key fob)
ICON_TYPE_SPECIFIC_REMOTE_CONTROL_SIMPLE_KEYFOB = 0x0B01

# Sensor Notification Device Type
ICON_TYPE_GENERIC_SENSOR_NOTIFICATION = 0x0C00
# Sensor Notification Device Type (Notification type Smoke Alarm)
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_SMOKE_ALARM = 0x0C01
# Sensor Notification Device Type (Notification type CO Alarm)
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_CO_ALARM = 0x0C02
# Sensor Notification Device Type (Notification type CO2 Alarm)
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_CO2_ALARM = 0x0C03
# Sensor Notification Device Type (Notification type Heat Alarm)
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_HEAT_ALARM = 0x0C04
# Sensor Notification Device Type (Notification type Water Alarm)
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_WATER_ALARM = 0x0C05
# Sensor Notification Device Type (Notification type Access Control)
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_ACCESS_CONTROL = 0x0C06
# Sensor Notification Device Type (Notification type Home Security)
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_HOME_SECURITY = 0x0C07
# Sensor Notification Device Type (Notification type Power Management)
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_POWER_MANAGEMENT = 0x0C08
# Sensor Notification Device Type (Notification type System)
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_SYSTEM = 0x0C09
# Sensor Notification Device Type (Notification type Emergency Alarm)
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_EMERGENCY_ALARM = 0x0C0
# Sensor Notification Device Type (Notification type Clock)
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_CLOCK = 0x0C0
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_APPLIANCE = 0x0C0C
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_HOME_HEALTH = 0x0C0D
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_SIREN = 0x0C0E
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_WATER_VALVE = 0x0C0F
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_WEATHER_ALARM = 0x0C10
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_IRRIGATION = 0x0C11
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_GAS_ALARM = 0x0C12
# Sensor Notification Device Type (Bundled Notification functions)
ICON_TYPE_SPECIFIC_SENSOR_NOTIFICATION_MULTIDEVICE = 0x0

# Sensor Multilevel Device Type
ICON_TYPE_GENERIC_SENSOR_MULTILEVEL = 0x0D00
# Sensor Multilevel Device Type (Sensor type Air Temperature)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_AIR_TEMPERATURE = 0x0D01
# Sensor Multilevel Device Type (Sensor type General Purpose Value)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_GENERAL_PURPOSE_VALUE = 0x0D02
# Sensor Multilevel Device Type (Sensor type Luminance)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_LUMINANCE = 0x0D03
# Sensor Multilevel Device Type (Sensor type Power)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_POWER = 0x0D04
# Sensor Multilevel Device Type (Sensor type Humidity)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_HUMIDITY = 0x0D05
# Sensor Multilevel Device Type (Sensor type Velocity)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_VELOCITY = 0x0D06
# Sensor Multilevel Device Type (Sensor type Direction)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_DIRECTION = 0x0D07
# Sensor Multilevel Device Type (Sensor type Atmospheric Pressure)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_ATMOSPHERIC_PRESSURE = 0x0D08
# Sensor Multilevel Device Type (Sensor type Barometric Pressure)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_BAROMETRIC_PRESSURE = 0x0D09
# Sensor Multilevel Device Type (Sensor type Solar Radiation)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_SOLOR_RADIATION = 0x0D0
# Sensor Multilevel Device Type (Sensor type Dew Point)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_DEW_POINT = 0x0D0
# Sensor Multilevel Device Type (Sensor type Rain Rate)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_RAIN_RATE = 0x0D0
# Sensor Multilevel Device Type (Sensor type Tide Level)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_TIDE_LEVEL = 0x0D0
# Sensor Multilevel Device Type (Sensor type Weight)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_WEIGHT = 0x0D0
# Sensor Multilevel Device Type (Sensor type Voltage)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_VOLTAGE = 0x0D0
# Sensor Multilevel Device Type (Sensor type Current)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_CURRENT = 0x0D10
# Sensor Multilevel Device Type (Sensor type CO2 Level)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_CO2_LEVEL = 0x0D11
# Sensor Multilevel Device Type (Sensor type Air Flow)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_AIR_FLOW = 0x0D12
# Sensor Multilevel Device Type (Sensor type Tank Capacity)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_TANK_CAPACITY = 0x0D13
# Sensor Multilevel Device Type (Sensor type Distance)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_DISTANCE = 0x0D14
# Sensor Multilevel Device Type (Sensor type Angle Position)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_ANGLE_POSITION = 0x0D15
# Sensor Multilevel Device Type (Sensor type Rotation)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_ROTATION = 0x0D16
# Sensor Multilevel Device Type (Sensor type Water Temperature)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_WATER_TEMPERATURE = 0x0D17
# Sensor Multilevel Device Type (Sensor type Soil Temperature)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_SOIL_TEMPERATURE = 0x0D18
# Sensor Multilevel Device Type (Sensor type Seismic Intensity)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_SEISMIC_INTENSITY = 0x0D19
# Sensor Multilevel Device Type (Sensor type Seismic Magnitude)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_SEISMIC_MAGNITUDE = 0x0D1
# Sensor Multilevel Device Type (Sensor type Ultraviolet)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_ULTRAVIOLET = 0x0D1
# Sensor Multilevel Device Type (Sensor type Electrical Resistivity)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_ELECTRICAL_RESISTIVITY = 0x0D1
# Sensor Multilevel Device Type (Sensor type Electrical Conductivity)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_ELECTRICAL_CONDUCTIVITY = 0x0D1
# Sensor Multilevel Device Type (Sensor type Loudness)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_LOUDNESS = 0x0D1
# Sensor Multilevel Device Type (Sensor type Moisture)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_MOISTURE = 0x0D1
# Sensor Multilevel Device Type (Sensor type Frequency)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_FREQUENCY = 0x0D20
# Sensor Multilevel Device Type (Sensor type Time )
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_TIME = 0x0D21
# Sensor Multilevel Device Type (Sensor type Target Temperature)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_TARGET_TEMPERATURE = 0x0D22
# Sensor Multilevel Device Type (Bundled Sensor functions)
ICON_TYPE_SPECIFIC_SENSOR_MULTILEVEL_MULTIDEVICE = 0x0

# Set Top Box Device Type
ICON_TYPE_GENERIC_SET_TOP_BOX = 0x0E00

# Siren Device Type
ICON_TYPE_GENERIC_SIREN = 0x0F00

# Sub Energy Meter Device Type
ICON_TYPE_GENERIC_SUB_ENERGY_METER = 0x1000

# Sub System Controller Device Type
ICON_TYPE_GENERIC_SUB_SYSTEM_CONTROLLER = 0x1100

# Thermostat Device Type
ICON_TYPE_GENERIC_THERMOSTAT = 0x1200
# Thermostat Line Voltage Device Type
ICON_TYPE_SPECIFIC_THERMOSTAT_LINE_VOLTAGE = 0x1201
# Thermostat Setback Device Type
ICON_TYPE_SPECIFIC_THERMOSTAT_SETBACK = 0x1202

# Thermostat Setback [Obsoleted] Device Type
ICON_TYPE_GENERIC_THERMOSTAT_SETBACK_OBSOLETED = 0x1300

# TV Device Type
ICON_TYPE_GENERIC_TV = 0x1400

# Valve Open/Close Device Type
ICON_TYPE_GENERIC_VALVE_OPEN_CLOSE = 0x1500

# Wall Controller Device Type
ICON_TYPE_GENERIC_WALL_CONTROLLER = 0x1600

# Whole Home Meter Simple Device Type
ICON_TYPE_GENERIC_WHOLE_HOME_METER_SIMPLE = 0x1700

# Window Covering No Position/Endpoint  Device Type
ICON_TYPE_GENERIC_WINDOW_COVERING_NO_POSITION_ENDPOINT = 0x1800

# Window Covering Endpoint Aware Device Type
ICON_TYPE_GENERIC_WINDOW_COVERING_ENDPOINT_AWARE = 0x1900

# Window Covering Position/Endpoint Aware Device Type
ICON_TYPE_GENERIC_WINDOW_COVERING_POSITION_ENDPOINT_AWARE = 0x1A00

# Repeater Device Type
ICON_TYPE_GENERIC_REPEATER = 0x1B00

# Wall Switch
ICON_TYPE_GENERIC_DIMMER_WALL_SWITCH = 0x1C00
# Wall Switch, 1 button
ICON_TYPE_SPECIFIC_DIMMER_WALL_SWITCH_ONE_BUTTON = 0x1C01
# Wall Switch, 2 buttons
ICON_TYPE_SPECIFIC_DIMMER_WALL_SWITCH_TWO_BUTTONS = 0x1C02
# Wall Switch, 3 buttons
ICON_TYPE_SPECIFIC_DIMMER_WALL_SWITCH_THREE_BUTTONS = 0x1C03
# Wall Switch, 4 buttons
ICON_TYPE_SPECIFIC_DIMMER_WALL_SWITCH_FOUR_BUTTONS = 0x1C04
# Wall Switch, 1 rotary knob
ICON_TYPE_SPECIFIC_DIMMER_WALL_SWITCH_ONE_ROTARY = 0x1CF1

# Wall Switch
ICON_TYPE_GENERIC_ON_OFF_WALL_SWITCH = 0x1D00
# Wall Switch, 1 button
ICON_TYPE_SPECIFIC_ON_OFF_WALL_SWITCH_ONE_BUTTON = 0x1D01
# Wall Switch, 2 buttons
ICON_TYPE_SPECIFIC_ON_OFF_WALL_SWITCH_TWO_BUTTONS = 0x1D02
# Wall Switch, 3 buttons
ICON_TYPE_SPECIFIC_ON_OFF_WALL_SWITCH_THREE_BUTTONS = 0x1D03
# Wall Switch, 4 buttons
ICON_TYPE_SPECIFIC_ON_OFF_WALL_SWITCH_FOUR_BUTTONS = 0x1D04
# Door Bell (button)
ICON_TYPE_SPECIFIC_ON_OFF_WALL_SWITCH_DOOR_BELL = 0x1DE1
# Wall Switch, 1 rotary knob
ICON_TYPE_SPECIFIC_ON_OFF_WALL_SWITCH_ONE_ROTARY = 0x1DF1

# Barrier
ICON_TYPE_GENERIC_BARRIER = 0x1E00

# Irrigation
ICON_TYPE_GENERIC_IRRIGATION = 0x1F00

# Entry Control
ICON_TYPE_GENERIC_ENTRY_CONTROL = 0x2000
# Entry Control Keypad 0-9
ICON_TYPE_SPECIFIC_ENTRY_CONTROL_KEYPAD = 0x2001
# Entry Control RFID tag reader, no button
ICON_TYPE_SPECIFIC_ENTRY_CONTROL_RFID_TAG_READER_NO_BUTTON = 0x2002
