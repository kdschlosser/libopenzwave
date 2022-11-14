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
:synopsis: COMMAND_CLASS_LOCK

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Lock Command Class - Depreciated
# Application
COMMAND_CLASS_LOCK = 0x76


# noinspection PyAbstractClass
class Lock(zwave_cmd_class.ZWaveCommandClass):
    """
    Lock Command Class

    symbol: `COMMAND_CLASS_LOCK`
    """

    class_id = COMMAND_CLASS_LOCK
    class_desc = 'COMMAND_CLASS_LOCK'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        lock_locked = 0

    @property
    def lock_locked(self):
        """
        Get/Set Lock Locked

        :param value: state `True`/`False`
        :type value: bool

        :return: `True`/`False`
        :rtype: bool
        """
        return self.values.lock_locked.data

    @lock_locked.setter
    def lock_locked(self, value):
        self.values.lock_locked.data = value
