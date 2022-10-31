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

import threading
import wx

class TextCtrl(wx.Panel):

    def __init__(self, parent, id=-1, value='', style=0):

        if style | wx.TE_READONLY == style:
            self.readonly = True
        else:
            self.readonly = False

        self.edit = False
        self.caret_position = 0
        self.caret_on = False
        self.caret_event = threading.Event()
        self.caret_event.set()

        wx.Panel.__init__(self, parent, id, style=wx.BORDER_NONE)

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)

        # self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        # self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_double)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_char)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)
        self.value = value
        self.on_paint(None)

    def DoGetBestClientSize(self):
        if self.value:
            width, height = self.GetFullTextExtent(self.value)[:2]
        else:
            width, height = self.GetFullTextExtent('Test String')[:2]
        width += 8
        height += 4
        return width, height

    def on_char(self, evt):
        if not self.edit:
            evt.Skip()
            return

        keycode = evt.GetKeyCode()

        if keycode in (wx.WXK_LEFT, wx.WXK_NUMPAD_LEFT):
            if self.caret_position:
                self.caret_position -= 1
        elif keycode in (wx.WXK_RIGHT, wx.WXK_NUMPAD_RIGHT):
            if self.caret_position < len(self.value):
                self.caret_position += 1
        elif keycode in (wx.WXK_HOME, wx.WXK_NUMPAD_HOME):
            self.caret_position = 0
        elif keycode in (wx.WXK_END, wx.WXK_NUMPAD_END):
            self.caret_position = len(self.value)
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE):
            if self.caret_position < len(self.value):
                value = list(self.value)
                value.pop(self.caret_position)
                self.value = ''.join(value)

        elif keycode == wx.WXK_BACK:
            if self.caret_position:
                value = list(self.value)
                self.caret_position -= 1
                value.pop(self.caret_position)
                self.value = ''.join(value)
        else:
            keycode = evt.GetUnicodeKey()

            if keycode != wx. WXK_NONE:
                char = chr(keycode).lower()

                if evt.ShiftDown():
                    char = char.upper()

                value = list(self.value)
                value.insert(self.caret_position, char)
                self.value = ''.join(value)
                self.caret_position += 1

        evt.Skip()

    def on_erase_background(self, _):
        pass

    def caret_loop(self):
        self.caret_event.clear()
        while not self.caret_event.is_set():
            self.caret_on = not self.caret_on
            def _do():
                self.Refresh()
                self.Update()
            wx.CallAfter(_do)

            self.caret_event.wait(0.5)

    def on_kill_focus(self, evt):
        self.caret_event.set()
        self.caret_position = 0
        self.caret_on = False
        self.edit = False
        self.Refresh()
        self.Update()
        evt.Skip()

    def on_destroy(self, evt):
        self.caret_event.set()
        evt.Skip()

    def on_left_up(self, evt):
        self.SetFocus()
        self.edit = True

        self.caret_position = 0

        if self.value:
            x, _ = evt.GetPosition()

            start_x = 4

            for i, char in enumerate(list(self.value)):
                if x < start_x:
                    self.caret_position = i - 1
                    break
                start_x += self.GetFullTextExtent(char)[0]
            else:
                self.caret_position = len(self.value) - 1

        if self.caret_event.is_set():
            t = threading.Thread(target=self.caret_loop)
            t.daemon = True
            t.start()

    def on_paint(self, evt):

        background_colour = self.GetBackgroundColour()
        foreground_colour = self.GetForegroundColour()
        font = self.GetFont()

        width, height = self.GetClientSize()
        dc = wx.MemoryDC()
        bmp = wx.Bitmap(width, height)
        dc.SelectObject(bmp)
        dc.SetPen(wx.Pen(background_colour, 1))
        dc.SetBrush(wx.Brush(background_colour))

        dc.DrawRectangle(0, 0, width, height)

        dc.SetFont(font)
        dc.SetTextForeground(foreground_colour)
        dc.SetTextBackground(background_colour)

        text_height = dc.GetFullTextExtent(self.value)[1]

        y = (height - text_height) / 2

        text_width = dc.GetFullTextExtent(self.value)[0]
        text_x = 4

        if self.edit:
            caret_x = 4

            for i, char in enumerate(list(self.value)):
                if i == self.caret_position:
                    break
                caret_x += dc.GetFullTextExtent(char)[0]

            dc.DrawText(self.value, text_x, y)
            if self.caret_on:
                dc.SetPen(wx.Pen(foreground_colour, 1))
                dc.SetBrush(wx.Brush(foreground_colour))

                dc.DrawLine(caret_x, 0, caret_x, height)

        else:
            dc.DrawText(self.value, text_x, y)

        dc.SelectObject(wx.NullBitmap)

        dc.Destroy()
        del dc

        if evt is None:
            cdc = wx.ClientDC(self)
            cdc.DrawBitmap(bmp, 0, 0)
        else:

            pdc = wx.PaintDC(self)
            pdc.DrawBitmap(bmp, 0, 0)



