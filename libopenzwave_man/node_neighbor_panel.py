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


class NodeNeighborsPanel(wx.Panel):

    def __init__(self, parent, node):
        self.node = node

        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        hp = header_panel.HeaderPanel(self, 'Neighbors', font_size=12)
        sizer.Add(hp)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(left_sizer, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 5)
        sizer.Add(right_sizer, 0, wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        self.ctrls = ctrls = []

        for i, neighbor in enumerate(list(node.neighbors)):
            ctrl = wx.StaticText(
                self, -1,
                neighbor.name + ' (0x' + hex(neighbor.id)[2:].upper() + ')'
            )

            ctrls += [ctrl]

            if i % 2:
                right_sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 5)
            else:
                left_sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 5)

        self.active_colour = wx.Colour(0, 125, 220)
        self.inactive_colour = self.GetForegroundColour()
        self.clicked_ctrl = None
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_window)

        self.SetSizer(sizer)

    def on_leave_window(self, evt):
        self.clicked_ctrl = None

        for ctrl in self.ctrls:
            ctrl.SetForegroundColour(self.inactive_colour)

        evt.Skip()

    def on_left_down(self, evt):
        x, y = evt.GetPosition()
        for ctrl in self.ctrls:
            if ctrl.HitTest(x, y) == wx.HT_WINDOW_INSIDE:
                self.clicked_ctrl = ctrl
                break
        else:
            self.clicked_ctrl = None

        evt.Skip()

    def on_left_up(self, evt):
        if self.clicked_ctrl is not None:
            x, y = evt.GetPosition()
            for ctrl in self.ctrls:
                if (
                    ctrl.HitTest(x, y) == wx.HT_WINDOW_INSIDE and
                    self.clicked_ctrl == ctrl
                ):
                    neighbor_id = ctrl.GetLabel().split('(')[-1].rstrip(')')
                    neighbor_id = int(neighbor_id, 16)

                    neighbor = self.node.network.nodes[neighbor_id]
                    self.GetGrandParent().node_pane.GetWindow().SetValue(neighbor)
                    break

        self.clicked_ctrl = None

        evt.Skip()

    def on_motion(self, evt):
        x, y = evt.GetPosition()
        for ctrl in self.ctrls:
            if ctrl.HitTest(x, y) == wx.HT_WINDOW_INSIDE:
                ctrl.SetForegroundColour(self.active_colour)
                if (
                    self.clicked_ctrl is not None and
                    self.clicked_ctrl != ctrl
                ):
                    self.clicked_ctrl = None
            else:
                ctrl.SetForegroundColour(self.inactive_colour)
        evt.Skip()


