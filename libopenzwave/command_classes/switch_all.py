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
:synopsis: COMMAND_CLASS_SWITCH_ALL

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# All Switch Command Class - Obsolete
# Application
COMMAND_CLASS_SWITCH_ALL = 0x27


# noinspection PyAbstractClass
class SwitchAll(zwave_cmd_class.ZWaveCommandClass):
    """
    Switch All Command Class

    symbol: `COMMAND_CLASS_SWITCH_ALL`
    """

    class_id = COMMAND_CLASS_SWITCH_ALL
    class_desc = 'COMMAND_CLASS_SWITCH_ALL'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        switch_all = 0

    @property
    def switch_all(self):
        """
        Gets/Sets Switch All

        :param value: one of :py:attr:`switch_all_items`
        :type value: str

        :return: one of :py:attr:`switch_all_items`
        :rtype: str
        """
        return self.values.switch_all.data

    @switch_all.setter
    def switch_all(self, value):
        self.values.switch_all.data = value

    @property
    def switch_all_items(self):
        """
        Allowed Switch All values

        :return: list of allowed values
        :rtype: List[str]
        """
        return self.values.switch_all.data_items

    @property
    def as_dict(self):
        return dict(
            switch_all=self.switch_all,
            switch_all_items=self.switch_all_items,
        )
