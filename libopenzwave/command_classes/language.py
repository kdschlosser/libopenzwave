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
:synopsis: COMMAND_CLASS_LANGUAGE

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Language Command Class - Active
# Application
COMMAND_CLASS_LANGUAGE = 0x89


# noinspection PyAbstractClass
class Language(zwave_cmd_class.ZWaveCommandClass):
    """
    Language Command Class

    symbol: `COMMAND_CLASS_LANGUAGE`
    """

    class_id = COMMAND_CLASS_LANGUAGE
    class_desc = 'COMMAND_CLASS_LANGUAGE'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        language_language = 0
        language_country = 1

    @property
    def language(self):
        """
        Get/Set Language

        :param value: language
        :type value: str

        :return: language
        :rtype: str
        """
        return self.values.language_language.data

    @language.setter
    def language(self, value):
        self.values.language_language.data = value

    @property
    def country(self):
        """
        Get/Set Country

        :param value: country
        :type value: str

        :return: country
        :rtype: str
        """
        return self.values.language_country.data

    @country.setter
    def country(self, value):
        self.values.language_country.data = value
