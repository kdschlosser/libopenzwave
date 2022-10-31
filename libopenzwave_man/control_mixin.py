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
from . import spin_int_ctrl
from . import spin_num_ctrl
from . import float_slider_ctrl


class ControlMixin(object):

    def StaticText(self, label):
        return wx.StaticText(self, -1, label)

    def TextCtrl(self, value='', style=0, size=(-1, -1)):
        return wx.TextCtrl(self, -1, value=value, style=style, size=size)

    def CheckBox(self, value):
        check_box = wx.CheckBox(self, -1, '')
        check_box.SetValue(value)
        return check_box

    def Choice(self, value='', choices=()):
        ctrl = wx.Choice(self, -1, choices=choices)
        if value in choices:
            ctrl.SetStringSelection(value)
        else:
            ctrl.SetSelection(0)

        def get_value():
            return ctrl.GetStringSelection()

        ctrl.GetValue = get_value

        return ctrl

    def StaticLine(self, thickness=3, style=wx.LI_HORIZONTAL):
        if style == wx.LI_HORIZONTAL:
            size = (0, thickness)
        elif style == wx.LI_VERTICAL:
            size = (thickness, 0)

        else:
            raise RuntimeError('Invalid Style')

        return wx.StaticLine(self, -1, size=size, style=style)

    def SpinIntCtrl(self, value=0, min=0, max=100, *args, **kwargs):
        return spin_int_ctrl.SpinIntCtrl(
            self,
            -1,
            value=value,
            min=min,
            max=max,
            *args,
            **kwargs
        )

    def SpinNumCtrl(self, value=0, min=0, max=100, *args, **kwargs):
        return spin_num_ctrl.SpinNumCtrl(
            self,
            -1,
            value=value,
            min=min,
            max=max,
            *args,
            **kwargs
        )

    def Button(self, label):
        return wx.Button(self, -1, label)

    def SliderCtrl(
        self,
        value=0,
        increment=1,
        min=0,
        max=100,
        style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_BOTTOM | wx.SL_LABELS,
    ):
        return float_slider_ctrl.FloatSliderCtrl(
            self,
            -1,
            value=value,
            increment=increment,
            minValue=min,
            maxValue=max,
            style=style
        )

