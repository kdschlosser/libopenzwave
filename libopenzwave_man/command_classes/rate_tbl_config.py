
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
:synopsis: RateTblConfigPanel

.. moduleauthor:: Kevin G Schlosser
"""

import wx

from libopenzwave.command_classes import COMMAND_CLASS_RATE_TBL_CONFIG

from .. import value_index_panel
from .. import header_panel


class ZWaveRateTableConfig(COMMAND_CLASS_RATE_TBL_CONFIG):

    def __init__(self):
        self._rate_tbl_config_panel = None
        super().__init__()

    def get_panel(self, parent):
        if self._rate_tbl_config_panel is None:
            self._rate_tbl_config_panel = RateTableConfigPanel(parent, self)

        return self._rate_tbl_config_panel


class RateTableConfigPanel(wx.Panel):

    def __init__(self, parent, node):
        self.node = node
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        sizer = wx.BoxSizer(wx.VERTICAL)

        hp = header_panel.HeaderPanel(self, COMMAND_CLASS_RATE_TBL_CONFIG.class_desc)
        index_rate_tbl_config_panel = value_index_panel.ValueIndexPanel(
            self,
            node,
            COMMAND_CLASS_RATE_TBL_CONFIG.class_desc
        )

        sizer.Add(hp)
        sizer.Add(index_rate_tbl_config_panel)

        self.SetSizer(sizer)

    def __eq__(self, other):
        return other == COMMAND_CLASS_RATE_TBL_CONFIG

    def __ne__(self, other):
        return not self.__eq__(other)
