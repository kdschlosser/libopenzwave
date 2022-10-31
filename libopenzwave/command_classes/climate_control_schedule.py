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
:synopsis: COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE

.. moduleauthor:: Kevin G Schlosser
"""

from . import zwave_cmd_class

# Climate Control Schedule Command Class - Depreciated
# Application
COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE = 0x46


def _remap(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min

    return (
        (((value - old_min) * new_range) / old_range) + new_min
    )


class _ScheduleSingleton(type):
    _instances = {}

    def __call__(cls, parent_node, hour, minute, value, index):

        if index is None:
            return super(_ScheduleSingleton, cls).__call__(
                parent_node,
                hour,
                minute,
                value,
                index
            )

        key = (parent_node, hour, minute, value)

        if key not in _ScheduleSingleton._instances:
            cls._instances[key] = (
                super(_ScheduleSingleton, cls).__call__(
                    parent_node,
                    hour,
                    minute,
                    value,
                    index
                )
            )

        instance = cls._instances[key]
        if instance.id is None:
            instance = (
                super(_ScheduleSingleton, cls).__call__(
                    parent_node,
                    hour,
                    minute,
                    value,
                    index
                )
            )

            cls._instances[key] = instance

        return instance


class Schedule(object, metaclass=_ScheduleSingleton):
    """
    This class represents a Climate Control Schedule
    """
    _id_count = 0

    def __init__(self, parent_node, hour, minute, value, index):
        self._node = parent_node
        self._value = value
        Schedule._id_count += 1
        self._id = Schedule._id_count
        self._index = index
        self._hour = hour
        self._minute = minute
        self._setback = None

    @property
    def parent_node(self):
        """
        The Parent node of this schedule

        :return: parent node
        :rtype: :py:class:`libopenzwave.node.ZWaveNode` instance
        """
        return self._node

    @property
    def home_id(self):
        """
        The id of the network this schedule belongs to

        :return: home id
        :rtype: int
        """
        return self.network.home_id

    @property
    def network(self):
        """
        The Network containing of this schedule

        :return: parent node
        :rtype: :py:class:`libopenzwave.network.ZWaveNetwork` instance
        """
        return self.parent_node.network

    @property
    def id(self):
        """
        The unique id of this schedule

        :return: id
        :rtype: int, Optional
        """
        return self._id

    def remove(self):
        """
        Remove this schedule item

        :return: `None`
        :rtype: None
        """
        data = self.__get_data()
        if data is None:
            return False

        if self.network.manager.RemoveSwitchPoint(self._value.id, *data[:-1]):
            self._id = None
            return True
        return False

    @property
    def day(self):
        """
        The day the schedule is to run on

        :return: day
        :rtype: str
        """
        return self._value.label

    def __get_data(self):
        if self._id is None:
            return None

        return self.network.manager.GetSwitchPoint(self._value.id, self._index)

    def __set_data(self, hour=None, minute=None, setback=None):

        if self._id is None:
            return False

        data = self.__get_data()
        if data is not None:
            self.network.manager.RemoveSwitchPoint(self._value.id, *data[:-1])
            self._hour, self._minute, self._setback = data

        if hour is None and self._hour is not None:
            hour = self._hour
        if minute is None and self._minute is not None:
            minute = self._minute
        if setback is None and self._setback is not None:
            setback = self._setback

        self._hour = hour
        self._minute = minute
        self._setback = setback

        if None in (hour, minute, setback):
            return False

        res = self.network.manager.SetSwitchPoint(
            self._value.id,
            hour,
            minute,
            setback
        )

        if not res:
            return False

        num_switch_points = (
            self.network.manager.GetNumSwitchPoints(self._value.id)
        )

        for i in range(num_switch_points):
            switch_point = (
                self.network.manager.GetSwitchPoint(self._value.id, i)
            )

            if switch_point is None:
                continue

            if switch_point == (hour, minute, setback):
                new_schedule = Schedule(
                    self._node,
                    hour,
                    minute,
                    self._value,
                    i
                )
                self.__dict__.update(new_schedule.__dict__)
                return True
        else:
            raise RuntimeError(
                'Set switch point error (This is not supposed to happen)'
            )

    @property
    def scale(self):
        """
        Get/Set the scale used for the degrees.

            * `"Celsius"`
            * `"Fahrenheit"`

        :param value: scale
        :type value: str

        :return: scale
        :rtype: str
        """
        return self._value.unit

    @scale.setter
    def scale(self, value):
        """
        :type value: str
        """
        self._value.unit = value

    @property
    def hour(self):
        """
        Get/Set the hour to run the schedule.

        24 hour clock. 0 to 23

        :param value: minute
        :type value: int

        :return: the hour
        :rtype: int
        """
        data = self.__get_data()
        if data is None:
            return None

        return data[0]

    @hour.setter
    def hour(self, value):
        """
        :type value: int
        """
        if 23 >= value >= 0:
            self.__set_data(hour=value)

    @property
    def minute(self):
        """
        Get/Set the minute in the hour to run the schedule.

        This ranges from 0 to 59

        :param value: minute
        :type value: int

        :return: the minute
        :rtype: int
        """
        data = self.__get_data()
        if data is None:
            return None

        return data[1]

    @minute.setter
    def minute(self, value):
        """
        :type value: int
        """
        if 59 >= value >= 0:
            self.__set_data(minute=value)

    @property
    def setback(self):
        """
        How many degrees to alter the current setpoint

        for Celsius you can adjust +- 1.2 degrees

        for Fahrenheit you can adjust +- 2.0 degrees

        :param value: the degrees to change
        :type value: float

        :return: the setback
        :rtype: float
        """
        data = self.__get_data()
        if data is None:
            return None

        setback = data[2]
        if setback >= 121:
            return None

        setback = float(setback) / 10.0
        setback += 273.5

        if self.scale.startswith('F'):
            setback = _remap(setback, -120.0, 120.0, -200.0, 200.0)

        return round(setback / 100.0)

    @setback.setter
    def setback(self, value):
        """
        :type value: float
        """
        if self.scale.startswith('F'):
            value = _remap(value, -2.0, 2.0, -1.1, 1.1)

        value = int(round(value * 100.0))

        self.__set_data(setback=value)

    @property
    def frost_protection(self):
        """
        Get/Set frost protection schedule item

        This is a pre defined setback in the device.

        :param value: `True` to enable, `False` to disable
        :type value: bool

        :return: 'True` if enabled, `False` if not
        :rtype: bool
        """
        data = self.__get_data()
        if data is None:
            return False

        return data[2] == 121

    @frost_protection.setter
    def frost_protection(self, value):
        """
        :type value: bool
        """
        if value:
            self.__set_data(setback=121)
        else:
            self.__set_data(setback=0)

    @property
    def energy_saving(self):
        """
        Get/Set energy saving schedule item

        This is a pre defined setback in the device.

        :param value: `True` to enable, `False` to disable
        :type value: bool

        :return: 'True` if enabled, `False` if not
        :rtype: bool
        """
        data = self.__get_data()
        if data is None:
            return False

        return data[2] == 122

    @energy_saving.setter
    def energy_saving(self, value):
        """
        :type value: bool
        """
        if value:
            self.__set_data(setback=122)
        else:
            self.__set_data(setback=0)


# noinspection PyAbstractClass
class ClimateControlSchedule(zwave_cmd_class.ZWaveCommandClass):
    """
    Climate Control Schedule Command Class

    symbol: `COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE`
    """

    class_id = COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE
    class_desc = 'COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        cc_schedule_monday = 1
        cc_schedule_tuesday = 2
        cc_schedule_wednesday = 3
        cc_schedule_thursday = 4
        cc_schedule_friday = 5
        cc_schedule_saturday = 6
        cc_schedule_sunday = 7
        cc_schedule_override_state = 8
        cc_schedule_override_setback = 9

    def climate_control_schedule_create(self, day):
        """
        Create a new schedule entry

        You will need to specify what day you wish to have the schedule run on.
        a list of the day names can be gotten using
        :py:meth:`climate_control_schedule_day_names`

        This is going to create an empty schedule item. Once the hour minute
        and setback have been supplied then the new schedule item will be
        added to the node.

        :param day: the day name
        :type day: str

        :return: new schedule item
        :rtype: Schedule
        """
        for value in (
            self.values.cc_schedule_monday,
            self.values.cc_schedule_tuesday,
            self.values.cc_schedule_wednesday,
            self.values.cc_schedule_thursday,
            self.values.cc_schedule_friday,
            self.values.cc_schedule_saturday,
            self.values.cc_schedule_sunday
        ):
            if value.label == day:
                return Schedule(self, None, None, value, None)

    @property
    def climate_control_schedule_day_names(self):
        """
        The names of the days.

        :return: a list of the day names. The first day is Monday and the
            last is Sunday
        :rtype: List[str]
        """

        return [
            self.values.cc_schedule_monday.label,
            self.values.cc_schedule_tuesday.label,
            self.values.cc_schedule_wednesday.label,
            self.values.cc_schedule_thursday.label,
            self.values.cc_schedule_friday.label,
            self.values.cc_schedule_saturday.label,
            self.values.cc_schedule_sunday.label
        ]

    @property
    def climate_control_schedule_monday(self):
        """
        Monday climate schedules.

        :return: list of :py:class:`Schedule` instances
        :rtype: List[Schedule]
        """
        res = []
        value_id = self.values.cc_schedule_monday.id
        for i in range(self.network.manager.GetNumSwitchPoints(value_id)):
            setpoint = (
                self.network.manager.GetSwitchPoint(value_id, i)
            )
            if setpoint is None:
                continue

            res += [
                Schedule(
                    self,
                    setpoint[0],
                    setpoint[1],
                    self.values.cc_schedule_monday,
                    i
                )
            ]
        return res

    @property
    def climate_control_schedule_tuesday(self):
        """
        Tuesday climate schedules.

        :return: list of :py:class:`Schedule` instances
        :rtype: List[Schedule]
        """
        res = []
        value_id = self.values.cc_schedule_tuesday.id
        for i in range(self.network.manager.GetNumSwitchPoints(value_id)):
            setpoint = (
                self.network.manager.GetSwitchPoint(value_id, i)
            )
            if setpoint is None:
                continue

            res += [
                Schedule(
                    self,
                    setpoint[0],
                    setpoint[1],
                    self.values.cc_schedule_tuesday,
                    i
                )
            ]
        return res

    @property
    def climate_control_schedule_wednesday(self):
        """
        Wednesday climate schedules.

        :return: list of :py:class:`Schedule` instances
        :rtype: List[Schedule]
        """
        res = []
        value_id = self.values.cc_schedule_wednesday.id
        for i in range(self.network.manager.GetNumSwitchPoints(value_id)):
            setpoint = (
                self.network.manager.GetSwitchPoint(value_id, i)
            )
            if setpoint is None:
                continue

            res += [
                Schedule(
                    self,
                    setpoint[0],
                    setpoint[1],
                    self.values.cc_schedule_wednesday,
                    i
                )
            ]
        return res

    @property
    def climate_control_schedule_thursday(self):
        """
        Thursday climate schedules.

        :return: list of :py:class:`Schedule` instances
        :rtype: List[Schedule]
        """
        res = []
        value_id = self.values.cc_schedule_thursday.id
        for i in range(self.network.manager.GetNumSwitchPoints(value_id)):
            setpoint = (
                self.network.manager.GetSwitchPoint(value_id, i)
            )
            if setpoint is None:
                continue

            res += [
                Schedule(
                    self,
                    setpoint[0],
                    setpoint[1],
                    self.values.cc_schedule_thursday,
                    i
                )
            ]
        return res

    @property
    def climate_control_schedule_friday(self):
        """
        Friday climate schedules.

        :return: list of :py:class:`Schedule` instances
        :rtype: List[Schedule]
        """
        res = []
        value_id = self.values.cc_schedule_friday.id
        for i in range(self.network.manager.GetNumSwitchPoints(value_id)):
            setpoint = (
                self.network.manager.GetSwitchPoint(value_id, i)
            )
            if setpoint is None:
                continue

            res += [
                Schedule(
                    self,
                    setpoint[0],
                    setpoint[1],
                    self.values.cc_schedule_friday,
                    i
                )
            ]
        return res

    @property
    def climate_control_schedule_saturday(self):
        """
        Saturday climate schedules.

        :return: list of :py:class:`Schedule` instances
        :rtype: List[Schedule]
        """
        res = []
        value_id = self.values.cc_schedule_saturday.id
        for i in range(self.network.manager.GetNumSwitchPoints(value_id)):
            setpoint = (
                self.network.manager.GetSwitchPoint(value_id, i)
            )
            if setpoint is None:
                continue

            res += [
                Schedule(
                    self,
                    setpoint[0],
                    setpoint[1],
                    self.values.cc_schedule_saturday,
                    i
                )
            ]
        return res

    @property
    def climate_control_schedule_sunday(self):
        """
        Sunday climate schedules.

        :return: list of :py:class:`Schedule` instances
        :rtype: List[Schedule]
        """
        res = []
        value_id = self.values.cc_schedule_sunday.id
        for i in range(self.network.manager.GetNumSwitchPoints(value_id)):
            setpoint = (
                self.network.manager.GetSwitchPoint(value_id, i)
            )
            if setpoint is None:
                continue

            res += [
                Schedule(
                    self,
                    setpoint[0],
                    setpoint[1],
                    self.values.cc_schedule_sunday,
                    i
                )
            ]
        return res

    def climate_control_schedule_set_override(
        self,
        override_type,
        override_setback
    ):
        """
        Overrides the current climate schedule.

        :param override_type: one of
            :py:attr:`ClimateControlSchedule.climate_schedule_override_type_items`
        :type override_type: str

        :param override_setback: the degrees to change. eg:
            `0.2`, `-0.2`, `-1.0`

            for Celsius you can adjust +- 1.2 degrees
            for Fahrenheit you can adjust +- 2.0 degrees

        :type override_setback: float

        :return: `None`
        :rtype: None
        """
        if self.values.monday.unit.startswith('F'):
            override_setback = _remap(override_setback, -2.0, 2.0, -1.2, 1.2)

        override_setback = int(round(override_setback * 100.0))

        self.values.cc_schedule_override_state.data = override_type
        self.values.cc_schedule_override_setback.data = override_setback

    def climate_control_schedule_get_override(self):
        """
        Overrides the current climate schedule.

        :return: tuple of (override type, setback)
        :rtype: Tuple[str, float]
        """
        override_setback = self.values.cc_schedule_override_setback.data
        override_type = self.values.cc_schedule_override_state.data

        if self.values.monday.unit.startswith('F'):
            override_setback = _remap(override_setback, -120, 120, -200, 200)

        override_setback /= 100.0

        return override_type, override_setback

    @property
    def climate_control_schedule_override_type_items(self):
        """
        Allowed override types

        :return: list of allowed override types
        :rtype: List[str]
        """
        return self.values.cc_schedule_override_state.data_list
