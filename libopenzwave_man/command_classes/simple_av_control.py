
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
:synopsis: SimpleAvControlPanel

.. moduleauthor:: Kevin G Schlosser
"""

import wx

from libopenzwave.command_classes import SimpleAVControl, COMMAND_CLASS_SIMPLE_AV_CONTROL

from .. import value_index_panel
from .. import header_panel


class ZWaveSimpleAVControl(SimpleAVControl):

    def __init__(self):
        self._simple_av_control_panel = None
        SimpleAVControl.__init__(self)

    def get_panel(self, parent):
        if self._simple_av_control_panel is None:
            self._simple_av_control_panel = SimpleAVControlPanel(parent, self)

        return self._simple_av_control_panel


class SimpleAvControlPanel(wx.Panel):

    def __init__(self, parent, node):
        self.node = node
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        sizer = wx.BoxSizer(wx.VERTICAL)

        hp = header_panel.HeaderPanel(self, COMMAND_CLASS_SIMPLE_AV_CONTROL.class_desc)
        index_simple_av_control_panel = value_index_panel.ValueIndexPanel(
            self,
            node,
            COMMAND_CLASS_SIMPLE_AV_CONTROL.class_desc
        )

        sizer.Add(hp)
        sizer.Add(index_simple_av_control_panel)

        self.SetSizer(sizer)

    def __eq__(self, other):
        return other == COMMAND_CLASS_SIMPLE_AV_CONTROL

    def __ne__(self, other):
        return not self.__eq__(other)
