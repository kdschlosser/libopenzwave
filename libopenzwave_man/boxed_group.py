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
# You should have received a copy of the GNU General Public License
# along with libopenzwave. If not, see http://www.gnu.org/licenses.

"""
This file is part of the **libopenzwave** project

:platform: Unix, Windows, OSX
:license: GPL(v3)

.. moduleauthor:: Kevin G Schlosser
"""

import wx


class BoxedGroup(wx.StaticBoxSizer):
    def __init__(self, parent, label="", *items):
        staticBox = wx.StaticBox(parent, -1, label)
        wx.StaticBoxSizer.__init__(self, staticBox, wx.VERTICAL)

        for item in items:
            if isinstance(item, tuple):
                self.Add(*item)
            else:
                self.Add(item)
