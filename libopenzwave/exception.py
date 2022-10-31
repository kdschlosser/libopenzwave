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
:synopsis: python-openzwave exception classes

.. moduleauthor:: Kevin G Schlosser
"""


# i changed how the exceptions work. because of the identical nature of
# everything except for the msg variable. we can simply set that at the class
# level and it will override the one that is in  ZWaveException. it removes the
# need for a bunch of duplicate code.
class ZWaveException(Exception):
    """
    Z-Wave Generic Exception
    """

    def __init__(self, value):
        """
        :param value:
        """
        self.value = value

    def __str__(self):
        try:
            return repr(self.__doc__ + b' : ' + self.value)
        except UnicodeError:
            return repr(self.__doc__ + b' : ' + self.value.decode('utf-8'))


class ZWaveCacheException(ZWaveException):
    """
    Z-Wave Cache Exception
    """


class ZWaveTypeException(ZWaveException):
    """
    Z-Wave Type Exception
    """


class ZWaveCommandClassException(ZWaveException):
    """
    Z-Wave Command Class Exception
    """
