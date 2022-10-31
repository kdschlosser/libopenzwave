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
from libc.stdint cimport int32_t
from libcpp cimport bool
from mylibc cimport string

cdef extern from "Options.h" namespace "OpenZWave":
    # noinspection PyClassicStyleClass,PyMissingOrEmptyDocstring,PyPep8Naming
    cdef cppclass Options:
        bool Lock() except +
        bool AreLocked() except +
        bool Destroy() except +
        bool AddOptionBool(string name, bool default ) except +
        bool AddOptionInt(string name, int32_t default ) except +
        bool AddOptionString(string name, string default, bool append ) except +
        bool GetOptionAsBool(string name, bool* o_option ) except +
        bool GetOptionAsInt(string name, int32_t* o_option ) except +
        bool GetOptionAsString(string name, string* o_option) except +
        OptionType GetType(string name) except +

    ctypedef enum OptionType:
        OptionType_Invalid = 0
        OptionType_Bool = 1
        OptionType_Int = 2
        OptionType_String = 3

cdef extern from "Options.h" namespace "OpenZWave::Options":
    # noinspection PyMissingOrEmptyDocstring,PyPep8Naming
    Options* Create(string a, string b, string c)
