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
:synopsis: COMMAND_CLASS_DOOR_LOCK

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Door Lock Command Class - Active
# Application
COMMAND_CLASS_DOOR_LOCK = 0x62


# noinspection PyAbstractClass
class DoorLock(zwave_cmd_class.ZWaveCommandClass):
    """
    Door Lock Command Class

    symbol: `COMMAND_CLASS_DOOR_LOCK`
    """

    class_id = COMMAND_CLASS_DOOR_LOCK
    class_desc = 'COMMAND_CLASS_DOOR_LOCK'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        door_lock_lock = 0
        door_lock_lock_mode = 1
        door_lock_timeout_mode = 2
        door_lock_minutes = 3
        door_lock_seconds = 4
        door_lock_outside_handles = 5
        door_lock_inside_handles = 6

    @property
    def doorlock_locked(self):
        """
        Get/Set Door Lock Locked

        :param value: locked state `True`/`False`
        :type value: bool

        :return: locked state `True`/`False`
        :rtype: bool
        """

        return self.values.door_lock_lock.data

    @doorlock_locked.setter
    def doorlock_locked(self, value):
        self.values.door_lock_lock.data = value

    @property
    def doorlock_lock_mode(self):
        """
        Get/Set Door Lock Locked (Advanced)

        :param value: one of the values returned from
            :py:attr:`doorlock_lock_mode_items`
        :type value: str

        :return: one of the values returned from
            :py:attr:`doorlock_lock_mode_items`
        :rtype: str
        """
        return self.values.door_lock_lock_mode.data

    @doorlock_lock_mode.setter
    def doorlock_lock_mode(self, value):
        self.values.door_lock_lock_mode.data = value

    @property
    def doorlock_lock_mode_items(self):
        """
        Allowed Door Lock Locked modes

        :return: list of allowed modes
        :rtype: List[str]
        """
        return self.values.door_lock_lock_mode.data_items

    @property
    def doorlock_outside_handle_control(self):
        """
        Get/Set Outside Handle Control

        Controls if the outside handle functions or not.

        :param value: handle state `True`/`False`
        :type value: bool

        :return: handle state `True`/`False`
        :rtype: bool
        """
        return self.values.door_lock_outside_handles.data

    @doorlock_outside_handle_control.setter
    def doorlock_outside_handle_control(self, value):
        self.values.door_lock_outside_handles.data = value

    @property
    def doorlock_inside_handle_control(self):
        """
        Get/Set Inside Handle Control

        Controls if the inside handle functions or not.

        :param value: handle state `True`/`False`
        :type value: bool

        :return: handle state `True`/`False`
        :rtype: bool
        """
        return self.values.door_lock_inside_handles.data

    @doorlock_inside_handle_control.setter
    def doorlock_inside_handle_control(self, value):
        self.values.door_lock_inside_handles.data = value

    @property
    def doorlock_timeout_mode(self):
        """
        Get/Set Door Lock Timeout Mode

        :param value: one of the values returned from
            :py:attr:`doorlock_timeout_mode_items`
        :type value: str

        :return: one of the values returned from
            :py:attr:`doorlock_timeout_mode_items`
        :rtype: str
        """
        return self.values.door_lock_timeout_mode.data

    @doorlock_timeout_mode.setter
    def doorlock_timeout_mode(self, value):
        self.values.door_lock_timeout_mode.data = value

    @property
    def doorlock_timeout_mode_items(self):
        return self.values.door_lock_timeout_mode.data_items

    @property
    def doorlock_timeout_minutes(self):
        """
        Get/Set Door Lock Timeout Minutes

        :param value: minutes
        :type value: int

        :return: miniutes
        :rtype: int
        """
        return self.values.door_lock_minutes.data

    @doorlock_timeout_minutes.setter
    def doorlock_timeout_minutes(self, value):
        self.values.door_lock_minutes.data = value

    @property
    def doorlock_timeout_seconds(self):
        """
        Get/Set Door Lock Timeout Seconds

        :param value: seconds
        :type value: int

        :return: seconds
        :rtype: int
        """
        return self.values.door_lock_seconds.data

    @doorlock_timeout_seconds.setter
    def doorlock_timeout_seconds(self, value):
        self.values.door_lock_seconds.data = value
