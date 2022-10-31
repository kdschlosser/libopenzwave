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
from wx.lib.agw import aui
from wx.lib import scrolledpanel
import libopenzwave
from . import command_classes
from . import boxed_group
from . import node_mixin
from . import value_mixin
from . import spin_int_ctrl


def equalize_widths(*ctrls):
    max_width = max(ctrl.GetBestSize()[0] for ctrl in ctrls)
    for ctrl in ctrls:
        ctrl.SetMinSize((max_width, -1))


class PaneInfo(aui.AuiPaneInfo):

    def __init__(self, name, caption):
        aui.AuiPaneInfo.__init__(self)

        self.Caption(caption)
        self.Name(name)

        self.CaptionVisible(True, True)
        self.CloseButton()
        self.MaximizeButton()
        self.MinimizeButton()
        self.Movable()
        self.PaneBorder()
        self.PinButton()
        self.Resizable()
        self.DestroyOnClose()
        self.Dockable()
        self.Floatable()
        self.Gripper()
        self.Show()


class ValuePanel(scrolledpanel.ScrolledPanel, value_mixin.ValueMixin):

    def __init__(self, parent, network, value):
        self.network = network
        scrolledpanel.ScrolledPanel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        value_mixin.ValueMixin.__init__(self, value)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.header, 0, wx.EXPAND)
        sizer.Add(self.data)
        sizer.Add(self.units)
        sizer.Add(self.index)
        sizer.Add(self.help)
        sizer.Add(self.max)
        sizer.Add(self.min)
        sizer.Add(self.type)
        sizer.Add(self.genre)
        sizer.Add(self.instance)
        sizer.Add(self.data_items)
        sizer.Add(self.is_set)
        sizer.Add(self.is_read_only)
        sizer.Add(self.is_write_only)
        sizer.Add(self.poll_intensity)
        sizer.Add(self.is_polled)
        sizer.Add(self.command_class)
        sizer.Add(self.refresh)
        sizer.Add(self.change_verified)
        sizer.Add(self.precision)
        sizer.Add(self.instance_label)
        self.SetSizer(sizer)
        self.SetupScrolling()

        pane = PaneInfo(str(value.id), value.label)
        parent.AddPane(self, pane)

        def on_name(*_, **__):
            pane.Caption(self.value.label)

        libopenzwave.SIGNAL_NODE_NAMING.register(on_name, value.node)

        def on_destroy(evt):
            libopenzwave.SIGNAL_NODE_NAMING.unregister(on_name, value.node)
            evt.Skip()

        self.Bind(wx.EVT_WINDOW_DESTROY, on_destroy)


class StatePanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        state_ctrl = wx.StaticText(self, -1, ' ' * 20)

        background_colour = state_ctrl.GetBackgroundColour()

        def state_callback(state, **kwargs):
            command = state.command + ': '
            error = state.error
            state = state.state

            if int(error):
                command += error + ' (' + state + ')'
                self.SetToolTipString(error.doc)
                state_ctrl.SetBackgroundColour(wx.RED)
            else:
                command += state
                self.SetToolTipString(state.doc)
                state_ctrl.SetBackgroundColour(background_colour)

            state_ctrl.SetLabel(command)

        libopenzwave.SIGNAL_NETWORK_CONTROLLER_COMMAND.register(state_callback)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(state_ctrl, 1)

        self.SetSizer(sizer)

        def on_destroy(evt):
            libopenzwave.SIGNAL_NETWORK_CONTROLLER_COMMAND.unregister(
                state_callback
            )
            evt.Skip()

        self.Bind(wx.EVT_WINDOW_DESTROY, on_destroy)


def h_sizer(*ctrls):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    for ctrl in ctrls:
        sizer.Add(ctrl, 0, wx.ALL, 5)

    return sizer


class NodeToolbar(aui.AuiToolBar):
    
    def __init__(self, parent):
        self.node = None
        self.parent = parent

        aui.AuiToolBar.__init__(
            self,
            parent,
            -1,
            agwStyle=aui.AUI_TB_HORZ_TEXT | aui.AUI_TB_NO_TOOLTIPS
        )

        refresh_node_id = wx.NewId()
        refresh_node_values_id = wx.NewId()
        network_update_id = wx.NewId()
        send_information_id = wx.NewId()
        update_return_route_id = wx.NewId()
        delete_return_routes_id = wx.NewId()
        request_config_params_id = wx.NewId()

        def on_left_down(evt):
            x, y = evt.GetPosition()
            item = self.FindToolForPosition(x, y)
            if item:
                id = item.GetId()

                if id == refresh_node_id:
                    self.node,refresh_node()

                elif id == refresh_node_values_id:
                    self.node.refresh_node_values()

                elif id == network_update_id:
                    self.node.network_update()

                elif id == send_information_id:
                    self.node.send_information()

                elif id == update_return_route_id:
                    self.node.update_return_route()

                elif id == delete_return_routes_id:
                    self.node.delete_return_routes()

                elif id == request_config_params_id:
                    self.node.request_config_params()

            evt.Skip()

        self.Bind(wx.EVT_LEFT_DOWN, on_left_down)

        refresh_node = self.AddSimpleTool(
            refresh_node_id,
            'Refresh Node',
            bitmap=wx.NullBitmap,
            kind=aui.ITEM_NORMAL
        )

        refresh_node_values = self.AddSimpleTool(
            refresh_node_values_id,
            'Refresh Node Values',
            bitmap=wx.NullBitmap,
            kind=aui.ITEM_NORMAL
        )
        network_update = self.AddSimpleTool(
            network_update_id,
            'Network Update',
            bitmap=wx.NullBitmap,
            kind=aui.ITEM_NORMAL
        )
        
        send_information = self.AddSimpleTool(
            send_information_id,
            'Send NIF',
            bitmap=wx.NullBitmap,
            kind=aui.ITEM_NORMAL
        )

        update_return_route = self.AddSimpleTool(
            update_return_route_id,
            'Update Return Routes',
            bitmap=wx.NullBitmap,
            kind=aui.ITEM_NORMAL
        )

        delete_return_routes = self.AddSimpleTool(
            delete_return_routes_id,
            'Delete Return Routes',
            bitmap=wx.NullBitmap,
            kind=aui.ITEM_NORMAL
        )

        self.AddSeparator()

        request_config_params = self.AddSimpleTool(
            request_config_params_id,
            'Request Config Params',
            bitmap=wx.NullBitmap,
            kind=aui.ITEM_NORMAL
        )

        config_panel = wx.Panel(self, -1, style=wx.BORDER_NONE)
        config_sizer = wx.BoxSizer(wx.VERTICAL)

        config_param_label = wx.StaticText(config_panel, -1, 'Param #:')
        config_param_ctrl = self.config_param_ctrl = spin_int_ctrl.SpinIntCtrl(config_panel, -1, value=0, min=0, max=255)
        config_param_sizer = h_sizer(config_param_label, config_param_ctrl)

        config_value_label = wx.StaticText(config_panel, -1, 'Value:')
        config_value_ctrl = self.config_value_ctrl = spin_int_ctrl.SpinIntCtrl(config_panel, -1, value=0)
        config_value_sizer = h_sizer(config_value_label, config_value_ctrl)

        config_execute = wx.Button(config_panel, -1, 'Execute')
        config_execute_sizer = wx.BoxSizer(wx.HORIZONTAL)
        config_execute_sizer.AddStretchSpacer(1)
        config_execute_sizer.Add(config_execute)
        config_execute_sizer.AddStretchSpacer(1)

        config_sizer.Add(config_param_sizer, 0, wx.EXPAND)
        config_sizer.Add(config_value_sizer, 0, wx.EXPAND)
        config_sizer.Add(config_execute_sizer)
        config_panel.SetSizer(config_sizer)

        def on_config(evt):
            self.node.set_config_param(self.config_param_ctrl.GetValue(), self.config_value.ctrl.GetValue())
            evt.Skip()

        config_execute.Bind(wx.EVT_BUTTON, on_config)

        self.AddControl(
            config_panel,
            'Set Config Param'
        )

        self.AddSeparator()

        test_panel = wx.Panel(self, -1, style=wx.BORDER_NONE)
        test_sizer = wx.BoxSizer(wx.VERTICAL)

        test_count_label = wx.StaticText(test_panel, -1, 'Test count:')
        test_count_ctrl = self.test_count_ctrl = spin_int_ctrl.SpinIntCtrl(test_panel, -1, value=1, min=1, max=100)
        test_count_sizer = h_sizer(test_count_label, test_count_ctrl)

        test_execute = wx.Button(test_panel, -1, 'Execute')
        test_execute_sizer = wx.BoxSizer(wx.HORIZONTAL)
        test_execute_sizer.AddStretchSpacer(1)
        test_execute_sizer.Add(test_execute)
        test_execute_sizer.AddStretchSpacer(1)

        test_sizer.Add(test_count_sizer, 0, wx.EXPAND)
        test_sizer.Add(test_execute_sizer)
        test_panel.SetSizer(test_sizer)

        def on_test(evt):
            self.node.test(test_count_ctrl.GetValue())
            evt.Skip()

        test_execute.Bind(wx.EVT_BUTTON, on_test)

        self.AddControl(
            test_panel,
            'Test Node'
        )

        self.AddSeparator()
        
        heal_panel = wx.Panel(self, -1, style=wx.BORDER_NONE)
        heal_sizer = wx.BoxSizer(wx.VERTICAL)

        heal_update_label = wx.StaticText(heal_panel, -1, 'Update Routes:')
        heal_update_ctrl = self.heal_update_ctrl = wx.CheckBox(heal_panel, -1, '')
        heal_update_ctrl.SetValue(True)
        heal_update_sizer = h_sizer(heal_update_label, heal_update_ctrl)
        
        heal_execute = wx.Button(heal_panel, -1, 'Execute')
        heal_execute_sizer = wx.BoxSizer(wx.HORIZONTAL)
        heal_execute_sizer.AddStretchSpacer(1)
        heal_execute_sizer.Add(heal_execute)
        heal_execute_sizer.AddStretchSpacer(1)
        
        heal_sizer.Add(heal_update_sizer, 0, wx.EXPAND)
        heal_sizer.Add(heal_execute_sizer)
        heal_panel.SetSizer(heal_sizer)

        def on_heal(evt):
            self.node.heal(heal_update_ctrl.GetValue())
            evt.Skip()

        heal_execute.Bind(wx.EVT_BUTTON, on_heal)

        self.AddControl(
            heal_panel,
            'Heal Node'
        )

    def SetNode(self, node):
        self.node = node
        self.config_param_ctrl.SetValue(0)
        self.config_value_ctrl.SetValue(0)
        self.test_count_ctrl.SetValue(1)
        self.heal_update_ctrl.SetValue(True)

        if node is None:
            self.parent.node_toolbar_pane.Show(False)
            self.parent.aui_manager.Update()
        else:
            self.parent.node_toolbar_pane.Show()
            self.parent.aui_manager.Update()


class ValueToolbar(aui.AuiToolBar):

    def __init__(self, parent):
        self.value = None
        self.parent = parent

        aui.AuiToolBar.__init__(
            self,
            parent,
            -1,
            agwStyle=aui.AUI_TB_HORZ_TEXT | aui.AUI_TB_NO_TOOLTIPS
        )

        refresh_value_id = wx.NewId()
        change_verified_id = wx.NewId()

        def on_left_down(evt):
            x, y = evt.GetPosition()
            item = self.FindToolForPosition(x, y)
            if item:
                id = item.GetId()

                if id == refresh_value_id:
                   self.value.refresh()

            evt.Skip()

        self.Bind(wx.EVT_LEFT_DOWN, on_left_down)

        def on_check(evt):
            x, y = evt.GetPosition()
            item = self.FindToolForPosition(x, y)
            if item:
                id = item.GetId()
                if id == change_verified_id:
                    self.value.change_verified = self.change_verified.GetState()

            evt.Skip()

        self.Bind(wx.EVT_CHECKBOX, on_check)

        self.AddSimpleTool(
            refresh_value_id,
            'Refresh Value',
            bitmap=wx.NullBitmap,
            kind=aui.ITEM_NORMAL
        )

        self.change_verified = self.AddCheckTool(
            change_verified_id,
            'Verify Value Changes',
            wx.NullBitmap,
            wx.NullBitmap
        )

        self.AddSeparator()

        poll_panel = wx.Panel(self, -1, style=wx.BORDER_NONE)
        poll_sizer = wx.BoxSizer(wx.VERTICAL)

        poll_intensity_label = wx.StaticText(poll_panel, -1, 'Poll intensity:')
        poll_intensity_ctrl = self.poll_intensity_ctrl = spin_int_ctrl.SpinIntCtrl(poll_panel, -1, value=0, min=0, max=100)
        poll_intensity_sizer = h_sizer(poll_intensity_label, poll_intensity_ctrl)

        poll_execute = wx.Button(poll_panel, -1, 'Execute')
        poll_execute_sizer = wx.BoxSizer(wx.HORIZONTAL)
        poll_execute_sizer.AddStretchSpacer(1)
        poll_execute_sizer.Add(poll_execute)
        poll_execute_sizer.AddStretchSpacer(1)

        poll_sizer.Add(poll_intensity_sizer, 0, wx.EXPAND)
        poll_sizer.Add(poll_execute_sizer)
        poll_panel.SetSizer(poll_sizer)

        def on_poll(evt):
            self.value.poll_intensity = poll_intensity_ctrl.GetValue()
            evt.Skip()

        poll_execute.Bind(wx.EVT_BUTTON, on_poll)

        self.AddControl(
            poll_panel,
            'Value Polling'
        )

    def SetValue(self, value):
        self.value = value

        if value is None:
            self.parent.value_toolbar_pane.Show(False)
            self.parent.aui_manager.Update()
        else:
            self.poll_intensity_ctrl.SetValue(value.poll_intensity)
            self.change_verified.SetState(value.change_verified)
            self.parent.value_toolbar_pane.Show()
            self.parent.aui_manager.Update()
            

class NodePanel(scrolledpanel.ScrolledPanel, node_mixin.NodeMixin):

    def __init__(self, parent, network, node):
        self.network = network
        scrolledpanel.ScrolledPanel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        node_mixin.NodeMixin.__init__(self, node)

        parent.node_toolbar.SetNode(node)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.header, 0, wx.EXPAND)

        category_box = boxed_group.BoxedGroup(
            self,
            'Category Info',
            self.category,
            self.sub_category
        )

        product_box = boxed_group.BoxedGroup(
            self,
            'Product Info',
            self.product_name,
            self.product_id,
            self.product_type,
        )

        manufacturer_box = boxed_group.BoxedGroup(
            self,
            'Manufacturer Info',
            self.manufacturer_name,
            self.manufacturer_id

        )

        neighbor_box = boxed_group.BoxedGroup(
            self,
            'Neighbor Info',
            (self.neighbors, 0, wx.EXPAND),
            self.update_neighbors,
        )

        node_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_node_sizer = wx.BoxSizer(wx.VERTICAL)
        right_node_sizer = wx.BoxSizer(wx.VERTICAL)

        left_node_sizer.Add(self.is_static_controller)
        right_node_sizer.Add(self.is_slave_controller)
        left_node_sizer.Add(self.is_portable_controller)
        right_node_sizer.Add(self.max_baud_rate)
        left_node_sizer.Add(self.is_listening_device)
        right_node_sizer.Add(self.is_routing_device)
        left_node_sizer.Add(self.is_frequent_listening_device)
        right_node_sizer.Add(self.is_failed)
        left_node_sizer.Add(self.is_security_device)
        right_node_sizer.Add(self.is_sleeping)
        left_node_sizer.Add(self.query_stage)
        right_node_sizer.Add(self.is_info_received)

        node_sizer.Add(left_node_sizer)
        node_sizer.Add(right_node_sizer)

        node_box = boxed_group.BoxedGroup(
            self,
            'Node Info',
            node_sizer
        )
     
        sizer.Add(category_box, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(product_box, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(manufacturer_box, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(neighbor_box, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(node_box, 0, wx.ALL | wx.EXPAND, 5)

        if node.is_openzwave_controller:
            sizer.Add(wx.StaticLine(self, -1, size=(0, 5)), 0, wx.ALL | wx.EXPAND, 5)

            py_lib_config_version_label = self.StaticText(
                'Python Library Config Version:'
            )
            py_lib_config_version_ctrl = self.TextCtrl(
                str(node.python_library_config_version),
                style=wx.TE_READONLY
            )
            py_lib_config_version_sizer = h_sizer(
                py_lib_config_version_label,
                py_lib_config_version_ctrl
            )

            py_lib_version_label = self.StaticText(
                'Python Library Version:'
            )
            py_lib_version_ctrl = self.TextCtrl(
                str(node.python_library_version),
                style=wx.TE_READONLY
            )
            py_lib_version_sizer = h_sizer(
                py_lib_version_label,
                py_lib_version_ctrl
            )

            py_lib_flavor_label = self.StaticText(
                'Python Library Flavor:'
            )
            py_lib_flavor_ctrl = self.TextCtrl(
                str(node.python_library_flavor),
                style=wx.TE_READONLY
            )
            py_lib_flavor_sizer = h_sizer(
                py_lib_flavor_label,
                py_lib_flavor_ctrl
            )

            lib_version_label = self.StaticText(
                'Library Version:'
            )
            lib_version_ctrl = self.TextCtrl(
                str(node.library_version),
                style=wx.TE_READONLY
            )
            lib_version_sizer = h_sizer(
                lib_version_label,
                lib_version_ctrl
            )

            lib_description_label = self.StaticText(
                'Library Description:'
            )
            lib_description_ctrl = self.TextCtrl(
                str(node.library_description),
                style=wx.TE_READONLY
            )
            lib_description_sizer = h_sizer(
                lib_description_label,
                lib_description_ctrl
            )

            lib_type_name_label = self.StaticText(
                'Library Type Name:'
            )
            lib_type_name_ctrl = self.TextCtrl(
                str(node.library_type_name),
                style=wx.TE_READONLY
            )
            lib_type_name_sizer = h_sizer(
                lib_type_name_label,
                lib_type_name_ctrl
            )

            ozw_lib_version_label = self.StaticText(
                'OpenZWave Library Version:'
            )
            ozw_lib_version_ctrl = self.TextCtrl(
                str(node.ozw_library_version),
                style=wx.TE_READONLY
            )
            ozw_lib_version_sizer = h_sizer(
                ozw_lib_version_label,
                ozw_lib_version_ctrl
            )

            user_path_label = self.StaticText(
                'User Path:'
            )
            user_path_ctrl = self.TextCtrl(
                str(node.library_user_path),
                style=wx.TE_READONLY
            )
            user_path_sizer = h_sizer(
                user_path_label,
                user_path_ctrl
            )

            config_path_label = self.StaticText(
                'Config Path:'
            )
            config_path_ctrl = self.TextCtrl(
                str(node.library_config_path),
                style=wx.TE_READONLY
            )
            config_path_sizer = h_sizer(
                config_path_label,
                config_path_ctrl
            )

            primary_controller_label = self.StaticText(
                'Primary Controller:'
            )
            primary_controller_ctrl = self.TextCtrl(
                str(node.is_primary_controller),
                style=wx.TE_READONLY
            )
            primary_controller_sizer = h_sizer(
                primary_controller_label,
                primary_controller_ctrl
            )

            sizer.Add(py_lib_config_version_sizer)
            sizer.Add(py_lib_version_sizer)
            sizer.Add(py_lib_flavor_sizer)
            sizer.Add(lib_version_sizer)
            sizer.Add(lib_description_sizer)
            sizer.Add(lib_type_name_sizer)
            sizer.Add(ozw_lib_version_sizer)
            sizer.Add(user_path_sizer)
            sizer.Add(config_path_sizer)
            sizer.Add(primary_controller_sizer)

        if node.is_openzwave_controller:
            hard_reset_button = self.Button('Hard Reset')

            def on_hard_reset(evt):
                node.hard_reset()
                evt.Skip()

            hard_reset_button.Bind(wx.EVT_BUTTON, on_hard_reset)

            soft_reset_button = self.Button('Soft Reset')

            def on_soft_reset(evt):
                node.soft_reset()
                evt.Skip()

            soft_reset_button.Bind(wx.EVT_BUTTON, on_soft_reset)

            create_new_primary_button = self.Button('Create New Primary')

            def on_create_new_primary(evt):
                node.create_new_primary()
                evt.Skip()

            create_new_primary_button.Bind(
                wx.EVT_BUTTON,
                on_create_new_primary
            )

            transfer_primary_role_button = self.Button('Transfer Primary Role')

            def on_transfer_primary_role(evt):
                node.transfer_primary_role()
                evt.Skip()

            transfer_primary_role_button.Bind(
                wx.EVT_BUTTON,
                on_transfer_primary_role
            )

            receive_configuration_button = self.Button('Receive Configuration')

            def on_receive_configuration(evt):
                node.receive_configuration()
                evt.Skip()

            receive_configuration_button.Bind(
                wx.EVT_BUTTON,
                on_receive_configuration
            )

            button_sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
            button_sizer_3.Add(hard_reset_button, 0, wx.ALL, 5)
            button_sizer_3.Add(soft_reset_button, 0, wx.ALL, 5)
            button_sizer_3.Add(create_new_primary_button, 0, wx.ALL, 5)
            button_sizer_3.Add(transfer_primary_role_button, 0, wx.ALL, 5)
            button_sizer_3.Add(receive_configuration_button, 0, wx.ALL, 5)

            sizer.Add(button_sizer_3)


        from libopenzwave.command_classes import COMMAND_CLASSES

        added_panels = []
        for cc_id in node._command_classes:
            cc = COMMAND_CLASSES[cc_id]
            cc_panel = cc.get_panel(node, self)
            if cc_panel not in added_panels:
                added_panels += [cc_panel]
                sizer.Add(cc_panel)

        self.SetSizer(sizer)
        self.SetupScrolling()

        node_pane = PaneInfo(
            str(node.id),
            node.name + ' (' + node.location + ')'
        )
        parent.AddPane(self, node_pane)


class IndexPanel(wx.Panel):

    def __init__(self, parent, pane):
        self.pane = pane
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(self.main_sizer)
        self.current_window = None

    def SetValue(self, value):
        if self.current_window is not None:
            self.main_sizer.Replace(self.current_window, value)
            self.current_window.Destroy()
            self.current_window = value

        else:
            self.main_sizer.Add(value, 1)
            self.current_window = value

        self.pane.Show()
        self.main_sizer.Layout()
        self.Layout()
        self.Refresh()


class NetworkPanel(wx.TreeCtrl):

    def __init__(self, parent):
        self.__add_node_lock = threading.Lock()
        self.add_nodes = []
        self.network = network = parent
        wx.TreeCtrl.__init__(
            self,
            parent,
            -1,
            style=(
                wx.TR_HAS_BUTTONS |
                wx.TR_FULL_ROW_HIGHLIGHT |
                wx.TR_SINGLE |
                wx.TR_EDIT_LABELS
            )
        )

        if network.id in (0, None):
            def ready_callback(*_, **__):
                self.SetItemText(self.root, 'Network ID: 0x' + hex(network.id)[2:].upper())

            libopenzwave.SIGNAL_NETWORK_READY.register(ready_callback)

            self.root = self.AddRoot('Network Loading...')
        else:
            self.root = self.AddRoot(
                'Network ID: 0x' + hex(network.id)[2:].upper()
            )

        libopenzwave.SIGNAL_NODE_ADDED.register(self.AddNode)
        libopenzwave.SIGNAL_NODE_DATASET_LOADED.register(self.AddNode)

        self.SetItemData(self.root, network)
        self._node_view = True

        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.on_collapsing)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.on_expanding)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_activated)

        for node in network:
            self.AddNode(node)

    @property
    def node_view(self):
        return self._node_view

    @node_view.setter
    def node_view(self, value):
        self.DeleteAllItems()
        self._node_view = value

        self.root = self.AddRoot(
            'Network ID: 0x' + hex(self.network.id)[2:].upper()
        )

        for node in self.network:
            self.AddNode(node)

    def on_activated(self, evt):
        item_id = evt.GetItem()

        from libopenzwave.node import ZWaveNode
        from libopenzwave.value import ZWaveValue

        data = self.GetItemData(item_id)

        if isinstance(data, ZWaveNode):
            pane = self.GetParent().aui_manager.GetPaneByName(str(data.id))
            if pane.IsOk():
                pane.Show()
            else:
                NodePanel(self.GetParent(), self.network, data)

        if isinstance(data, ZWaveValue):
            pane = self.GetParent().aui_manager.GetPaneByName(str(data.id))

            if pane.IsOk():
                pane.Show()
            else:
                pane = self.GetParent().aui_manager.GetPaneByName(
                    str(data.parent_id)
                )

                if not pane.IsOk():
                    NodePanel(self.GetParent(), self.network, data.node)

                ValuePanel(self.GetParent(), self.network, data)

        evt.Skip()

    def AddNode(self, node, *_, **__):
        with self.__add_node_lock:
            if node in self.add_nodes:
                return

            self.add_nodes += [node]
            if not self.IsExpanded(self.root):
                self.Expand(self.root)

            if self.node_view:
                for i, n in enumerate(self.network):
                    if n == node:
                        break
                else:
                    return

                item_id = self.InsertItem(
                    self.root,
                    i,
                    node.name +
                    ' (' + node.location + ') loading...'
                )

                if node.is_ready:
                    self.SetItemText(
                        item_id,
                        node.name +' (' + node.location + ')'
                    )

                else:
                    def node_ready(*_, **__):
                        self.SetItemText(
                            item_id,
                            node.name + ' (' + node.location + ')'
                        )
                        libopenzwave.SIGNAL_NODE_READY.unregister(node_ready, node)

                    libopenzwave.SIGNAL_NODE_READY.register(node_ready, node)


                self.SetItemData(item_id, node)
                self.SetItemHasChildren(item_id, True)
            else:
                item_id, cookie = self.GetFirstChild(self.root)

                while item_id.IsOk():
                    location = self.GetItemData(item_id)

                    if node in location:
                        if self.IsExpanded(item_id):
                            self.Collapse(item_id)
                            self.Expand(item_id)
                        return

                    item_id = self.GetNextChild(self.root, item_id)

                for i, location in enumerate(self.network):
                    if node in location:
                        break

                else:
                    return

                item_id = self.InsertItem(self.root, i, location.name)
                self.SetItemData(item_id, location)
                self.SetItemHasChildren(item_id, True)

    def on_expanding(self, evt):
        from libopenzwave.node import ZWaveNode

        item_id = evt.GetItem()
        data = self.GetItemData(item_id)

        if isinstance(data, ZWaveNode):
            for value in data:
                child_id = self.AppendItem(item_id, value.label, data=value)

        self.Unbind(wx.EVT_TREE_ITEM_EXPANDING, handler=self.on_expanding)
        self.Expand(item_id)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.on_expanding)

    def on_collapsing(self, evt):
        item_id = evt.GetItem()
        self.Unbind(wx.EVT_TREE_ITEM_COLLAPSING, handler=self.on_collapsing)
        self.Collapse(item_id)

        self.DeleteChildren(item_id)
        self.SetItemHasChildren(item_id)

        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.on_collapsing)

import threading

class InfoBar(wx.InfoBar):

    def __init__(self, parent):
        wx.InfoBar.__init__(self, parent)
        self.SetShowHideEffects(
            wx.SHOW_EFFECT_ROLL_TO_BOTTOM,
            wx.SHOW_EFFECT_ROLL_TO_TOP
        )

        self.node = None
        self.node_button = None
        self.dismiss_thread = threading.Thread(target=self.dismiss_timer)
        self.dismiss_thread.daemon = True
        self.dismiss_event = threading.Event()

    def __get_message(self, state):
        error = state.error
        command = state.command
        state = state.state

        message = [command.label]

        if int(error):
            icon = wx.ICON_ERROR
            message += ['ERROR: ' + error.doc]
        else:
            if state in (
                'Starting',
                'Cancel',
                'InProgress',
                'Completed',
                'NodeOK'
            ):
                icon = wx.ICON_INFORMATION
            elif state in ('Sleeping', 'NodeFailed'):
                icon = wx.ICON_WARNING
            elif state in ('Waiting',):
                icon = wx.ICON_QUESTION
            elif state in ('Error', 'Failed'):
                icon = wx.ICON_ERROR
            else:
                return

            message += [state.doc]
        return message, icon

    def dismiss_timer(self):
        self.dismiss_event.wait(30)
        self.Dismiss()
        if self.node_button is not None:
            self.Unbind(
                wx.EVT_BUTTON,
                handler=self.on_node_button,
                id=self.node_button
            )
            self.RemoveButton(self.node_button)
            self.node = None
            self.node_button = None

        self.dismiss_thread = threading.Thread(target=self.dismiss_timer)
        self.dismiss_thread.daemon = True
        self.dismiss_event.clear()

    def ShowNetworkMessage(self, state):
        if not int(state.command):
            return

        message, icon = self.__get_message(state)
        message = ['Network'] + message

        if self.dismiss_thread.is_alive():
            self.dismiss_event.set()
            while self.dismiss_event.is_set():
                pass

        self.ShowMessage('\n'.join(message), icon)
        self.dismiss_thread.start()

    def ShowNodeMessage(self, state, node):
        if not int(state.command):
            return

        message, icon = self.__get_message(state)
        message = [node.name + '(' + node.location + ')'] + message

        if self.dismiss_thread.is_alive():
            self.dismiss_event.set()
            while self.dismiss_event.is_set():
                pass

        self.node = node
        self.node_button = wx.NewId()
        self.AddButton(self.node_button, 'Go To Node')
        self.Bind(wx.EVT_BUTTON, self.on_node_button, id=self.node_button)

        self.ShowMessage('\n'.join(message), icon)
        self.dismiss_thread.start()

    def ShowAlert(self, alert, node):

        if not int(alert):
            return

        if alert in ('ConfigOutOfDate', 'MFSOutOfDate'):
            icon = wx.ICON_WARNING
        elif alert in (
            'NodeReloadRequired',
            'ApplicationStatus_Retry',
            'ApplicationStatus_Queued'
        ):
            icon = wx.ICON_INFORMATION
        elif alert in (
            'ConfigFileDownloadFailed',
            'DNSError',
            'UnsupportedController',
            'ApplicationStatus_Rejected'
        ):
            icon = wx.ICON_ERROR
        else:
            return

        if self.dismiss_thread.is_alive():
            self.dismiss_event.set()
            while self.dismiss_event.is_set():
                pass

        if node is None:
            message = ['Network']

        else:
            message = [node.name + '(' + node.location + ')']
            self.node = node
            self.node_button = wx.NewId()
            self.AddButton(self.node_button, 'Go To Node')
            self.Bind(wx.EVT_BUTTON, self.on_node_button, id=self.node_button)

        message += [alert.doc]

        self.ShowMessage('\n'.join(message), icon)
        self.dismiss_thread.start()

    def on_node_button(self, _):
        node = self.node
        self.dismiss_event.set()

        parent = self.GetParent()
        parent.network_ctrl.SelectNode(node)


from libopenzwave import ZWaveNetwork


@libopenzwave.subclass_zwave_class(ZWaveNetwork, wx.Frame)
class UIManager:
    def __init__(self, options, auto_start=True):
        ZWaveNetwork.__init__(self, options, auto_start=auto_start)

        wx.Frame.__init__(self, None, -1, size=(1800, 900), title='Z-Wave Manager', pos=(0, 0))
        
        self.aui_manager = aui.AuiManager(
            self,
            agwFlags=(
                aui.AUI_MGR_ALLOW_FLOATING |
                aui.AUI_MGR_ALLOW_ACTIVE_PANE |
                aui.AUI_MGR_TRANSPARENT_DRAG |
                aui.AUI_MGR_TRANSPARENT_HINT |
                aui.AUI_MGR_PREVIEW_MINIMIZED_PANES |
                aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE |
                aui.AUI_MGR_RECTANGLE_HINT |
                aui.AUI_MGR_LIVE_RESIZE |
                aui.AUI_MGR_SMOOTH_DOCKING |
                aui.AUI_MGR_WHIDBEY_DOCKING_GUIDES
            )
        )

        self.info_bar = InfoBar(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.info_bar, 1, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(sizer)

        libopenzwave.SIGNAL_USER_ALERTS.register(self.on_user_alert)
        libopenzwave.SIGNAL_NETWORK_CONTROLLER_COMMAND.register(self.on_network_command)
        libopenzwave.SIGNAL_NODE_CONTROLLER_COMMAND.register(self.on_node_command)

        self.network_toolbar = NetworkToolbar(self)
        self.network_toolbar_pane = PaneInfo('network_toolbar', 'Network Actions')
        self.network_toolbar_pane.CaptionVisible(True)
        self.network_toolbar_pane.ToolbarPane()
        self.network_toolbar_pane.Right()
        
        self.node_toolbar = NodeToolbar(self)
        self.node_toolbar_pane = PaneInfo('node_toolbar', 'Node Actions')
        self.node_toolbar_pane.CaptionVisible(True)
        self.node_toolbar_pane.ToolbarPane()
        self.node_toolbar_pane.Left()
        
        self.value_toolbar = ValueToolbar(self)
        self.value_toolbar_pane = PaneInfo('value_toolbar', 'Network Actions')
        self.value_toolbar_pane.CaptionVisible(True)
        self.value_toolbar_pane.ToolbarPane()
        self.value_toolbar_pane.Left()

        self.AddPane(self.network_toolbar, self.network_toolbar_pane)
        self.AddPane(self.node_toolbar, self.node_toolbar_pane)
        self.AddPane(self.value_toolbar, self.value_toolbar_pane)
        
        self.node_toolbar.SetNode(None)
        self.value_toolbar.SetValue(None)

        self.network_ctrl = NetworkPanel(self)
        self.network_pane = PaneInfo('network_pane', 'Network')
        self.network_pane.CenterPane()
        self.AddPane(self.network_ctrl, self.network_pane)

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)

    def on_close(self, evt):
        self.Hide()
        self.stop()
        self.Destroy()
        
    def stop(self):
        stop_event = threading.Event()
        def stop_callback(*_, **__):
            stop_event.set()
                
        libopenzwave.SIGNAL_NETWORK_STOPPED.register(stop_callback)
        ZWaveNetwork.stop(self)
        stop_event.wait()
        libopenzwave.SIGNAL_NETWORK_STOPPED.unregister(stop_callback)

    def on_destroy(self, evt):
        if self.state != self.STATE_STOPPED:
            self.stop()
        evt.Skip()

    def on_network_command(self, state, *_, **__):
        wx.CallAfter(self.info_bar.ShowNetworkMessage, state)

    def on_node_command(self, state, node, *_, **__):
        wx.CallAfter(self.info_bar.ShowNodeMessage, state, node)

    def on_user_alert(self, alert, node=None, *_, **__):
        wx.CallAfter(self.info_bar.ShowAlert, alert, node)

    def AddPane(self, window, pane_info):
        self.aui_manager.AddPane(window, pane_info)
        self.aui_manager.Update()
        pane_info.Show()


class NetworkToolbar(aui.AuiToolBar):
    
    def __init__(self, parent):

        aui.AuiToolBar.__init__(
            self,
            parent,
            -1,
            agwStyle=aui.AUI_TB_HORZ_TEXT | aui.AUI_TB_NO_TOOLTIPS
        )

        node_security_id = wx.NewId()
        add_node_id = wx.NewId()
        remove_node_id = wx.NewId()
        test_id = wx.NewId()
        heal_id = wx.NewId()
        heal_routes_id = wx.NewId()
        check_mfs_id = wx.NewId()
        download_mfs_id = wx.NewId()
        poll_id = wx.NewId()
        poll_between_id = wx.NewId()

        self.AddSimpleTool(
            check_mfs_id,
            'Check Latest MFS Revision',
            bitmap=wx.NullBitmap,
            kind=aui.ITEM_NORMAL
        )

        self.AddSimpleTool(
            download_mfs_id,
            'Download Latest MFS Revision',
            bitmap=wx.NullBitmap,
            kind=aui.ITEM_NORMAL
        )
        self.AddSimpleTool(
            remove_node_id,
            'Remove Node',
            bitmap=wx.NullBitmap,
            kind=aui.ITEM_NORMAL
        )

        self.AddSeparator()

        add_panel = wx.Panel(self, -1, style=wx.BORDER_NONE)
        add_sizer = wx.BoxSizer(wx.VERTICAL)

        add_security_label = wx.StaticText(add_panel, -1, 'Use secutiry:')
        add_security_ctrl = wx.CheckBox(add_panel, -1, '')
        add_security_sizer = h_sizer(add_security_label, add_security_ctrl)

        add_execute = wx.Button(add_panel, -1, 'Add Node')

        add_sizer.Add(add_execute, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        add_sizer.Add(add_security_sizer, 0, wx.EXPAND)

        add_panel.SetSizer(add_sizer)

        def on_add(evt):
            parent.add_node(add_security_ctrl.GetValue())
            evt.Skip()

        add_execute.Bind(wx.EVT_BUTTON, on_add)

        self.AddControl(
            add_panel,
            'Add Node'
        )

        self.AddSeparator()

        test_panel = wx.Panel(self, -1, style=wx.BORDER_NONE)
        test_sizer = wx.BoxSizer(wx.VERTICAL)

        test_count_label = wx.StaticText(test_panel, -1, 'Test count:')
        test_count_ctrl = spin_int_ctrl.SpinIntCtrl(test_panel, -1, value=1, min=1, max=100)
        test_count_sizer = h_sizer(test_count_label, test_count_ctrl)

        test_execute = wx.Button(test_panel, -1, 'Test Network')

        test_sizer.Add(test_execute, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        test_sizer.Add(test_count_sizer, 0, wx.EXPAND)
        test_panel.SetSizer(test_sizer)

        def on_test(evt):
            parent.test(test_count_ctrl.GetValue())
            evt.Skip()

        test_execute.Bind(wx.EVT_BUTTON, on_test)

        self.AddControl(
            test_panel,
            'Test Network'
        )

        self.AddSeparator()

        heal_panel = wx.Panel(self, -1, style=wx.BORDER_NONE)
        heal_sizer = wx.BoxSizer(wx.VERTICAL)

        heal_update_label = wx.StaticText(heal_panel, -1, 'Update Routes:')
        heal_update_ctrl = self.heal_update_ctrl = wx.CheckBox(heal_panel, -1, '')
        heal_update_ctrl.SetValue(True)
        heal_update_sizer = h_sizer(heal_update_label, heal_update_ctrl)

        heal_execute = wx.Button(heal_panel, -1, 'Heal Network')

        heal_sizer.Add(heal_execute, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        heal_sizer.Add(heal_update_sizer, 0, wx.EXPAND)
        heal_panel.SetSizer(heal_sizer)

        def on_heal(evt):
            parent.heal(heal_update_ctrl.GetValue())
            evt.Skip()

        heal_execute.Bind(wx.EVT_BUTTON, on_heal)

        self.AddControl(
            heal_panel,
            'Heal Network'
        )
        
        self.AddSeparator()

        poll_panel = wx.Panel(self, -1, style=wx.BORDER_NONE)
        poll_sizer = wx.BoxSizer(wx.VERTICAL)

        poll_interval_label = wx.StaticText(poll_panel, -1, 'Poll Interval (ms):')
        poll_interval_ctrl = spin_int_ctrl.SpinIntCtrl(poll_panel, -1, value=500, min=1)
        poll_interval_sizer = h_sizer(poll_interval_label, poll_interval_ctrl)

        poll_between_label = wx.StaticText(poll_panel, -1, 'Interval Between Polls:')
        poll_between_ctrl = self.poll_between_ctrl = wx.CheckBox(poll_panel, -1, '')
        poll_between_sizer = h_sizer(poll_between_label, poll_between_ctrl)

        poll_execute = wx.Button(poll_panel, -1, 'Set Network Polling')

        poll_sizer.Add(poll_execute, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        poll_sizer.Add(poll_interval_sizer, 0, wx.EXPAND)
        poll_sizer.Add(poll_between_sizer, 0, wx.EXPAND)
        poll_panel.SetSizer(poll_sizer)

        def on_poll(evt):
            parent.set_poll_interval(poll_interval_ctrl.GetValue(), poll_between_ctrl.GetValue())
            evt.Skip()

        poll_execute.Bind(wx.EVT_BUTTON, on_poll)

        self.AddControl(
            poll_panel,
            'Set Network Polling'
        )

        def on_left_down(evt):
            x, y = evt.GetPosition()
            item = self.FindToolForPosition(x, y)
            if item:
                id = item.GetId()
                if id == remove_node_id:
                    parent.remove_node()
                elif id == check_mfs_id:
                    parent.check_latest_mfs_revision()
                elif id == download_mfs_id:
                    parent.download_latest_mfs_revision()

            evt.Skip()

        self.Bind(wx.EVT_LEFT_DOWN, on_left_down)

        