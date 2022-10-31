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

cdef extern from "Python.h":
    # noinspection PyMissingOrEmptyDocstring,PyPep8Naming
    void PyEval_InitThreads()
    # noinspection PyMissingOrEmptyDocstring,PyPep8Naming
    void Py_Initialize()

cdef extern from *:
    ctypedef char* const_char_ptr "const char*"

cdef extern from "<string>" namespace "std":
    # noinspection PyClassicStyleClass,PyMissingOrEmptyDocstring,PyPep8Naming
    cdef cppclass string:
        string()
        string(char *)
        string (size_t n, char c)
        char * c_str()
