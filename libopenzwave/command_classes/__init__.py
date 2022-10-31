# -*- coding: utf-8 -*-
"""

This file is part of **python-openzwave**
project https://github.com/OpenZWave/python-openzwave.

:platform: Unix, Windows, MacOS X
:synopsis: openzwave wrapper

.. moduleauthor:: Kevin G Schlosser

License : GPL(v3)

**python-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**python-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.

"""

# command_class.py
#
# This is a very unique module. It handles a variety of things all at once.
# It provides the user with command class names and it also matches those names
# with a class that represents the actual command class.
#
# By having the classes for each of the command classes it gives an organized
# way of adding code that is specific to a specific command class. it removes
# the need for a method to check a node to see if it is switch, or if you can
# wake it.
#
# this modules when imported for the first time places the instance of a class
# object in sys.modules in place of the actual module it's self. This is done
# to handle the routing of data that is needed to build a node class as well as
# handle user import of command class constants. what I have done is made the
# object act as a dict and when a command class is used in the same fashion as
# you would to get the value from a dict the class representation of the
# command class constant that is passed is returned. If command_class.py is
# imported as a whole i used __getattr__ to return the proper object that is
# being requested. This gives the means to access the objects that are in the
# module without the handler changing anything about.
#
# In the node.py file I have commented on how the nodes are built.

# from .alarm import Alarm
from .antitheft import Antitheft
from .application_capability import ApplicationCapability
from .application_status import ApplicationStatus
from .association import Association
from .association_command_configuration import AssociationCommandConfiguration
from .association_grp_info import AssociationGroupInfo
from .authentication import Authentication
from .authentication_media_write import AuthenticationMediaWrite
from .av_content_directory_md import AVContentDirectoryMD
from .av_content_search_md import AVContentSearchMD
from .av_renderer_status import AVRendererStatus
from .av_tagging_md import AVTaggingMD
from .barrier_operator import BarrierOperator
from .basic import Basic
from .basic_tariff_info import BasicTariffInfo
from .basic_window_covering import BasicWindowCovering
from .battery import Battery
from .central_scene import CentralScene
from .chimney_fan import ChimneyFan
from .climate_control_schedule import ClimateControlSchedule
from .clock import Clock
from .configuration import Configuration
from .controller_replication import ControllerReplication
from .crc_16_encap import CRC16Encap
from .dcp_config import DCPConfig
from .dcp_monitor import DCPMonitor
from .device_reset_locally import DeviceResetLocally
from .dmx import DMX
from .door_lock import DoorLock
from .door_lock_logging import DoorLockLogging
from .energy_production import EnergyProduction
from .entry_control import EntryControl
from .firmware_update_md import FirmwareUpdateMD
from .geographic_location import GeographicLocation
from .grouping_name import GroupingName
from .hail import Hail
from .hrv_control import HRVControl
from .hrv_status import HRVStatus
from .humidity_control_mode import HumidityControlMode
from .humidity_control_operating_state import HumidityControlOperatingState
from .humidity_control_setpoint import HumidityControlSetpoint
from .inclusion_controller import InclusionController
from .indicator import Indicator
from .ip_association import IPAssociation
from .ip_configuration import IPConfiguration
from .ir_repeater import IRRepeater
from .irrigation import Irrigation
from .language import Language
from .lock import Lock
from .mailbox import Mailbox
from .manufacturer_proprietary import ManufacturerProprietary
from .manufacturer_specific import ManufacturerSpecific
from .mark import Mark
from .meter import Meter
from .meter_pulse import MeterPulse
from .meter_tbl_config import MeterTableConfig
from .meter_tbl_monitor import MeterTableMonitor
from .meter_tbl_push import MeterTablePush
from .mtp_window_covering import MTPWindowCovering
from .multi_channel import MultiChannel
from .multi_channel_association import MultiChannelAssociation
from .multi_cmd import MultiCommand
from .network_management_basic import NetworkManagementBasic
from .network_management_inclusion import NetworkManagementInclusion
from .network_management_installation_maintenance import NetworkManagementInstallationMaintenance
from .network_management_primary import NetworkManagementPrimary
from .network_management_proxy import NetworkManagementProxy
from .non_interoperable import NonInteroperable
from .no_operation import NoOperation
from .node_naming import NodeNaming
from .node_provisioning import NodeProvisioning
from .notification import Notification
from .powerlevel import Powerlevel
from .prepayment import Prepayment
from .prepayment_encapsulation import PrepaymentEncapsulation
from .protection import Protection
from .proprietary import Proprietary
from .rate_tbl_config import RateTableConfig
from .rate_tbl_monitor import RateTableMonitor
from .remote_association_activate import RemoteAssociationActivate
from .remote_association import RemoteAssociation
from .scene_activation import SceneActivation
from .scene_actuator_conf import SceneActuatorConfig
from .scene_controller_conf import SceneControllerConfig
from .schedule import Schedule
from .schedule_entry_lock import ScheduleEntryLock
from .screen_attributes import ScreenAttributes
from .screen_md import ScreenMD
from .security import Security
from .security_2 import Security2
from .security_scheme0_mark import SecurityScheme0Mark
from .security_panel_mode import SecurityPanelMode
from .security_panel_zone import SecurityPanelZone
from .security_panel_zone_sensor import SecurityPanelZoneSensor
from .sensor_alarm import SensorAlarm
from .sensor_binary import SensorBinary
from .sensor_configuration import SensorConfiguration
from .sensor_multilevel import SensorMultilevel
from .silence_alarm import SilenceAlarm
from .simple_av_control import SimpleAVControl
from .sound_switch import SoundSwitch
from .supervision import Supervision
from .switch_all import SwitchAll
from .switch_binary import SwitchBinary
from .switch_color import SwitchColor
from .switch_multilevel import SwitchMultilevel
from .switch_toggle_binary import SwitchToggleBinary
from .switch_toggle_multilevel import SwitchToggleMultilevel
from .tariff_config import TariffConfig
from .tariff_tbl_monitor import TariffTableMonitor
from .thermostat_fan_mode import ThermostatFanMode
from .thermostat_fan_state import ThermostatFanState
from .thermostat_mode import ThermostatMode
from .thermostat_operating_state import ThermostatOperatingState
from .thermostat_setback import ThermostatSetback
from .thermostat_setpoint import ThermostatSetpoint
from .time import Time
from .time_parameters import TimeParameters
from .transport_service import TransportService
from .user_code import UserCode
from .version import Version
from .wake_up import WakeUp
from .window_covering import WindowCovering
from .zensor_net import ZensorNet
from .zip import ZIP
from .zip_6lowpan import ZIP6Lowpan
from .zip_gateway import ZIPGateway
from .zip_naming import ZIPNaming
from .zip_nd import ZIPND
from .zip_portal import ZIPPortal
from .zwave_plus_info import ZwavePlusInfo
from .zwave_cmd_class import ZWaveCommandClass

# COMMAND_CLASS_ALARM = Alarm
COMMAND_CLASS_ALARM = Notification
COMMAND_CLASS_ANTITHEFT = Antitheft
COMMAND_CLASS_APPLICATION_CAPABILITY = ApplicationCapability
COMMAND_CLASS_APPLICATION_STATUS = ApplicationStatus
COMMAND_CLASS_ASSOCIATION = Association
COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION = (
    AssociationCommandConfiguration
)
COMMAND_CLASS_ASSOCIATION_GRP_INFO = AssociationGroupInfo
COMMAND_CLASS_AUTHENTICATION = Authentication
COMMAND_CLASS_AUTHENTICATION_MEDIA_WRITE = AuthenticationMediaWrite
COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD = AVContentDirectoryMD
COMMAND_CLASS_AV_CONTENT_SEARCH_MD = AVContentSearchMD
COMMAND_CLASS_AV_RENDERER_STATUS = AVRendererStatus
COMMAND_CLASS_AV_TAGGING_MD = AVTaggingMD
COMMAND_CLASS_BARRIER_OPERATOR = BarrierOperator
COMMAND_CLASS_BASIC = Basic
COMMAND_CLASS_BASIC_TARIFF_INFO = BasicTariffInfo
COMMAND_CLASS_BASIC_WINDOW_COVERING = BasicWindowCovering
COMMAND_CLASS_BATTERY = Battery
COMMAND_CLASS_CENTRAL_SCENE = CentralScene
COMMAND_CLASS_CHIMNEY_FAN = ChimneyFan
COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE = ClimateControlSchedule
COMMAND_CLASS_CLOCK = Clock
COMMAND_CLASS_CONFIGURATION = Configuration
COMMAND_CLASS_CONTROLLER_REPLICATION = ControllerReplication
COMMAND_CLASS_CRC_16_ENCAP = CRC16Encap
COMMAND_CLASS_DCP_CONFIG = DCPConfig
COMMAND_CLASS_DCP_MONITOR = DCPMonitor
COMMAND_CLASS_DEVICE_RESET_LOCALLY = DeviceResetLocally
COMMAND_CLASS_DMX = DMX
COMMAND_CLASS_DOOR_LOCK = DoorLock
COMMAND_CLASS_DOOR_LOCK_LOGGING = DoorLockLogging
COMMAND_CLASS_ENERGY_PRODUCTION = EnergyProduction
COMMAND_CLASS_ENTRY_CONTROL = EntryControl
COMMAND_CLASS_FIRMWARE_UPDATE_MD = FirmwareUpdateMD
COMMAND_CLASS_GEOGRAPHIC_LOCATION = GeographicLocation
COMMAND_CLASS_GROUPING_NAME = GroupingName
COMMAND_CLASS_HAIL = Hail
COMMAND_CLASS_HRV_CONTROL = HRVControl
COMMAND_CLASS_HRV_STATUS = HRVStatus
COMMAND_CLASS_HUMIDITY_CONTROL_MODE = HumidityControlMode
COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE = (
    HumidityControlOperatingState
)
COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT = HumidityControlSetpoint
COMMAND_CLASS_INCLUSION_CONTROLLER = InclusionController
COMMAND_CLASS_INDICATOR = Indicator
COMMAND_CLASS_IP_ASSOCIATION = IPAssociation
COMMAND_CLASS_IP_CONFIGURATION = IPConfiguration
COMMAND_CLASS_IR_REPEATER = IRRepeater
COMMAND_CLASS_IRRIGATION = Irrigation
COMMAND_CLASS_LANGUAGE = Language
COMMAND_CLASS_LOCK = Lock
COMMAND_CLASS_MAILBOX = Mailbox
COMMAND_CLASS_MANUFACTURER_PROPRIETARY = ManufacturerProprietary
COMMAND_CLASS_MANUFACTURER_SPECIFIC = ManufacturerSpecific
COMMAND_CLASS_MARK = Mark
COMMAND_CLASS_METER = Meter
COMMAND_CLASS_METER_PULSE = MeterPulse
COMMAND_CLASS_METER_TBL_CONFIG = MeterTableConfig
COMMAND_CLASS_METER_TBL_MONITOR = MeterTableMonitor
COMMAND_CLASS_METER_TBL_PUSH = MeterTablePush
COMMAND_CLASS_MTP_WINDOW_COVERING = MTPWindowCovering
COMMAND_CLASS_MULTI_CHANNEL = MultiChannel
COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION = MultiChannelAssociation
COMMAND_CLASS_MULTI_CMD = MultiCommand
COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC = NetworkManagementBasic
COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION = NetworkManagementInclusion
COMMAND_CLASS_NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE = (
    NetworkManagementInstallationMaintenance
)
COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY = NetworkManagementPrimary
COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY = NetworkManagementProxy
COMMAND_CLASS_NON_INTEROPERABLE = NonInteroperable
COMMAND_CLASS_NO_OPERATION = NoOperation
COMMAND_CLASS_NODE_NAMING = NodeNaming
COMMAND_CLASS_NODE_PROVISIONING = NodeProvisioning
COMMAND_CLASS_NOTIFICATION = Notification
COMMAND_CLASS_POWERLEVEL = Powerlevel
COMMAND_CLASS_PREPAYMENT = Prepayment
COMMAND_CLASS_PREPAYMENT_ENCAPSULATION = PrepaymentEncapsulation
COMMAND_CLASS_PROTECTION = Protection
COMMAND_CLASS_PROPRIETARY = Proprietary
COMMAND_CLASS_RATE_TBL_CONFIG = RateTableConfig
COMMAND_CLASS_RATE_TBL_MONITOR = RateTableMonitor
COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE = RemoteAssociationActivate
COMMAND_CLASS_REMOTE_ASSOCIATION = RemoteAssociation
COMMAND_CLASS_SCENE_ACTIVATION = SceneActivation
COMMAND_CLASS_SCENE_ACTUATOR_CONF = SceneActuatorConfig
COMMAND_CLASS_SCENE_CONTROLLER_CONF = SceneControllerConfig
COMMAND_CLASS_SCHEDULE = Schedule
COMMAND_CLASS_SCHEDULE_ENTRY_LOCK = ScheduleEntryLock
COMMAND_CLASS_SCREEN_ATTRIBUTES = ScreenAttributes
COMMAND_CLASS_SCREEN_MD = ScreenMD
COMMAND_CLASS_SECURITY = Security
COMMAND_CLASS_SECURITY_2 = Security2
COMMAND_CLASS_SECURITY_SCHEME0_MARK = SecurityScheme0Mark
COMMAND_CLASS_SECURITY_PANEL_MODE = SecurityPanelMode
COMMAND_CLASS_SECURITY_PANEL_ZONE = SecurityPanelZone
COMMAND_CLASS_SECURITY_PANEL_ZONE_SENSOR = SecurityPanelZoneSensor
COMMAND_CLASS_SENSOR_ALARM = SensorAlarm
COMMAND_CLASS_SENSOR_BINARY = SensorBinary
COMMAND_CLASS_SENSOR_CONFIGURATION = SensorConfiguration
COMMAND_CLASS_SENSOR_MULTILEVEL = SensorMultilevel
COMMAND_CLASS_SILENCE_ALARM = SilenceAlarm
COMMAND_CLASS_SIMPLE_AV_CONTROL = SimpleAVControl
COMMAND_CLASS_SOUND_SWITCH = SoundSwitch
COMMAND_CLASS_SUPERVISION = Supervision
COMMAND_CLASS_SWITCH_ALL = SwitchAll
COMMAND_CLASS_SWITCH_BINARY = SwitchBinary
COMMAND_CLASS_SWITCH_COLOR = SwitchColor
COMMAND_CLASS_SWITCH_MULTILEVEL = SwitchMultilevel
COMMAND_CLASS_SWITCH_TOGGLE_BINARY = SwitchToggleBinary
COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL = SwitchToggleMultilevel
COMMAND_CLASS_TARIFF_CONFIG = TariffConfig
COMMAND_CLASS_TARIFF_TBL_MONITOR = TariffTableMonitor
COMMAND_CLASS_THERMOSTAT_FAN_MODE = ThermostatFanMode
COMMAND_CLASS_THERMOSTAT_FAN_STATE = ThermostatFanState
COMMAND_CLASS_THERMOSTAT_MODE = ThermostatMode
COMMAND_CLASS_THERMOSTAT_OPERATING_STATE = ThermostatOperatingState
COMMAND_CLASS_THERMOSTAT_SETBACK = ThermostatSetback
COMMAND_CLASS_THERMOSTAT_SETPOINT = ThermostatSetpoint
COMMAND_CLASS_TIME = Time
COMMAND_CLASS_TIME_PARAMETERS = TimeParameters
COMMAND_CLASS_TRANSPORT_SERVICE = TransportService
COMMAND_CLASS_USER_CODE = UserCode
COMMAND_CLASS_VERSION = Version
COMMAND_CLASS_WAKE_UP = WakeUp
COMMAND_CLASS_WINDOW_COVERING = WindowCovering
COMMAND_CLASS_ZENSOR_NET = ZensorNet
COMMAND_CLASS_ZIP = ZIP
COMMAND_CLASS_ZIP_6LOWPAN = ZIP6Lowpan
COMMAND_CLASS_ZIP_GATEWAY = ZIPGateway
COMMAND_CLASS_ZIP_NAMING = ZIPNaming
COMMAND_CLASS_ZIP_ND = ZIPND
COMMAND_CLASS_ZIP_PORTAL = ZIPPortal
ZWAVE_CMD_CLASS = ZWaveCommandClass
COMMAND_CLASS_ZWAVEPLUS_INFO = ZwavePlusInfo


class CommandClassString(str):
    class_id = 0
    class_desc = ''
    id = 0
    _cc = None

    def __eq__(self, other):
        """
        :param other: int, object
        :rtype: bool
        """
        if isinstance(other, int):
            return other == self._cc.class_id
        try:
            return other.class_id == self._cc.class_id
        except AttributeError:
            pass

        try:
            return other.id == self.id
        except AttributeError:
            return False

    def __ne__(self, other):
        """
        :param other: int, object
        :rtype: bool
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        :rtype hash:
        """
        return hash(repr(self))

    def __int__(self):
        """
        :rtype: int
        """
        return self._cc.class_id

    @property
    def doc(self):
        return self._cc.__doc__


class COMMAND_CLASSES_(object):

    def __init__(self):
        self._attr_names = [
            'COMMAND_CLASS_ALARM',
            'COMMAND_CLASS_ANTITHEFT',
            'COMMAND_CLASS_APPLICATION_CAPABILITY',
            'COMMAND_CLASS_APPLICATION_STATUS',
            'COMMAND_CLASS_ASSOCIATION',
            'COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION',
            'COMMAND_CLASS_ASSOCIATION_GRP_INFO',
            'COMMAND_CLASS_AUTHENTICATION',
            'COMMAND_CLASS_AUTHENTICATION_MEDIA_WRITE',
            'COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD',
            'COMMAND_CLASS_AV_CONTENT_SEARCH_MD',
            'COMMAND_CLASS_AV_RENDERER_STATUS',
            'COMMAND_CLASS_AV_TAGGING_MD',
            'COMMAND_CLASS_BARRIER_OPERATOR',
            'COMMAND_CLASS_BASIC',
            'COMMAND_CLASS_BASIC_TARIFF_INFO',
            'COMMAND_CLASS_BASIC_WINDOW_COVERING',
            'COMMAND_CLASS_BATTERY',
            'COMMAND_CLASS_CENTRAL_SCENE',
            'COMMAND_CLASS_CHIMNEY_FAN',
            'COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE',
            'COMMAND_CLASS_CLOCK',
            'COMMAND_CLASS_CONFIGURATION',
            'COMMAND_CLASS_CONTROLLER_REPLICATION',
            'COMMAND_CLASS_CRC_16_ENCAP',
            'COMMAND_CLASS_DCP_CONFIG',
            'COMMAND_CLASS_DCP_MONITOR',
            'COMMAND_CLASS_DEVICE_RESET_LOCALLY',
            'COMMAND_CLASS_DMX',
            'COMMAND_CLASS_DOOR_LOCK',
            'COMMAND_CLASS_DOOR_LOCK_LOGGING',
            'COMMAND_CLASS_ENERGY_PRODUCTION',
            'COMMAND_CLASS_ENTRY_CONTROL',
            'COMMAND_CLASS_FIRMWARE_UPDATE_MD',
            'COMMAND_CLASS_GEOGRAPHIC_LOCATION',
            'COMMAND_CLASS_GROUPING_NAME',
            'COMMAND_CLASS_HAIL',
            'COMMAND_CLASS_HRV_CONTROL',
            'COMMAND_CLASS_HRV_STATUS',
            'COMMAND_CLASS_HUMIDITY_CONTROL_MODE',
            'COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE',
            'COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT',
            'COMMAND_CLASS_INCLUSION_CONTROLLER',
            'COMMAND_CLASS_INDICATOR',
            'COMMAND_CLASS_IP_ASSOCIATION',
            'COMMAND_CLASS_IP_CONFIGURATION',
            'COMMAND_CLASS_IR_REPEATER',
            'COMMAND_CLASS_IRRIGATION',
            'COMMAND_CLASS_LANGUAGE',
            'COMMAND_CLASS_LOCK',
            'COMMAND_CLASS_MAILBOX',
            'COMMAND_CLASS_MANUFACTURER_PROPRIETARY',
            'COMMAND_CLASS_MANUFACTURER_SPECIFIC',
            'COMMAND_CLASS_MARK',
            'COMMAND_CLASS_METER',
            'COMMAND_CLASS_METER_PULSE',
            'COMMAND_CLASS_METER_TBL_CONFIG',
            'COMMAND_CLASS_METER_TBL_MONITOR',
            'COMMAND_CLASS_METER_TBL_PUSH',
            'COMMAND_CLASS_MTP_WINDOW_COVERING',
            'COMMAND_CLASS_MULTI_CHANNEL',
            'COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION',
            'COMMAND_CLASS_MULTI_CMD',
            'COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC',
            'COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION',
            'COMMAND_CLASS_NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE',
            'COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY',
            'COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY',
            'COMMAND_CLASS_NON_INTEROPERABLE',
            'COMMAND_CLASS_NO_OPERATION',
            'COMMAND_CLASS_NODE_NAMING',
            'COMMAND_CLASS_NODE_PROVISIONING',
            'COMMAND_CLASS_NOTIFICATION',
            'COMMAND_CLASS_POWERLEVEL',
            'COMMAND_CLASS_PREPAYMENT',
            'COMMAND_CLASS_PREPAYMENT_ENCAPSULATION',
            'COMMAND_CLASS_PROTECTION',
            'COMMAND_CLASS_PROPRIETARY',
            'COMMAND_CLASS_RATE_TBL_CONFIG',
            'COMMAND_CLASS_RATE_TBL_MONITOR',
            'COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE',
            'COMMAND_CLASS_REMOTE_ASSOCIATION',
            'COMMAND_CLASS_SCENE_ACTIVATION',
            'COMMAND_CLASS_SCENE_ACTUATOR_CONF',
            'COMMAND_CLASS_SCENE_CONTROLLER_CONF',
            'COMMAND_CLASS_SCHEDULE',
            'COMMAND_CLASS_SCHEDULE_ENTRY_LOCK',
            'COMMAND_CLASS_SCREEN_ATTRIBUTES',
            'COMMAND_CLASS_SCREEN_MD',
            'COMMAND_CLASS_SECURITY',
            'COMMAND_CLASS_SECURITY_2',
            'COMMAND_CLASS_SECURITY_SCHEME0_MARK',
            'COMMAND_CLASS_SECURITY_PANEL_MODE',
            'COMMAND_CLASS_SECURITY_PANEL_ZONE',
            'COMMAND_CLASS_SECURITY_PANEL_ZONE_SENSOR',
            'COMMAND_CLASS_SENSOR_ALARM',
            'COMMAND_CLASS_SENSOR_BINARY',
            'COMMAND_CLASS_SENSOR_CONFIGURATION',
            'COMMAND_CLASS_SENSOR_MULTILEVEL',
            'COMMAND_CLASS_SILENCE_ALARM',
            'COMMAND_CLASS_SIMPLE_AV_CONTROL',
            'COMMAND_CLASS_SOUND_SWITCH',
            'COMMAND_CLASS_SUPERVISION',
            'COMMAND_CLASS_SWITCH_ALL',
            'COMMAND_CLASS_SWITCH_BINARY',
            'COMMAND_CLASS_SWITCH_COLOR',
            'COMMAND_CLASS_SWITCH_MULTILEVEL',
            'COMMAND_CLASS_SWITCH_TOGGLE_BINARY',
            'COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL',
            'COMMAND_CLASS_TARIFF_CONFIG',
            'COMMAND_CLASS_TARIFF_TBL_MONITOR',
            'COMMAND_CLASS_THERMOSTAT_FAN_MODE',
            'COMMAND_CLASS_THERMOSTAT_FAN_STATE',
            'COMMAND_CLASS_THERMOSTAT_MODE',
            'COMMAND_CLASS_THERMOSTAT_OPERATING_STATE',
            'COMMAND_CLASS_THERMOSTAT_SETBACK',
            'COMMAND_CLASS_THERMOSTAT_SETPOINT',
            'COMMAND_CLASS_TIME',
            'COMMAND_CLASS_TIME_PARAMETERS',
            'COMMAND_CLASS_TRANSPORT_SERVICE',
            'COMMAND_CLASS_USER_CODE',
            'COMMAND_CLASS_VERSION',
            'COMMAND_CLASS_WAKE_UP',
            'COMMAND_CLASS_WINDOW_COVERING',
            'COMMAND_CLASS_ZENSOR_NET',
            'COMMAND_CLASS_ZIP',
            'COMMAND_CLASS_ZIP_6LOWPAN',
            'COMMAND_CLASS_ZIP_GATEWAY',
            'COMMAND_CLASS_ZIP_NAMING',
            'COMMAND_CLASS_ZIP_ND',
            'COMMAND_CLASS_ZIP_PORTAL',
            'COMMAND_CLASS_ZWAVEPLUS_INFO'
        ]

    def str_wrapper(self, cc_id):
        """
        :param cc_id: int
        :rtype: CommandClassString
        """
        cc = self[cc_id]

        command_class = type(
            cc.class_desc,
            (CommandClassString,),
            {
                'class_id': cc.class_id,
                'class_desc': cc.class_desc,
                'id': cc.class_id,
                '_cc': cc,
            }
        )
        
        return command_class(cc.class_desc)

    def __getitem__(self, item):
        """
        :param item: int, str
        :rtype: Any
        """
        import sys
        mod = sys.modules[__name__]

        if isinstance(item, int):
            for attr_name in self._attr_names:
                cc = getattr(mod, attr_name)

                if cc.class_id == item:
                    return cc
            raise IndexError('Command class does not exist ({0})'.format(item))
        else:
            return getattr(mod, item)

    def __iter__(self):
        import sys
        mod = sys.modules[__name__]

        for attr_name in self._attr_names:
            yield getattr(mod, attr_name)

    def __contains__(self, item):
        """
        :param item: int, str
        :rtype: bool
        """
        import sys
        mod = sys.modules[__name__]

        for attr_name in self._attr_names:
            if getattr(mod, attr_name) == item:
                return True
        
        return False


COMMAND_CLASSES = COMMAND_CLASSES_()
