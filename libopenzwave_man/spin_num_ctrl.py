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
from wx import SystemSettings
from wx.lib import masked


import sys
from wx.lib.masked import NumCtrl

_num_ctrl = NumCtrl


class _NumCtrl(_num_ctrl):

    def __init__(self, parent, id=-1, value=None, *args, **kwargs):
        self._hold_value = value
        self.SetParameters = self._set_parameters
        super(_NumCtrl, self).__init__(parent, id, value, *args, **kwargs)
        del self._hold_value

    def _set_parameters(self, **kwargs):
        try:
            self.SetValue(self._hold_value)
            _num_ctrl.SetParameters(self, **kwargs)
        except:
            _num_ctrl.SetParameters(self, **kwargs)
            self.SetValue(self._hold_value)

        self.SetParameters = _num_ctrl.SetParameters


sys.modules['wx.lib.masked.numctrl'].NumCtrl = _NumCtrl
sys.modules['wx.lib.masked'].NumCtrl = _NumCtrl

masked.NumCtrl = _NumCtrl

lcl = wx.Locale()
lcl.Init(language=wx.LANGUAGE_DEFAULT, flags=wx.LOCALE_LOAD_DEFAULT)
THOUSANDS_SEP = lcl.GetInfo(wx.LOCALE_THOUSANDS_SEP)
DECIMAL_POINT = lcl.GetInfo(wx.LOCALE_DECIMAL_POINT)


class SpinNumError(ValueError):
    _msg = ''

    def __init__(self, *args):
        if args:
            self._msg = self._msg.format(*args)

    def __str__(self):
        return self._msg


class MinValueError(SpinNumError):
    _msg = 'The set value {0} is lower then the minimum of {1}'


class MaxValueError(SpinNumError):
    _msg = 'The set value {0} is higher then the maximum of {1}'


class MinMaxValueError(SpinNumError):
    _msg = 'The minimum value {0} is higher the the max value {0}.'


class NegativeValueError(SpinNumError):
    _msg = 'The minimum value needs to be set when using negative values.'


class SpinNumCtrl(wx.Window):
    """
    A wx.Control that shows a fixed width floating point value and spin
    buttons to let the user easily input a floating point value.
    """
    _defaultArgs = {
        "integerWidth": 3,
        "fractionWidth": 2,
        "limited": True,
        "groupChar": THOUSANDS_SEP,
        "decimalChar": DECIMAL_POINT,
    }

    def __init__(
        self,
        parent,
        id=-1,
        value=0.0,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.TE_RIGHT,
        validator=wx.DefaultValidator,
        name="eg.SpinNumCtrl",
        **kwargs
    ):

        self.increment = kwargs.pop("increment", 1)
        min_val = kwargs.pop('min', None)
        max_val = kwargs.pop('max', None)
        allow_negative = kwargs.pop("allowNegative", False)

        tmp = self._defaultArgs.copy()
        tmp.update(kwargs)
        kwargs = tmp

        if max_val is None and min_val is None:
            if value < 0:
                raise NegativeValueError

        elif min_val is None and max_val is not None:
            if value > max_val:
                raise MaxValueError(value, max_val)
            if max_val < 0:
                allow_negative = True

        elif max_val is None and min_val is not None:
            if value < min_val:
                raise MinValueError(value, min_val)
            if min_val < 0:
                allow_negative = True

        else:
            if min_val > max_val:
                raise MinMaxValueError(min_val, max_val)
            if value < min_val:
                raise MinValueError(value, min_val)
            if value > max_val:
                raise MaxValueError(value, max_val)
            if min_val < 0:
                allow_negative = True

        if max_val is None:
            max_val = (
                (10 ** kwargs["integerWidth"]) -
                (10 ** -kwargs["fractionWidth"])
            )

        wx.Window.__init__(self, parent, id, pos, size, 0)
        self.SetThemeEnabled(True)
        num_ctrl = masked.NumCtrl(
            self,
            -1,
            value,
            pos,
            size,
            style,
            validator,
            name,
            allowNone=True,
            allowNegative=allow_negative,
            min=min_val,
            max=max_val,
            **kwargs
        )
        self.num_ctrl = num_ctrl

        num_ctrl.SetCtrlParameters(
            validBackgroundColour=SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW),
            emptyBackgroundColour=SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW),
            foregroundColour=SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT),
        )

        height = num_ctrl.GetSize()[1]
        spin_button = wx.SpinButton(
            self,
            -1,
            style=wx.SP_VERTICAL,
            size=(height * 2 / 3, height)
        )
        spin_button.MoveBeforeInTabOrder(num_ctrl)
        self.spin_button = spin_button
        num_ctrl.Bind(wx.EVT_CHAR, self.OnChar)
        spin_button.Bind(wx.EVT_SPIN_UP, self.OnSpinUp)
        spin_button.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown)

        sizer = self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(num_ctrl, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        sizer.Add(spin_button, 0, wx.ALIGN_CENTER)
        self.SetSizerAndFit(sizer)
        self.Layout()
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        wx.CallAfter(num_ctrl.SetSelection, -1, -1)

    def GetValue(self):
        return self.num_ctrl.GetValue()

    def OnChar(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_UP:
            self.OnSpinUp(event)
            return
        if key == wx.WXK_DOWN:
            self.OnSpinDown(event)
            return
        event.Skip()

    def OnSetFocus(self, _):
        self.num_ctrl.SetFocus()
        self.num_ctrl.SetSelection(-1, -1)

    def OnSize(self, _):
        if self.GetAutoLayout():
            self.Layout()

    def OnSpinDown(self, _):
        value = self.num_ctrl.GetValue() - self.increment
        self.SetValue(value)

    def OnSpinUp(self, _):
        value = self.num_ctrl.GetValue() + self.increment
        self.SetValue(value)

    def SetValue(self, value):
        min_value, max_value = self.num_ctrl.GetBounds()
        if max_value is not None and value > max_value:
            value = max_value
        if min_value is not None and value < min_value:
            value = min_value
        if value < 0 and not self.num_ctrl.IsNegativeAllowed():
            value = 0
        res = self.num_ctrl.SetValue(value)
        return res

    def __OnSpin(self, pos):
        """
        This is the function that gets called in response to up/down arrow or
        bound spin button events.
        """

        # Ensure adjusted control regains focus and has adjusted portion
        # selected:
        num_ctrl = self.num_ctrl
        num_ctrl.SetFocus()
        start, end = num_ctrl._FindField(pos)._extent
        num_ctrl.SetInsertionPoint(start)
        num_ctrl.SetSelection(start, end)
