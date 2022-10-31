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
:synopsis: COMMAND_CLASS_PROTECTION

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Protection Command Class - Active
# Application
COMMAND_CLASS_PROTECTION = 0x75


# noinspection PyAbstractClass
class Protection(zwave_cmd_class.ZWaveCommandClass):
    """
    Protection Command Class

    symbol: `COMMAND_CLASS_PROTECTION`
    """

    class_id = COMMAND_CLASS_PROTECTION
    class_desc = 'COMMAND_CLASS_PROTECTION'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        protection = 0
    
    @property
    def protection(self):
        """
        Get/Set Protection

        :param value: one of :py:attr:`protection_items`
        :type value: str

        :return: one of :py:attr:`protection_items`
        :rtype: str
        """
        return self.values.protection.data

    @protection.setter
    def protection(self, value):
        self.values.protection.data = value

    @property
    def protection_items(self):
        """
        Protection Items

        :return: list of allowed protection values.
        :rtype: List[str]
        """
        return self.values.protection.data_items
