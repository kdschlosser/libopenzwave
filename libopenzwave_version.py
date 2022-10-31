# -*- coding: utf-8 -*-
"""
This file is part of **libopenzwave** project
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave API

.. moduleauthor: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

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
libopenzwave_version = '0.5.0'

if "-" in libopenzwave_version:
    libopenzwave_version_short = libopenzwave_version.split("-")
else:
    libopenzwave_version_short = libopenzwave_version

ozw_version = (1, 6)

if __name__ == '__main__':
    print(libopenzwave_version)

