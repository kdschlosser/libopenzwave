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
:synopsis: COMMAND_CLASS_BASIC_WINDOW_COVERING

.. moduleauthor:: Kevin G Schlosser
"""


from . import zwave_cmd_class

# Basic Window Covering Command Class - Obsolete
# Application
COMMAND_CLASS_BASIC_WINDOW_COVERING = 0x50


# noinspection PyAbstractClass
class BasicWindowCovering(zwave_cmd_class.ZWaveCommandClass):
    """
    Basic Window Covering Command Class

    symbol: `COMMAND_CLASS_BASIC_WINDOW_COVERING`
    """

    class_id = COMMAND_CLASS_BASIC_WINDOW_COVERING
    class_desc = 'COMMAND_CLASS_BASIC_WINDOW_COVERING'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        open = 0
        close = 1

    def window_covering_open(self):
        """
        Open Window Covering
        :rtype: None
        """
        self.values.open.data = True

    @property
    def is_window_covering_opening(self):
        """
        Checks if the window covering is opening.

        :return: `True` if it is opening
        :rtype: bool
        """
        return self.values.open.data

    def window_covering_close(self):
        """
        Close Window Covering

        :return: `None`
        :rtype: None
        """
        self.values.close.data = True

    @property
    def is_window_covering_closing(self):
        """
        Checks if the window covering is closing.

        :return: `True` if it is closing
        :rtype: bool
        """
        return self.values.close.data
