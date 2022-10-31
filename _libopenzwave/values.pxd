# -*- coding: utf-8 -*-
"""
This file is part of **libopenzwave** project

License : GPL(v3)

**libopenzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**libopenzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with libopenzwave. If not, see http://www.gnu.org/licenses.

"""
from libc.stdint cimport uint32_t, uint64_t, uint8_t, uint16_t
from mylibc cimport string


cdef extern from "ValueID.h" namespace "OpenZWave::ValueID":

    cdef enum ValueGenre:
        # The 'level' as controlled by basic commands.  Usually duplicated
        # by another command class.
        ValueGenre_Basic = 0
        # Basic values an ordinary user would be interested in.
        ValueGenre_User = 1
        # Device-specific configuration parameters.  These cannot be
        # automatically discovered via Z-Wave, and are usually described in
        # the user manual instead.
        ValueGenre_Config = 2
        # Values of significance only to users who understand the Z-Wave
        # protocol.
        ValueGenre_System = 3
        # A count of the number of genres defined.  Not to be used as a
        # genre itself.
        ValueGenre_Count = 4

    cdef enum ValueType:
        # Boolean, true or false
        ValueType_Bool = 0
        # 8-bit unsigned value
        ValueType_Byte = 1
        # Represents a non-integer value as a string, to avoid floating point
        # accuracy issues.
        ValueType_Decimal = 2
        # 32-bit signed value
        ValueType_Int = 3
        # List from which one item can be selected
        ValueType_List = 4
        # Complex type used with the Climate Control Schedule command class
        ValueType_Schedule = 5
        # 16-bit signed value
        ValueType_Short = 6
        # Text string
        ValueType_String = 7
        # A write-only value that is the equivalent of pressing a button to
        # send a command to a device
        ValueType_Button = 8
        # Used as a list of Bytes
        ValueType_Raw = 9
        # Bitset
        ValueType_BitSet = 10
        # The highest-number type defined.  Not to be used as a type itself.
        ValueType_Max = ValueType_BitSet


cdef extern from "ValueID.h" namespace "OpenZWave":
    # noinspection PyClassicStyleClass,PyMissingOrEmptyDocstring,PyPep8Naming
    cdef cppclass ValueID:
        uint32_t GetHomeId() except +
        uint8_t GetNodeId() except +
        ValueGenre GetGenre() except +
        uint8_t GetCommandClassId() except +
        uint8_t GetInstance() except +
        uint16_t GetIndex() except +
        ValueType GetType() except +
        uint64_t GetId() except +
        string GetTypeAsString() except +
        string GetGenreAsString() except +
