
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
:synopsis: TariffTblMonitorPanel

.. moduleauthor:: Kevin G Schlosser
"""

import wx

from libopenzwave.command_classes import COMMAND_CLASS_TARIFF_TBL_MONITOR

from .. import value_index_panel
from .. import header_panel


class ZWaveTariffTableMonitor(COMMAND_CLASS_TARIFF_TBL_MONITOR):

    def __init__(self):
        self._tariff_tbl_monitor_panel = None
        super().__init__()

    def get_panel(self, parent):
        if self._tariff_tbl_monitor_panel is None:
            self._tariff_tbl_monitor_panel = TariffTableMonitorPanel(parent, self)

        return self._tariff_tbl_monitor_panel


class TariffTableMonitorPanel(wx.Panel):

    def __init__(self, parent, node):
        self.node = node
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        sizer = wx.BoxSizer(wx.VERTICAL)

        hp = header_panel.HeaderPanel(self, COMMAND_CLASS_TARIFF_TBL_MONITOR.class_desc)
        index_tariff_tbl_monitor_panel = value_index_panel.ValueIndexPanel(
            self,
            node,
            COMMAND_CLASS_TARIFF_TBL_MONITOR.class_desc
        )

        sizer.Add(hp)
        sizer.Add(index_tariff_tbl_monitor_panel)

        self.SetSizer(sizer)

    def __eq__(self, other):
        return other == COMMAND_CLASS_TARIFF_TBL_MONITOR

    def __ne__(self, other):
        return not self.__eq__(other)
