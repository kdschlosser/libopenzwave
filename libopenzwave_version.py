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

import sys

libopenzwave_version = '0.5.0'

if "-" in libopenzwave_version:
    libopenzwave_version_short = libopenzwave_version.split("-")
else:
    libopenzwave_version_short = libopenzwave_version


ozw_version = (1, 6)


class DynamicModule(object):

    def __init__(self):
        mod = sys.modules[__name__]
        self.__name__ = __name__
        self.__module__ = mod.__module__
        self.__package__ = mod.__package__
        self.__file__ = mod.__package__
        self.__loader__ = mod.__loader__
        self.__spec__ = mod.__spec__
        self.__original_module__ = mod

        sys.modules[__name__] = self

    def __setattr__(self, key, value):
        try:
            attr = getattr(DynamicModule, key)
            if not isinstance(attr, property):
                raise AttributeError

            if attr.fset is None:
                raise RuntimeError

            attr.fset(self, value)
            return

        except AttributeError:
            pass

        except RuntimeError:
            raise AttributeError(key)

        object.__setattr__(self, key, value)

    def __getattr__(self, item):
        try:
            value = getattr(DynamicModule, item)
            if not isinstance(value, property):
                raise AttributeError

            return value.fget(self)

        except AttributeError:
            pass

        if item in self.__dict__:
            return self.__dict__[item]

        return getattr(self.__original_module__, item)

    @property
    def OZW_VERSION_MAJ(self):
        return str(ozw_version[0])

    @property
    def OZW_VERSION_MIN(self):
        return str(ozw_version[1])

    @property
    def OZW_VERSION(self):
        return '.'.join(str(item) for item in ozw_version[:2])

    @property
    def OZW_VERSION_REV(self):
        if len(ozw_version) == 3:
            return str(ozw_version[2])
        else:
            return '-1'

    @OZW_VERSION_REV.setter
    def OZW_VERSION_REV(self, value):
        global ozw_version

        ozw_version = ozw_version[:2] + (int(value),)


_dynamic_module = DynamicModule()

OZW_VERSION_MAJ = ''
OZW_VERSION_MIN = ''
OZW_VERSION_REV = ''
OZW_VERSION = ''


if __name__ == '__main__':
    print(libopenzwave_version)

