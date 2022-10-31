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
:synopsis: ZWave Values

.. moduleauthor:: Kevin G Schlosser
"""

import logging
import traceback
import threading

from .object import ZWaveObject
from . import utils
from . import xml_handler
from . import signals

from .command_classes import (
    COMMAND_CLASS_CONFIGURATION,
    COMMAND_CLASS_MANUFACTURER_SPECIFIC,
    COMMAND_CLASS_POWERLEVEL,
    COMMAND_CLASS_VERSION,
    COMMAND_CLASS_THERMOSTAT_FAN_MODE,
    COMMAND_CLASS_THERMOSTAT_FAN_STATE,
    COMMAND_CLASS_THERMOSTAT_MODE,
    COMMAND_CLASS_THERMOSTAT_OPERATING_STATE,
    COMMAND_CLASSES
)


import _libopenzwave

PyNotifications = _libopenzwave.PyNotifications

logger = logging.getLogger(__name__)


FAN_STATE_MAPPING = {
    'State 03': 'Running Medium',
    'State 04': 'Circulation',
    'State 05': 'Humidity Circulation',
    'State 06': 'Left & Right Circulation',
    'State 07': 'Up & Down Circulation',
    'State 08': 'Quiet Circulation'
}

_new_id_lock = threading.Lock()
_new_value_ids = -1


def new_value_id():
    global _new_value_ids

    with _new_id_lock:
        _new_value_ids -= 1
        return _new_value_ids


class ZWaveValueTypeBool(int):

    def __init__(self, value):
        """
        :param value:
        """
        self.value = value
        self.is_ok = False

    def __eq__(self, other):
        """
        :param other:
        :type other: int, bool

        :rtype: bool
        """
        if self.is_ok:
            return int.__eq__(self, other)
        else:
            return other == bool

    def __ne__(self, other):
        """
        :param other:
        :type other: int, bool

        :rtype: bool
        """
        return not self.__eq__(other)

    def __call__(self, data):
        """
        :param data:
        :type data: str, bytes, int, bool
        """
        if isinstance(data, bytes):
            data = data.decode('utf-8')

        if isinstance(data, str):
            if data in ["False", "false", "FALSE", "0"]:
                data = 0
            else:
                data = 1

        if not isinstance(data, int):
            data = int(bool(data))

        self.is_ok = True

        int.__new__(self, data)


class ZWaveValueTypeStr(str):

    # noinspection PyMissingConstructor
    def __init__(self, value):
        """
        :param value:
        """
        self._value = value
        self.is_ok = False

    def __eq__(self, other):
        """
        :param other:

        :rtype: bool
        """
        if self.is_ok:
            return str.__eq__(self, other)

        else:
            return other == str

    def __ne__(self, other):
        """
        :param other:

        :rtype: bool
        """
        return not self.__eq__(other)

    def __call__(self, data):
        """
        :param data:
        """
        if isinstance(data, bytes):
            data = data.decode('utf-8')

        if not isinstance(data, str):
            data = str(data)

        if self._value.type == "List":
            if data not in self._value.data_items:
                logger.error(
                    'new value data not in list of items: '
                    'node: {0} - value: {1}\n{2}'.format(
                        self._value.parent_id,
                        self._value.id,
                        str(self._value.data_items)
                    )
                )

                data = self._value.data

        self.is_ok = True
        str.__new__(self, data)


class ZWaveValueTypeFloat(float):

    # noinspection PyMissingConstructor
    def __init__(self, value):
        """
        :param value:
        """
        self._value = value
        self.is_ok = False

    def __eq__(self, other):
        """
        :param other:

        :rtype: bool
        """
        if self.is_ok:
            return float.__eq__(self, other)
        else:
            return other == float

    def __ne__(self, other):
        """
        :param other:

        :rtype: bool
        """
        return not self.__eq__(other)

    def __call__(self, data):
        """
        :param data:
        """
        if not isinstance(data, float):
            try:
                data = float(data)
            except:  # NOQA
                logger.error(
                    'new value data cannot be evaluated: '
                    'node: {0} - value: {1}\n{2}'.format(
                        self._value.parent_id,
                        self._value.id,
                        traceback.format_exc()
                    )
                )
                data = self._value.data

            if data < self._value.min:
                data = self._value.min

            if data > self._value.max:
                data = self._value.max

        self.is_ok = True
        float.__new__(self, data)


class ZWaveValueTypeInt(int):

    # noinspection PyMissingConstructor
    def __init__(self, value):
        """
        :param value:
        """
        self._value = value
        self.is_ok = False

    def __eq__(self, other):
        """
        :param other:

        :rtype: bool
        """
        if self.is_ok:
            return int.__eq__(self, other)
        else:
            return other == int

    def __ne__(self, other):
        """
        :param other:

        :rtype: bool
        """
        return not self.__eq__(other)

    def __call__(self, data):
        """
        :param data:
        """
        type_ = self._value.type

        if not isinstance(data, int):
            try:
                data = int(data)
            except:  # NOQA
                logger.error(
                    'new value data cannot be evaluated: '
                    'node: {0} - value: {1}\n{2}'.format(
                        self._value.parent_id,
                        self._value.id,
                        traceback.format_exc()
                    )
                )
                data = self._value.data

        if type_ == "Byte":
            if data < 0:
                data = 0
            elif data > 255:
                data = 255

        elif type_ == "Int":
            if data < -2147483648:
                data = -2147483648
            elif data > 2147483647:
                data = 2147483647

        elif type_ == "Short":
            if data < -32768:
                data = -32768
            elif data > 32767:
                data = 32767

        if data < self._value.min:
            data = self._value.min

        if data > self._value.max:
            data = self._value.max

        self.is_ok = True

        int.__new__(self, data)


class Bool(int):
    __name__ = 'bool'

    def __str__(self):
        if self == 1:
            return 'True'
        else:
            return 'False'


class ZWaveValueDataMeta(type):

    def __init__(cls, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """
        cls._instances = {}
        super(ZWaveValueDataMeta, cls).__init__(*args, **kwargs)

    def __call__(cls, original_data, value_data, index=None, xml_data=None):
        """
        :param original_data:
        :param value_data:
        :param index:
        :param xml_data:
        """

        data_type = type(value_data)
        if data_type == bool:
            data_type = Bool

        class IsInstanceMeta(type):
            def __instancecheck__(self, instance):
                if type(instance) == bool and data_type == Bool:
                    return True

                return isinstance(instance, data_type)

        def value_(self):
            return self._original_data

        def data_(self):
            return self._data

        def label_get_(self):
            if None not in (self._index, self._xml_handler):
                if 'label' in self._xml_handler.attrib:
                    return self._xml_handler['label']

                return self._xml_handler.text
            return str(self._data)

        def label_set_(self, value):
            if None not in (self._index, self._xml_handler):
                self._xml_handler['label'] = value

        def index_(self):
            return self._index

        def xml_handler_(self):
            return self._xml_handler

        def getattr_(self, item):
            if item in self.__dict__:
                return self.__dict__[item]

            if item in self.__class__.__dict__:
                obj = self.__class__.__dict__[item]
                if hasattr(obj, 'fget'):
                    return obj.fget(self)

            return getattr(self._original_data, item)

        namespace = {
            '_index': index,
            'index': property(fget=index_),
            '_data': value_data,
            'data': property(fget=data_),
            '_original_data': original_data,
            '_xml_handler': xml_data,
            'xml_handler': property(fget=xml_handler_),
            '__module__': ZWaveValueData.__module__,
            '__getattr__': getattr_,
            'label': property(fget=label_get_, fset=label_set_),
            'value': property(fget=value_)
        }

        cls_ = type(data_type.__name__, (data_type,), namespace)

        cls_ = IsInstanceMeta(
            cls_.__name__,
            cls_.__bases__,  # NOQA
            cls_.__dict__.copy()
        )

        return cls_(value_data)


class ZWaveValueData(object, metaclass=ZWaveValueDataMeta):

    def __init__(self, original_data, data, index=None, xml_data=None):
        """
        :param original_data:
        :param data:
        :param index:
        :param xml_data:
        """
        self._index = index
        self._data = data
        self._original_data = original_data
        self._xml_handler = xml_data

    @property
    def value(self):
        return self._original_data

    @property
    def data(self):
        return self._data

    @property
    def label(self):
        if None not in (self._index, self._xml_handler):
            return self._xml_handler.text

    @label.setter
    def label(self, value):
        if None not in (self._index, self._xml_handler):
            self._xml_handler.text = value

    @property
    def index(self):
        return self._index

    @property
    def xml_handler(self):
        return self._xml_handler


# TODO: don't report controller node as sleeping
class ZWaveValue(ZWaveObject):
    """
    Represents a single value.
    """
    def __init__(self, id_, network, parent, xml_data=None):
        """
        Initialize value

        .. code-block:: python

                n['valueId'] = {'home_id' : v.GetHomeId(),
                    * 'parent_id' : v.GetNodeId(),
                    * 'commandClass' :
                      PyManager.COMMAND_CLASS_DESC[v.GetCommandClassId()],
                    * 'instance' : v.GetInstance(),
                    * 'index' : v.GetIndex(),
                    * 'id' : v.GetId(),
                    * 'genre' : PyGenres[v.GetGenre()],
                    * 'type' : PyValueTypes[v.GetType()],
                    * #'value' : value.c_str(),
                    * 'value' : getValueFromType(manager,v.GetId()),
                    * 'label' : label.c_str(),
                    * 'units' : units.c_str(),
                    * 'readOnly': manager.IsValueReadOnly(v),
                    }

        :param id_: ID of the value
        :type id_: int

        :param network: The network object to access the manager
        :type network: ZWaveNetwork

        :param parent:
        :type parent: ZWaveNode

        :param xml_data:
        :type xml_data: xml_handler.XMLElement, optional
        """
        ZWaveObject.__init__(self, id_, network=network, xml_data=xml_data)
        logger.debug(u"Create object value (valueId:%s)", id_)
        self._parent = parent

        if (
            self.command_class in (
                COMMAND_CLASS_CONFIGURATION,
                COMMAND_CLASS_MANUFACTURER_SPECIFIC,
                COMMAND_CLASS_POWERLEVEL,
                COMMAND_CLASS_VERSION,
            ) or self.type == 'Button'
        ):
            self._is_ready = True
        else:
            self._is_ready = False

        if xml_data is None:
            type_ = self.type
            if type_ == 'List':
                items = network.manager.getValueListItems(self.id)
                orig_items = network.manager.getValueListValues(self.id)

            elif type_ in ('Bool', 'Button'):
                items = [False, True]
                orig_items = [False, True]
            else:
                items = []
                orig_items = []

            self.__data_list = []

            for i, item in enumerate(items):
                self.__data_list += [
                    ZWaveValueData(orig_items[i], item, i)
                ]

            signals.SIGNAL_VALUE_ADDED.send(
                sender=parent,
                network=parent.network,
                controller=parent.network.controller,
                node=parent,
                value=self
            )
            if self._is_ready:
                signals.SIGNAL_VALUE_READY.send(
                    sender=self,
                    network=parent.network,
                    controller=parent.network.controller,
                    node=parent,
                    value=self
                )
        else:
            if xml_data['type'] in ('List', 'Bool', 'Button'):
                self.__data_list = []

                for item in xml_data.ValueItems:
                    try:
                        data = eval(item.text)
                    except:
                        data = item.text

                    self.__data_list += [
                        ZWaveValueData(item['value'], data, item['index'], item)
                    ]
            else:
                self.__data_list = []

            signals.SIGNAL_VALUE_DATASET_LOADED.send(
                sender=parent,
                network=parent.network,
                controller=parent.network.controller,
                node=parent,
                value=self
            )

            if self._is_ready:
                signals.SIGNAL_VALUE_READY.send(
                    sender=self,
                    network=parent.network,
                    controller=parent.network.controller,
                    node=parent,
                    value=self
                )

    def _id(self, new_id):
        self._object_id = new_id
        if self._xml_handler is not None:
            self._xml_handler['id'] = '0x{0:04X}'.format(self.id)

    _id = property(fset=_id)

    @property
    def id(self):
        if self._object_id < 0:
            return int(self._xml_handler['id'], 16)
        else:
            return self._object_id

    def _update_dataset(self, endpoint=None):
        if self._xml_handler is None:
            handler = xml_handler.XMLElement('Value')

            if endpoint is not None:
                endpoint.append(handler)
            else:
                self.node.xml_handler.Values.append(handler)

            handler['endpoint'] = self._network.manager.getValueInstance(self.id) - 1
            handler['units'] = self._network.manager.getValueUnits(self.id)
            handler['max'] = self._network.manager.getValueMax(self.id)
            handler['min'] = self._network.manager.getValueMin(self.id)
            handler['type'] = self._network.manager.getValueType(self.id)
            handler['genre'] = self._network.manager.getValueGenre(self.id)
            handler['index'] = self._network.manager.getValueIndex(self.id)
            handler['label'] = self._network.manager.getValueLabel(self.id)
            handler['instance_label'] = self._network.manager.getInstanceLabel(self.id)

            handler['read_only'] = (
                self._network.manager.isValueReadOnly(self.id)
            )
            handler['write_only'] = (
                self._network.manager.isValueWriteOnly(self.id)
            )
            handler['poll_intensity'] = (
                self._network.manager.getPollIntensity(self.id)
            )
            handler['change_verified'] = (
                self._network.manager.getChangeVerified(self.id)
            )
            command_class = xml_handler.XMLElement('CommandClass')
            cc = self._network.manager.getValueCommandClass(self.id)
            cc = COMMAND_CLASSES[cc]
            command_class['id'] = cc.class_id
            command_class['symbol'] = cc.class_desc
            handler.append(command_class)

            help = xml_handler.XMLElement('Help')
            h = self._network.manager.getValueHelp(self.id)
            if h.strip():
                help.text = h

            handler.Help = help

            handler.Data = xml_handler.XMLElement('Data')
            handler.Data.text =  'Not Set'
            handler.Data['value'] = 'Not Set'
            handler.Data['index'] = None

            type = handler['type']
            self.__data_list = []

            if type == 'List':
                items = self._network.manager.getValueListItems(self.id)
                orig_items = self._network.manager.getValueListValues(self.id)

            elif type in ('Bool', 'Button'):
                items = [False, True]
                orig_items = [False, True]
            else:
                items = []
                orig_items = []

            if items:
                value_items = xml_handler.XMLElement('ValueItems')
                handler.ValueItems = value_items

                for i, label in enumerate(items):
                    value = orig_items[i]
                    value_item = xml_handler.XMLElement('ValueItem')
                    value_item.text = str(label)
                    value_item['value'] = value
                    value_item['index'] = i
                    value_items.append(value_item)

                    self.__data_list += [
                        ZWaveValueData(value, label, i, value_item)
                    ]
        else:
            handler = self._xml_handler

        if self.id > -1:
            handler['id'] = '0x{0:04X}'.format(self.id)

        self._xml_handler = handler

    def __handle_fan_state(self, data):
        if data == 'Running':
            fan_mode = self.node.values.thermostat_fan_mode
            fan_values = self._network.manager.getValueListValues(fan_mode.id)

            speed_count = 0
            for auto, manual in (
                (0x00, 0x01),
                (0x02, 0x03),
                (0x04, 0x05)
            ):
                if auto in fan_values or manual in fan_values:
                    speed_count += 1

            if speed_count > 1:
                data = 'Running Low'

        if data in FAN_STATE_MAPPING:
            data = FAN_STATE_MAPPING[data]

        return data

    @utils.logit
    def _handle_notification(self, notif):

        if notif == PyNotifications.ValueRemoved:
            self._xml_handler.parent.remove(self._xml_handler)
            signals.SIGNAL_VALUE_REMOVED.send(
                sender=self.node,
                network=self.node.network,
                controller=self.node.network.controller,
                node=self.node,
                value=self
            )
            return

        data = notif.value.data
        instance = self.instance

        if instance > 1:
            for endpoint in self.node.endpoints:
                if endpoint.instance_id == instance:
                    endpoint._update_dataset(notif)
                    break
            else:
                if self._xml_handler is None:
                    self._update_dataset()

        elif self._xml_handler is None:
            self._update_dataset()

        old_data = self._xml_handler.Data.text

        for item in self.__data_list:
            if item == data:
                self._xml_handler.Data.text = str(item)
                self._xml_handler.Data['value'] = item.value
                self._xml_handler.Data['index'] = item.index
                self._xml_handler.Data['label'] = item.label
                break
        else:
            if self.command_class == COMMAND_CLASS_THERMOSTAT_FAN_STATE:
                data = self.__handle_fan_state(data)

            self._xml_handler.Data.text = str(data)
            self._xml_handler.Data['value'] = data
            self._xml_handler.Data['index'] = None

            item = ZWaveValueData(data, data)

        if not self._is_ready:
            self._is_ready = True
            signals.SIGNAL_VALUE_READY.send(
                sender=self,
                network=self.network,
                controller=self.network.controller,
                node=self.node,
                value=self,
                value_data=item
            )

        if notif == PyNotifications.ValueChanged:
            if old_data is not None:
                try:
                    old_data = eval(old_data)
                except:  # NOQA
                    pass

            if item.data != old_data:
                signals.SIGNAL_VALUE_CHANGED.send(
                    sender=self,
                    network=self.node.network,
                    controller=self.node.network.controller,
                    node=self.node,
                    value=self,
                    value_data=item
                )

        elif notif == PyNotifications.ValueRefreshed:
            signals.SIGNAL_VALUE_REFRESHED.send(
                sender=self,
                network=self.node.network,
                controller=self.node.network.controller,
                node=self.node,
                value=self,
                value_data=item
            )

    def __eq__(self, other):
        """
        :param other:
        :rtype: bool
        """
        if isinstance(other, ZWaveValue):
            return other.id == self.id
        try:
            return other.class_id == self.command_class.class_id
        except AttributeError:
            return False

    @property
    def is_ready(self):
        return self._is_ready

    def destroy(self):
        """
        Internal use.

        removes this value from the instance singleton list.

        :return: None
        """
        if self.instance == 1:
            self._update_dataset()

        if self._is_ready and not self._xml_handler.Data.text:

            if self.is_write_only:
                self._xml_handler.Data.text = 'Write Only'
                self._xml_handler.Data['value'] = None
                self._xml_handler.Data['index'] = None
            else:
                data = self._network.manager.getValue(self.id)

                if self._xml_handler['type'] in ('List', 'Bool', 'Button'):
                    for item in self.__data_list:
                        if item == data:
                            self._xml_handler.Data.text = str(item)
                            self._xml_handler.Data['value'] = item.value
                            self._xml_handler.Data['index'] = item.index
                            self._xml_handler.Data['label'] = item.label
                            break
                    else:
                        if data == '':
                            self._xml_handler.Data.text = 'Not Set'
                            self._xml_handler.Data['value'] = None
                            self._xml_handler.Data['index'] = None
                        else:
                            self._xml_handler.Data.text = str(data)
                            self._xml_handler.Data['value'] = data
                            self._xml_handler.Data['index'] = None
                else:
                    if data == '':
                        self._xml_handler.Data.text = 'Not Set'
                        self._xml_handler.Data['value'] = None
                        self._xml_handler.Data['index'] = None
                    else:
                        if self.command_class == COMMAND_CLASS_THERMOSTAT_FAN_STATE:
                            data = self.__handle_fan_state(data)

                        self._xml_handler.Data.text = str(data)
                        self._xml_handler.Data['value'] = data
                        self._xml_handler.Data['index'] = None

        logger.debug(str(self.id) + ' - destroyed')

    @property
    def parent_id(self):
        """
        Get the parent_id of the value.

        :rtype: int
        """
        return self._parent.object_id

    @property
    def id_on_network(self):
        """
        Get an unique id for this value.

        The scenes use this to retrieve values

        .. code-block:: xml

                <Scene id="1" label="scene1">
                        <Value homeId="0x014d0ef5" nodeId="2" genre="user"
                        commandClassId="38" instance="1" index="0"
                        type="byte">54</Value>
                </Scene>

        The format is :

            home_id.node_id.command_class.instance.index

        :rtype: str
        """
        separator = self._network.id_separator
        return "%0.8x%s%s%s%0.2x%s%s%s%s" % (
            self._network.home_id,
            separator,
            self.parent_id,
            separator,
            self.command_class,
            separator,
            self.instance,
            separator,
            self.index
        )

    @property
    def node(self):
        """
        The parent node

        :rtype: ZWaveNode
        """
        return self._parent

    @property
    @utils.logit
    def label(self):
        """
        Gets/Sets the label of the value.

        :param value: The new label value
        :type value: str

        :rtype: str
        """

        if self._xml_handler is None:
            return self._network.manager.getValueLabel(self.id)
        else:
            return self._xml_handler['label']

    @label.setter
    @utils.logit
    def label(self, value):
        if self._xml_handler is not None:
            self._xml_handler['label'] = value

        self._network.manager.setValueLabel(self.id, value)

    @property
    def help(self):
        """
        Gets/Sets a help string describing the value's purpose and usage.

        :param value: The new help value
        :type value: str

        :rtype: str
        """

        if self._xml_handler is None:
            return self._network.manager.getValueHelp(self.id)
        else:
            return self._xml_handler.Help.text

    @help.setter
    def help(self, value):
        if self._xml_handler is not None:
            self._xml_handler.Help.text = value

        self._network.manager.setValueHelp(self.id, value)

    @property
    def units(self):
        """
        Gets/Sets the units that the value is measured in.

        :param value: The new units value
        :type value: str

        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getValueUnits(self.id)
        else:
            return self._xml_handler['units']

    @units.setter
    @utils.logit
    def units(self, value):
        if self._xml_handler is not None:
            self._xml_handler['units'] = value

        self._network.manager.setValueUnits(self.id, value)

    @property
    def max(self):
        """
        Gets the maximum that this value may contain.

        :rtype: int
        """
        if self._xml_handler is None:
            type = self.type

            if type in ('Decimal', 'Int', 'Short', 'Byte'):
                return self._network.manager.getValueMax(self.id)

            if type == 'Bool':
                return 1
            if type == 'List':
                return len(self.data_items) - 1
        else:
            return self._xml_handler['max']

    @property
    def min(self):
        """
        Gets the minimum that this value may contain.

        :rtype: int
        """
        if self._xml_handler is None:
            type = self.type
            if type in ('Decimal', 'Int', 'Short', 'Byte'):
                return self._network.manager.getValueMin(self.id)

            if type in ('Bool', 'List'):
                return 0
        else:
            return self._xml_handler['min']

    @property
    def type(self):
        """
        Get the type of the value.

        The type describes the data held by the value and enables the user to
        select the correct value accessor method in the Manager class.

        :return: type of the value
        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getValueType(self.id)
        else:
            return self._xml_handler['type']

    @property
    def py_type(self):
        """
        The python data type the value uses when setting the data.


        ..code-block:: python

            new_value = False

            # old way
            if value.type == 'String':
                value.data = str(new_value)

            # new_way
            value.data = value.py_type(new_value)

        not a big difference but it is helpful


        Returns one of the following based on
        :py:func:`libopenzwave.value.ZWaveValue.type`

            * `"Bool"`: `bool`
            * `"Button"`: `bool`
            * `"Short"`: `int`
            * `"Int"`: `int`
            * `"Byte"`: `int`
            * `"BitSet"`: `int`
            * `"Decimal"`: `float`
            * `"String"`: `str`
            * `"List"`: `str`
            * Default: `None` - This should not happen. If it does please
              report the bug

        :rtype: bool, int, float, str, None

        """
        type_ = self.type

        if type_ in ('Bool', 'Button'):
            return ZWaveValueTypeBool(self)
        if type_ in ('Byte', 'Int', 'Short', 'BitSet'):
            return ZWaveValueTypeInt(self)
        if type_ in ('String', 'List'):
            return ZWaveValueTypeStr(self)
        if type_ == "Decimal":
            return ZWaveValueTypeFloat(self)

    @property
    def genre(self):
        """
        Get the genre of the value.

        The genre classifies a value to enable low-level system or
        configuration parameters to be filtered out by the application

        :return: genre of the value (Basic, User, Config, System)
        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getValueGenre(self.id)
        else:
            return self._xml_handler['genre']

    @property
    @utils.logit
    def index(self):
        """
        Get the value index.

        The index is used to identify one of multiple values created and
        managed by a command class. In the case of configurable parameters
        (handled by the configuration command class), the index is the same as
        the parameter ID.

        :return: index of the value
        :rtype: int
        """
        if self._xml_handler is None:
            return self._network.manager.getValueIndex(self.id)
        else:
            return self._xml_handler['index']

    @property
    @utils.logit
    def instance(self):
        """
        Get the command class instance of this value.

         It is possible for there to be multiple instances of a command class,
         although currently it appears that only the SensorMultilevel command
         class ever does this.

        :return: instance of the value
        :rtype: int
        """

        if self._xml_handler is None:
            return self._network.manager.getValueInstance(self.id)
        else:
            return self._xml_handler['endpoint'] + 1

    @property
    @utils.logit
    def data(self):
        """
        Get/Set the current data of the value.

        :param value: the new value to be set
        :type value: str, float, int, bool

        :return: The data of the value
        :rtype: str, float, int, bool
        """
        if self.is_write_only:
            logger.warning('value is write only ({0})'.format(self.id))

            return ZWaveValueData('Write Only', 'Write Only')

        if not self._is_ready:

            if self._xml_handler is not None:
                data = self._xml_handler.Data
                try:
                    res = eval(data.text)
                except:
                    res = data.text

                return ZWaveValueData(data['value'], res, data['index'], data)
        else:
            res = self._network.manager.getValue(self.id)

            if self.type in ('List', 'Bool', 'Button'):
                for item in self.__data_list:
                    if item == res:
                        return ZWaveValueData(
                            item.value,
                            item.data,
                            item.index,
                            item.xml_handler
                        )
            if self.command_class == COMMAND_CLASS_THERMOSTAT_FAN_STATE:
                res = self.__handle_fan_state(res)

            if res == '' or res is None:
                return ZWaveValueData(
                    'Not Set',
                    'Not Set',
                )

            return ZWaveValueData(res, res)

    @data.setter
    @utils.logit
    def data(self, value):
        if self.is_read_only:
            logger.warning('value is read only ({0}, {1})'.format(self.id, value))
            return

        type = self.type

        if type == 'Bool' and isinstance(value, int):
            value = bool(value)

        if type in ('Bool', 'Button', 'List'):
            for item in self.__data_list:
                if (
                    item.label == value or
                    item.data == value or
                    item.value == value
                ):
                    if type == 'Button':
                        if item.data is True:
                            self.network.manager.pressButton(self.id)
                        elif item.data is False:
                            self.network.manager.releaseButton(self.id)
                    else:
                        self._network.manager.setValue(self.id, item.data)

                    break
            else:
                logger.error('value data not in data list')
        else:
            self._network.manager.setValue(self.id, value)

    @property
    def data_as_string(self):
        """
        Get the value data as String.

        :rtype: str
        """

        if self.type == 'BitSet':
            return str(self._network.manager.getValueAsBitSet(self.id, None))
        return self._network.manager.getValueAsString(self.id)

    @property
    @utils.logit
    def data_items(self):
        """
        When type of value is list, data_items contains a list of valid values

        :return: The valid values or a help string
        :rtype: str, set
        """

        data_list = []
        for item in self.__data_list:
            data_list += [
                ZWaveValueData(
                    item.value,
                    item.data,
                    item.index,
                    item.xml_handler
                )
            ]
        return data_list

    def check_data(self, data):
        """
        Check that data is correct for this value.
        Return the data in a correct type. None is data is incorrect.

        :param data:  The data value to check
        :type data: lambda

        :return: A variable of the good type if the data is correct.
            `None` otherwise.
        :rtype: Any, None
        """
        if self.is_read_only:
            return None

        new_data = None
        logger.debug(u"check_data type :%s", self.type)
        if self.type == "Bool":
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            if isinstance(data, str):
                if data in ["False", "false", "FALSE", "0"]:
                    new_data = False
                else:
                    new_data = True
            else:
                try:
                    new_data = bool(data)
                except:  # NOQA
                    new_data = None

        elif self.type == "Byte":
            try:
                new_data = int(data)
            except:
                new_data = None
            if new_data is not None:
                if new_data < 0:
                    new_data = 0
                elif new_data > 255:
                    new_data = 255

        elif self.type == "Decimal":
            try:
                new_data = float(data)
            except:
                new_data = None

        elif self.type == "Int":
            try:
                new_data = int(data)
            except:  # NOQA
                new_data = None
            if new_data is not None:
                if new_data < -2147483648:
                    new_data = -2147483648
                elif new_data > 2147483647:
                    new_data = 2147483647

        elif self.type == "Short":
            try:
                new_data = int(data)
            except:  # NOQA
                new_data = None
            if new_data is not None:
                if new_data < -32768:
                    new_data = -32768
                elif new_data > 32767:
                    new_data = 32767

        elif self.type == "String":
            if isinstance(data, bytes):
                data = data.decode('utf-8')

            new_data = data
        elif self.type == "Button":
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            if isinstance(data, str):
                if data in ["False", "false", "FALSE", "0"]:
                    new_data = False
                else:
                    new_data = True
            else:
                try:
                    new_data = bool(data)
                except:  # NOQA
                    new_data = None
        elif self.type == "List":
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            if isinstance(data, str):
                if data in self.data_items:
                    new_data = data
                else:
                    new_data = None
        return new_data

    @property
    def is_set(self):
        """
        Test whether the value has been set.

        :return: `True` if the value has actually been set by a status message
            from the device, rather than simply being the default.
        :rtype: bool
        """
        return self._network.manager.isValueSet(self.id)

    @property
    def is_read_only(self):
        """
        Test whether the value is read-only.

        :return: `True` if the value cannot be changed by the user.
        :rtype: bool
        """
        if self._xml_handler is None:
            return self._network.manager.isValueReadOnly(self.id)
        else:
            return self._xml_handler['read_only']

    @property
    def is_write_only(self):
        """
        Test whether the value is write-only.

        :return: `True` if the value can only be written to and not read.
        :rtype: bool
        """
        if self._xml_handler is None:
            return self._network.manager.isValueWriteOnly(self.id)
        else:
            return self._xml_handler['write_only']

    @property
    @utils.logit
    def poll_intensity(self):
        """
        Get/Set the poll intensity.

        possible values:

            * `0`: none
            * `1`: every time through the list
            * `2`: every other time, etc

        :param value: intensity
        :type value: int

        :return: intensity
        :rtype: int
        """
        if self._xml_handler is None:
            # always ask to manager to get poll intensity
            return self._network.manager.getPollIntensity(self.id)
        else:
            return self._xml_handler['poll_intensity']

    @poll_intensity.setter
    @utils.logit
    def poll_intensity(self, value):
        if self._xml_handler is not None:
            self._xml_handler['poll_intensity'] = value

        if value == 0:
            self._network.manager.disablePoll(self.id)
        else:
            self._network.manager.enablePoll(self.id, value)

    @property
    def is_polled(self):
        """
        Verify that the value is polled.

        :rtype: bool
        """
        return self._network.manager.isPolled(self.id)

    @property
    def command_class(self):
        """
        The command class of the value.

        :returns: The command class of this value
        :rtype: int
        """
        if self._xml_handler is None:
            command_class = self._network.manager.getValueCommandClass(self.id)
        else:
            command_class = int(self._xml_handler.CommandClass['id'])

        return COMMAND_CLASSES[command_class]

    @utils.logit
    def refresh(self):
        """
        Refresh the value.

        :returns: `True` if the command was transmitted to controller
        :rtype: bool
        """
        return self._network.manager.refreshValue(self.id)

    @property
    def precision(self):
        """
        Gets a float value's precision.

        :returns: a float value's precision
        :rtype: int
        """

        if self.type == 'Decimal':
            if self._xml_handler is None:
                return self._network.manager.getValueFloatPrecision(self.id)
            else:
                return self._xml_handler['precision']

    @property
    def change_verified(self):
        """
        Determine if value changes upon a refresh should be verified.

        If so, the library will immediately refresh the value a second time
        whenever a change is observed. This helps to filter out spurious data
        reported occasionally by some devices.

        :param verify: if `True`, verify changes. If `False` don't verify changes.
        :type verify: bool

        :rtype: bool
        """
        if self._is_ready:
            return self._network.manager.getChangeVerified(self.id)
        elif self._xml_handler is not None:
            return self._xml_handler['change_verified']

    @change_verified.setter
    def change_verified(self, verify):
        logger.debug(
            'Set change verified %s for valueId [%s]',
            verify,
            self.id
        )

        if self._xml_handler is not None:
            self._xml_handler['change_verified'] = verify

        self._network.manager.setChangeVerified(self.id, verify)

    @property
    @utils.logit
    def instance_label(self):
        """
        Gets the Instance label for this value

        :param value:
        :type value: str

        :rtype: str
        """
        if self._xml_handler is None:
            return self._network.manager.getInstanceLabel(self.id)
        else:
            return self._xml_handler['instance_label']

    @instance_label.setter
    def instance_label(self, value):
        if self._xml_handler is not None:
            self._xml_handler['instance_label'] = value

    @utils.logit
    def get_bit(self, pos):
        """
        Get a single bit value.

        This method is only for BitSet value types.

        :param pos: Bit position.
        :type pos: int

        :return: Can be one of the following values.

            Possible Values:

                * `True`: The bit is set.
                * `False`: The bit is not set.
                * `None`: The value type is not BitSet

        :rtype: bool, None
        """
        if self.type == 'BitSet':
            return self._network.manager.getValueAsBitSet(self.id, pos)

    @utils.logit
    def set_bit(self, pos, value):
        """
        Set a single bit value.

        This method is only for BitSet value types.

        :param pos: Bit position.
        :type pos: int

        :param value: Can be one of the following values.

            Allowed Values:

                * `True`: sets the bit
                * `False`: un-sets the bit

        :return: Can be one of the following values.

            Possible Values:

                * `True`: Command was sent.
                * `False`: Command failed.
                * `None`: the value type is not BitSet

        :rtype: bool, None
        """
        if self.type == 'BitSet':
            return self._network.manager.setValue(self.id, value, pos)

    @property
    def as_dict(self):
        """
        Return a dict representation of a value.

        :rtype: dict
        """

        res = dict(
            label=self.label,
            id=self.id,
            units=self.units,
            genre=self.genre,
            data=self.data,
            data_items=self.data_items,
            command_class=dict(
                id=self.command_class,
                desc=self.node.get_command_class_as_string(self.command_class)
            ),
            is_read_only=self.is_read_only,
            is_write_only=self.is_write_only,
            type=self.type,
            index=self.index,
            instance=self.instance,
            data_as_string=self.data_as_string,
            is_polled=self.is_polled,
            poll_intensity=self.poll_intensity,
            precision=self.precision,
            min=self.min,
            max=self.max,
            help=self.help
        )
        if self.instance > 0:
            res['instance_label'] = self.instance_label

        return res


class DummyValue(object):

    def __init__(self, node, index):
        self._node = node
        self._index = index

    @property
    def label(self):
        return ''

    @label.setter
    def label(self, _):
        pass

    @property
    def id(self):
        return -1

    @property
    def units(self):
        return ''

    @units.setter
    def units(self, _):
        pass

    @property
    def genre(self):
        return ''

    @property
    def data(self):
        return None

    @data.setter
    def data(self, _):
        pass

    @property
    def data_items(self):
        return []

    @property
    def command_class(self):
        return -1

    @property
    def is_read_only(self):
        return True

    @property
    def is_write_only(self):
        return True

    @property
    def type(self):
        return ''

    @property
    def index(self):
        return self._index

    @property
    def instance(self):
        return -1

    @property
    def data_as_string(self):
        return ''

    @property
    def is_polled(self):
        return False

    @property
    def precision(self):
        return -1

    @property
    def min(self):
        return -1

    @property
    def max(self):
        return -1

    @property
    def help(self):
        return ''

    @help.setter
    def help(self, _):
        pass

    @property
    def instance_label(self):
        return ''

    @property
    def is_change_verified(self):
        return False

    @property
    def node(self):
        return self._node

    @property
    def id_on_network(self):
        return ''

    @property
    def parent_id(self):
        return -1

    def __str__(self):
        return ''

    @property
    def poll_intensity(self):
        return 0

    @poll_intensity.setter
    def poll_intensity(self, _):
        pass

    @property
    def is_set(self):
        return False

    def check_data(self, _):
        pass

    def refresh(self):
        pass

    def set_bit(self, _, __):
        pass

    def get_bit(self, _):
        pass

    def set_change_verified(self, _):
        pass

    @property
    def as_dict(self):
        return {}


# noinspection PyProtectedMember
class ZWaveValues(object):

    def __init__(self, node):
        """
        :param node:
        :type node: ZWaveNode
        """
        self._node = node
        self._values = {}
        self._lock = threading.Lock()

        for base in node._bases:
            object.__setattr__(self, base.class_desc, base.ValueIndexes())

    @utils.logit
    def __getitem__(self, item):
        """
        :param item:
        """
        with self._lock:
            if item in self._values:
                return self._values[item]

        raise KeyError(item)

    @utils.logit
    def __setitem__(self, key, value):
        """
        :param key:
        :param value:
        """
        from .node import ZWaveNode

        index = value.index
        command_class = value.command_class

        for cls in self._node._bases:
            if cls.class_id == command_class.class_id:
                for name, idx in cls.ValueIndexes.__dict__.items():
                    if idx == index:
                        if (
                            (
                                isinstance(self._node, ZWaveNode) and
                                value.instance == 1
                            ) or (
                                not isinstance(self._node, ZWaveNode) and
                                value.instance > 1
                            )
                        ):
                            with self._lock:
                                self.__dict__[name] = value

                        with self._lock:
                            self._values[key] = value
                        return

        output = (
            'unable to locate index for value - '
            'node id={0}, '
            'id={1}, '
            'genre={2}, '
            'type={3}, '
            'cc={4}, '
            'label={5}, '
            'index={6}, '
            'instance={7}'
        ).format(
            value.parent_id,
            value.id,
            value.genre,
            value.type,
            value.command_class.class_desc,
            value.label,
            value.index,
            value.instance
        )
        logger.warning(output)

        with self._lock:
            self._values[key] = value

    @utils.logit
    def __getattr__(self, item):
        """
        :param item:
        """
        if item in self.__dict__:
            return self.__dict__[item]

        for cls in self._node._bases:
            for name, idx in cls.ValueIndexes.__dict__.items():
                if item == name:
                    return DummyValue(self._node, idx)

        raise AttributeError(item)

    def __contains__(self, item):
        """
        :param item:
        """
        with self._lock:
            return item in self._values

    def __iter__(self):
        with self._lock:
            return iter(self._values)

    def __delitem__(self, key):
        """
        :param key:
        """
        with self._lock:
            if key in self._values:
                del self._values[key]

    def keys(self):
        with self._lock:
            return self._values.keys()

    def values(self):
        with self._lock:
            return self._values.values()

    def items(self):
        with self._lock:
            return self._values.items()

    def get(self, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """
        with self._lock:
            return self._values.get(*args, **kwargs)

    def pop(self, key):
        """
        :param key:
        """
        with self._lock:
            return self._values.pop(key)
