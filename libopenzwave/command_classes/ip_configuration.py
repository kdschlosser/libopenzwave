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
:synopsis: COMMAND_CLASS_IP_CONFIGURATION

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# IP Configuration Command Class - Obsolete
# Management
COMMAND_CLASS_IP_CONFIGURATION = 0x9A


# noinspection PyAbstractClass
class IPConfiguration(zwave_cmd_class.ZWaveCommandClass):
    """
    IP Configuration Command Class

    symbol: `COMMAND_CLASS_IP_CONFIGURATION`
    """

    class_id = COMMAND_CLASS_IP_CONFIGURATION
    class_desc = 'COMMAND_CLASS_IP_CONFIGURATION'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        pass
