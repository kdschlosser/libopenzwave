
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
:synopsis: HumidityControlOperatingStatePanel

.. moduleauthor:: Kevin G Schlosser
"""

import wx

from libopenzwave.command_classes import HumidityControlOperatingState, COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE

from .. import value_index_panel
from .. import header_panel


class ZWaveHumidityControlOperatingState(HumidityControlOperatingState):

    def __init__(self):
        self._humidity_control_operating_state_panel = None
        HumidityControlOperatingState.__init__(self)

    def get_panel(self, parent):
        if self._humidity_control_operating_state_panel is None:
            self._humidity_control_operating_state_panel = HumidityControlOperatingStatePanel(parent, self)

        return self._humidity_control_operating_state_panel


class HumidityControlOperatingStatePanel(wx.Panel):

    def __init__(self, parent, node):
        self.node = node
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        sizer = wx.BoxSizer(wx.VERTICAL)

        hp = header_panel.HeaderPanel(self, COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE.class_desc)
        index_humidity_control_operating_state_panel = value_index_panel.ValueIndexPanel(
            self,
            node,
            COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE.class_desc
        )

        sizer.Add(hp)
        sizer.Add(index_humidity_control_operating_state_panel)

        self.SetSizer(sizer)

    def __eq__(self, other):
        return other == COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE

    def __ne__(self, other):
        return not self.__eq__(other)
