# -*- coding: utf-8 -*-

# License : GPL(v3)
#
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

This file is part of **python-openzwave**
project https://github.com/OpenZWave/python-openzwave.

:platform: Unix, Windows, MacOS X
:synopsis: openzwave wrapper

.. moduleauthor:: Kevin G Schlosser

"""

from .. import singleton


ZWAVE_CMD_CLASS = 0x01


class ValueIndexMeta(type):

    def __new__(mcs, name, bases, dct):
        cls = (
            super(ValueIndexMeta, mcs).__new__(mcs, name, bases, dct)
        )

        try:
            ValueIndexes
        except NameError:
            return cls

        if cls.__doc__ is None:
            cls.__doc__ = ValueIndexes.__doc__

        if cls.__doc__ != ValueIndexes.__doc__:
            cls.__doc__ = (
                ValueIndexes.__doc__ +
                '\n'.encode('utf-8') +
                cls.__doc__
            )

        instance = cls()
        cls.__doc__ += '\n\n        '

        index_doc = []
        for key, value in instance:
            index_doc += [
                '            * `{key}`: `{value}`'.format(
                    key=key,
                    value=value
                )
            ]

        if index_doc:
            cls.__doc__ += 'Available Value ValueIndexes:\n\n'
            cls.__doc__ += '\n'.join(index_doc)
        else:
            cls.__doc__ += (
                'There are no available value indexes for this command class'
            )

        cls.__doc__ += '\n'
        return cls


class ValueIndexes(object, metaclass=ValueIndexMeta):
    """
    The Value Index class is used as a data container for the indexes
    that are attached to specific values a node has. The only way of
    identifying a value is by it's command class and it's index. a single
    node may have more then one value at the same index. Numbers are not
    the easiest thing to use as an identification and we wanted to make
    this API as easy to use as possible.

    The system that has been designed in a manner that makes it really
    easy to use but also offers the flexibility for the more advanced
    programmer.

    The values container for a node in the past has been a dictionary. This
    has not changed But there is a new "twist" I extended the functionality
    of the container so it will also be able to return a value by using
    the attribute name of the index located in this class. We have made it
    so that there are no name collisions between command classes.

    If you have a node that supports COMMAND_CLASS_SWITCH_MULTILEVEL and
    you want to access the level value directly you would use
    `node.values.level`. If you have a need to access this class directly
    to get the index numbers you would use the attribute name used
    to identify the command class you want to obtain. So using the above
    example to get the ValueIndex class
    'node.values.COMMAND_CLASS_SWITCH_MULTILEVEL`.

    You are able to iterate over the class to get (name, index) pairs.
    """

    def __iter__(self):
        res = []
        for key, value in self.__class__.__dict__.items():
            if not key.startswith('_') and isinstance(value, int):
                res += [(key, value)]

        res = sorted(res, key=lambda x: x[1])

        return iter(res)

    def __call__(self):
        return self

    def __setattr__(self, key, value):
        raise AttributeError('Changing of value indexes is not allowed')

    def __delattr__(self, item):
        raise AttributeError('Deleting if value indexes is not allowed')


# noinspection PyAbstractClass
class ZWaveCommandClass(object, metaclass=singleton.InstanceSingleton):
    """
    ZWave Command Class

    symbol: `ZWAVE_CMD_CLASS`

    This is the base class for all of the ZWave Command Classes
    There is quite a bit of complex code that is used to make the joining of
    nodes and values as easy to use as possible while still offering an API to
    be able to access the underlying components easily.

    The command classes are created dynamically when the node information is
    received from OpenZwave. once the command class structure for a node if
    received the matching command class classes are then gathered up and
    placed into the attribute __bases__. That attribute is located in the
    node instance. This is done so you have the ability to iterate over the
    parent command classes to access things like the class_id, class_desc
    attributes as well as the ValueIndexes class that houses the value indexes
    for that specific command class.
    """

    class_id = ZWAVE_CMD_CLASS
    """
    The ZWave command class id
    """
    class_desc = 'ZWAVE_CMD_CLASS'
    """
    the string representation of the class_id attribute
    """

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(ValueIndexes):
        pass

    def __init__(self):
        self._command_classes = []
        self.values = getattr(self, 'values')
        self._bases = getattr(self, '_bases')
        try:
            self.ValueIndexes = self.ValueIndexes()
        except TypeError:
            print(self._bases)
            print(self.class_desc)
            raise

    @property
    def network(self):
        raise NotImplementedError

    @property
    def id(self):
        raise NotImplementedError

    @property
    def home_id(self):
        raise NotImplementedError

    @property
    def as_dict(self):
        return {}
