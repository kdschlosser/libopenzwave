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

from . import header_panel


class ValueIndexPanel(wx.Panel):

    def __init__(self, parent, node, command_class_name):
        self.node = node

        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_SUNKEN)
        index_sizer = wx.BoxSizer(wx.HORIZONTAL)

        hp = header_panel.HeaderPanel(self, 'Values', font_size=16)
        index_sizer.Add(hp)

        index_left_sizer = wx.BoxSizer(wx.VERTICAL)
        index_right_sizer = wx.BoxSizer(wx.VERTICAL)

        index_sizer.Add(index_left_sizer, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 5)
        index_sizer.Add(index_right_sizer, 0, wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        self.ctrls = ctrls = []

        value_indexes = getattr(node.values, command_class_name)

        for i, (index_name, index) in enumerate(list(value_indexes)):
            ctrl = wx.StaticText(
                self, -1,
                index_name + ' (' + str(index) + ')'
            )

            ctrls += [ctrl]

            if i % 2:
                index_right_sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 5)
            else:
                index_left_sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 5)

        self.active_colour = wx.Colour(0, 125, 220)
        self.inactive_colour = self.GetForegroundColour()
        self.clicked_ctrl = None
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_window)

        self.SetSizer(index_sizer)

    def on_leave_window(self, evt):
        self.clicked_ctrl = None

        for index_ctrl in self.ctrls:
            index_ctrl.SetForegroundColour(self.inactive_colour)

        evt.Skip()

    def on_left_down(self, evt):
        x, y = evt.GetPosition()
        for index_ctrl in self.ctrls:
            if index_ctrl.HitTest(x, y) == wx.HT_WINDOW_INSIDE:
                self.clicked_ctrl = index_ctrl
                break
        else:
            self.clicked_ctrl = None

        evt.Skip()

    def on_left_up(self, evt):
        if self.clicked_ctrl is not None:
            x, y = evt.GetPosition()
            for index_ctrl in self.ctrls:
                if (
                    index_ctrl.HitTest(x, y) == wx.HT_WINDOW_INSIDE and
                    self.clicked_ctrl == index_ctrl
                ):
                    index_name = index_ctrl.GetLabel().split('(')[0]
                    value = getattr(self.node.values, index_name)
                    self.GetGrandParent().index_pane.GetWindow().SetValue(value)
                    break

        self.clicked_ctrl = None

        evt.Skip()

    def on_motion(self, evt):
        x, y = evt.GetPosition()
        for index_ctrl in self.ctrls:
            if index_ctrl.HitTest(x, y) == wx.HT_WINDOW_INSIDE:
                index_ctrl.SetForegroundColour(self.active_colour)
                if (
                    self.clicked_ctrl is not None and
                    self.clicked_ctrl != index_ctrl
                ):
                    self.clicked_ctrl = None
            else:
                index_ctrl.SetForegroundColour(self.inactive_colour)
        evt.Skip()
