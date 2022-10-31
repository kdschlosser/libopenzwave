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
:synopsis: COMMAND_CLASS_MANUFACTURER_PROPRIETARY

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Manufacturer proprietary Command Class - Active
# Application
COMMAND_CLASS_MANUFACTURER_PROPRIETARY = 0x91


# noinspection PyAbstractClass
class ManufacturerProprietary(zwave_cmd_class.ZWaveCommandClass):
    """
    Manufacturer Proprietary Command Class

    symbol: `COMMAND_CLASS_MANUFACTURER_PROPRIETARY`
    """

    class_id = COMMAND_CLASS_MANUFACTURER_PROPRIETARY
    class_desc = 'COMMAND_CLASS_MANUFACTURER_PROPRIETARY'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        fibaro_venetian_blinds_position = 0
        fibaro_venetian_blinds_tilt = 1

    @property
    def fibaro_blinds_position(self):
        """
        :type value: int
        :rtype: int
        """
        return self.values.fibaro_venetian_blinds_position.data

    @fibaro_blinds_position.setter
    def fibaro_blinds_position(self, value):
        self.values.fibaro_venetian_blinds_position.data = value

    @property
    def fibaro_blinds_tilt(self):
        """
        :type value: int
        :rtype: int
        """
        return self.values.fibaro_venetian_blinds_tilt.data

    @fibaro_blinds_tilt.setter
    def fibaro_blinds_tilt(self, value):
        self.values.fibaro_venetian_blinds_tilt.data = value
