===========================
Command Class documentation
===========================

This is a new system that we developed. A node (device) on a network has
specific abilities. The abilities a node has is define by what command classes
the manufacturer has used in the software on the device. Each command class
allows for changes/operation of the device. Because ZWave supports so many
device types the devices themselves do not support all of the comand classes.

We do not want to provide controls for a device that is not able to support
that command set. So we dynamically build a representation of the node using
these command classes. Some of these command classes do not provide any
additional control, they are here for completeness as well as possible future
additions.

There are 2 ways to be able to change the various settings and to control a
device. These classes are one way, the other is by accessing the values
directly and making changes. These classes provide a mechanism that accesses
the values for you and makes the changes that are needed or returns the data.
Any alterations to the input data or output data that may need to be done is
handled already.

.. toctree::
    :maxdepth: 1

    COMMAND_CLASS_ALARM <alarm>
    COMMAND_CLASS_ANTITHEFT <antitheft>
    COMMAND_CLASS_APPLICATION_CAPABILITY <application_capability>
    COMMAND_CLASS_APPLICATION_STATUS <application_status>
    COMMAND_CLASS_ASSOCIATION <association>
    COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION <association_command_configuration>
    COMMAND_CLASS_ASSOCIATION_GRP_INFO <association_grp_info>
    COMMAND_CLASS_AUTHENTICATION <authentication>
    COMMAND_CLASS_AUTHENTICATION_MEDIA_WRITE <authentication_media_write>
    COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD <av_content_directory_md>
    COMMAND_CLASS_AV_CONTENT_SEARCH_MD <av_content_search_md>
    COMMAND_CLASS_AV_RENDERER_STATUS <av_renderer_status>
    COMMAND_CLASS_AV_TAGGING_MD <av_tagging_md>
    COMMAND_CLASS_BARRIER_OPERATOR <barrier_operator>
    COMMAND_CLASS_BASIC <basic>
    COMMAND_CLASS_BASIC_TARIFF_INFO <basic_tariff_info>
    COMMAND_CLASS_BASIC_WINDOW_COVERING <basic_window_covering>
    COMMAND_CLASS_BATTERY <battery>
    COMMAND_CLASS_CENTRAL_SCENE <central_scene>
    COMMAND_CLASS_CHIMNEY_FAN <chimney_fan>
    COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE <climate_control_schedule>
    COMMAND_CLASS_CLOCK <clock>
    COMMAND_CLASS_CONFIGURATION <configuration>
    COMMAND_CLASS_CONTROLLER_REPLICATION <controller_replication>
    COMMAND_CLASS_CRC_16_ENCAP <crc_16_encap>
    COMMAND_CLASS_DCP_CONFIG <dcp_config>
    COMMAND_CLASS_DCP_MONITOR <dcp_monitor>
    COMMAND_CLASS_DEVICE_RESET_LOCALLY <device_reset_locally>
    COMMAND_CLASS_DMX <dmx>
    COMMAND_CLASS_DOOR_LOCK <door_lock>
    COMMAND_CLASS_DOOR_LOCK_LOGGING <door_lock_logging>
    COMMAND_CLASS_ENERGY_PRODUCTION <energy_production>
    COMMAND_CLASS_ENTRY_CONTROL <entry_control>
    COMMAND_CLASS_FIRMWARE_UPDATE_MD <firmware_update_md>
    COMMAND_CLASS_GEOGRAPHIC_LOCATION <geographic_location>
    COMMAND_CLASS_GROUPING_NAME <grouping_name>
    COMMAND_CLASS_HAIL <hail>
    COMMAND_CLASS_HRV_CONTROL <hrv_control>
    COMMAND_CLASS_HRV_STATUS <hrv_status>
    COMMAND_CLASS_HUMIDITY_CONTROL_MODE <humidity_control_mode>
    COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE <humidity_control_operating_state>
    COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT <humidity_control_setpoint>
    COMMAND_CLASS_INCLUSION_CONTROLLER <inclusion_controller>
    COMMAND_CLASS_INDICATOR <indicator>
    COMMAND_CLASS_IP_ASSOCIATION <ip_association>
    COMMAND_CLASS_IP_CONFIGURATION <ip_configuration>
    COMMAND_CLASS_IR_REPEATER <irrigation>
    COMMAND_CLASS_IRRIGATION <ir_repeater>
    COMMAND_CLASS_LANGUAGE <language>
    COMMAND_CLASS_LOCK <lock>
    COMMAND_CLASS_MAILBOX <mailbox>
    COMMAND_CLASS_MANUFACTURER_PROPRIETARY <manufacturer_proprietary>
    COMMAND_CLASS_MANUFACTURER_SPECIFIC <manufacturer_specific>
    COMMAND_CLASS_MARK <mark>
    COMMAND_CLASS_METER <meter>
    COMMAND_CLASS_METER_PULSE <meter_pulse>
    COMMAND_CLASS_METER_TBL_CONFIG <meter_tbl_config>
    COMMAND_CLASS_METER_TBL_MONITOR <meter_tbl_monitor>
    COMMAND_CLASS_METER_TBL_PUSH <meter_tbl_push>
    COMMAND_CLASS_MTP_WINDOW_COVERING <mtp_window_covering>
    COMMAND_CLASS_MULTI_CHANNEL <multi_channel>
    COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION <multi_channel_association>
    COMMAND_CLASS_MULTI_CMD <multi_cmd>
    COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC <network_management_basic>
    COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION <network_management_inclusion>
    COMMAND_CLASS_NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE <network_management_installation_maintenance>
    COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY <network_management_primary>
    COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY <network_management_proxy>
    COMMAND_CLASS_NON_INTEROPERABLE <node_naming>
    COMMAND_CLASS_NO_OPERATION <node_provisioning>
    COMMAND_CLASS_NODE_NAMING <non_interoperable>
    COMMAND_CLASS_NODE_PROVISIONING <notification>
    COMMAND_CLASS_NOTIFICATION <no_operation>
    COMMAND_CLASS_POWERLEVEL <powerlevel>
    COMMAND_CLASS_PREPAYMENT <prepayment>
    COMMAND_CLASS_PREPAYMENT_ENCAPSULATION <prepayment_encapsulation>
    COMMAND_CLASS_PROTECTION <proprietary>
    COMMAND_CLASS_PROPRIETARY <protection>
    COMMAND_CLASS_RATE_TBL_CONFIG <rate_tbl_config>
    COMMAND_CLASS_RATE_TBL_MONITOR <rate_tbl_monitor>
    COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE <remote_association>
    COMMAND_CLASS_REMOTE_ASSOCIATION <remote_association_activate>
    COMMAND_CLASS_SCENE_ACTIVATION <scene_activation>
    COMMAND_CLASS_SCENE_ACTUATOR_CONF <scene_actuator_conf>
    COMMAND_CLASS_SCENE_CONTROLLER_CONF <scene_controller_conf>
    COMMAND_CLASS_SCHEDULE <schedule>
    COMMAND_CLASS_SCHEDULE_ENTRY_LOCK <schedule_entry_lock>
    COMMAND_CLASS_SCREEN_ATTRIBUTES <screen_attributes>
    COMMAND_CLASS_SCREEN_MD <screen_md>
    COMMAND_CLASS_SECURITY <security>
    COMMAND_CLASS_SECURITY_2 <security_2>
    COMMAND_CLASS_SECURITY_SCHEME0_MARK <security_panel_mode>
    COMMAND_CLASS_SECURITY_PANEL_MODE <security_panel_zone>
    COMMAND_CLASS_SECURITY_PANEL_ZONE <security_panel_zone_sensor>
    COMMAND_CLASS_SECURITY_PANEL_ZONE_SENSOR <security_scheme0_mark>
    COMMAND_CLASS_SENSOR_ALARM <sensor_alarm>
    COMMAND_CLASS_SENSOR_BINARY <sensor_binary>
    COMMAND_CLASS_SENSOR_CONFIGURATION <sensor_configuration>
    COMMAND_CLASS_SENSOR_MULTILEVEL <sensor_multilevel>
    COMMAND_CLASS_SILENCE_ALARM <silence_alarm>
    COMMAND_CLASS_SIMPLE_AV_CONTROL <simple_av_control>
    COMMAND_CLASS_SOUND_SWITCH <sound_switch>
    COMMAND_CLASS_SUPERVISION <supervision>
    COMMAND_CLASS_SWITCH_ALL <switch_all>
    COMMAND_CLASS_SWITCH_BINARY <switch_binary>
    COMMAND_CLASS_SWITCH_COLOR <switch_color>
    COMMAND_CLASS_SWITCH_MULTILEVEL <switch_multilevel>
    COMMAND_CLASS_SWITCH_TOGGLE_BINARY <switch_toggle_binary>
    COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL <switch_toggle_multilevel>
    COMMAND_CLASS_TARIFF_CONFIG <tariff_config>
    COMMAND_CLASS_TARIFF_TBL_MONITOR <tariff_tbl_monitor>
    COMMAND_CLASS_THERMOSTAT_FAN_MODE <thermostat_fan_mode>
    COMMAND_CLASS_THERMOSTAT_FAN_STATE <thermostat_fan_state>
    COMMAND_CLASS_THERMOSTAT_MODE <thermostat_mode>
    COMMAND_CLASS_THERMOSTAT_OPERATING_STATE <thermostat_operating_state>
    COMMAND_CLASS_THERMOSTAT_SETBACK <thermostat_setback>
    COMMAND_CLASS_THERMOSTAT_SETPOINT <thermostat_setpoint>
    COMMAND_CLASS_TIME <time>
    COMMAND_CLASS_TIME_PARAMETERS <time_parameters>
    COMMAND_CLASS_TRANSPORT_SERVICE <transport_service>
    COMMAND_CLASS_USER_CODE <user_code>
    COMMAND_CLASS_VERSION <version>
    COMMAND_CLASS_WAKE_UP <wake_up>
    COMMAND_CLASS_WINDOW_COVERING <window_covering>
    COMMAND_CLASS_ZENSOR_NET <zensor_net>
    COMMAND_CLASS_ZIP <zip>
    COMMAND_CLASS_ZIP_6LOWPAN <zip_6lowpan>
    COMMAND_CLASS_ZIP_GATEWAY <zip_gateway>
    COMMAND_CLASS_ZIP_NAMING <zip_naming>
    COMMAND_CLASS_ZIP_ND <zip_nd>
    COMMAND_CLASS_ZIP_PORTAL <zip_portal>
    ZWAVE_CMD_CLASS <zwave_cmd_class>
    COMMAND_CLASS_ZWAVEPLUS_INFO <zwave_plus_info>

.. automodule:: libopenzwave.command_classes
    :members:
    :show-inheritance:
