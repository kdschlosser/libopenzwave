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

cdef extern from "Log.h" namespace "OpenZWave":

    cdef enum LogLevel:
        # Disable all logging
        LogLevel_None = 0
        # These messages should always be shown
        LogLevel_Always = 1
        # A likely fatal issue in the library
        LogLevel_Fatal = 2
        # A serious issue with the library or the network
        LogLevel_Error = 3
        # A minor issue from which the library should be able to recover
        LogLevel_Warning = 4
        # Something unexpected by the library about which the controlling
        # application should be aware
        LogLevel_Alert = 5
        # Everything's working fine...these messages provide streamlined
        # feedback on each message
        LogLevel_Info = 6
        # Detailed information on the progress of each message
        LogLevel_Detail = 7
        # Very detailed information on progress that will create a huge log
        # file quickly. But this level (as others) can be queued and sent to
        # the log only on an error or warning
        LogLevel_Debug = 8
        # Will include low-level byte transfers from controller to buffer to
        # application and back
        LogLevel_StreamDetail = 9
        # Used only within the log class (uses existing timestamp, etc.)
        LogLevel_Internal = 10
