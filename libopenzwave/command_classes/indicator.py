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
:synopsis: COMMAND_CLASS_INDICATOR

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Indicator Command Class - Active
# Management
COMMAND_CLASS_INDICATOR = 0x87


# noinspection PyAbstractClass
class Indicator(zwave_cmd_class.ZWaveCommandClass):
    """
    Indicator Command Class

    symbol: `COMMAND_CLASS_INDICATOR`
    """

    class_id = COMMAND_CLASS_INDICATOR
    class_desc = 'COMMAND_CLASS_INDICATOR'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        indicator = 0
        indicator_armed = 1
        indicator_not_armed = 2
        indicator_ready = 3
        indicator_fault = 4
        indicator_busy = 5
        indicator_enter_id = 6
        indicator_enter_pin = 7
        indicator_code_accepted = 8
        indicator_code_not_accepted = 9
        indicator_armed_stay = 10
        indicator_armed_away = 11
        indicator_alarming = 12
        indicator_alarming_burglar = 13
        indicator_alarming_smoke_fire = 14
        indicator_alarming_carbon_monoxide = 15
        indicator_bypass_challenge = 16
        indicator_entry_delay = 17
        indicator_exit_delay = 18
        indicator_alarming_medical = 19
        indicator_alarming_freeze_warning = 20
        indicator_alarming_water_leak = 21
        indicator_alarming_panic = 22
        indicator_zone_1_armed = 32
        indicator_zone_2_armed = 33
        indicator_zone_3_armed = 34
        indicator_zone_4_armed = 35
        indicator_zone_5_armed = 36
        indicator_zone_6_armed = 37
        indicator_zone_7_armed = 38
        indicator_zone_8_armed = 39
        indicator_lcd_backlight = 48
        indicator_button_backlight_letters = 64
        indicator_button_backlight_digits = 65
        indicator_button_backlight_command = 66
        indicator_button_1 = 67
        indicator_button_2 = 68
        indicator_button_3 = 69
        indicator_button_4 = 70
        indicator_button_5 = 71
        indicator_button_6 = 72
        indicator_button_7 = 73
        indicator_button_8 = 74
        indicator_button_9 = 75
        indicator_button_10 = 76
        indicator_button_11 = 77
        indicator_button_12 = 78
        indicator_node_identify = 80
        indicator_generic_event_sound_notification_1 = 96
        indicator_generic_event_sound_notification_2 = 97
        indicator_generic_event_sound_notification_3 = 98
        indicator_generic_event_sound_notification_4 = 99
        indicator_generic_event_sound_notification_5 = 100
        indicator_generic_event_sound_notification_6 = 101
        indicator_generic_event_sound_notification_7 = 102
        indicator_generic_event_sound_notification_8 = 103
        indicator_generic_event_sound_notification_9 = 104
        indicator_generic_event_sound_notification_10 = 105
        indicator_generic_event_sound_notification_11 = 106
        indicator_generic_event_sound_notification_12 = 107
        indicator_generic_event_sound_notification_13 = 108
        indicator_generic_event_sound_notification_14 = 109
        indicator_generic_event_sound_notification_15 = 110
        indicator_generic_event_sound_notification_16 = 111
        indicator_generic_event_sound_notification_17 = 112
        indicator_generic_event_sound_notification_18 = 113
        indicator_generic_event_sound_notification_19 = 114
        indicator_generic_event_sound_notification_20 = 115
        indicator_generic_event_sound_notification_21 = 116
        indicator_generic_event_sound_notification_22 = 117
        indicator_generic_event_sound_notification_23 = 118
        indicator_generic_event_sound_notification_24 = 119
        indicator_generic_event_sound_notification_25 = 120
        indicator_generic_event_sound_notification_26 = 121
        indicator_generic_event_sound_notification_27 = 122
        indicator_generic_event_sound_notification_28 = 123
        indicator_generic_event_sound_notification_29 = 124
        indicator_generic_event_sound_notification_30 = 125
        indicator_generic_event_sound_notification_31 = 126
        indicator_generic_event_sound_notification_32 = 127
        indicator_manufacturer_defined_1 = 128
        indicator_manufacturer_defined_2 = 129
        indicator_manufacturer_defined_3 = 130
        indicator_manufacturer_defined_4 = 131
        indicator_manufacturer_defined_5 = 132
        indicator_manufacturer_defined_6 = 133
        indicator_manufacturer_defined_7 = 134
        indicator_manufacturer_defined_8 = 135
        indicator_manufacturer_defined_9 = 136
        indicator_manufacturer_defined_10 = 137
        indicator_manufacturer_defined_11 = 138
        indicator_manufacturer_defined_12 = 139
        indicator_manufacturer_defined_13 = 140
        indicator_manufacturer_defined_14 = 141
        indicator_manufacturer_defined_15 = 142
        indicator_manufacturer_defined_16 = 143
        indicator_manufacturer_defined_17 = 144
        indicator_manufacturer_defined_18 = 145
        indicator_manufacturer_defined_19 = 146
        indicator_manufacturer_defined_20 = 147
        indicator_manufacturer_defined_21 = 148
        indicator_manufacturer_defined_22 = 149
        indicator_manufacturer_defined_23 = 150
        indicator_manufacturer_defined_24 = 151
        indicator_manufacturer_defined_25 = 152
        indicator_manufacturer_defined_26 = 153
        indicator_manufacturer_defined_27 = 154
        indicator_manufacturer_defined_28 = 155
        indicator_manufacturer_defined_29 = 156
        indicator_manufacturer_defined_30 = 157
        indicator_manufacturer_defined_31 = 158
        indicator_manufacturer_defined_32 = 159
        indicator_buzzer = 240

    @property
    def indicator(self):
        """
        Get/Set Indicator

        :param value: ?
        :type value: int

        :return: ?
        :rtype: int
        """
        return self.values.indicator.data

    @indicator.setter
    def indicator(self, value):
        self.values.indicator.data = value
