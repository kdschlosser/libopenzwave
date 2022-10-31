
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
:synopsis: SwitchMultilevelPanel

.. moduleauthor:: Kevin G Schlosser
"""

import wx
import threading
from libopenzwave.command_classes import SwitchMultilevel, COMMAND_CLASS_SWITCH_MULTILEVEL
import libopenzwave


from .. import value_index_panel
from .. import header_panel
from .. import float_slider_ctrl
from .. import boxed_group


class ZWaveSwitchMultilevel(SwitchMultilevel):

    def __init__(self):
        self._switch_multilevel_panel = None
        SwitchMultilevel.__init__(self)

    def get_panel(self, parent):
        if self._switch_multilevel_panel is None:
            self._switch_multilevel_panel = SwitchMultilevelPanel(parent, self)

            def on_destroy(evt):
                self._switch_multilevel_panel = None
                evt.Skip()

            self._switch_multilevel_panel.Bind(wx.EVT_WINDOW_DESTROY, on_destroy)

        return self._switch_multilevel_panel


def h_sizer(*ctrls):
    sizer = wx.BoxSizer(wx.HORIZONTAL)

    for ctrl in ctrls:
        sizer.Add(ctrl, 0, wx.ALL, 5)

    return sizer

def v_sizer(ctrl1, ctrl2):
    sizer = wx.BoxSizer(wx.VERTICAL)

    ctrl1_sizer = wx.BoxSizer(wx.HORIZONTAL)
    ctrl1_sizer.AddStretchSpacer(1)
    ctrl1_sizer.Add(ctrl1, 0, wx.ALL, 5)
    ctrl1_sizer.AddStretchSpacer(1)

    sizer.Add(ctrl1_sizer)
    sizer.Add(ctrl2, 1, wx.ALL | wx.EXPAND, 5)
    return sizer


class SwitchMultilevelPanel(wx.Panel):

    def __init__(self, parent, node):
        self.node = node
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        sizer = wx.BoxSizer(wx.VERTICAL)

        hp = header_panel.HeaderPanel(self, COMMAND_CLASS_SWITCH_MULTILEVEL.class_desc, font_size=10)

        use_current_label = wx.StaticText(self, -1, 'Use current level:')
        self.use_current_ctrl = wx.CheckBox(self, -1, '')

        start_level_label = wx.StaticText(self, -1, 'Start Level')
        self.start_level_ctrl = float_slider_ctrl.FloatSliderCtrl(
            self,
            -1,
            value=node.values.switch_multilevel_start_level.data.data,
            minValue=0,
            maxValue=99,
            increment=1,
            style=(
                wx.SL_LABELS |
                wx.SL_BOTTOM |
                wx.SL_AUTOTICKS |
                wx.SL_HORIZONTAL
            )
        )

        ignore_start = node.values.switch_multilevel_ignore_start_level.data.data

        self.use_current_ctrl.SetValue(not ignore_start)
        self.start_level_ctrl.Enable(not ignore_start)

        def on_check(evt):
            self.start_level_ctrl.Enable(not self.use_current_ctrl.GetValue())
            evt.Skip()

        self.use_current_ctrl.Bind(wx.EVT_CHECKBOX, on_check)

        start_level_sizer = h_sizer(
            v_sizer(start_level_label, self.start_level_ctrl),
            h_sizer(use_current_label, self.use_current_ctrl)
        )

        step_duration = node.values.switch_multilevel_duration.data

        if step_duration is None:
            step_value = 150
        else:
            step_value = step_duration.data.data
            step_value = int(step_value / 100)

            if step_value > 2550:
                step_value = 2550

        step_duration_label = wx.StaticText(self, -1, 'Duration Between Level Changes (milliseconds)')
        self.step_duration_ctrl = float_slider_ctrl.FloatSliderCtrl(
            self,
            -1,
            value=step_value,
            minValue=0,
            maxValue=2550,
            increment=1,
            style=(
                    wx.SL_LABELS |
                    wx.SL_BOTTOM |
                    wx.SL_AUTOTICKS |
                    wx.SL_HORIZONTAL
            )
        )

        step_duration_sizer = v_sizer(step_duration_label, self.step_duration_ctrl)

        duration_label = wx.StaticText(self, -1, 'Ramp Target Level')
        self.duration_ctrl = float_slider_ctrl.FloatSliderCtrl(
            self,
            -1,
            value=50,
            minValue=1,
            maxValue=99,
            increment=1,
            style=(
                    wx.SL_LABELS |
                    wx.SL_BOTTOM |
                    wx.SL_AUTOTICKS |
                    wx.SL_HORIZONTAL
            )
        )

        duration_sizer = v_sizer(duration_label, self.duration_ctrl)

        self.on_button = wx.Button(self, -1, 'On', size=(50, 100))
        self.off_button = wx.Button(self, -1, 'Off', size=(50, 100))

        self.timer = None

        on_off_sizer = wx.BoxSizer(wx.VERTICAL)
        on_off_sizer.AddStretchSpacer(1)
        on_off_sizer.Add(self.on_button, 0, wx.EXPAND)
        on_off_sizer.Add(self.off_button, 0, wx.EXPAND)
        on_off_sizer.AddStretchSpacer(1)

        self.on_button.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.on_button.Bind(wx.EVT_LEFT_UP, self.on_left_up)

        self.off_button.Bind(wx.EVT_LEFT_DOWN, self.off_left_down)
        self.off_button.Bind(wx.EVT_LEFT_UP, self.off_left_up)

        self.ramp_up_button = wx.Button(self, -1, 'Ramp\n Up', size=(50, 100))
        self.ramp_down_button = wx.Button(self, -1, 'Ramp\nDown', size=(50, 100))

        self.timer = None

        ramp_button_sizer = wx.BoxSizer(wx.VERTICAL)
        ramp_button_sizer.AddStretchSpacer(1)
        ramp_button_sizer.Add(self.ramp_up_button, 0, wx.EXPAND)
        ramp_button_sizer.Add(self.ramp_down_button, 0, wx.EXPAND)
        ramp_button_sizer.AddStretchSpacer(1)

        self.ramp_up_button.Bind(wx.EVT_BUTTON, self.ramp_up)
        self.ramp_down_button.Bind(wx.EVT_BUTTON, self.ramp_down)

        ramp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ramp_right_sizer = wx.BoxSizer(wx.VERTICAL)

        ramp_right_sizer.Add(start_level_sizer)
        ramp_right_sizer.Add(step_duration_sizer)
        ramp_right_sizer.Add(duration_sizer)

        ramp_sizer.Add(ramp_button_sizer)
        ramp_sizer.Add(ramp_right_sizer)

        ramp_level_sizer = boxed_group.BoxedGroup(self, 'Level Ramping', ramp_sizer)
        rocker_sizer = boxed_group.BoxedGroup(self, 'Manual Rocker', on_off_sizer)

        self.ctrl = float_slider_ctrl.FloatSliderCtrl(
            self,
            -1,
            value=self.node.switch_level.data,
            minValue=0,
            maxValue=100,
            increment=1,
            style=(
                    wx.SL_AUTOTICKS |
                    wx.SL_HORIZONTAL |
                    wx.SL_BOTTOM |
                    wx.SL_LABELS
            )
        )
        self.ctrl.SetTickFreq(2)
        self.ctrl.SetBackgroundColour(self.GetBackgroundColour())

        if self.node.switch_level.data > 0:
            self.on_button.SetForegroundColour(wx.BLUE)
        else:
            self.off_button.SetForegroundColour(wx.BLUE)

        self.ctrl.Bind(wx.EVT_SCROLL_CHANGED, self.on_slider)

        switch_sizer = wx.BoxSizer(wx.HORIZONTAL)

        switch_sizer.Add(rocker_sizer, 0, wx.ALL | wx.EXPAND, 10)
        switch_sizer.Add(ramp_level_sizer, 0, wx.ALL | wx.EXPAND, 10)

        level_label = wx.StaticText(self, -1, 'Light Level')
        light_level_sizer = v_sizer(level_label, self.ctrl)

        sizer.Add(hp)
        sizer.Add(switch_sizer, 1)
        sizer.Add(light_level_sizer)
        self.SetSizer(sizer)

        openzwave.SIGNAL_VALUE_CHANGED.register(self.on_change, self.node.values.switch_multilevel_level)

    def ramp_up(self, evt):
        step_duration = self.step_duration_ctrl.GetValue()
        target_level = self.duration_ctrl.GetValue()

        if self.use_current_ctrl.GetValue():
            start_level = None
        else:
            start_level = self.start_level_ctrl.GetValue()

        self.node.switch_ramp_up.start(target_level, step_duration, start_level)
        evt.Skip()

    def ramp_down(self, evt):
        step_duration = self.step_duration_ctrl.GetValue()
        target_level = self.duration_ctrl.GetValue()

        if self.use_current_ctrl.GetValue():
            start_level = None

        else:
            start_level = self.start_level_ctrl.GetValue()

        self.node.switch_ramp_down.start(target_level, step_duration, start_level)

        evt.Skip()

    def on_left_down(self, evt):

        def callback():
            self.timer = None
            ramp = self.node.switch_ramp_up
            self.on_button.Unbind(wx.EVT_LEFT_UP, handler=self.on_left_up)

            def up_callback(e):
                ramp.stop()
                self.on_button.Unbind(wx.EVT_LEFT_UP, handler=up_callback)
                wx.CallAfter(self.on_button.Bind, wx.EVT_LEFT_UP, self.on_left_up)
                e.Skip()

            self.on_button.Bind(wx.EVT_LEFT_UP, up_callback)

        self.timer = threading.Timer(0.5, callback)
        self.timer.start()

        evt.Skip()

    def on_left_up(self, evt):
        try:
            self.timer.cancel()
        except AttributeError:
            pass

        self.node.switch_state = True
        evt.Skip()


    def off_left_down(self, evt):
        def callback():
            self.timer = None
            ramp = self.node.switch_ramp_down
            self.off_button.Unbind(wx.EVT_LEFT_UP, handler=self.off_left_up)
            ramp.start()

            def up_callback(e):
                ramp.stop()
                self.off_button.Unbind(wx.EVT_LEFT_UP, handler=up_callback)
                wx.CallAfter(self.off_button.Bind, wx.EVT_LEFT_UP, self.off_left_up)
                e.Skip()

            self.off_button.Bind(wx.EVT_LEFT_UP, up_callback)

        self.timer = threading.Timer(0.5, callback)
        self.timer.start()

        evt.Skip()

    def off_left_up(self, evt):
        try:
            self.timer.cancel()
        except AttributeError:
            pass

        self.node.switch_state = False
        evt.Skip()

    def on_close(self, evt):
        openzwave.SIGNAL_VALUE_CHANGED.unregister(self.on_change, self.level_value)
        evt.Skip()

    def on_destroy(self, evt):
        openzwave.SIGNAL_VALUE_CHANGED.unregister(self.on_change, self.level_value)
        evt.Skip()

    def on_slider(self, evt):
        val = self.ctrl.GetValue()
        if val != 100:
            self.node.switch_ge_jasco_level = val

    def on_change(self, value_data, *_, **__):
        self.ctrl.SetValue(value_data.data)
        self.on_button.SetForegroundColour(self.GetForegroundColour())
        self.off_button.SetForegroundColour(self.GetForegroundColour())

        if value_data == 0:
            self.off_button.SetForegroundColour(wx.BLUE)
        else:
            self.on_button.SetForegroundColour(wx.BLUE)

    def __eq__(self, other):
        return other == COMMAND_CLASS_SWITCH_MULTILEVEL

    def __ne__(self, other):
        return not self.__eq__(other)
