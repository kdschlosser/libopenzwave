# -*- coding: utf-8 -*-

# ****************** READ COMMENTS STARTING AT LINE 31 ************************

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
:synopsis: Test Script

.. moduleauthor:: Kevin G Schlosser
"""


# This is a simple test script. It is only designed to show you some of the
# changes made. and also how easy it is to now use the new system. There are
# some options to set so scroll down a but to set them. If you are using a
# new set of user config files the startup is going to be slower the first
# time around because the program has to populate all of the cached data to
# build the files. running the script more then a single time should be done.

# you need not worry about telling the program what serial port your ZStick
# is on. It does all of this automatically now.

import logging


# Set this variable to the user config folder. If you leave this blank it is
# going to make one for you
# Windows = programdata/.python-openzwave, others = ~/.python-openzwave
USER_CONFIG = r''

# set this to one of the following, setting this to DEBUG is going to slow
# down the program. This is because of the logging routine I wrote that
# prints out the filename and line number of where a function was called from
# and also where the function is located. It also times the execution time of
# the called function and displays any arguments passed as well as any
# return data.
# logging.NOTSET
# logging.DEBUG
# logging.INFO

# you optionally have these 3 to use as well and I think the names describe
# them pretty well.
# openzwave.LOGGING_DATA_PATH
# openzwave.LOGGING_DATA_PATH_WITH_RETURN
# openzwave.LOGGING_TIME_FUNCTION_CALLS
POZW_LOGGING = logging.NOTSET

# set this to either True or False
OZW_LOGGING = False


# This option changes the notification system to use a single thread to
# handle all notifications or to create a new thread for each node. Now I use
# that term create per node. and it does do this. But if there are no
# notifications being processed or queued to be processed the thread shuts
# down. when a notification comes in then a new thread gets created. This
# process gets done either way. This is going to give you an idea of the
# changes in performance from what it used to be and what it is now. It is
# not 100% because the whole system is designed to not stall OZW. so the
# difference you see using this is going to be 10 times more if it was the
# old way vs the new
SINGLE_NOTIFICATION_HANDLER = True

import sys
import os
import libopenzwave
import threading

if not USER_CONFIG:
    if sys.platform.startswith('win'):
        USER_CONFIG = os.path.join(os.path.expandvars('%programdata%'), '.python-openzwave')
    else:
        USER_CONFIG = os.path.join(os.path.expanduser('~'), '.python-openzwave')

    if not os.path.exists(USER_CONFIG):
        os.mkdir(USER_CONFIG)


libopenzwave.logger.setLevel(POZW_LOGGING)

option = libopenzwave.ZWaveOption(user_path=USER_CONFIG)
option.logging = OZW_LOGGING
option.console_output = OZW_LOGGING
option.single_notification_handler = SINGLE_NOTIFICATION_HANDLER
option.lock()

event = threading.Event()


def stop_callback(**__):
    print('******** FINISHED STOPPING NETWORK ********')
    event.set()


def ready_callback(**__):
    print('******** FINISHED LOADING NETWORK ********')
    print(
        'This is when the typical app will load the information that is '
        'needed.'
    )
    event.set()


def failed_callback(**__):
    print('******** NETWORK FAILED ********')
    event.set()


def node_cached_callback(sender, **__):
    print('------ NODE CACHED')
    print('NODE ID:', sender.id)
    print('NODE NAME:', sender.name)
    print('NODE LOCATION:', sender.location)
    print(
        'Run code to create an icon maybe with a banner indicating that '
        'the node is still loading.'
    )

    print('\n\n')


def value_cached_callback(val, nde, **__):
    print('------ VALUE CACHED')
    print('NODE ID:', nde.id)
    print('NODE NAME:', nde.name)
    print('VALUE ID:', val.id)
    print('VALUE INDEX:', val.index)
    print('VALUE LABEL:', val.label)
    print('VALUE_COMMAND CLASS:', val.command_class.class_desc)
    print(
        'Run code to create the GUI representation of the value '
        'with some kind of an identifier that any dynamic information is'
        'still loading.'
    )

    print('\n\n')


def node_ready_callback(sender, **__):
    print('------ NODE READY')
    print('NODE ID:', sender.id)
    print('NODE NAME:', sender.name)
    print('NODE LOCATION:', sender.location)
    print(
        'run code to update the GUI so that the user knows the node has '
        'been fully loaded.'
    )
    print('\n\n')


def value_ready_callback(nde, val, **__):
    print('------ VALUE READY')
    print('NODE ID:', nde.id)
    print('NODE NAME:', nde.name)
    print('VALUE INDEX:', val.index)
    print('VALUE LABEL:', val.label)
    print('VALUE_COMMAND CLASS:', val.command_class.class_desc)
    print(
        'run code to update the GUI so that the user knows the value has '
        'been fully loaded.'
    )

    print('\n\n')


def value_changed_callback(nde, val, val_data, **__):
    print('------ VALUE CHANGED')
    print('NODE ID:', nde.id)
    print('NODE NAME:', nde.name)
    print('VALUE INDEX:', val.index)
    print('VALUE LABEL:', val.label)
    print('VALUE COMMAND CLASS:', val.command_class.class_desc)
    print('VALUE DATA (caused signal):', val_data.data)
    print('VALUE DATA (from value):', val.data)
    print(
        'You may or may not see a difference in the value data. '
        'You will always want to use value_data.data to get the data that '
        'is associated with the signal.'
    )

    print('\n\n')


libopenzwave.SIGNAL_NODE_READY.register(node_ready_callback)
libopenzwave.SIGNAL_VALUE_READY.register(value_ready_callback)

# comment the next line to import startup performance. This causes a heap of
# extra network activity because of using value.data in the callback.
# It does this for every single value for every single node on the network
libopenzwave.SIGNAL_VALUE_CHANGED.register(value_changed_callback)

libopenzwave.SIGNAL_NODE_DATASET_LOADED.register(node_cached_callback)
libopenzwave.SIGNAL_VALUE_DATASET_LOADED.register(value_cached_callback)
libopenzwave.SIGNAL_NETWORK_READY.register(ready_callback)
libopenzwave.SIGNAL_NETWORK_FAILED.register(failed_callback)
libopenzwave.SIGNAL_NETWORK_STOPPED.register(stop_callback)

network = libopenzwave.ZWaveNetwork(option)

event.wait()


from libopenzwave.command_classes import(
    COMMAND_CLASS_ALARM,
    COMMAND_CLASS_ANTITHEFT,
    COMMAND_CLASS_APPLICATION_CAPABILITY,
    COMMAND_CLASS_APPLICATION_STATUS,
    COMMAND_CLASS_ASSOCIATION,
    COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION,
    COMMAND_CLASS_ASSOCIATION_GRP_INFO,
    COMMAND_CLASS_AUTHENTICATION,
    COMMAND_CLASS_AUTHENTICATION_MEDIA_WRITE,
    COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD,
    COMMAND_CLASS_AV_CONTENT_SEARCH_MD,
    COMMAND_CLASS_AV_RENDERER_STATUS,
    COMMAND_CLASS_AV_TAGGING_MD,
    COMMAND_CLASS_BARRIER_OPERATOR,
    COMMAND_CLASS_BASIC,
    COMMAND_CLASS_BASIC_TARIFF_INFO,
    COMMAND_CLASS_BASIC_WINDOW_COVERING,
    COMMAND_CLASS_BATTERY,
    COMMAND_CLASS_CENTRAL_SCENE,
    COMMAND_CLASS_CHIMNEY_FAN,
    COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE,
    COMMAND_CLASS_CLOCK,
    COMMAND_CLASS_CONFIGURATION,
    COMMAND_CLASS_CONTROLLER_REPLICATION,
    COMMAND_CLASS_CRC_16_ENCAP,
    COMMAND_CLASS_DCP_CONFIG,
    COMMAND_CLASS_DCP_MONITOR,
    COMMAND_CLASS_DEVICE_RESET_LOCALLY,
    COMMAND_CLASS_DMX,
    COMMAND_CLASS_DOOR_LOCK,
    COMMAND_CLASS_DOOR_LOCK_LOGGING,
    COMMAND_CLASS_ENERGY_PRODUCTION,
    COMMAND_CLASS_ENTRY_CONTROL,
    COMMAND_CLASS_FIRMWARE_UPDATE_MD,
    COMMAND_CLASS_GEOGRAPHIC_LOCATION,
    COMMAND_CLASS_GROUPING_NAME,
    COMMAND_CLASS_HAIL,
    COMMAND_CLASS_HRV_CONTROL,
    COMMAND_CLASS_HRV_STATUS,
    COMMAND_CLASS_HUMIDITY_CONTROL_MODE,
    COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE,
    COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT,
    COMMAND_CLASS_INCLUSION_CONTROLLER,
    COMMAND_CLASS_INDICATOR,
    COMMAND_CLASS_IP_ASSOCIATION,
    COMMAND_CLASS_IP_CONFIGURATION,
    COMMAND_CLASS_IR_REPEATER,
    COMMAND_CLASS_IRRIGATION,
    COMMAND_CLASS_LANGUAGE,
    COMMAND_CLASS_LOCK,
    COMMAND_CLASS_MAILBOX,
    COMMAND_CLASS_MANUFACTURER_PROPRIETARY,
    COMMAND_CLASS_MANUFACTURER_SPECIFIC,
    COMMAND_CLASS_MARK,
    COMMAND_CLASS_METER,
    COMMAND_CLASS_METER_PULSE,
    COMMAND_CLASS_METER_TBL_CONFIG,
    COMMAND_CLASS_METER_TBL_MONITOR,
    COMMAND_CLASS_METER_TBL_PUSH,
    COMMAND_CLASS_MTP_WINDOW_COVERING,
    COMMAND_CLASS_MULTI_CHANNEL,
    COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION,
    COMMAND_CLASS_MULTI_CMD,
    COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC,
    COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION,
    COMMAND_CLASS_NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE,
    COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY,
    COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY,
    COMMAND_CLASS_NON_INTEROPERABLE,
    COMMAND_CLASS_NO_OPERATION,
    COMMAND_CLASS_NODE_NAMING,
    COMMAND_CLASS_NODE_PROVISIONING,
    COMMAND_CLASS_NOTIFICATION,
    COMMAND_CLASS_POWERLEVEL,
    COMMAND_CLASS_PREPAYMENT,
    COMMAND_CLASS_PREPAYMENT_ENCAPSULATION,
    COMMAND_CLASS_PROTECTION,
    COMMAND_CLASS_PROPRIETARY,
    COMMAND_CLASS_RATE_TBL_CONFIG,
    COMMAND_CLASS_RATE_TBL_MONITOR,
    COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE,
    COMMAND_CLASS_REMOTE_ASSOCIATION,
    COMMAND_CLASS_SCENE_ACTIVATION,
    COMMAND_CLASS_SCENE_ACTUATOR_CONF,
    COMMAND_CLASS_SCENE_CONTROLLER_CONF,
    COMMAND_CLASS_SCHEDULE,
    COMMAND_CLASS_SCHEDULE_ENTRY_LOCK,
    COMMAND_CLASS_SCREEN_ATTRIBUTES,
    COMMAND_CLASS_SCREEN_MD,
    COMMAND_CLASS_SECURITY,
    COMMAND_CLASS_SECURITY_2,
    COMMAND_CLASS_SECURITY_SCHEME0_MARK,
    COMMAND_CLASS_SECURITY_PANEL_MODE,
    COMMAND_CLASS_SECURITY_PANEL_ZONE,
    COMMAND_CLASS_SECURITY_PANEL_ZONE_SENSOR,
    COMMAND_CLASS_SENSOR_ALARM,
    COMMAND_CLASS_SENSOR_BINARY,
    COMMAND_CLASS_SENSOR_CONFIGURATION,
    COMMAND_CLASS_SENSOR_MULTILEVEL,
    COMMAND_CLASS_SILENCE_ALARM,
    COMMAND_CLASS_SIMPLE_AV_CONTROL,
    COMMAND_CLASS_SOUND_SWITCH,
    COMMAND_CLASS_SUPERVISION,
    COMMAND_CLASS_SWITCH_ALL,
    COMMAND_CLASS_SWITCH_BINARY,
    COMMAND_CLASS_SWITCH_COLOR,
    COMMAND_CLASS_SWITCH_MULTILEVEL,
    COMMAND_CLASS_SWITCH_TOGGLE_BINARY,
    COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL,
    COMMAND_CLASS_TARIFF_CONFIG,
    COMMAND_CLASS_TARIFF_TBL_MONITOR,
    COMMAND_CLASS_THERMOSTAT_FAN_MODE,
    COMMAND_CLASS_THERMOSTAT_FAN_STATE,
    COMMAND_CLASS_THERMOSTAT_MODE,
    COMMAND_CLASS_THERMOSTAT_OPERATING_STATE,
    COMMAND_CLASS_THERMOSTAT_SETBACK,
    COMMAND_CLASS_THERMOSTAT_SETPOINT,
    COMMAND_CLASS_TIME,
    COMMAND_CLASS_TIME_PARAMETERS,
    COMMAND_CLASS_TRANSPORT_SERVICE,
    COMMAND_CLASS_USER_CODE,
    COMMAND_CLASS_VERSION,
    COMMAND_CLASS_WAKE_UP,
    COMMAND_CLASS_WINDOW_COVERING,
    COMMAND_CLASS_ZENSOR_NET,
    COMMAND_CLASS_ZIP,
    COMMAND_CLASS_ZIP_6LOWPAN,
    COMMAND_CLASS_ZIP_GATEWAY,
    COMMAND_CLASS_ZIP_NAMING,
    COMMAND_CLASS_ZIP_ND,
    COMMAND_CLASS_ZIP_PORTAL,
    ZWAVE_CMD_CLASS,
    COMMAND_CLASS_ZWAVEPLUS_INFO,
)


for node in network:
    print(node.name)
    print('ID:', node.id)

    if isinstance(node, COMMAND_CLASS_ALARM):
        print('notifications:', node.notifications)

    if isinstance(node, COMMAND_CLASS_ANTITHEFT):
        pass

    if isinstance(node, COMMAND_CLASS_APPLICATION_CAPABILITY):
        pass

    if isinstance(node, COMMAND_CLASS_APPLICATION_STATUS):
        pass

    if isinstance(node, COMMAND_CLASS_ASSOCIATION):
        pass

    if isinstance(node, COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION):
        print('association_max_command_length:', node.association_max_command_length)
        print('association_commands_are_values:', node.association_commands_are_values)
        print('association_commands_are_configurable:', node.association_commands_are_configurable)
        print('association_free_commands:', node.association_free_commands)
        print('association_max_commands:', node.association_max_commands)


    if isinstance(node, COMMAND_CLASS_ASSOCIATION_GRP_INFO):
        pass

    if isinstance(node, COMMAND_CLASS_AUTHENTICATION):
        pass

    if isinstance(node, COMMAND_CLASS_AUTHENTICATION_MEDIA_WRITE):
        pass

    if isinstance(node, COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD):
        pass

    if isinstance(node, COMMAND_CLASS_AV_CONTENT_SEARCH_MD):
        pass

    if isinstance(node, COMMAND_CLASS_AV_RENDERER_STATUS):
        pass

    if isinstance(node, COMMAND_CLASS_AV_TAGGING_MD):
        pass

    if isinstance(node, COMMAND_CLASS_BARRIER_OPERATOR):
        print('barrier_state:', node.barrier_state)
        print('barrier_state_items:', node.barrier_state_items)
        print('is_barrier_audible_supported:', node.is_barrier_audible_supported)
        if node.is_barrier_audible_supported:
            print('barrier_audible_notification:', node.barrier_audible_notification)

        print('is_barrier_visual_supported:', node.is_barrier_visual_supported)
        if node.is_barrier_visual_supported:
            print('barrier_visual_notification:', node.barrier_visual_notification)

    if isinstance(node, COMMAND_CLASS_BASIC):
        pass

    if isinstance(node, COMMAND_CLASS_BASIC_TARIFF_INFO):
        pass

    if isinstance(node, COMMAND_CLASS_BASIC_WINDOW_COVERING):
        print('is_window_covering_opening:', node.is_window_covering_opening)
        print('is_window_covering_closing:', node.is_window_covering_closing)

    if isinstance(node, COMMAND_CLASS_BATTERY):
        print('battery_level:', node.battery_level)

    if isinstance(node, COMMAND_CLASS_CENTRAL_SCENE):
        print('scene_count:', node.scene_count)

    if isinstance(node, COMMAND_CLASS_CHIMNEY_FAN):
        pass

    if isinstance(node, COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE):
        day_names = node.climate_control_schedule_day_names

        days = [
            node.climate_control_schedule_monday,
            node.climate_control_schedule_tuesday,
            node.climate_control_schedule_wednesday,
            node.climate_control_schedule_thursday,
            node.climate_control_schedule_friday,
            node.climate_control_schedule_saturday,
            node.climate_control_schedule_sunday
        ]

        for day_name, schedules in zip(day_names, days):
            print(day_name, 'schedule')
            for schedule in schedules:
                print('    id:', schedule.id)
                print('    scale:', schedule.scale)
                print('    hour:', schedule.hour)
                print('    minute:', schedule.minute)
                print('    setback:', schedule.setback)
                print('    frost_protection:', schedule.frost_protection)
                print('    energy_saving:', schedule.energy_saving)

            print('climate_control_schedule_override_type_items:', node.climate_control_schedule_override_type_items)
            print('climate_control_schedule_get_override:', node.climate_control_schedule_get_override())

    if isinstance(node, COMMAND_CLASS_CLOCK):
        print('clock_day:', node.clock_day)
        print('clock_hour:', node.clock_hour)
        print('clock_minute:', node.clock_minute)
        print('clock_day_items:', node.clock_day_items)

    if isinstance(node, COMMAND_CLASS_CONFIGURATION):
        pass

    if isinstance(node, COMMAND_CLASS_CONTROLLER_REPLICATION):
        print('replication_node_id:', node.replication_node_id)
        print('replication_function:', node.replication_function)
        print('replication_function_items:', node.replication_function_items)

    if isinstance(node, COMMAND_CLASS_CRC_16_ENCAP):
        pass

    if isinstance(node, COMMAND_CLASS_DCP_CONFIG):
        pass

    if isinstance(node, COMMAND_CLASS_DCP_MONITOR):
        pass

    if isinstance(node, COMMAND_CLASS_DEVICE_RESET_LOCALLY):
        pass

    if isinstance(node, COMMAND_CLASS_DMX):
        pass

    if isinstance(node, COMMAND_CLASS_DOOR_LOCK):
        print('doorlock_locked:', node.doorlock_locked)
        print('doorlock_lock_mode:', node.doorlock_lock_mode)
        print('doorlock_lock_mode_items:', node.doorlock_lock_mode_items)
        print('doorlock_outside_handle_control:', node.doorlock_outside_handle_control)
        print('doorlock_inside_handle_control:', node.doorlock_inside_handle_control)
        print('doorlock_timeout_mode:', node.doorlock_timeout_mode)
        print('doorlock_timeout_mode_items:', node.doorlock_timeout_mode_items)
        print('doorlock_timeout_minutes:', node.doorlock_timeout_minutes)
        print('doorlock_timeout_seconds:', node.doorlock_timeout_seconds)

    if isinstance(node, COMMAND_CLASS_DOOR_LOCK_LOGGING):
        print('doorlock_logging_max_records:', node.doorlock_logging_max_records)
        print('doorlock_logging_current_record_number:', node.doorlock_logging_current_record_number)
        print('doorlock_logging_records:', node.doorlock_logging_records)

    if isinstance(node, COMMAND_CLASS_ENERGY_PRODUCTION):
        print('doorlock_timeout_seconds:', node.energy_production_current)
        print('doorlock_timeout_seconds:', node.energy_production_total)
        print('doorlock_timeout_seconds:', node.energy_production_today)
        print('doorlock_timeout_seconds:', node.energy_production_total_time)


    if isinstance(node, COMMAND_CLASS_ENTRY_CONTROL):
        pass

    if isinstance(node, COMMAND_CLASS_FIRMWARE_UPDATE_MD):
        pass

    if isinstance(node, COMMAND_CLASS_GEOGRAPHIC_LOCATION):
        pass

    if isinstance(node, COMMAND_CLASS_GROUPING_NAME):
        pass

    if isinstance(node, COMMAND_CLASS_HAIL):
        pass

    if isinstance(node, COMMAND_CLASS_HRV_CONTROL):
        pass

    if isinstance(node, COMMAND_CLASS_HRV_STATUS):
        pass

    if isinstance(node, COMMAND_CLASS_HUMIDITY_CONTROL_MODE):
        pass

    if isinstance(node, COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE):
        pass

    if isinstance(node, COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT):
        pass

    if isinstance(node, COMMAND_CLASS_INCLUSION_CONTROLLER):
        pass

    if isinstance(node, COMMAND_CLASS_INDICATOR):
        pass

    if isinstance(node, COMMAND_CLASS_IP_ASSOCIATION):
        pass

    if isinstance(node, COMMAND_CLASS_IP_CONFIGURATION):
        pass

    if isinstance(node, COMMAND_CLASS_IR_REPEATER):
        pass

    if isinstance(node, COMMAND_CLASS_IRRIGATION):
        pass

    if isinstance(node, COMMAND_CLASS_LANGUAGE):
        pass

    if isinstance(node, COMMAND_CLASS_LOCK):
        pass

    if isinstance(node, COMMAND_CLASS_MAILBOX):
        pass

    if isinstance(node, COMMAND_CLASS_MANUFACTURER_PROPRIETARY):
        pass

    if isinstance(node, COMMAND_CLASS_MANUFACTURER_SPECIFIC):
        pass

    if isinstance(node, COMMAND_CLASS_MARK):
        pass

    if isinstance(node, COMMAND_CLASS_METER):
        pass

    if isinstance(node, COMMAND_CLASS_METER_PULSE):
        pass

    if isinstance(node, COMMAND_CLASS_METER_TBL_CONFIG):
        pass

    if isinstance(node, COMMAND_CLASS_METER_TBL_MONITOR):
        pass

    if isinstance(node, COMMAND_CLASS_METER_TBL_PUSH):
        pass

    if isinstance(node, COMMAND_CLASS_MTP_WINDOW_COVERING):
        pass

    if isinstance(node, COMMAND_CLASS_MULTI_CHANNEL):
        pass

    if isinstance(node, COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION):
        pass

    if isinstance(node, COMMAND_CLASS_MULTI_CMD):
        pass

    if isinstance(node, COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC):
        pass

    if isinstance(node, COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION):
        pass

    if isinstance(node,
                  COMMAND_CLASS_NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE):
        pass

    if isinstance(node, COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY):
        pass

    if isinstance(node, COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY):
        pass

    if isinstance(node, COMMAND_CLASS_NON_INTEROPERABLE):
        pass

    if isinstance(node, COMMAND_CLASS_NO_OPERATION):
        pass

    if isinstance(node, COMMAND_CLASS_NODE_NAMING):
        pass

    if isinstance(node, COMMAND_CLASS_NODE_PROVISIONING):
        pass

    if isinstance(node, COMMAND_CLASS_NOTIFICATION):
        pass

    if isinstance(node, COMMAND_CLASS_POWERLEVEL):
        pass

    if isinstance(node, COMMAND_CLASS_PREPAYMENT):
        pass

    if isinstance(node, COMMAND_CLASS_PREPAYMENT_ENCAPSULATION):
        pass

    if isinstance(node, COMMAND_CLASS_PROTECTION):
        pass

    if isinstance(node, COMMAND_CLASS_PROPRIETARY):
        pass

    if isinstance(node, COMMAND_CLASS_RATE_TBL_CONFIG):
        pass

    if isinstance(node, COMMAND_CLASS_RATE_TBL_MONITOR):
        pass

    if isinstance(node, COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE):
        pass

    if isinstance(node, COMMAND_CLASS_REMOTE_ASSOCIATION):
        pass

    if isinstance(node, COMMAND_CLASS_SCENE_ACTIVATION):
        pass

    if isinstance(node, COMMAND_CLASS_SCENE_ACTUATOR_CONF):
        pass

    if isinstance(node, COMMAND_CLASS_SCENE_CONTROLLER_CONF):
        pass

    if isinstance(node, COMMAND_CLASS_SCHEDULE):
        pass

    if isinstance(node, COMMAND_CLASS_SCHEDULE_ENTRY_LOCK):
        pass

    if isinstance(node, COMMAND_CLASS_SCREEN_ATTRIBUTES):
        pass

    if isinstance(node, COMMAND_CLASS_SCREEN_MD):
        pass

    if isinstance(node, COMMAND_CLASS_SECURITY):
        pass

    if isinstance(node, COMMAND_CLASS_SECURITY_2):
        pass

    if isinstance(node, COMMAND_CLASS_SECURITY_SCHEME0_MARK):
        pass

    if isinstance(node, COMMAND_CLASS_SECURITY_PANEL_MODE):
        pass

    if isinstance(node, COMMAND_CLASS_SECURITY_PANEL_ZONE):
        pass

    if isinstance(node, COMMAND_CLASS_SECURITY_PANEL_ZONE_SENSOR):
        pass

    if isinstance(node, COMMAND_CLASS_SENSOR_ALARM):
        pass

    if isinstance(node, COMMAND_CLASS_SENSOR_BINARY):
        pass

    if isinstance(node, COMMAND_CLASS_SENSOR_CONFIGURATION):
        pass

    if isinstance(node, COMMAND_CLASS_SENSOR_MULTILEVEL):
        pass

    if isinstance(node, COMMAND_CLASS_SILENCE_ALARM):
        pass

    if isinstance(node, COMMAND_CLASS_SIMPLE_AV_CONTROL):
        pass

    if isinstance(node, COMMAND_CLASS_SOUND_SWITCH):
        pass

    if isinstance(node, COMMAND_CLASS_SUPERVISION):
        pass

    if isinstance(node, COMMAND_CLASS_SWITCH_ALL):
        pass

    if isinstance(node, COMMAND_CLASS_SWITCH_BINARY):
        print('switch_state:', node.switch_state)

    if isinstance(node, COMMAND_CLASS_SWITCH_COLOR):
        print('switch_color_rgb:', node.switch_color_rgb)
        print('switch_color_cmy:', node.switch_color_cmy)
        print('switch_color_hsv:', node.switch_color_hsv)
        print('switch_color_fade_duration:', node.switch_color_fade_duration)
        print('switch_color_warm_white:', node.switch_color_warm_white)

    if isinstance(node, COMMAND_CLASS_SWITCH_MULTILEVEL):
        print('switch_level:', node.switch_level)

    if isinstance(node, COMMAND_CLASS_SWITCH_TOGGLE_BINARY):
        pass

    if isinstance(node, COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL):
        pass

    if isinstance(node, COMMAND_CLASS_TARIFF_CONFIG):
        pass

    if isinstance(node, COMMAND_CLASS_TARIFF_TBL_MONITOR):
        pass

    if isinstance(node, COMMAND_CLASS_THERMOSTAT_FAN_MODE):
        pass

    if isinstance(node, COMMAND_CLASS_THERMOSTAT_FAN_STATE):
        pass

    if isinstance(node, COMMAND_CLASS_THERMOSTAT_MODE):
        pass

    if isinstance(node, COMMAND_CLASS_THERMOSTAT_OPERATING_STATE):
        pass

    if isinstance(node, COMMAND_CLASS_THERMOSTAT_SETBACK):
        pass

    if isinstance(node, COMMAND_CLASS_THERMOSTAT_SETPOINT):
        pass

    if isinstance(node, COMMAND_CLASS_TIME):
        pass

    if isinstance(node, COMMAND_CLASS_TIME_PARAMETERS):
        pass

    if isinstance(node, COMMAND_CLASS_TRANSPORT_SERVICE):
        pass

    if isinstance(node, COMMAND_CLASS_USER_CODE):
        pass

    if isinstance(node, COMMAND_CLASS_VERSION):
        pass

    if isinstance(node, COMMAND_CLASS_WAKE_UP):
        pass

    if isinstance(node, COMMAND_CLASS_WINDOW_COVERING):
        pass

    if isinstance(node, COMMAND_CLASS_ZENSOR_NET):
        pass

    if isinstance(node, COMMAND_CLASS_ZIP):
        pass

    if isinstance(node, COMMAND_CLASS_ZIP_6LOWPAN):
        pass

    if isinstance(node, COMMAND_CLASS_ZIP_GATEWAY):
        pass

    if isinstance(node, COMMAND_CLASS_ZIP_NAMING):
        pass

    if isinstance(node, COMMAND_CLASS_ZIP_ND):
        pass

    if isinstance(node, COMMAND_CLASS_ZIP_PORTAL):
        pass

    if isinstance(node, ZWAVE_CMD_CLASS):
        pass

    if isinstance(node, COMMAND_CLASS_ZWAVEPLUS_INFO):
        pass
    
    
    stats = node.stats

    
    print(stats.sentCnt.doc, ':', stats.sentCnt)
    print(stats.sentFailed.doc, ':', stats.sentFailed)
    print(stats.retries.doc, ':', stats.retries)
    print(stats.receivedCnt.doc, ':', stats.receivedCnt)
    print(stats.receivedDups.doc, ':', stats.receivedDups)
    print(stats.receivedUnsolicited.doc, ':', stats.receivedUnsolicited)
    print(stats.sentTS.doc, ':', stats.sentTS)
    print(stats.receivedTS.doc, ':', stats.receivedTS)
    print(stats.lastRequestRTT.doc, ':', stats.lastRequestRTT)
    print(stats.averageRequestRTT.doc, ':', stats.averageRequestRTT)
    print(stats.lastResponseRTT.doc, ':', stats.lastResponseRTT)
    print(stats.averageResponseRTT.doc, ':', stats.averageResponseRTT)
    print(stats.quality.doc, ':', stats.quality)
    print(stats.lastReceivedMessage.doc, ':', stats.lastReceivedMessage)
    print(stats.txStatusReportSupported.doc, ':', stats.txStatusReportSupported)
    print(stats.txStatusReportSupported.doc, ':', stats.txStatusReportSupported)
    print(stats.txTime.doc, ':', stats.txTime)
    print(stats.hops.doc, ':', stats.hops)
    print(stats.rssi_1.doc, ':', stats.rssi_1)
    print(stats.rssi_2.doc, ':', stats.rssi_2)
    print(stats.rssi_3.doc, ':', stats.rssi_3)
    print(stats.rssi_4.doc, ':', stats.rssi_4)
    print(stats.rssi_5.doc, ':', stats.rssi_5)
    print(stats.ackChannel.doc, ':', stats.ackChannel)
    print(stats.lastTxChannel.doc, ':', stats.lastTxChannel)
    print(stats.routeScheme.doc, ':', stats.routeScheme)
    print(stats.routeUsed.doc, ':', stats.routeUsed)
    print(stats.routeSpeed.doc, ':', stats.routeSpeed)
    print(stats.routeTries.doc, ':', stats.routeTries)
    print(stats.lastFailedLinkFrom.doc, ':', stats.lastFailedLinkFrom)
    print(stats.lastFailedLinkTo.doc, ':', stats.lastFailedLinkTo)

    print(stats.ccData.doc, ':')

    for ccd in stats.ccData:
        print('   ', ccd.commandClassId.doc, ':', ccd.commandClassId)
        print('   ', ccd.sentCnt.doc, ':', ccd.sentCnt)
        print('   ', ccd.receivedCnt.doc, ':', ccd.receivedCnt)


event.clear()
print('********* STOPPING NETWORK *************')
network.stop()
event.wait()

