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
:synopsis: COMMAND_CLASS_VERSION

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Version Command Class - Active
# Management
COMMAND_CLASS_VERSION = 0x86


# noinspection PyAbstractClass
class Version(zwave_cmd_class.ZWaveCommandClass):
    """
    Version Command Class

    symbol: `COMMAND_CLASS_VERSION`
    """

    class_id = COMMAND_CLASS_VERSION
    class_desc = 'COMMAND_CLASS_VERSION'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        version_library = 0
        version_protocol = 1
        version_application = 2

    @property
    def library_version(self):
        """
        Library Version

        :rtype: str
        """
        return self.values.version_library.data

    @property
    def protocol_version(self):
        """
        ZWave Protocol Version

        :rtype: str
        """
        return self.values.version_protocol.data

    @property
    def application_version(self):
        """
        Application Version

        :rtype: str
        """
        return self.values.version_application.data
