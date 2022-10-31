
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
:synopsis: NotificationPanel

.. moduleauthor:: Kevin G Schlosser
"""

import wx

from libopenzwave.command_classes import Notification, COMMAND_CLASS_NOTIFICATION

from .. import value_index_panel
from .. import header_panel


class ZWaveNotification(Notification):

    def __init__(self):
        self._notification_panel = None
        Notification.__init__(self)

    def get_panel(self, parent):
        if self._notification_panel is None:
            self._notification_panel = NotificationPanel(parent, self)

        return self._notification_panel


class NotificationPanel(wx.Panel):

    def __init__(self, parent, node):
        self.node = node
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        sizer = wx.BoxSizer(wx.VERTICAL)

        hp = header_panel.HeaderPanel(self, COMMAND_CLASS_NOTIFICATION.class_desc)
        index_notification_panel = value_index_panel.ValueIndexPanel(
            self,
            node,
            COMMAND_CLASS_NOTIFICATION.class_desc
        )

        sizer.Add(hp)
        sizer.Add(index_notification_panel)

        self.SetSizer(sizer)

    def __eq__(self, other):
        return other == COMMAND_CLASS_NOTIFICATION

    def __ne__(self, other):
        return not self.__eq__(other)
