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
:synopsis: COMMAND_CLASS_ZWAVEPLUS_INFO

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Z-Wave Plus Info Command Class - Active
# Management
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_ZWAVEPLUS_INFO = 0x5E


# noinspection PyAbstractClass
class ZwavePlusInfo(zwave_cmd_class.ZWaveCommandClass):
    """
    Zwave Plus Info Command Class

    symbol: `COMMAND_CLASS_ZWAVEPLUS_INFO`
    """

    class_id = COMMAND_CLASS_ZWAVEPLUS_INFO
    class_desc = 'COMMAND_CLASS_ZWAVEPLUS_INFO'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        zwave_plus_version = 0
        zwave_plus_installer_icon = 1
        zwave_plus_user_icon = 2

    @property
    def zwave_plus_version(self):
        """
        Gets the ZWave Plus Version

        :rtype: str
        """
        return self.values.zwave_plus_version.data

    @property
    def zwave_plus_installer_icon(self):
        """
        Gets the id of the installer icon.

        :rtype: int
        """
        return self.values.zwave_plus_installer_icon.data

    @property
    def zwave_plus_user_icon(self):
        """
        Gets the id of the user icon.

        :rtype: int
        """
        return self.values.zwave_plus_user_icon.data
