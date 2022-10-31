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
:synopsis: COMMAND_CLASS_SOUND_SWITCH

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Sound Switch Command Class - Active
# Application
COMMAND_CLASS_SOUND_SWITCH = 0x79


# noinspection PyAbstractClass
class SoundSwitch(zwave_cmd_class.ZWaveCommandClass):
    """
    Sound Switch Command Class

    symbol: `COMMAND_CLASS_SOUND_SWITCH`
    """

    class_id = COMMAND_CLASS_SOUND_SWITCH
    class_desc = 'COMMAND_CLASS_SOUND_SWITCH'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        sound_switch_tone_count = 0
        sound_switch_tones = 1
        sound_switch_volume = 2
        sound_switch_default_tone = 3

    @property
    def sound_switch_volume(self):
        """
        Get/Set Volume.

        :param value: volume
        :type value: str

        :return: volume
        :rtype: str

        """
        return self.values.sound_switch_volume.data

    @sound_switch_volume.setter
    def sound_switch_volume(self, value):
        self.values.sound_switch_volume.data = value

    @property
    def sound_switch_tone_count(self):
        """
        :rtype: int
        """
        return self.values.sound_switch_tone_count.data

    @property
    def sound_switch_default_tone(self):
        """
        :rtype: str
        """
        return self.values.sound_switch_default_tone.data

    @property
    def sound_switch_tone(self):
        """
        Get/Set Tone.

        :param value: one of :py:attr:`tone_items`
        :type value: str

        :return: one of :py:attr:`tone_items`
        :rtype: str
        """
        return self.values.sound_switch_tone.data

    @sound_switch_tone.setter
    def sound_switch_tone(self, value):
        self.values.sound_switch_tone.data = value

    @property
    def sound_switch_tone_items(self):
        """
        Tone Items

        :return: list of tone items
        :rtype: List[str]
        """
        return self.values.sound_switch_tone.data_items

    @property
    def as_dict(self):
        return dict(
            sound_switch_tone=self.sound_switch_tone,
            sound_switch_default_tone=self.sound_switch_default_tone,
            sound_switch_tone_items=self.sound_switch_tone_items,
            sound_switch_tone_count=self.sound_switch_tone_count,
            sound_switch_volume=self.sound_switch_volume
        )
