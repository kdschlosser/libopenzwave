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
:synopsis: COMMAND_CLASS_DEVICE_RESET_LOCALLY

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Device Reset Locally Command Class - Active
# Management
COMMAND_CLASS_DEVICE_RESET_LOCALLY = 0x5A


# noinspection PyAbstractClass
class DeviceResetLocally(zwave_cmd_class.ZWaveCommandClass):
    """
    Device Reset Locally Command Class

    symbol: `COMMAND_CLASS_DEVICE_RESET_LOCALLY`
    """

    class_id = COMMAND_CLASS_DEVICE_RESET_LOCALLY
    class_desc = 'COMMAND_CLASS_DEVICE_RESET_LOCALLY'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        pass
