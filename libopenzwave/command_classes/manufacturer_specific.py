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
:synopsis: COMMAND_CLASS_MANUFACTURER_SPECIFIC

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Manufacturer Specific Command Class - Active
# Management
# Nodes MUST reply to Manufacturer Specific Get Commands received non-securely
# if S0 is the highest granted key (CC:0072.01.00.41.004)
COMMAND_CLASS_MANUFACTURER_SPECIFIC = 0x72


# noinspection PyAbstractClass
class ManufacturerSpecific(zwave_cmd_class.ZWaveCommandClass):
    """
    Manufacturer Specific Command Class

    symbol: `COMMAND_CLASS_MANUFACTURER_SPECIFIC`
    """

    class_id = COMMAND_CLASS_MANUFACTURER_SPECIFIC
    class_desc = 'COMMAND_CLASS_MANUFACTURER_SPECIFIC'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        mfg_loaded_config = 0
        mfg_local_config = 1
        mfg_latest_config = 2
        mfg_device_id = 3
        mfg_serial_number = 4

    @property
    def mfg_loaded_config(self):
        """
        :rtype: Any
        """
        return self.values.mfg_loaded_config.data

    @property
    def mfg_local_config(self):
        """
        :rtype: Any
        """
        return self.values.mfg_local_config.data

    @property
    def mfg_latest_config(self):
        """
        :rtype: Any
        """
        return self.values.mfg_latest_config.data

    @property
    def mfg_device_id(self):
        """
        :rtype: int
        """
        return self.values.mfg_device_id.data

    @property
    def mfg_serial_number(self):
        """
        :rtype: str
        """
        return self.values.mfg_serial_number.data
