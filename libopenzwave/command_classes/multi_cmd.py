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
:synopsis: COMMAND_CLASS_MULTI_CMD

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Multi Command Command Class - Active
# Transport-Encapsulation
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_MULTI_CMD = 0x8F


# noinspection PyAbstractClass
class MultiCommand(zwave_cmd_class.ZWaveCommandClass):
    """
    Multi Command Command Class

    symbol: `COMMAND_CLASS_MULTI_CMD`
    """

    class_id = COMMAND_CLASS_MULTI_CMD
    class_desc = 'COMMAND_CLASS_MULTI_CMD'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        pass
