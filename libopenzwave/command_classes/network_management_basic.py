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
:synopsis: COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Network Management Basic Node Command Class - Active
# Network-Protocol
COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC = 0x4D


# noinspection PyAbstractClass
class NetworkManagementBasic(zwave_cmd_class.ZWaveCommandClass):
    """
    Network Management Basic Command Class

    symbol: `COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC`
    """

    class_id = COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC
    class_desc = 'COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        pass
