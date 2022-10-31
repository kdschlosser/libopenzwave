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
:synopsis: COMMAND_CLASS_SWITCH_TOGGLE_BINARY

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Binary Toggle Switch Command Class - Obsolete
# Application
COMMAND_CLASS_SWITCH_TOGGLE_BINARY = 0x28


# noinspection PyAbstractClass
class SwitchToggleBinary(zwave_cmd_class.ZWaveCommandClass):
    """
    Switch Toggle Binary Command Class

    symbol: `COMMAND_CLASS_SWITCH_TOGGLE_BINARY`
    """

    class_id = COMMAND_CLASS_SWITCH_TOGGLE_BINARY
    class_desc = 'COMMAND_CLASS_SWITCH_TOGGLE_BINARY'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        toggle_binary_switch = 0

    def switch_toggle(self):
        """
        :rtype: None
        """
        self.values.toggle_binary_switch.data = True
