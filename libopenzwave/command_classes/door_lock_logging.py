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
:synopsis: COMMAND_CLASS_DOOR_LOCK_LOGGING

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Door Lock Logging Command Class - Active
# Application
COMMAND_CLASS_DOOR_LOCK_LOGGING = 0x4C


# noinspection PyAbstractClass
class DoorLockLogging(zwave_cmd_class.ZWaveCommandClass):
    """
    Door Lock Logging Command Class

    symbol: `COMMAND_CLASS_DOOR_LOCK_LOGGING`
    """

    class_id = COMMAND_CLASS_DOOR_LOCK_LOGGING
    class_desc = 'COMMAND_CLASS_DOOR_LOCK_LOGGING'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        door_lock_log_max_records = 0
        door_lock_log_record_no = 1
        door_lock_log_record = 2

    @property
    def doorlock_logging_max_records(self):
        """
        Door Lock Logging Max Number of Records

        :return: max number of records
        :rtype: int
        """
        return self.values.door_lock_log_max_records.data

    @property
    def doorlock_logging_current_record_number(self):
        """
        Door Lock Logging Current Record Number

        :param value: record number
        :type value: int

        :return: record number
        :rtype: int
        """
        return self.values.door_lock_log_record_no.data

    @doorlock_logging_current_record_number.setter
    def doorlock_logging_current_record_number(self, value):
        self.values.door_lock_log_record_no.data = value

    @property
    def doorlock_logging_records(self):
        """
        Door Lock Logging Records

        List of door lock change records

        :return: list of records
        :rtype: List[Any]
        """

        res = []
        for i in range(self.doorlock_logging_max_records):
            res += [self.doorlock_logging_log_record(i)]

        return res

    def doorlock_logging_log_record(self, record_num):
        """
        Door Lock Logging Record

        :param record_num: record number to retrieve
        :type record_num: int

        :return: logging entry
        :rtype: str
        """

        if record_num <= self.doorlock_logging_max_records:
            self.doorlock_logging_current_record_number = record_num

        return self.values.door_lock_log_record.data
