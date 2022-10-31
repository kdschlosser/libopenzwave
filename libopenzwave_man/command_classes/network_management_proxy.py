
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
:synopsis: NetworkManagementProxyPanel

.. moduleauthor:: Kevin G Schlosser
"""

import wx

from libopenzwave.command_classes import NetworkManagementProxy, COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY

from .. import value_index_panel
from .. import header_panel


class ZWaveNetworkManagementProxy(NetworkManagementProxy):

    def __init__(self):
        self._network_management_prox_panel = None
        NetworkManagementProxy.__init__(self)

    def get_panel(self, parent):
        if self._network_management_prox_panel is None:
            self._network_management_prox_panel = NetworkManagementProxyPanel(parent, self)

        return self._network_management_prox_panel


class NetworkManagementProxyPanel(wx.Panel):

    def __init__(self, parent, node):
        self.node = node
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        sizer = wx.BoxSizer(wx.VERTICAL)

        hp = header_panel.HeaderPanel(self, COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY.class_desc)
        index_network_management_prox_panel = value_index_panel.ValueIndexPanel(
            self,
            node,
            COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY.class_desc
        )

        sizer.Add(hp)
        sizer.Add(index_network_management_prox_panel)

        self.SetSizer(sizer)

    def __eq__(self, other):
        return other == COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY

    def __ne__(self, other):
        return not self.__eq__(other)
