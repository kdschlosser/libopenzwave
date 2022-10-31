========================
Node Types documentation
========================


-----------
Basic Types
-----------

.. py:data:: libopenzwave.node_types.ROLE_TYPE_UNKNOWN

    * `str(ROLE_TYPE_UNKNOWN)`: Basic Type Unknown
    * `int(ROLE_TYPE_UNKNOWN)`: -1


.. py:data:: libopenzwave.node_types.ROLE_TYPE_CONTROLLER_SUB_STATIC

    * `str(ROLE_TYPE_CONTROLLER_SUB_STATIC)`: Portable Controller
    * `int(ROLE_TYPE_CONTROLLER_SUB_STATIC)`: 0x1


.. py:data:: libopenzwave.node_types.ROLE_TYPE_SLAVE_PORTABLE

    * `str(ROLE_TYPE_SLAVE_PORTABLE)`: Routing Slave
    * `int(ROLE_TYPE_SLAVE_PORTABLE)`: 0x4


.. py:data:: libopenzwave.node_types.ROLE_TYPE_CONTROLLER_PORTABLE_REPORTING

    * `str(ROLE_TYPE_CONTROLLER_PORTABLE_REPORTING)`: Slave
    * `int(ROLE_TYPE_CONTROLLER_PORTABLE_REPORTING)`: 0x3


.. py:data:: libopenzwave.node_types.ROLE_TYPE_CONTROLLER_PORTABLE

    * `str(ROLE_TYPE_CONTROLLER_PORTABLE)`: Static Controller
    * `int(ROLE_TYPE_CONTROLLER_PORTABLE)`: 0x2




-------------
Generic Types
-------------

.. py:data:: libopenzwave.node_types.GENERIC_TYPE_UNKNOWN

    * `str(GENERIC_TYPE_UNKNOWN)`: Generic Type Unknown
    * `int(GENERIC_TYPE_UNKNOWN)`: -1
    * Specific Types: `None`


.. py:data:: libopenzwave.node_types.GENERIC_TYPE_GENERIC_CONTROLLER

    * `str(GENERIC_TYPE_GENERIC_CONTROLLER)`: Remote Controller
    * `int(GENERIC_TYPE_GENERIC_CONTROLLER)`: 0x1
    * Specific Types:

        * `SPECIFIC_TYPE_PORTABLE_REMOTE_CONTROLLER`:

            * `str(SPECIFIC_TYPE_PORTABLE_REMOTE_CONTROLLER)`: Remote Control (Multi Purpose)
            * `int(SPECIFIC_TYPE_PORTABLE_REMOTE_CONTROLLER)`: 0x1

        * `SPECIFIC_TYPE_PORTABLE_SCENE_CONTROLLER`:

            * `str(SPECIFIC_TYPE_PORTABLE_SCENE_CONTROLLER)`: Portable Scene Controller
            * `int(SPECIFIC_TYPE_PORTABLE_SCENE_CONTROLLER)`: 0x2

        * `SPECIFIC_TYPE_PORTABLE_INSTALLER_TOOL`:

            * `str(SPECIFIC_TYPE_PORTABLE_INSTALLER_TOOL)`: Installer Tool
            * `int(SPECIFIC_TYPE_PORTABLE_INSTALLER_TOOL)`: 0x3

        * `SPECIFIC_TYPE_REMOTE_CONTROL_AV`:

            * `str(SPECIFIC_TYPE_REMOTE_CONTROL_AV)`: Remote Control (AV)
            * `int(SPECIFIC_TYPE_REMOTE_CONTROL_AV)`: 0x4

        * `SPECIFIC_TYPE_REMOTE_CONTROL_SIMPLE`:

            * `str(SPECIFIC_TYPE_REMOTE_CONTROL_SIMPLE)`: Remote Control (Simple)
            * `int(SPECIFIC_TYPE_REMOTE_CONTROL_SIMPLE)`: 0x6




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_STATIC_CONTROLLER

    * `str(GENERIC_TYPE_STATIC_CONTROLLER)`: Static Controller
    * `int(GENERIC_TYPE_STATIC_CONTROLLER)`: 0x2
    * Specific Types:

        * `SPECIFIC_TYPE_PC_CONTROLLER`:

            * `str(SPECIFIC_TYPE_PC_CONTROLLER)`: Central Controller
            * `int(SPECIFIC_TYPE_PC_CONTROLLER)`: 0x1

        * `SPECIFIC_TYPE_SCENE_CONTROLLER`:

            * `str(SPECIFIC_TYPE_SCENE_CONTROLLER)`: Scene Controller
            * `int(SPECIFIC_TYPE_SCENE_CONTROLLER)`: 0x2

        * `SPECIFIC_TYPE_STATIC_INSTALLER_TOOL`:

            * `str(SPECIFIC_TYPE_STATIC_INSTALLER_TOOL)`: Installer Tool
            * `int(SPECIFIC_TYPE_STATIC_INSTALLER_TOOL)`: 0x3

        * `SPECIFIC_TYPE_SET_TOP_BOX`:

            * `str(SPECIFIC_TYPE_SET_TOP_BOX)`: Set Top Box
            * `int(SPECIFIC_TYPE_SET_TOP_BOX)`: 0x4

        * `SPECIFIC_TYPE_SUB_SYSTEM_CONTROLLER`:

            * `str(SPECIFIC_TYPE_SUB_SYSTEM_CONTROLLER)`: Sub System Controller
            * `int(SPECIFIC_TYPE_SUB_SYSTEM_CONTROLLER)`: 0x5

        * `SPECIFIC_TYPE_TV`:

            * `str(SPECIFIC_TYPE_TV)`: TV
            * `int(SPECIFIC_TYPE_TV)`: 0x6

        * `SPECIFIC_TYPE_GATEWAY`:

            * `str(SPECIFIC_TYPE_GATEWAY)`: Gateway
            * `int(SPECIFIC_TYPE_GATEWAY)`: 0x7




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_AV_CONTROL_POINT

    * `str(GENERIC_TYPE_AV_CONTROL_POINT)`: AV Control Point
    * `int(GENERIC_TYPE_AV_CONTROL_POINT)`: 0x3
    * Specific Types:

        * `SPECIFIC_TYPE_DOORBELL`:

            * `str(SPECIFIC_TYPE_DOORBELL)`: Doorbell
            * `int(SPECIFIC_TYPE_DOORBELL)`: 0x12

        * `SPECIFIC_TYPE_SATELLITE_RECEIVER`:

            * `str(SPECIFIC_TYPE_SATELLITE_RECEIVER)`: Satellite Receiver
            * `int(SPECIFIC_TYPE_SATELLITE_RECEIVER)`: 0x4

        * `SPECIFIC_TYPE_SATELLITE_RECEIVER_V2`:

            * `str(SPECIFIC_TYPE_SATELLITE_RECEIVER_V2)`: Satellite Receiver V2
            * `int(SPECIFIC_TYPE_SATELLITE_RECEIVER_V2)`: 0x11

        * `SPECIFIC_TYPE_SOUND_SWITCH`:

            * `str(SPECIFIC_TYPE_SOUND_SWITCH)`: Sound Switch
            * `int(SPECIFIC_TYPE_SOUND_SWITCH)`: 0x1




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_DISPLAY

    * `str(GENERIC_TYPE_DISPLAY)`: Display
    * `int(GENERIC_TYPE_DISPLAY)`: 0x4
    * Specific Types:

        * `SPECIFIC_TYPE_SIMPLE_DISPLAY`:

            * `str(SPECIFIC_TYPE_SIMPLE_DISPLAY)`: Display (simple)
            * `int(SPECIFIC_TYPE_SIMPLE_DISPLAY)`: 0x1




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_NETWORK_EXTENDER

    * `str(GENERIC_TYPE_NETWORK_EXTENDER)`: Network Extender
    * `int(GENERIC_TYPE_NETWORK_EXTENDER)`: 0x5
    * Specific Types:

        * `SPECIFIC_TYPE_SECURE_EXTENDER`:

            * `str(SPECIFIC_TYPE_SECURE_EXTENDER)`: Secure Extender
            * `int(SPECIFIC_TYPE_SECURE_EXTENDER)`: 0x1




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_APPLIANCE

    * `str(GENERIC_TYPE_APPLIANCE)`: Appliance
    * `int(GENERIC_TYPE_APPLIANCE)`: 0x6
    * Specific Types:

        * `SPECIFIC_TYPE_GENERAL_APPLIANCE`:

            * `str(SPECIFIC_TYPE_GENERAL_APPLIANCE)`: General Appliance
            * `int(SPECIFIC_TYPE_GENERAL_APPLIANCE)`: 0x1

        * `SPECIFIC_TYPE_KITCHEN_APPLIANCE`:

            * `str(SPECIFIC_TYPE_KITCHEN_APPLIANCE)`: Kitchen Appliance
            * `int(SPECIFIC_TYPE_KITCHEN_APPLIANCE)`: 0x2

        * `SPECIFIC_TYPE_LAUNDRY_APPLIANCE`:

            * `str(SPECIFIC_TYPE_LAUNDRY_APPLIANCE)`: Laundry Appliance
            * `int(SPECIFIC_TYPE_LAUNDRY_APPLIANCE)`: 0x3




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_SENSOR_NOTIFICATION

    * `str(GENERIC_TYPE_SENSOR_NOTIFICATION)`: Sensor (notification)
    * `int(GENERIC_TYPE_SENSOR_NOTIFICATION)`: 0x7
    * Specific Types: `None`


.. py:data:: libopenzwave.node_types.GENERIC_TYPE_THERMOSTAT

    * `str(GENERIC_TYPE_THERMOSTAT)`: Thermostat
    * `int(GENERIC_TYPE_THERMOSTAT)`: 0x8
    * Specific Types:

        * `SPECIFIC_TYPE_SETBACK_SCHEDULE_THERMOSTAT`:

            * `str(SPECIFIC_TYPE_SETBACK_SCHEDULE_THERMOSTAT)`: Setback Schedule Thermostat
            * `int(SPECIFIC_TYPE_SETBACK_SCHEDULE_THERMOSTAT)`: 0x3

        * `SPECIFIC_TYPE_SETBACK_THERMOSTAT`:

            * `str(SPECIFIC_TYPE_SETBACK_THERMOSTAT)`: Thermostat Setback
            * `int(SPECIFIC_TYPE_SETBACK_THERMOSTAT)`: 0x5

        * `SPECIFIC_TYPE_SETPOINT_THERMOSTAT`:

            * `str(SPECIFIC_TYPE_SETPOINT_THERMOSTAT)`: Thermostat Setpoint
            * `int(SPECIFIC_TYPE_SETPOINT_THERMOSTAT)`: 0x4

        * `SPECIFIC_TYPE_THERMOSTAT_GENERAL`:

            * `str(SPECIFIC_TYPE_THERMOSTAT_GENERAL)`: Thermostat General
            * `int(SPECIFIC_TYPE_THERMOSTAT_GENERAL)`: 0x2

        * `SPECIFIC_TYPE_THERMOSTAT_GENERAL_V2`:

            * `str(SPECIFIC_TYPE_THERMOSTAT_GENERAL_V2)`: Thermostat HVAC
            * `int(SPECIFIC_TYPE_THERMOSTAT_GENERAL_V2)`: 0x6

        * `SPECIFIC_TYPE_THERMOSTAT_HEATING`:

            * `str(SPECIFIC_TYPE_THERMOSTAT_HEATING)`: Thermostat Heating
            * `int(SPECIFIC_TYPE_THERMOSTAT_HEATING)`: 0x1




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_WINDOW_COVERING

    * `str(GENERIC_TYPE_WINDOW_COVERING)`: Window Covering
    * `int(GENERIC_TYPE_WINDOW_COVERING)`: 0x9
    * Specific Types:

        * `SPECIFIC_TYPE_SIMPLE_WINDOW_COVERING`:

            * `str(SPECIFIC_TYPE_SIMPLE_WINDOW_COVERING)`: Simple Window Covering Control
            * `int(SPECIFIC_TYPE_SIMPLE_WINDOW_COVERING)`: 0x1




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_REPEATER_SLAVE

    * `str(GENERIC_TYPE_REPEATER_SLAVE)`: Repeater Slave
    * `int(GENERIC_TYPE_REPEATER_SLAVE)`: 0xF
    * Specific Types:

        * `SPECIFIC_TYPE_REPEATER_SLAVE`:

            * `str(SPECIFIC_TYPE_REPEATER_SLAVE)`: Basic Repeater Slave
            * `int(SPECIFIC_TYPE_REPEATER_SLAVE)`: 0x1

        * `SPECIFIC_TYPE_VIRTUAL_NODE`:

            * `str(SPECIFIC_TYPE_VIRTUAL_NODE)`: Virtual Node
            * `int(SPECIFIC_TYPE_VIRTUAL_NODE)`: 0x2




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_SWITCH_BINARY

    * `str(GENERIC_TYPE_SWITCH_BINARY)`: Binary Switch
    * `int(GENERIC_TYPE_SWITCH_BINARY)`: 0x10
    * Specific Types:

        * `SPECIFIC_TYPE_POWER_SWITCH_BINARY`:

            * `str(SPECIFIC_TYPE_POWER_SWITCH_BINARY)`: On/Off Power Switch
            * `int(SPECIFIC_TYPE_POWER_SWITCH_BINARY)`: 0x1

        * `SPECIFIC_TYPE_SCENE_SWITCH_BINARY`:

            * `str(SPECIFIC_TYPE_SCENE_SWITCH_BINARY)`: Binary Scene Switch
            * `int(SPECIFIC_TYPE_SCENE_SWITCH_BINARY)`: 0x3

        * `SPECIFIC_TYPE_POWER_STRIP`:

            * `str(SPECIFIC_TYPE_POWER_STRIP)`: Power Strip
            * `int(SPECIFIC_TYPE_POWER_STRIP)`: 0x4

        * `SPECIFIC_TYPE_SIREN`:

            * `str(SPECIFIC_TYPE_SIREN)`: Siren
            * `int(SPECIFIC_TYPE_SIREN)`: 0x5

        * `SPECIFIC_TYPE_VALVE_OPEN_CLOSE`:

            * `str(SPECIFIC_TYPE_VALVE_OPEN_CLOSE)`: Valve (open/close)
            * `int(SPECIFIC_TYPE_VALVE_OPEN_CLOSE)`: 0x6

        * `SPECIFIC_TYPE_COLOR_TUNABLE_BINARY`:

            * `str(SPECIFIC_TYPE_COLOR_TUNABLE_BINARY)`: Turnable Switch
            * `int(SPECIFIC_TYPE_COLOR_TUNABLE_BINARY)`: 0x2

        * `SPECIFIC_TYPE_IRRIGATION_CONTROLLER`:

            * `str(SPECIFIC_TYPE_IRRIGATION_CONTROLLER)`: Irrigation
            * `int(SPECIFIC_TYPE_IRRIGATION_CONTROLLER)`: 0x7




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_SWITCH_MULTILEVEL

    * `str(GENERIC_TYPE_SWITCH_MULTILEVEL)`: Multilevel Switch
    * `int(GENERIC_TYPE_SWITCH_MULTILEVEL)`: 0x11
    * Specific Types:

        * `SPECIFIC_TYPE_CLASS_A_MOTOR_CONTROL`:

            * `str(SPECIFIC_TYPE_CLASS_A_MOTOR_CONTROL)`: Window Covering No Position/Endpoint
            * `int(SPECIFIC_TYPE_CLASS_A_MOTOR_CONTROL)`: 0x5

        * `SPECIFIC_TYPE_CLASS_B_MOTOR_CONTROL`:

            * `str(SPECIFIC_TYPE_CLASS_B_MOTOR_CONTROL)`: Window Covering Endpoint Aware
            * `int(SPECIFIC_TYPE_CLASS_B_MOTOR_CONTROL)`: 0x6

        * `SPECIFIC_TYPE_CLASS_C_MOTOR_CONTROL`:

            * `str(SPECIFIC_TYPE_CLASS_C_MOTOR_CONTROL)`: Window Covering Position/Endpoint Aware
            * `int(SPECIFIC_TYPE_CLASS_C_MOTOR_CONTROL)`: 0x7

        * `SPECIFIC_TYPE_MOTOR_MULTIPOSITION`:

            * `str(SPECIFIC_TYPE_MOTOR_MULTIPOSITION)`: Multiposition Motor
            * `int(SPECIFIC_TYPE_MOTOR_MULTIPOSITION)`: 0x3

        * `SPECIFIC_TYPE_POWER_SWITCH_MULTILEVEL`:

            * `str(SPECIFIC_TYPE_POWER_SWITCH_MULTILEVEL)`: Light Dimmer Switch
            * `int(SPECIFIC_TYPE_POWER_SWITCH_MULTILEVEL)`: 0x1

        * `SPECIFIC_TYPE_SCENE_SWITCH_MULTILEVEL`:

            * `str(SPECIFIC_TYPE_SCENE_SWITCH_MULTILEVEL)`: Multilevel Scene Switch
            * `int(SPECIFIC_TYPE_SCENE_SWITCH_MULTILEVEL)`: 0x4

        * `SPECIFIC_TYPE_FAN_SWITCH`:

            * `str(SPECIFIC_TYPE_FAN_SWITCH)`: Fan Switch
            * `int(SPECIFIC_TYPE_FAN_SWITCH)`: 0x8

        * `SPECIFIC_TYPE_COLOR_TUNABLE_MULTILEVEL`:

            * `str(SPECIFIC_TYPE_COLOR_TUNABLE_MULTILEVEL)`: Turnable (multilevel) Switch
            * `int(SPECIFIC_TYPE_COLOR_TUNABLE_MULTILEVEL)`: 0x2




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_SWITCH_REMOTE

    * `str(GENERIC_TYPE_SWITCH_REMOTE)`: Remote Switch
    * `int(GENERIC_TYPE_SWITCH_REMOTE)`: 0x12
    * Specific Types:

        * `SPECIFIC_TYPE_SWITCH_REMOTE_BINARY`:

            * `str(SPECIFIC_TYPE_SWITCH_REMOTE_BINARY)`: Binary Remote Switch
            * `int(SPECIFIC_TYPE_SWITCH_REMOTE_BINARY)`: 0x1

        * `SPECIFIC_TYPE_SWITCH_REMOTE_MULTILEVEL`:

            * `str(SPECIFIC_TYPE_SWITCH_REMOTE_MULTILEVEL)`: Multilevel Remote Switch
            * `int(SPECIFIC_TYPE_SWITCH_REMOTE_MULTILEVEL)`: 0x2

        * `SPECIFIC_TYPE_SWITCH_REMOTE_TOGGLE_BINARY`:

            * `str(SPECIFIC_TYPE_SWITCH_REMOTE_TOGGLE_BINARY)`: Binary Toggle Remote Switch
            * `int(SPECIFIC_TYPE_SWITCH_REMOTE_TOGGLE_BINARY)`: 0x3

        * `SPECIFIC_TYPE_SWITCH_REMOTE_TOGGLE_MULTILEVEL`:

            * `str(SPECIFIC_TYPE_SWITCH_REMOTE_TOGGLE_MULTILEVEL)`: Multilevel Toggle Remote Switch
            * `int(SPECIFIC_TYPE_SWITCH_REMOTE_TOGGLE_MULTILEVEL)`: 0x4




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_SWITCH_TOGGLE

    * `str(GENERIC_TYPE_SWITCH_TOGGLE)`: Toggle Switch
    * `int(GENERIC_TYPE_SWITCH_TOGGLE)`: 0x13
    * Specific Types:

        * `SPECIFIC_TYPE_SWITCH_TOGGLE_BINARY`:

            * `str(SPECIFIC_TYPE_SWITCH_TOGGLE_BINARY)`: Binary Toggle Switch
            * `int(SPECIFIC_TYPE_SWITCH_TOGGLE_BINARY)`: 0x1

        * `SPECIFIC_TYPE_SWITCH_TOGGLE_MULTILEVEL`:

            * `str(SPECIFIC_TYPE_SWITCH_TOGGLE_MULTILEVEL)`: Multilevel Toggle Switch
            * `int(SPECIFIC_TYPE_SWITCH_TOGGLE_MULTILEVEL)`: 0x2




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_ZIP_GATEWAY

    * `str(GENERIC_TYPE_ZIP_GATEWAY)`: ZIP Gateway
    * `int(GENERIC_TYPE_ZIP_GATEWAY)`: 0x14
    * Specific Types: `None`


.. py:data:: libopenzwave.node_types.GENERIC_TYPE_ZIP_NODE

    * `str(GENERIC_TYPE_ZIP_NODE)`: ZIP
    * `int(GENERIC_TYPE_ZIP_NODE)`: 0x15
    * Specific Types:

        * `SPECIFIC_TYPE_ZIP_ADV_NODE`:

            * `str(SPECIFIC_TYPE_ZIP_ADV_NODE)`: ZIP (adv)
            * `int(SPECIFIC_TYPE_ZIP_ADV_NODE)`: 0x2

        * `SPECIFIC_TYPE_ZIP_TUN_NODE`:

            * `str(SPECIFIC_TYPE_ZIP_TUN_NODE)`: ZIP (tun)
            * `int(SPECIFIC_TYPE_ZIP_TUN_NODE)`: 0x1




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_VENTILATION

    * `str(GENERIC_TYPE_VENTILATION)`: Ventilation
    * `int(GENERIC_TYPE_VENTILATION)`: 0x16
    * Specific Types:

        * `SPECIFIC_TYPE_RESIDENTIAL_HRV`:

            * `str(SPECIFIC_TYPE_RESIDENTIAL_HRV)`: Residential HRV
            * `int(SPECIFIC_TYPE_RESIDENTIAL_HRV)`: 0x1




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_SECURITY_PANEL

    * `str(GENERIC_TYPE_SECURITY_PANEL)`: Security Panel
    * `int(GENERIC_TYPE_SECURITY_PANEL)`: 0x17
    * Specific Types:

        * `SPECIFIC_TYPE_ZONED_SECURITY_PANEL`:

            * `str(SPECIFIC_TYPE_ZONED_SECURITY_PANEL)`: Zoned Security Panel
            * `int(SPECIFIC_TYPE_ZONED_SECURITY_PANEL)`: 0x1




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_WALL_CONTROLLER

    * `str(GENERIC_TYPE_WALL_CONTROLLER)`: Wall Controller
    * `int(GENERIC_TYPE_WALL_CONTROLLER)`: 0x18
    * Specific Types:

        * `SPECIFIC_TYPE_BASIC_WALL_CONTROLLER`:

            * `str(SPECIFIC_TYPE_BASIC_WALL_CONTROLLER)`: Wall Controller
            * `int(SPECIFIC_TYPE_BASIC_WALL_CONTROLLER)`: 0x1




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_SENSOR_BINARY

    * `str(GENERIC_TYPE_SENSOR_BINARY)`: Binary Sensor
    * `int(GENERIC_TYPE_SENSOR_BINARY)`: 0x20
    * Specific Types:

        * `SPECIFIC_TYPE_ROUTING_SENSOR_BINARY`:

            * `str(SPECIFIC_TYPE_ROUTING_SENSOR_BINARY)`: Routing Binary Sensor
            * `int(SPECIFIC_TYPE_ROUTING_SENSOR_BINARY)`: 0x1




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_SENSOR_MULTILEVEL

    * `str(GENERIC_TYPE_SENSOR_MULTILEVEL)`: Multilevel Sensor
    * `int(GENERIC_TYPE_SENSOR_MULTILEVEL)`: 0x21
    * Specific Types:

        * `SPECIFIC_TYPE_ROUTING_SENSOR_MULTILEVEL`:

            * `str(SPECIFIC_TYPE_ROUTING_SENSOR_MULTILEVEL)`: Sensor (Multilevel)
            * `int(SPECIFIC_TYPE_ROUTING_SENSOR_MULTILEVEL)`: 0x1

        * `SPECIFIC_TYPE_CHIMNEY_FAN`:

            * `str(SPECIFIC_TYPE_CHIMNEY_FAN)`: Chimney Fan
            * `int(SPECIFIC_TYPE_CHIMNEY_FAN)`: 0x2




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_METER_PULSE

    * `str(GENERIC_TYPE_METER_PULSE)`: Pulse Meter
    * `int(GENERIC_TYPE_METER_PULSE)`: 0x30
    * Specific Types: `None`


.. py:data:: libopenzwave.node_types.GENERIC_TYPE_METER

    * `str(GENERIC_TYPE_METER)`: Meter
    * `int(GENERIC_TYPE_METER)`: 0x31
    * Specific Types:

        * `SPECIFIC_TYPE_SIMPLE_METER`:

            * `str(SPECIFIC_TYPE_SIMPLE_METER)`: Sub Energy Meter
            * `int(SPECIFIC_TYPE_SIMPLE_METER)`: 0x1

        * `SPECIFIC_TYPE_ADV_ENERGY_CONTROL`:

            * `str(SPECIFIC_TYPE_ADV_ENERGY_CONTROL)`: Whole Home Energy Meter (Advanced)
            * `int(SPECIFIC_TYPE_ADV_ENERGY_CONTROL)`: 0x2

        * `SPECIFIC_TYPE_WHOLE_HOME_METER_SIMPLE`:

            * `str(SPECIFIC_TYPE_WHOLE_HOME_METER_SIMPLE)`: Whole Home Meter (Simple)
            * `int(SPECIFIC_TYPE_WHOLE_HOME_METER_SIMPLE)`: 0x3




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_ENTRY_CONTROL

    * `str(GENERIC_TYPE_ENTRY_CONTROL)`: Entry Control
    * `int(GENERIC_TYPE_ENTRY_CONTROL)`: 0x40
    * Specific Types:

        * `SPECIFIC_TYPE_DOOR_LOCK`:

            * `str(SPECIFIC_TYPE_DOOR_LOCK)`: Door Lock
            * `int(SPECIFIC_TYPE_DOOR_LOCK)`: 0x1

        * `SPECIFIC_TYPE_ADVANCED_DOOR_LOCK`:

            * `str(SPECIFIC_TYPE_ADVANCED_DOOR_LOCK)`: Advanced Door Lock
            * `int(SPECIFIC_TYPE_ADVANCED_DOOR_LOCK)`: 0x2

        * `SPECIFIC_TYPE_SECURE_KEYPAD_DOOR_LOCK`:

            * `str(SPECIFIC_TYPE_SECURE_KEYPAD_DOOR_LOCK)`: Door Lock (keypad lever)
            * `int(SPECIFIC_TYPE_SECURE_KEYPAD_DOOR_LOCK)`: 0x3

        * `SPECIFIC_TYPE_SECURE_KEYPAD_DOOR_LOCK_DEADBOLT`:

            * `str(SPECIFIC_TYPE_SECURE_KEYPAD_DOOR_LOCK_DEADBOLT)`: Door Lock (keypad deadbolt)
            * `int(SPECIFIC_TYPE_SECURE_KEYPAD_DOOR_LOCK_DEADBOLT)`: 0x4

        * `SPECIFIC_TYPE_SECURE_DOOR`:

            * `str(SPECIFIC_TYPE_SECURE_DOOR)`: Secure Door
            * `int(SPECIFIC_TYPE_SECURE_DOOR)`: 0x5

        * `SPECIFIC_TYPE_SECURE_GATE`:

            * `str(SPECIFIC_TYPE_SECURE_GATE)`: Secure Gate
            * `int(SPECIFIC_TYPE_SECURE_GATE)`: 0x6

        * `SPECIFIC_TYPE_SECURE_BARRIER_ADDON`:

            * `str(SPECIFIC_TYPE_SECURE_BARRIER_ADDON)`: Barrier Addon
            * `int(SPECIFIC_TYPE_SECURE_BARRIER_ADDON)`: 0x7

        * `SPECIFIC_TYPE_SECURE_BARRIER_OPEN_ONLY`:

            * `str(SPECIFIC_TYPE_SECURE_BARRIER_OPEN_ONLY)`: Barrier Open Only
            * `int(SPECIFIC_TYPE_SECURE_BARRIER_OPEN_ONLY)`: 0x8

        * `SPECIFIC_TYPE_SECURE_BARRIER_CLOSE_ONLY`:

            * `str(SPECIFIC_TYPE_SECURE_BARRIER_CLOSE_ONLY)`: Barrier Close Only
            * `int(SPECIFIC_TYPE_SECURE_BARRIER_CLOSE_ONLY)`: 0x9

        * `SPECIFIC_TYPE_SECURE_LOCKBOX`:

            * `str(SPECIFIC_TYPE_SECURE_LOCKBOX)`: Lock Box
            * `int(SPECIFIC_TYPE_SECURE_LOCKBOX)`: 0xA

        * `SPECIFIC_TYPE_SECURE_KEYPAD`:

            * `str(SPECIFIC_TYPE_SECURE_KEYPAD)`: Keypad
            * `int(SPECIFIC_TYPE_SECURE_KEYPAD)`: 0xB




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_SEMI_INTEROPERABLE

    * `str(GENERIC_TYPE_SEMI_INTEROPERABLE)`: Semi Interoperable
    * `int(GENERIC_TYPE_SEMI_INTEROPERABLE)`: 0x50
    * Specific Types:

        * `SPECIFIC_TYPE_ENERGY_PRODUCTION`:

            * `str(SPECIFIC_TYPE_ENERGY_PRODUCTION)`: Energy Production
            * `int(SPECIFIC_TYPE_ENERGY_PRODUCTION)`: 0x1




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_SENSOR_ALARM

    * `str(GENERIC_TYPE_SENSOR_ALARM)`: Sensor Alarm
    * `int(GENERIC_TYPE_SENSOR_ALARM)`: 0xA1
    * Specific Types:

        * `SPECIFIC_TYPE_ADV_ZENSOR_NET_ALARM_SENSOR`:

            * `str(SPECIFIC_TYPE_ADV_ZENSOR_NET_ALARM_SENSOR)`: Zensor Net Alarm (advanced) Sensor
            * `int(SPECIFIC_TYPE_ADV_ZENSOR_NET_ALARM_SENSOR)`: 0x5

        * `SPECIFIC_TYPE_ADV_ZENSOR_NET_SMOKE_SENSOR`:

            * `str(SPECIFIC_TYPE_ADV_ZENSOR_NET_SMOKE_SENSOR)`: Zensor Net Smoke (advanced) Sensor
            * `int(SPECIFIC_TYPE_ADV_ZENSOR_NET_SMOKE_SENSOR)`: 0xA

        * `SPECIFIC_TYPE_BASIC_ROUTING_ALARM_SENSOR`:

            * `str(SPECIFIC_TYPE_BASIC_ROUTING_ALARM_SENSOR)`: Routing Alarm (basic) Sensor
            * `int(SPECIFIC_TYPE_BASIC_ROUTING_ALARM_SENSOR)`: 0x1

        * `SPECIFIC_TYPE_BASIC_ROUTING_SMOKE_SENSOR`:

            * `str(SPECIFIC_TYPE_BASIC_ROUTING_SMOKE_SENSOR)`: Routing Smoke (basic) Sensor
            * `int(SPECIFIC_TYPE_BASIC_ROUTING_SMOKE_SENSOR)`: 0x6

        * `SPECIFIC_TYPE_BASIC_ZENSOR_NET_ALARM_SENSOR`:

            * `str(SPECIFIC_TYPE_BASIC_ZENSOR_NET_ALARM_SENSOR)`: Zensor Net Alarm (basic) Sensor
            * `int(SPECIFIC_TYPE_BASIC_ZENSOR_NET_ALARM_SENSOR)`: 0x3

        * `SPECIFIC_TYPE_BASIC_ZENSOR_NET_SMOKE_SENSOR`:

            * `str(SPECIFIC_TYPE_BASIC_ZENSOR_NET_SMOKE_SENSOR)`: Zensor Net Smoke (basic) Sensor
            * `int(SPECIFIC_TYPE_BASIC_ZENSOR_NET_SMOKE_SENSOR)`: 0x8

        * `SPECIFIC_TYPE_ROUTING_ALARM_SENSOR`:

            * `str(SPECIFIC_TYPE_ROUTING_ALARM_SENSOR)`: Routing Alarm Sensor
            * `int(SPECIFIC_TYPE_ROUTING_ALARM_SENSOR)`: 0x2

        * `SPECIFIC_TYPE_ROUTING_SMOKE_SENSOR`:

            * `str(SPECIFIC_TYPE_ROUTING_SMOKE_SENSOR)`: Routing Smoke Sensor
            * `int(SPECIFIC_TYPE_ROUTING_SMOKE_SENSOR)`: 0x7

        * `SPECIFIC_TYPE_ZENSOR_NET_ALARM_SENSOR`:

            * `str(SPECIFIC_TYPE_ZENSOR_NET_ALARM_SENSOR)`: Zensor Net Alarm Sensor
            * `int(SPECIFIC_TYPE_ZENSOR_NET_ALARM_SENSOR)`: 0x4

        * `SPECIFIC_TYPE_ZENSOR_NET_SMOKE_SENSOR`:

            * `str(SPECIFIC_TYPE_ZENSOR_NET_SMOKE_SENSOR)`: Zensor Net Smoke Sensor
            * `int(SPECIFIC_TYPE_ZENSOR_NET_SMOKE_SENSOR)`: 0x9

        * `SPECIFIC_TYPE_ALARM_SENSOR`:

            * `str(SPECIFIC_TYPE_ALARM_SENSOR)`: Sensor (Alarm)
            * `int(SPECIFIC_TYPE_ALARM_SENSOR)`: 0xB




.. py:data:: libopenzwave.node_types.GENERIC_TYPE_NON_INTEROPERABLE

    * `str(GENERIC_TYPE_NON_INTEROPERABLE)`: Non interoperable
    * `int(GENERIC_TYPE_NON_INTEROPERABLE)`: 0xFF
    * Specific Types: `None`




----------
Role Types
----------

.. py:data:: libopenzwave.node_types.DEVICE_TYPE_UNKNOWN

    * `str(DEVICE_TYPE_UNKNOWN)`: Role Type Unknown
    * `int(DEVICE_TYPE_UNKNOWN)`: -1


.. py:data:: libopenzwave.node_types.ROLE_TYPE_CONTROLLER_CENTRAL_STATIC

    * `str(ROLE_TYPE_CONTROLLER_CENTRAL_STATIC)`: Central Static Controller (CSC)
    * `int(ROLE_TYPE_CONTROLLER_CENTRAL_STATIC)`: 0x0


.. py:data:: libopenzwave.node_types.SPECIFIC_TYPE_SOUND_SWITCH

    * `str(SPECIFIC_TYPE_SOUND_SWITCH)`: Sub Static Controller (SSC)
    * `int(SPECIFIC_TYPE_SOUND_SWITCH)`: 0x1


.. py:data:: libopenzwave.node_types.SPECIFIC_TYPE_ADVANCED_DOOR_LOCK

    * `str(SPECIFIC_TYPE_ADVANCED_DOOR_LOCK)`: Portable Controller (PC)
    * `int(SPECIFIC_TYPE_ADVANCED_DOOR_LOCK)`: 0x2


.. py:data:: libopenzwave.node_types.GENERIC_TYPE_AV_CONTROL_POINT

    * `str(GENERIC_TYPE_AV_CONTROL_POINT)`: Reporting Portable Controller (RPC)
    * `int(GENERIC_TYPE_AV_CONTROL_POINT)`: 0x3


.. py:data:: libopenzwave.node_types.SPECIFIC_TYPE_SATELLITE_RECEIVER

    * `str(SPECIFIC_TYPE_SATELLITE_RECEIVER)`: Portable Slave (PS)
    * `int(SPECIFIC_TYPE_SATELLITE_RECEIVER)`: 0x4


.. py:data:: libopenzwave.node_types.SPECIFIC_TYPE_SECURE_DOOR

    * `str(SPECIFIC_TYPE_SECURE_DOOR)`: Always On Slave (AOS)
    * `int(SPECIFIC_TYPE_SECURE_DOOR)`: 0x5


.. py:data:: libopenzwave.node_types.SPECIFIC_TYPE_SECURE_GATE

    * `str(SPECIFIC_TYPE_SECURE_GATE)`: Reporting Sleeping Slave (RSS)
    * `int(SPECIFIC_TYPE_SECURE_GATE)`: 0x6


.. py:data:: libopenzwave.node_types.SPECIFIC_TYPE_SECURE_BARRIER_ADDON

    * `str(SPECIFIC_TYPE_SECURE_BARRIER_ADDON)`: Listening Sleeping Slave (LSS)
    * `int(SPECIFIC_TYPE_SECURE_BARRIER_ADDON)`: 0x7


.. py:data:: libopenzwave.node_types.SPECIFIC_TYPE_SECURE_BARRIER_OPEN_ONLY

    * `str(SPECIFIC_TYPE_SECURE_BARRIER_OPEN_ONLY)`: Network Aware Slave (NAS)
    * `int(SPECIFIC_TYPE_SECURE_BARRIER_OPEN_ONLY)`: 0x8




------------
Device Types
------------

.. py:data:: libopenzwave.node_types.DEVICE_TYPE_UNKNOWN

    * `str(DEVICE_TYPE_UNKNOWN)`: Type Unknown
    * `int(DEVICE_TYPE_UNKNOWN)`: -1


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_CENTRAL_CONTROLLER

    * `str(DEVICE_TYPE_CENTRAL_CONTROLLER)`: Central Controller
    * `int(DEVICE_TYPE_CENTRAL_CONTROLLER)`: 0x100


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_DISPLAY_SIMPLE

    * `str(DEVICE_TYPE_DISPLAY_SIMPLE)`: Display (simple)
    * `int(DEVICE_TYPE_DISPLAY_SIMPLE)`: 0x200


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_DOOR_LOCK_KEYPAD

    * `str(DEVICE_TYPE_DOOR_LOCK_KEYPAD)`: Door Lock Keypad
    * `int(DEVICE_TYPE_DOOR_LOCK_KEYPAD)`: 0x300


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SWITCH_FAN

    * `str(DEVICE_TYPE_SWITCH_FAN)`: Fan Switch
    * `int(DEVICE_TYPE_SWITCH_FAN)`: 0x400


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_GATEWAY

    * `str(DEVICE_TYPE_GATEWAY)`: Gateway
    * `int(DEVICE_TYPE_GATEWAY)`: 0x500


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SWITCH_MULTILEVEL

    * `str(DEVICE_TYPE_SWITCH_MULTILEVEL)`: Light Dimmer Switch
    * `int(DEVICE_TYPE_SWITCH_MULTILEVEL)`: 0x600


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SWITCH_BINARY

    * `str(DEVICE_TYPE_SWITCH_BINARY)`: On/Off Power Switch
    * `int(DEVICE_TYPE_SWITCH_BINARY)`: 0x700


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_POWER_STRIP

    * `str(DEVICE_TYPE_POWER_STRIP)`: Power Strip
    * `int(DEVICE_TYPE_POWER_STRIP)`: 0x800


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_REMOTE_CONTROL_AV

    * `str(DEVICE_TYPE_REMOTE_CONTROL_AV)`: Remote Control (AV)
    * `int(DEVICE_TYPE_REMOTE_CONTROL_AV)`: 0x900


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_REMOTE_CONTROL_MULTI_PURPOSE

    * `str(DEVICE_TYPE_REMOTE_CONTROL_MULTI_PURPOSE)`: Remote Control (multi purpose)
    * `int(DEVICE_TYPE_REMOTE_CONTROL_MULTI_PURPOSE)`: 0xA00


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_REMOTE_CONTROL_SIMPLE

    * `str(DEVICE_TYPE_REMOTE_CONTROL_SIMPLE)`: Remote Control (simple)
    * `int(DEVICE_TYPE_REMOTE_CONTROL_SIMPLE)`: 0xB00


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_KEY_FOB

    * `str(DEVICE_TYPE_KEY_FOB)`: Key Fob
    * `int(DEVICE_TYPE_KEY_FOB)`: 0xB01


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_NOTIFICATION

    * `str(DEVICE_TYPE_SENSOR_NOTIFICATION)`: Sensor (notification)
    * `int(DEVICE_TYPE_SENSOR_NOTIFICATION)`: 0xC00


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_SMOKE_ALARM

    * `str(DEVICE_TYPE_SENSOR_SMOKE_ALARM)`: Sensor (smoke alarm)
    * `int(DEVICE_TYPE_SENSOR_SMOKE_ALARM)`: 0xC01


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_CO_ALARM

    * `str(DEVICE_TYPE_SENSOR_CO_ALARM)`: Sensor (CO)
    * `int(DEVICE_TYPE_SENSOR_CO_ALARM)`: 0xC02


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_CO2_ALARM

    * `str(DEVICE_TYPE_SENSOR_CO2_ALARM)`: Sensor (CO2)
    * `int(DEVICE_TYPE_SENSOR_CO2_ALARM)`: 0xC03


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_HEAT_ALARM

    * `str(DEVICE_TYPE_SENSOR_HEAT_ALARM)`: Sensor (heat)
    * `int(DEVICE_TYPE_SENSOR_HEAT_ALARM)`: 0xC04


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_WATER_ALARM

    * `str(DEVICE_TYPE_SENSOR_WATER_ALARM)`: Sensor (water)
    * `int(DEVICE_TYPE_SENSOR_WATER_ALARM)`: 0xC05


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_ACCESS_CONTROL

    * `str(DEVICE_TYPE_SENSOR_ACCESS_CONTROL)`: Sensor (access control)
    * `int(DEVICE_TYPE_SENSOR_ACCESS_CONTROL)`: 0xC06


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_HOME_SECURITY

    * `str(DEVICE_TYPE_SENSOR_HOME_SECURITY)`: Sensor (security)
    * `int(DEVICE_TYPE_SENSOR_HOME_SECURITY)`: 0xC07


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_POWER_MANAGEMENT

    * `str(DEVICE_TYPE_SENSOR_POWER_MANAGEMENT)`: Sensor (power management)
    * `int(DEVICE_TYPE_SENSOR_POWER_MANAGEMENT)`: 0xC08


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_SYSTEM

    * `str(DEVICE_TYPE_SENSOR_SYSTEM)`: Sensor (system)
    * `int(DEVICE_TYPE_SENSOR_SYSTEM)`: 0xC09


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_EMERGENCY_ALARM

    * `str(DEVICE_TYPE_SENSOR_EMERGENCY_ALARM)`: Sensor (emergency)
    * `int(DEVICE_TYPE_SENSOR_EMERGENCY_ALARM)`: 0xC0A


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_CLOCK

    * `str(DEVICE_TYPE_SENSOR_CLOCK)`: Sensor (clock)
    * `int(DEVICE_TYPE_SENSOR_CLOCK)`: 0xC0B


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_MULTIDEVICE_1

    * `str(DEVICE_TYPE_SENSOR_MULTIDEVICE_1)`: Sensor (multi device 1)
    * `int(DEVICE_TYPE_SENSOR_MULTIDEVICE_1)`: 0xCFF


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_MULTILEVEL

    * `str(DEVICE_TYPE_SENSOR_MULTILEVEL)`: Sensor (multi level)
    * `int(DEVICE_TYPE_SENSOR_MULTILEVEL)`: 0xD00


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_AIR_TEMPERATURE

    * `str(DEVICE_TYPE_SENSOR_AIR_TEMPERATURE)`: Sensor (air)
    * `int(DEVICE_TYPE_SENSOR_AIR_TEMPERATURE)`: 0xD01


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_GENERAL_PURPOSE

    * `str(DEVICE_TYPE_SENSOR_GENERAL_PURPOSE)`: Sensor (general)
    * `int(DEVICE_TYPE_SENSOR_GENERAL_PURPOSE)`: 0xD02


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_LUMINANCE

    * `str(DEVICE_TYPE_SENSOR_LUMINANCE)`: Sensor (luminance)
    * `int(DEVICE_TYPE_SENSOR_LUMINANCE)`: 0xD03


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_POWER

    * `str(DEVICE_TYPE_SENSOR_POWER)`: Sensor (power)
    * `int(DEVICE_TYPE_SENSOR_POWER)`: 0xD04


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_HUMIDITY

    * `str(DEVICE_TYPE_SENSOR_HUMIDITY)`: Sensor (humidity)
    * `int(DEVICE_TYPE_SENSOR_HUMIDITY)`: 0xD05


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_VELOCITY

    * `str(DEVICE_TYPE_SENSOR_VELOCITY)`: Sensor (velocity)
    * `int(DEVICE_TYPE_SENSOR_VELOCITY)`: 0xD06


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_DIRECTION

    * `str(DEVICE_TYPE_SENSOR_DIRECTION)`: Sensor (direction)
    * `int(DEVICE_TYPE_SENSOR_DIRECTION)`: 0xD07


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_ATMOSPHERIC_PRESSURE

    * `str(DEVICE_TYPE_SENSOR_ATMOSPHERIC_PRESSURE)`: Sensor (atmospheric pressure)
    * `int(DEVICE_TYPE_SENSOR_ATMOSPHERIC_PRESSURE)`: 0xD08


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_BAROMETRIC_PRESSURE

    * `str(DEVICE_TYPE_SENSOR_BAROMETRIC_PRESSURE)`: Sensor (barometric pressure)
    * `int(DEVICE_TYPE_SENSOR_BAROMETRIC_PRESSURE)`: 0xD09


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_SOLAR_RADIATION

    * `str(DEVICE_TYPE_SENSOR_SOLAR_RADIATION)`: Sensor (solar radiation)
    * `int(DEVICE_TYPE_SENSOR_SOLAR_RADIATION)`: 0xD0A


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_DEW_POINT

    * `str(DEVICE_TYPE_SENSOR_DEW_POINT)`: Sensor (dew point)
    * `int(DEVICE_TYPE_SENSOR_DEW_POINT)`: 0xD0B


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_RAIN_RATE

    * `str(DEVICE_TYPE_SENSOR_RAIN_RATE)`: Sensor (rain rate)
    * `int(DEVICE_TYPE_SENSOR_RAIN_RATE)`: 0xD0C


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_TIDE_LEVEL

    * `str(DEVICE_TYPE_SENSOR_TIDE_LEVEL)`: Sensor (tide level)
    * `int(DEVICE_TYPE_SENSOR_TIDE_LEVEL)`: 0xD0D


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_WEIGHT

    * `str(DEVICE_TYPE_SENSOR_WEIGHT)`: Sensor (weight)
    * `int(DEVICE_TYPE_SENSOR_WEIGHT)`: 0xD0E


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_VOLTAGE

    * `str(DEVICE_TYPE_SENSOR_VOLTAGE)`: Sensor (voltage)
    * `int(DEVICE_TYPE_SENSOR_VOLTAGE)`: 0xD0F


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_CURRENT

    * `str(DEVICE_TYPE_SENSOR_CURRENT)`: Sensor (current)
    * `int(DEVICE_TYPE_SENSOR_CURRENT)`: 0xD10


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_CO2_LEVEL

    * `str(DEVICE_TYPE_SENSOR_CO2_LEVEL)`: Sensor (CO2 level)
    * `int(DEVICE_TYPE_SENSOR_CO2_LEVEL)`: 0xD11


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_AIR_FLOW

    * `str(DEVICE_TYPE_SENSOR_AIR_FLOW)`: Sensor (air flow)
    * `int(DEVICE_TYPE_SENSOR_AIR_FLOW)`: 0xD12


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_TANK_CAPACITY

    * `str(DEVICE_TYPE_SENSOR_TANK_CAPACITY)`: Sensor (tank capacity)
    * `int(DEVICE_TYPE_SENSOR_TANK_CAPACITY)`: 0xD13


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_DISTANCE

    * `str(DEVICE_TYPE_SENSOR_DISTANCE)`: Sensor (distance)
    * `int(DEVICE_TYPE_SENSOR_DISTANCE)`: 0xD14


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_ANGLE_POSTITION

    * `str(DEVICE_TYPE_SENSOR_ANGLE_POSTITION)`: Sensor (angle position)
    * `int(DEVICE_TYPE_SENSOR_ANGLE_POSTITION)`: 0xD15


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_ROTATION

    * `str(DEVICE_TYPE_SENSOR_ROTATION)`: Sensor (rotation)
    * `int(DEVICE_TYPE_SENSOR_ROTATION)`: 0xD16


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_WATER_TEMPERATURE

    * `str(DEVICE_TYPE_SENSOR_WATER_TEMPERATURE)`: Sensor (H2O temperature)
    * `int(DEVICE_TYPE_SENSOR_WATER_TEMPERATURE)`: 0xD17


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_SOIL_TEMPERATURE

    * `str(DEVICE_TYPE_SENSOR_SOIL_TEMPERATURE)`: Sensor (soil temperature)
    * `int(DEVICE_TYPE_SENSOR_SOIL_TEMPERATURE)`: 0xD18


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_SEISMIC_INTENSITY

    * `str(DEVICE_TYPE_SENSOR_SEISMIC_INTENSITY)`: Sensor (seismic intensity)
    * `int(DEVICE_TYPE_SENSOR_SEISMIC_INTENSITY)`: 0xD19


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_SEISMIC_MAGNITUDE

    * `str(DEVICE_TYPE_SENSOR_SEISMIC_MAGNITUDE)`: Sensor (seismic magnatitude)
    * `int(DEVICE_TYPE_SENSOR_SEISMIC_MAGNITUDE)`: 0xD1A


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_ULTRAVIOLET

    * `str(DEVICE_TYPE_SENSOR_ULTRAVIOLET)`: Sensor (ultraviolet)
    * `int(DEVICE_TYPE_SENSOR_ULTRAVIOLET)`: 0xD1B


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_ELECTRICAL_RESISTIVITY

    * `str(DEVICE_TYPE_SENSOR_ELECTRICAL_RESISTIVITY)`: Sensor (electrical resistivity)
    * `int(DEVICE_TYPE_SENSOR_ELECTRICAL_RESISTIVITY)`: 0xD1C


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_ELECTRICAL_CONDUCTIVITY

    * `str(DEVICE_TYPE_SENSOR_ELECTRICAL_CONDUCTIVITY)`: Sensor (electrical conductivity)
    * `int(DEVICE_TYPE_SENSOR_ELECTRICAL_CONDUCTIVITY)`: 0xB1D


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_LOUDNESS

    * `str(DEVICE_TYPE_SENSOR_LOUDNESS)`: Sensor (loudness)
    * `int(DEVICE_TYPE_SENSOR_LOUDNESS)`: 0xB1E


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_MOISTURE

    * `str(DEVICE_TYPE_SENSOR_MOISTURE)`: Sensor (moisture)
    * `int(DEVICE_TYPE_SENSOR_MOISTURE)`: 0xB1F


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_FREQUENCY

    * `str(DEVICE_TYPE_SENSOR_FREQUENCY)`: Sensor (frequency)
    * `int(DEVICE_TYPE_SENSOR_FREQUENCY)`: 0xB20


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_TIME

    * `str(DEVICE_TYPE_SENSOR_TIME)`: Sensor (time)
    * `int(DEVICE_TYPE_SENSOR_TIME)`: 0xB21


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_TARGET_TEMPERATURE

    * `str(DEVICE_TYPE_SENSOR_TARGET_TEMPERATURE)`: Sensot (target temperature)
    * `int(DEVICE_TYPE_SENSOR_TARGET_TEMPERATURE)`: 0xB22


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SENSOR_MULTIDEVICE_2

    * `str(DEVICE_TYPE_SENSOR_MULTIDEVICE_2)`: Sensor (multi device 2)
    * `int(DEVICE_TYPE_SENSOR_MULTIDEVICE_2)`: 0xBFF


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SET_TOP_BOX

    * `str(DEVICE_TYPE_SET_TOP_BOX)`: Set Top Box
    * `int(DEVICE_TYPE_SET_TOP_BOX)`: 0xE00


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SIREN

    * `str(DEVICE_TYPE_SIREN)`: Siren
    * `int(DEVICE_TYPE_SIREN)`: 0xF00


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SUB_ENERGY_METER

    * `str(DEVICE_TYPE_SUB_ENERGY_METER)`: Sub Energy Meter
    * `int(DEVICE_TYPE_SUB_ENERGY_METER)`: 0x1000


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_SUB_SYSTEM_CONTROLLER

    * `str(DEVICE_TYPE_SUB_SYSTEM_CONTROLLER)`: Sub System Controller
    * `int(DEVICE_TYPE_SUB_SYSTEM_CONTROLLER)`: 0x1100


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_THERMOSTAT_HVAC

    * `str(DEVICE_TYPE_THERMOSTAT_HVAC)`: Thermostat HVAC
    * `int(DEVICE_TYPE_THERMOSTAT_HVAC)`: 0x1200


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_THERMOSTAT_SETBACK

    * `str(DEVICE_TYPE_THERMOSTAT_SETBACK)`: Thermostat Setback
    * `int(DEVICE_TYPE_THERMOSTAT_SETBACK)`: 0x1300


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_TV

    * `str(DEVICE_TYPE_TV)`: TV
    * `int(DEVICE_TYPE_TV)`: 0x1400


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_VALVE_OPEN_CLOSE

    * `str(DEVICE_TYPE_VALVE_OPEN_CLOSE)`: Valve (open/close)
    * `int(DEVICE_TYPE_VALVE_OPEN_CLOSE)`: 0x1500


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_WALL_CONTROLLER

    * `str(DEVICE_TYPE_WALL_CONTROLLER)`: Wall Controller
    * `int(DEVICE_TYPE_WALL_CONTROLLER)`: 0x1600


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_WHOLE_HOME_METER_SIMPLE

    * `str(DEVICE_TYPE_WHOLE_HOME_METER_SIMPLE)`: Whole Home Meter (simple)
    * `int(DEVICE_TYPE_WHOLE_HOME_METER_SIMPLE)`: 0x1700


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_WINDOW_COVERING_NO_POSITION_ENDPOINT

    * `str(DEVICE_TYPE_WINDOW_COVERING_NO_POSITION_ENDPOINT)`: Window Covering (no position endpoint)
    * `int(DEVICE_TYPE_WINDOW_COVERING_NO_POSITION_ENDPOINT)`: 0x1800


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_WINDOW_COVERING_ENDPOINT_AWARE

    * `str(DEVICE_TYPE_WINDOW_COVERING_ENDPOINT_AWARE)`: Window Covering (endpoint aware)
    * `int(DEVICE_TYPE_WINDOW_COVERING_ENDPOINT_AWARE)`: 0x1900


.. py:data:: libopenzwave.node_types.DEVICE_TYPE_WINDOW_COVERING_POSITION_ENDPOINT_AWARE

    * `str(DEVICE_TYPE_WINDOW_COVERING_POSITION_ENDPOINT_AWARE)`: Window Covering (position endpoint aware)
    * `int(DEVICE_TYPE_WINDOW_COVERING_POSITION_ENDPOINT_AWARE)`: 0x1A00




----------
Node Types
----------

.. py:data:: libopenzwave.node_types.ROLE_TYPE_UNKNOWN

    * `str(ROLE_TYPE_UNKNOWN)`: Node Type Unknown
    * `int(ROLE_TYPE_UNKNOWN)`: -1


.. py:data:: libopenzwave.node_types.ROLE_TYPE_CONTROLLER_CENTRAL_STATIC

    * `str(ROLE_TYPE_CONTROLLER_CENTRAL_STATIC)`: Z-Wave+ Node
    * `int(ROLE_TYPE_CONTROLLER_CENTRAL_STATIC)`: 0x0


.. py:data:: libopenzwave.node_types.ROLE_TYPE_CONTROLLER_SUB_STATIC

    * `str(ROLE_TYPE_CONTROLLER_SUB_STATIC)`: Z-Wave+ IP Router
    * `int(ROLE_TYPE_CONTROLLER_SUB_STATIC)`: 0x1


.. py:data:: libopenzwave.node_types.ROLE_TYPE_CONTROLLER_PORTABLE

    * `str(ROLE_TYPE_CONTROLLER_PORTABLE)`: Z-Wave+ IP Gateway
    * `int(ROLE_TYPE_CONTROLLER_PORTABLE)`: 0x2


.. py:data:: libopenzwave.node_types.ROLE_TYPE_CONTROLLER_PORTABLE_REPORTING

    * `str(ROLE_TYPE_CONTROLLER_PORTABLE_REPORTING)`: Z-Wave+ IP Client and IP Node
    * `int(ROLE_TYPE_CONTROLLER_PORTABLE_REPORTING)`: 0x3


.. py:data:: libopenzwave.node_types.ROLE_TYPE_SLAVE_PORTABLE

    * `str(ROLE_TYPE_SLAVE_PORTABLE)`: Z-Wave+ IP Client and Z-Wave Node
    * `int(ROLE_TYPE_SLAVE_PORTABLE)`: 0x4



