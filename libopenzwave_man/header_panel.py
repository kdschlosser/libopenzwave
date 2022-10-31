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


class HeaderPanel(wx.Panel):

    def __init__(self, parent, label, font_size=8):
        self.parent = parent
        wx.Panel.__init__(self, parent, -1)

        label_ctrl = wx.StaticText(self, -1, label)
        font = wx.Font(
            font_size,
            wx.FONTFAMILY_SWISS,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD
        )

        label_ctrl.SetFont(font)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(label_ctrl, 0, wx.ALIGN_LEFT | wx.ALL, 15)

        line = wx.StaticLine(self, -1, size=(0, 5))

        main_sizer.Add(line, 0, wx.ALL, 5)

        self.SetSizer(main_sizer)
        self.SetAutoLayout(True)
        main_sizer.Fit(self)
        main_sizer.Layout()
        self.Layout()
