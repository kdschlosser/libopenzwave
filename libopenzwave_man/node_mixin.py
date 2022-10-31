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

from . import text_ctrl
from . import control_mixin


class NodeMixin(control_mixin.ControlMixin):

    def __init__(self, node):
        self.node = node

        self._header = None
        self._product_name_ctrl = None
        self._product_type_ctrl = None
        self._product_id_ctrl = None
        self._manufacturer_id_ctrl = None
        self._manufacturer_name_ctrl = None
        self._baud_ctrl = None
        self._neighbors_ctrl = None
        self._associated_ctrl = None
        self._category_ctrl = None
        self._sub_category_ctrl = None
        self._static_ctrl = None
        self._slave_ctrl = None
        self._portable_ctrl = None
        self._listening_ctrl = None
        self._freq_ctrl = None
        self._security_ctrl = None
        self._routing_ctrl = None
        self._locked_ctrl = None
        self._sleeping_ctrl = None
        self._failed_ctrl = None
        self._query_stage_ctrl = None
        self._info_ctrl = None
        self._update_neighbors_ctrl = None
        self._heal_ctrl = None
        self._test_ctrl = None
        self._return_route_ctrl = None
        self._refresh_node_ctrl = None
        self._refresh_values_ctrl = None
        self._delete_routes_ctrl = None
        self._send_information_ctrl = None
        self._network_update_ctrl = None
        self._request_params_ctrl = None
        self._set_param_ctrl = None

    @property
    def command_state(self):

        # SIGNAL_NODE_POLLING_DISABLED
        # SIGNAL_NODE_POLLING_ENABLED
        # SIGNAL_NODE_ASSOCIATION_GROUP
        # SIGNAL_NODE_LOADING_CACHED
        # SIGNAL_NODE_READY
        # SIGNAL_NODES_LOADED
        #
        # SIGNAL_NETWORK_CONTROLLER_COMMAND
        # SIGNAL_NETWORK_STOPPED
        # SIGNAL_NETWORK_READY
        # SIGNAL_NETWORK_FAILED
        #
        # SIGNAL_VALUE_LOADING_CACHED
        # SIGNAL_VALUE_CHANGED
        #
        # SIGNAL_VALUE_READY
        #
        # SIGNAL_USER_ALERTS

        if self._command_state_ctrl is None:
            ctrl = wx.Panel(self, -1, style=wx.BORDER_SIMPLE)
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            state_ctrl = wx.StaticText(ctrl, -1, '\n'.join([' ' * 40] * 3))

            sizer.Add(state_ctrl, 0, wx.ALL, 10)
            ctrl.SetSizer(sizer)

            def callback(state, *_, **__):

                label = [
                    str(state.command) + ': ' + state.command.doc,
                    str(state.state) + ': ' + state.state.doc
                ]
                if int(state.error) != 0:
                    label += [str(state.error) + ': ' + state.error.doc]
                    state_ctrl.SetBackgroundColour(wx.RED)

                else:
                    state_ctrl.SetBackgroundColour(ctrl.GetBackgroundColour())

                state_ctrl.SetLabel('\n'.join(label))

            def on_destroy(evt):
                libopenzwave.SIGNAL_NODE_CONTROLLER_COMMAND.unregister(
                    callback,
                    sender=self.node
                )
                evt.Skip()

            self.Bind(wx.EVT_WINDOW_DESTROY, on_destroy)

            libopenzwave.SIGNAL_NODE_CONTROLLER_COMMAND.register(
                callback,
                sender=self.node
            )

            self._command_state_ctrl = ctrl

        return self._command_state_ctrl

    @property
    def header(self):
        if self._header is None:
            panel = wx.Panel(self, -1, style=wx.BORDER_RAISED)

            name_ctrl = text_ctrl.TextCtrl(panel, -1, self.node.name)

            font = wx.Font(
                28,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )

            name_ctrl.SetFont(font)

            name_set = wx.Button(panel, -1, 'Set')
            name_reset = wx.Button(panel, -1, 'Reset')

            name_sizer = wx.BoxSizer(wx.HORIZONTAL)
            name_sizer.Add(name_ctrl, 0, wx.ALL, 5)
            name_sizer.AddSpacer(1)
            name_sizer.Add(name_set, 0, wx.ALL, 5)
            name_sizer.Add(name_reset, 0, wx.ALL, 5)

            def on_name_set(evt):
                self.node.name = name_ctrl.value
                evt.Skip()

            def on_name_reset(evt):
                name_ctrl.value = self.node.name
                evt.Skip()

            name_set.Bind(wx.EVT_BUTTON, on_name_set)
            name_reset.Bind(wx.EVT_BUTTON, on_name_reset)

            location_ctrl = text_ctrl.TextCtrl(panel, -1, self.node.location)
            font = wx.Font(
                16,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )

            location_ctrl.SetFont(font)
            location_set = wx.Button(panel, -1, 'Set')
            location_reset = wx.Button(panel, -1, 'Reset')

            location_sizer = wx.BoxSizer(wx.HORIZONTAL)
            location_sizer.Add(location_ctrl, 1, wx.ALL, 5)
            location_sizer.AddSpacer(1)
            location_sizer.Add(location_set, 0, wx.ALL, 5)
            location_sizer.Add(location_reset, 0, wx.ALL, 5)

            def on_location_set(evt):
                self.node.location = location_ctrl.value
                evt.Skip()

            def on_location_reset(evt):
                location_ctrl.value = self.node.location
                evt.Skip()

            location_set.Bind(wx.EVT_BUTTON, on_location_set)
            location_reset.Bind(wx.EVT_BUTTON, on_location_reset)

            id_label = wx.StaticText(
                panel,
                -1,
                'Id: 0x' + hex(self.node.id)[2:].upper()
            )

            font = wx.Font(
                12,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )

            id_label.SetFont(font)

            main_sizer = wx.BoxSizer(wx.VERTICAL)

            main_sizer.Add(name_sizer)
            main_sizer.Add(location_sizer)
            main_sizer.Add(id_label, 0, wx.ALL, 5)
            panel.SetSizer(main_sizer)

            self._header = panel

        return self._header

    @property
    def product_name(self):
        if self._product_name_ctrl is None:
            label = self.StaticText('Product name:')
            ctrl = self.TextCtrl(self.node.product_name, size=(200, -1))
            set_button = self.Button('Set')
            reset_button = self.Button('Reset')

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.AddSpacer(1)
            sizer.Add(set_button, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(reset_button, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            def on_set_button(evt):
                self.node.product_name = ctrl.GetValue()
                evt.Skip()

            def on_reset_button(evt):
                ctrl.SetValue(self.node.product_name)
                evt.Skip()

            set_button.Bind(wx.EVT_BUTTON, on_set_button)
            reset_button.Bind(wx.EVT_BUTTON, on_reset_button)

            self._product_name_ctrl = sizer

        return self._product_name_ctrl

    @property
    def product_type(self):
        if self._product_type_ctrl is None:
            label = self.StaticText('Product type:')
            ctrl = self.TextCtrl(
                self.node.product_type,
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._product_type_ctrl = sizer

        return self._product_type_ctrl

    @property
    def product_id(self):
        if self._product_id_ctrl is None:
            label = self.StaticText('Product id:')
            ctrl = self.TextCtrl(
                self.node.product_id,
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._product_id_ctrl = sizer

        return self._product_id_ctrl

    @property
    def manufacturer_id(self):
        if self._manufacturer_id_ctrl is None:
            label = self.StaticText('Manufacturer id:')
            ctrl = self.TextCtrl(
                self.node.manufacturer_id,
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._manufacturer_id_ctrl = sizer

        return self._manufacturer_id_ctrl

    @property
    def manufacturer_name(self):  # get/set

        if self._manufacturer_name_ctrl is None:
            label = self.StaticText('Manufacturer name:')
            ctrl = self.TextCtrl(self.node.manufacturer_name, size=(200, -1))
            set_button = self.Button('Set')
            reset_button = self.Button('Reset')

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.AddSpacer(1)
            sizer.Add(set_button, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(reset_button, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            def on_set_button(evt):
                self.node.manufacturer_name = ctrl.GetValue()
                evt.Skip()

            def on_reset_button(evt):
                ctrl.SetValue(self.node.manufacturer_name)
                evt.Skip()

            set_button.Bind(wx.EVT_BUTTON, on_set_button)
            reset_button.Bind(wx.EVT_BUTTON, on_reset_button)

            self._manufacturer_name_ctrl = sizer

        return self._manufacturer_name_ctrl

    # types # get
    @property
    def max_baud_rate(self):

        if self._baud_ctrl is None:
            label = self.StaticText('Max BAUD rate:')
            ctrl = self.TextCtrl(
                str(self.node.max_baud_rate),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._baud_ctrl = sizer

        return self._baud_ctrl

    @property
    def neighbors(self):
        if self._neighbors_ctrl is None:

            from . import node_neighbor_panel

            ctrl = node_neighbor_panel.NodeNeighborsPanel(self, self.node)
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._neighbors_ctrl = sizer

        return self._neighbors_ctrl

    @property
    def is_associated_to(self):  # get/set

        if self._associated_ctrl is None:
            from . import associated_to_panel

            ctrl = associated_to_panel.AssociatedToPanel(self, self.node)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._associated_ctrl = sizer

        return self._associated_ctrl

    @property
    def category(self):
        if self._category_ctrl is None:
            label = self.StaticText('Category:')
            ctrl = self.TextCtrl(
                str(self.node.category),
                style=wx.TE_READONLY,
                size=(200, -1)
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._category_ctrl = sizer

        return self._category_ctrl

    @property
    def sub_category(self):
        if self._sub_category_ctrl is None:
            label = self.StaticText('Sub category:')
            ctrl = self.TextCtrl(
                str(self.node.sub_category),
                style=wx.TE_READONLY,
                size=(200, -1)
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._sub_category_ctrl = sizer

        return self._sub_category_ctrl

    @property
    def is_static_controller(self):
        if self._static_ctrl is None:
            label = self.StaticText('Static controller:')
            ctrl = self.TextCtrl(
                str(self.node.is_static_controller),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._static_ctrl = sizer

        return self._static_ctrl

    @property
    def is_slave_controller(self):
        if self._slave_ctrl is None:
            label = self.StaticText('Slave controller:')
            ctrl = self.TextCtrl(
                str(self.node.is_slave_controller),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._slave_ctrl = sizer

        return self._slave_ctrl

    @property
    def is_portable_controller(self):
        if self._portable_ctrl is None:
            label = self.StaticText('Portable controller:')
            ctrl = self.TextCtrl(
                str(self.node.is_portable_controller),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._portable_ctrl = sizer

        return self._portable_ctrl

    @property
    def is_listening_device(self):
        if self._listening_ctrl is None:
            label = self.StaticText('Listening device:')
            ctrl = self.TextCtrl(
                str(self.node.is_listening_device),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._listening_ctrl = sizer

        return self._listening_ctrl

    @property
    def is_frequent_listening_device(self):
        if self._freq_ctrl is None:
            label = self.StaticText('Frequent listening device:')
            ctrl = self.TextCtrl(
                str(self.node.is_frequent_listening_device),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._freq_ctrl = sizer

        return self._freq_ctrl

    @property
    def is_security_device(self):
        if self._security_ctrl is None:
            label = self.StaticText('Security device:')
            ctrl = self.TextCtrl(
                str(self.node.is_security_device),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._security_ctrl = sizer

        return self._security_ctrl

    @property
    def is_routing_device(self):
        if self._routing_ctrl is None:
            label = self.StaticText('Routing device:')
            ctrl = self.TextCtrl(
                str(self.node.is_routing_device),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._routing_ctrl = sizer

        return self._routing_ctrl

    @property
    def is_locked(self):
        if self._locked_ctrl is None:
            label = self.StaticText('Locked:')
            ctrl = self.TextCtrl(
                str(self.node.is_locked),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._locked_ctrl = sizer

        return self._locked_ctrl

    @property
    def is_sleeping(self):
        if self._sleeping_ctrl is None:
            label = self.StaticText('Sleeping:')
            ctrl = self.TextCtrl(
                str(self.node.is_sleeping),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._sleeping_ctrl = sizer

        return self._sleeping_ctrl

    @property
    def is_failed(self):
        if self._failed_ctrl is None:
            is_failed = self.node.is_failed
            label = self.StaticText('Failed:')
            ctrl = self.TextCtrl(str(is_failed), style=wx.TE_READONLY)
            remove_button = self.Button('Remove Node')
            replace_button = self.Button('Replace Node')

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.AddSpacer(1)
            sizer.Add(remove_button, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(replace_button, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            def on_remove(evt):
                self.node.network.remove_node(self.node)
                evt.Skip()

            def on_replace(evt):
                self.node.network.replace_failed_node(self.node)
                evt.Skip()

            remove_button.Bind(wx.EVT_BUTTON, on_remove)
            replace_button.Bind(wx.EVT_BUTTON, on_replace)
            remove_button.Enable(is_failed)
            replace_button.Enable(is_failed)

            self._failed_ctrl = sizer

        return self._failed_ctrl

    @property
    def query_stage(self):
        if self._query_stage_ctrl is None:
            label = self.StaticText('Query stage:')
            ctrl = self.TextCtrl(self.node.query_stage, style=wx.TE_READONLY)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._query_stage_ctrl = sizer

        return self._query_stage_ctrl

    @property
    def is_info_received(self):
        if self._info_ctrl is None:
            label = self.StaticText('Info received:')
            ctrl = self.TextCtrl(
                str(self.node.is_info_received),
                style=wx.TE_READONLY
            )

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            self._info_ctrl = sizer

        return self._info_ctrl

    @property
    def update_neighbors(self):
        if self._update_neighbors_ctrl is None:
            ctrl = self.Button('Update Neighbors')

            def on_update(evt):
                self.node.update_neighbors()
                evt.Skip()

            ctrl.Bind(wx.EVT_BUTTON, on_update)

            self._update_neighbors_ctrl = ctrl

        return self._update_neighbors_ctrl

    @property
    def heal(self):
        if self._heal_ctrl is None:
            ctrl1 = self.Button('Heal Node')
            label = self.StaticText('Update Routes:')
            ctrl2 = self.CheckBox(False)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(ctrl1, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl2, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            def on_heal(evt):
                self.node.heal(ctrl2.GetValue())
                evt.Skip()

            ctrl1.Bind(wx.EVT_BUTTON, on_heal)

            self._heal_ctrl = sizer

        return self._heal_ctrl

    @property
    def test(self):
        if self._test_ctrl is None:
            ctrl1 = self.Button('Test Node')
            label = self.StaticText('Test count:')
            ctrl2 = self.SpinIntCtrl(1, min=1, max=100)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(ctrl1, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(label, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl2, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            def on_test(evt):
                self.node.test(ctrl2.GetValue())
                evt.Skip()

            ctrl1.Bind(wx.EVT_BUTTON, on_test)

            self._test_ctrl = sizer

        return self._test_ctrl

    @property
    def update_return_route(self):
        if self._return_route_ctrl is None:
            ctrl = self.Button('Update Return Route')

            def on_update(evt):
                self.node.update_return_route()
                evt.Skip()

            ctrl.Bind(wx.EVT_BUTTON, on_update)

            self._return_route_ctrl = ctrl

        return self._return_route_ctrl

    @property
    def refresh_node(self):
        if self._refresh_node_ctrl is None:
            ctrl = self.Button('Refresh Node')

            def on_update(evt):
                self.node.refresh_node()
                evt.Skip()

            ctrl.Bind(wx.EVT_BUTTON, on_update)

            self._refresh_node_ctrl = ctrl

        return self._refresh_node_ctrl

    @property
    def refresh_node_values(self):
        if self._refresh_values_ctrl is None:
            ctrl = self.Button('Refresh Values')

            def on_refresh(evt):
                self.node.refresh_node_values()
                evt.Skip()

            ctrl.Bind(wx.EVT_BUTTON, on_refresh)

            self._refresh_values_ctrl = ctrl

        return self._refresh_values_ctrl

    @property
    def delete_return_routes(self):
        if self._delete_routes_ctrl is None:
            ctrl = self.Button('Delete Return Routes')

            def on_delete(evt):
                self.node.delete_return_routes()
                evt.Skip()

            ctrl.Bind(wx.EVT_BUTTON, on_delete)

            self._delete_routes_ctrl = ctrl

        return self._delete_routes_ctrl

    @property
    def send_information(self):
        if self._send_information_ctrl is None:
            ctrl = self.Button('Send Information')

            def on_send(evt):
                self.node.send_information()
                evt.Skip()

            ctrl.Bind(wx.EVT_BUTTON, on_send)

            self._send_information_ctrl = ctrl

        return self._send_information_ctrl

    @property
    def network_update(self):
        if self._network_update_ctrl is None:
            ctrl = self.Button('Network Update')

            def on_update(evt):
                self.node.network_update()
                evt.Skip()

            ctrl.Bind(wx.EVT_BUTTON, on_update)

            self._network_update_ctrl = ctrl

        return self._network_update_ctrl

    @property
    def request_config_params(self):
        if self._request_params_ctrl is None:
            ctrl = self.Button('Request Cfg Params')

            def on_request(evt):
                self.node.request_config_params()
                evt.Skip()

            ctrl.Bind(wx.EVT_BUTTON, on_request)

            self._request_params_ctrl = ctrl

        return self._request_params_ctrl

    @property
    def set_config_param(self):
        if self._set_param_ctrl is None:
            ctrl1 = self.Button('Set Cfg Param')
            label1 = self.StaticText('Param #:')
            ctrl2 = self.SpinIntCtrl(1, min=1, max=100)

            label2 = self.StaticText('Value:')
            ctrl3 = self.SpinIntCtrl(0, min=0, max=1000000)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(ctrl1, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(label1, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl2, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(label2, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
            sizer.Add(ctrl3, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

            def on_set(evt):
                self.node.test(ctrl2.GetValue(), ctrl3.GetValue())
                evt.Skip()

            ctrl1.Bind(wx.EVT_BUTTON, on_set)

            self._set_param_ctrl = sizer

        return self._set_param_ctrl

    # stats # get
