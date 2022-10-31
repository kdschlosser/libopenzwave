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
import libopenzwave

from . import control_mixin
from . import float_slider_ctrl
from . import text_ctrl



class CtrlBase(wx.BoxSizer):

    def __init__(self, parent, value):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)

        self.parent = parent
        self.value = value

        label = wx.StaticText(parent, -1, 'Data:')
        ctrl = self.data_ctrl

        self.Add(label, 0, wx.ALL, 5)
        self.Add(ctrl, 1, wx.ALL, 5)
        self.AddSpacer(1)

        if self.value.type != 'Button':
            set_button = wx.Button(parent, -1, 'Set')
            reset_button = wx.Button(parent, -1, 'Reset')

            self.Add(set_button, 0, wx.ALL, 5)
            self.Add(reset_button, 0, wx.ALL, 5)

            set_button.Bind(wx.EVT_BUTTON, self.on_set_button)
            reset_button.Bind(wx.EVT_BUTTON, self.on_reset_button)

        libopenzwave.SIGNAL_VALUE_CHANGED.register(
            self.on_value_changed,
            sender=self.value
        )

        parent.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)

    def on_reset_button(self, evt):
        self.data_ctrl.SetValue(self.value.data)
        evt.Skip()

    def on_set_button(self, evt):
        self.value.data = self.data_ctrl.GetValue()
        evt.Skip()

    def on_value_changed(self, value_data, **kwargs):
        self.data_ctrl.SetValue(value_data)

    def on_destroy(self, evt):
        libopenzwave.SIGNAL_VALUE_CHANGED.unregister(
            self.on_value_changed,
            sender=self.value
        )
        evt.Skip()

    @property
    def data_ctrl(self):
        raise NotImplementedError

    def SetValue(self, value):
        self.data_ctrl.SetValue(value)


class BoolCtrl(CtrlBase):

    def __init__(self, parent, value):
        self._data_ctrl = None
        CtrlBase.__init__(self, parent, value)

    @property
    def data_ctrl(self):
        if self._data_ctrl is None:
            if self.value.is_write_only:
                data = False
            else:
                data = self.value.data

            self._data_ctrl = wx.CheckBox(self.parent, -1, '')
            self._data_ctrl.SetValue(data)

            if self.value.is_read_only:
                self._data_ctrl.Enable(False)

        return self._data_ctrl


class ScheduleCtrl(CtrlBase):

    def __init__(self, parent, value):
        self._data_ctrl = None
        CtrlBase.__init__(self, parent, value)

    @property
    def data_ctrl(self):
        if self._data_ctrl is None:
            if self.value.is_write_only:
                data = ''
            else:
                data = self.value.data

            self._data_ctrl = wx.TextCtrl(self.parent, -1, data)

            if self.value.is_read_only:
                self._data_ctrl.Enable(False)

        return self._data_ctrl


class StringCtrl(CtrlBase):

    def __init__(self, parent, value):
        self._data_ctrl = None
        CtrlBase.__init__(self, parent, value)

    @property
    def data_ctrl(self):
        if self._data_ctrl is None:
            if self.value.is_write_only:
                data = ''
            else:
                data = self.value.data

            if self.value.is_read_only:
                style = wx.TE_READONLY
            else:
                style = 0

            self._data_ctrl = wx.TextCtrl(self.parent, -1, data, style=style)

        return self._data_ctrl


class ButtonCtrl(CtrlBase):
    def __init__(self, parent, value):
        self._data_ctrl = None
        self.states = ['Released', 'Pressed']
        CtrlBase.__init__(self, parent, value)

    @property
    def data_ctrl(self):
        if self._data_ctrl is None:
            print(self.value.data.data)
            self._data_ctrl = wx.ToggleButton(self.parent, -1, self.states[0])

            def on_press(evt):
                self._data_ctrl.SetLabel(self.states[1])
                self.value.data = True
                evt.Skip()

            self._data_ctrl.Bind(wx.EVT_LEFT_DOWN, on_press)

            def on_release(evt):
                self.value.data = False
                self._data_ctrl.SetValue(False)
                self._data_ctrl.SetLabel(self.states[0])
                evt.Skip()

            self._data_ctrl.Bind(wx.EVT_LEFT_UP, on_release)

        return self._data_ctrl

    def on_value_changed(self, value_data, **kwargs):
        pass

    def GetValue(self):
        return self.data_ctrl.GetValue()

    def SetValue(self, value):
        pass


class BitSetPanel(wx.Panel):

    @staticmethod
    def get_bit(v, index):
        return v >> index & 1

    @staticmethod
    def set_bit(v, index, x):
        mask = 1 << index
        v &= ~mask
        if x:
            v |= mask
        return v

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        label = wx.StaticText(self, -1, 'Bits:')
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label, 0, wx.ALL | wx.EXPAND, 5)

        self.ctrls = []
        for i in range(8):
            ctrl = wx.CheckBox(self, -1, '')
            ctrl.SetValue(False)
            bit_label = wx.StaticText(self, -1, str(i) + ':')
            sizer.Add(bit_label, 0, wx.ALL | wx.EXPAND, 5)
            sizer.Add(ctrl, 0, wx.ALL | wx.EXPAND, 5)
            self.ctrls += [ctrl]

        self.SetSizer(sizer)

    def GetValue(self):
        value = 0

        for i, ctrl in enumerate(self.ctrls):
            value = self.set_bit(value, i, int(ctrl.GetValue()))

        return value

    def SetValue(self, value):

        for i in range(8):
            ctrl = self.ctrls[i]
            ctrl.SetValue(bool(self.get_bit(value, i)))


class BitSetCtrl(CtrlBase):

    def __init__(self, parent, value):
        self._data_ctrl = None
        CtrlBase.__init__(self, parent, value)

    @property
    def data_ctrl(self):
        if self._data_ctrl is None:
            if self.value.is_write_only:
                data = 0
            else:
                data = self.value.data

            self._data_ctrl = BitSetPanel(self.parent)
            self._data_ctrl.SetValue(data)

            if self.value.is_read_only:
                self._data_ctrl.Enable(False)

        return self._data_ctrl


class ListCtrl(CtrlBase):

    def __init__(self, parent, value):
        self._data_ctrl = None
        CtrlBase.__init__(self, parent, value)

    @property
    def data_ctrl(self):
        if self._data_ctrl is None:

            data_items = self.value.data_items

            if self.value.is_write_only:
                data = data_items[0]
            else:
                data = self.value.data

            self._data_ctrl = wx.Choice(self.parent, -1, choices=data_items)
            self._data_ctrl.SetValue = self._data_ctrl.SetStringSelection
            self._data_ctrl.GetValue = self._data_ctrl.GetStringSelection
            self._data_ctrl.SetValue(data)

            if self.value.is_read_only:
                self._data_ctrl.Enable(False)

        return self._data_ctrl


class DecimalCtrl(CtrlBase):

    def __init__(self, parent, value):
        self._data_ctrl = None
        CtrlBase.__init__(self, parent, value)

    @property
    def data_ctrl(self):
        if self._data_ctrl is None:
            if self.value.is_write_only:
                data = 0.0
            else:
                data = self.value.data

            min_value = self.value.min
            max_value = self.value.max

            if min_value is None:
                min_value = 0.0

            self._data_ctrl = float_slider_ctrl.FloatSliderCtrl(
                self.parent,
                -1,
                value=data,
                minValue=min_value,
                maxValue=max_value,
                style=(
                    wx.SL_AUTOTICKS |
                    wx.SL_LABELS |
                    wx.SL_HORIZONTAL |
                    wx.SL_BOTTOM
                )
            )

            self._data_ctrl.SetTickFreq(int((max_value - min_value) * 0.10))
            if self.value.is_read_only:
                self._data_ctrl.Enable(False)

        return self._data_ctrl


class IntBase(CtrlBase):
    min = 0
    max = 0
    tick_freq = 0

    def __init__(self, parent, value):
        self._data_ctrl = None
        CtrlBase.__init__(self, parent, value)

    @property
    def data_ctrl(self):
        if self._data_ctrl is None:
            if self.value.is_write_only:
                data = 0
            else:
                data = self.value.data

            if self.value.is_read_only:
                self._data_ctrl = wx.TextCtrl(self.parent, -1, str(data), style=wx.TE_READONLY)

                _set_value = self._data_ctrl.SetValue
                _get_value = self._data_ctrl.GetValue
                def set_value(value):
                    _set_value(str(value))

                def get_value():
                    return int(_get_value())

                self._data_ctrl.SetValue = set_value
                self._data_ctrl.GetValue = get_value

            else:
                min = self.value.min
                max = self.value.max

                if min is None:
                    min = self.min

                if max is None:
                    max = self.max

                self._data_ctrl = float_slider_ctrl.FloatSliderCtrl(
                    self.parent,
                    -1,
                    value=data,
                    minValue=min,
                    maxValue=max,
                    increment=1,
                    style=(
                        wx.SL_AUTOTICKS |
                        wx.SL_LABELS |
                        wx.SL_HORIZONTAL |
                        wx.SL_BOTTOM
                    )
                )

                tick_freq = int((max - min) * 0.10)

                if tick_freq < self.tick_freq:
                    tick_freq = self.tick_freq

                if tick_freq < 100:
                    tick_freq = int(tick_freq / 4)

                self._data_ctrl.SetTickFreq(tick_freq)

        return self._data_ctrl


class ByteCtrl(IntBase):
    min = 0
    max = 255
    tick_freq = int((max - min) * 0.20)

class IntCtrl(IntBase):
    min = -2147483648
    max = 2147483647
    tick_freq = int((max - min) * 0.02)

class ShortCtrl(IntBase):
    min = -32768
    max = 32767
    tick_freq = int((max - min) * 0.05)


class ValueMixin(control_mixin.ControlMixin):

    def __init__(self, value):
        self.value = value

        self._header = None
        self._data = None
        self._units_ctrl = None
        self._index_ctrl = None
        self._label_ctrl = None
        self._help_ctrl = None
        self._max_ctrl = None
        self._min_ctrl = None
        self._type_ctrl = None
        self._genre_ctrl = None
        self._index_ctrl = None
        self._instance_ctrl = None
        self._items_ctrl = None
        self._set_ctrl = None
        self._read_ctrl = None
        self._write_ctrl = None
        self._poll_ctrl = None
        self._is_poll_ctrl = None
        self._cc_ctrl = None
        self._refresh_ctrl = None
        self._verified_ctrl = None
        self._precison_ctrl = None
        self._instance_label_ctrl = None

    @property
    def header(self):
        if self._header is None:
            panel = wx.Panel(self, -1, style=wx.BORDER_RAISED)

            name_ctrl = text_ctrl.TextCtrl(panel, -1, self.value.label)

            font = wx.Font(
                8,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )

            name_ctrl.SetFont(font)

            id_label = wx.StaticText(
                panel,
                -1,
                '(0x' + hex(self.value.id)[2:].upper() + ')'
            )
            name_set = wx.Button(panel, -1, chr(0x2714))
            name_reset = wx.Button(panel, -1, 'X')

            button_sizer = wx.BoxSizer(wx.VERTICAL)
            button_sizer.Add(name_set, 0, wx.ALIGN_BOTTOM | wx.ALL, 2)
            button_sizer.Add(name_reset, 0, wx.ALIGN_BOTTOM | wx.ALL, 2)

            name_sizer = wx.BoxSizer(wx.HORIZONTAL)
            name_sizer.Add(name_ctrl, 0, wx.ALL, 5)
            name_sizer.Add(button_sizer, 0, wx.ALL, 2)
            name_sizer.AddSpacer(1)
            name_sizer.Add(id_label, 0, wx.ALL, 5)

            def on_name_set(evt):
                self.node.name = name_ctrl.value
                evt.Skip()

            def on_name_reset(evt):
                name_ctrl.value = self.node.name
                evt.Skip()

            name_set.Bind(wx.EVT_BUTTON, on_name_set)
            name_reset.Bind(wx.EVT_BUTTON, on_name_reset)

            main_sizer = wx.BoxSizer(wx.VERTICAL)
            main_sizer.Add(name_sizer)
            panel.SetSizer(main_sizer)

            self._header = panel

        return self._header

    @property
    def data(self):
        if self._data is None:
            value_type = self.value.type
            if value_type == 'Byte':
                ctrl = ByteCtrl(self, self.value)
            elif value_type == 'Int':
                ctrl = IntCtrl(self, self.value)
            elif value_type == 'Short':
                ctrl = ShortCtrl(self, self.value)
            elif value_type == 'Bool':
                ctrl = BoolCtrl(self, self.value)
            elif value_type == 'Decimal':
                ctrl = DecimalCtrl(self, self.value)
            elif value_type == 'List':
                ctrl = ListCtrl(self, self.value)
            elif value_type == 'Schedule':
                ctrl = ScheduleCtrl(self, self.value)
            elif value_type == 'String':
                ctrl = StringCtrl(self, self.value)
            elif value_type == 'Button':
                ctrl = ButtonCtrl(self, self.value)
            elif value_type == 'BitSet':
                ctrl = BitSetCtrl(self, self.value)
            else:
                ctrl = wx.BoxSizer(wx.HORIZONTAL)

            self._data = ctrl

        return self._data

    @property
    def units(self):
        if self._units_ctrl is None:
            label = self.StaticText('Units:')
            ctrl = self.TextCtrl(self.value.units)
            set_button = self.Button('Set')
            reset_button = self.Button('Reset')

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)
            sizer.AddSpacer(1)
            sizer.Add(set_button, 0, wx.ALL, 5)
            sizer.Add(reset_button, 0, wx.ALL, 5)

            def on_set_button(evt):
                self.value.units = ctrl.GetValue()
                evt.Skip()

            def on_reset_button(evt):
                ctrl.SetValue(self.value.units)
                evt.Skip()

            set_button.Bind(wx.EVT_BUTTON, on_set_button)
            reset_button.Bind(wx.EVT_BUTTON, on_reset_button)

            self._units_ctrl = sizer

        return self._units_ctrl

    @property
    def index(self):
        if self._index_ctrl is None:
            label = self.StaticText('Index:')
            ctrl = self.TextCtrl(str(self.value.index), style=wx.TE_READONLY)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)

            self._index_ctrl = sizer

        return self._index_ctrl

    @property
    def label(self):
        if self._label_ctrl is None:
            label = self.StaticText('Label:')
            ctrl = self.TextCtrl(self.value.label)
            set_button = self.Button('Set')
            reset_button = self.Button('Reset')

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)
            sizer.AddSpacer(1)
            sizer.Add(set_button, 0, wx.ALL, 5)
            sizer.Add(reset_button, 0, wx.ALL, 5)

            def on_set_button(evt):
                self.value.label = ctrl.GetValue()
                evt.Skip()

            def on_reset_button(evt):
                ctrl.SetValue(self.value.label)
                evt.Skip()

            set_button.Bind(wx.EVT_BUTTON, on_set_button)
            reset_button.Bind(wx.EVT_BUTTON, on_reset_button)

            self._label_ctrl = sizer

        return self._label_ctrl

    @property
    def help(self):
        if self._help_ctrl is None:
            label = self.StaticText('Help:')
            ctrl = self.TextCtrl(
                self.value.help,
                style=wx.TE_MULTILINE
            )
            set_button = self.Button('Set')
            reset_button = self.Button('Reset')

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)
            sizer.AddSpacer(1)
            sizer.Add(set_button, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(reset_button, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            def on_set_button(evt):
                self.value.help = ctrl.GetValue()
                evt.Skip()

            def on_reset_button(evt):
                ctrl.SetValue(self.value.help)
                evt.Skip()

            set_button.Bind(wx.EVT_BUTTON, on_set_button)
            reset_button.Bind(wx.EVT_BUTTON, on_reset_button)

            self._help_ctrl = sizer

        return self._help_ctrl

    @property
    def max(self):
        if self._max_ctrl is None:
            if self.value.type in ('Int', 'Decimal', 'Short'):
                label = self.StaticText('Max:')
                ctrl = self.TextCtrl(str(self.value.max), style=wx.TE_READONLY)

                sizer = wx.BoxSizer(wx.HORIZONTAL)
                sizer.Add(label, 0, wx.ALL, 5)
                sizer.Add(ctrl, 1, wx.ALL, 5)

                self._max_ctrl = sizer

            else:
                self._max_ctrl = wx.BoxSizer(wx.HORIZONTAL)

        return self._max_ctrl

    @property
    def min(self):
        if self._min_ctrl is None:
            if self.value.type in ('Int', 'Decimal', 'Short'):
                label = self.StaticText('Min:')
                ctrl = self.TextCtrl(str(self.value.min), style=wx.TE_READONLY)

                sizer = wx.BoxSizer(wx.HORIZONTAL)
                sizer.Add(label, 0, wx.ALL, 5)
                sizer.Add(ctrl, 1, wx.ALL, 5)

                self._min_ctrl = sizer

            else:
                self._min_ctrl = wx.BoxSizer(wx.HORIZONTAL)

        return self._min_ctrl

    @property
    def type(self):
        if self._type_ctrl is None:
            label = self.StaticText('Type:')
            ctrl = self.TextCtrl(self.value.type, style=wx.TE_READONLY)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)

            self._type_ctrl = sizer

        return self._type_ctrl

    @property
    def genre(self):
        if self._genre_ctrl is None:
            label = self.StaticText('Genre:')
            ctrl = self.TextCtrl(self.value.genre, style=wx.TE_READONLY)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)

            self._genre_ctrl = sizer

        return self._genre_ctrl

    @property
    def instance(self):
        if self._instance_ctrl is None:
            label = self.StaticText('Instance:')
            ctrl = self.TextCtrl(
                str(self.value.instance),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)

            self._instance_ctrl = sizer

        return self._instance_ctrl

    @property
    def data_items(self):
        if self._items_ctrl is None:
            if self.value.type == 'List':
                label = self.StaticText('Genre:')
                ctrl = self.TextCtrl(
                    '\n'.join(self.value.data_items),
                    style=wx.TE_READONLY | wx.TE_MULTILINE
                )

                sizer = wx.BoxSizer(wx.HORIZONTAL)
                sizer.Add(label, 0, wx.ALL, 5)
                sizer.Add(ctrl, 1, wx.ALL, 5)

                self._items_ctrl = sizer
            else:
                self._items_ctrl =  wx.BoxSizer(wx.HORIZONTAL)

        return self._items_ctrl

    @property
    def is_set(self):
        if self._set_ctrl is None:
            label = self.StaticText('Is set:')
            ctrl = self.TextCtrl(str(self.value.is_set), style=wx.TE_READONLY)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)

            self._set_ctrl = sizer

        return self._set_ctrl

    @property
    def is_read_only(self):
        if self._read_ctrl is None:
            label = self.StaticText('Read only:')
            ctrl = self.TextCtrl(
                str(self.value.is_read_only),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)

            self._read_ctrl = sizer

        return self._read_ctrl

    @property
    def is_write_only(self):
        if self._write_ctrl is None:
            label = self.StaticText('Write only:')
            ctrl = self.TextCtrl(
                str(self.value.is_write_only),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)

            self._write_ctrl = sizer

        return self._write_ctrl

    @property
    def poll_intensity(self):
        if self._poll_ctrl is None:
            label = self.StaticText('Poll Intensity:')
            ctrl = self.SpinIntCtrl(
                self.value.poll_intensity,
                min=0,
                max=60
            )
            set_button = self.Button('Set')
            reset_button = self.Button('Reset')

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)
            sizer.AddSpacer(1)
            sizer.Add(set_button, 0, wx.ALL, 5)
            sizer.Add(reset_button, 0, wx.ALL, 5)

            def on_set_button(evt):
                self.value.poll_intensity = ctrl.GetValue()
                evt.Skip()

            def on_reset_button(evt):
                ctrl.SetValue(self.value.poll_intensity)
                evt.Skip()

            set_button.Bind(wx.EVT_BUTTON, on_set_button)
            reset_button.Bind(wx.EVT_BUTTON, on_reset_button)

            self._poll_ctrl = sizer

        return self._poll_ctrl

    @property
    def is_polled(self):
        if self._is_poll_ctrl is None:
            label = self.StaticText('Is polled:')
            ctrl = self.TextCtrl(
                str(self.value.is_polled),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)

            self._is_poll_ctrl = sizer

        return self._is_poll_ctrl

    @property
    def command_class(self):
        if self._cc_ctrl is None:
            label = self.StaticText('Command class:')
            ctrl = self.TextCtrl(
                self.value.command_class.class_desc,
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)

            self._cc_ctrl = sizer

        return self._cc_ctrl

    @property
    def refresh(self):
        if self._refresh_ctrl is None:
            ctrl = self.Button('Refresh')

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.AddSpacer(4)
            sizer.Add(ctrl, 0, wx.ALL, 5)

            def on_refresh_button(evt):
                self.value.refresh()
                evt.Skip()

            ctrl.Bind(wx.EVT_BUTTON, on_refresh_button)

            self._refresh_ctrl = sizer

        return self._refresh_ctrl

    @property
    def change_verified(self):
        if self._verified_ctrl is None:
            label = self.StaticText('Change verified:')
            change_verified = self.value.change_verified
            if change_verified is None:
                change_verified = False

            ctrl = self.CheckBox(change_verified)
            set_button = self.Button('Set')
            reset_button = self.Button('Reset')

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)
            sizer.AddSpacer(1)
            sizer.Add(set_button, 0, wx.ALL, 5)
            sizer.Add(reset_button, 0, wx.ALL, 5)

            def on_set_button(evt):
                self.value.change_verified = ctrl.GetValue()
                evt.Skip()

            def on_reset_button(evt):
                ctrl.SetValue(self.value.change_verified)
                evt.Skip()

            set_button.Bind(wx.EVT_BUTTON, on_set_button)
            reset_button.Bind(wx.EVT_BUTTON, on_reset_button)

            self._verified_ctrl = sizer

        return self._verified_ctrl

    @property
    def precision(self):
        if self._precison_ctrl is None:
            if self.value.type == 'Decimal':
                label = self.StaticText('Decimal precision:')
                ctrl = self.TextCtrl(
                    str(self.value.precision),
                    style=wx.TE_READONLY
                )

                sizer = wx.BoxSizer(wx.HORIZONTAL)
                sizer.Add(label, 0, wx.ALL, 5)
                sizer.Add(ctrl, 1, wx.ALL, 5)

                self._precison_ctrl = sizer

            else:
                self._precison_ctrl = wx.BoxSizer(wx.HORIZONTAL)

        return self._precison_ctrl

    @property
    def instance_label(self):
        if self._instance_label_ctrl is None:
            label = self.StaticText('Instance label:')
            ctrl = self.TextCtrl(
                self.value.instance_label,
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)

            self._instance_label_ctrl = sizer

        return self._instance_label_ctrl
