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
:synopsis: COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Association Command Configuration Command Class - Active
# Management
COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION = 0x9B


# noinspection PyAbstractClass
class AssociationCommandConfiguration(zwave_cmd_class.ZWaveCommandClass):
    """
    Association Command Configuration Command Class

    symbol: `COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION`
    """

    class_id = COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION
    class_desc = 'COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        max_command_length = 0
        commands_are_values = 1
        commands_are_configurable = 2
        num_free_commands = 3
        max_commands = 4

    @property
    def association_max_command_length(self):
        """
        Association Max Command Length

        :return: maximum command length
        :rtype: int
        """
        return self.values.max_command_length.data

    @property
    def association_commands_are_values(self):
        """
        Association Commands are Values

        :return: `True`/`False`
        :rtype: bool
        """
        return self.values.commands_are_values.data

    @property
    def association_commands_are_configurable(self):
        """
        Association Commands are Configurable

        :return: `True`/`False`
        :rtype: bool
        """
        return self.values.commands_are_configurable.data

    @property
    def association_free_commands(self):
        """
        Association Free Commands

        :return: number of free commands
        :rtype: int
        """
        return self.values.num_free_commands.data

    @property
    def association_max_commands(self):
        """
        Association Max Commands

        :return: total number of association commands available
        :rtype: int
        """
        return self.values.max_commands.data
