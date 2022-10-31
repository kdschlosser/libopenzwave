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
:synopsis: energy use history plugin

.. moduleauthor:: Kevin G Schlosser
"""

import time
import datetime

from ... import utils
from ... import xml_handler


class EnergyMixin(object):

    @utils.logit
    def __init__(self, node, command_class, type):
        handler = node.xml_handler
        if handler is None:
            node._update_dataset()
            handler = node.xml_handler
            energy = xml_handler.XMLElement('Energy')
            energy['type'] = type
            if type == 'heat':
                energy['units'] = 'btus'
                energy['btus'] = 0
            else:
                energy['units'] = 'watts'
                energy['watts'] = 0
            handler.append(energy)
        else:
            for energy in handler:
                if energy.tag == 'Energy' and energy['type'] == type:
                    break
            else:
                energy = xml_handler.XMLElement('Energy')
                energy['type'] = type
                if type == 'heat':
                    energy['units'] = 'btus'
                    energy['btus'] = 0
                else:
                    energy['units'] = 'watts'
                    energy['watts'] = 0
                handler.append(energy)

        energy.CommandClass = xml_handler.XMLElement('CommandClass')
        energy.CommandClass['id'] = '0x{0:04X}'.format(command_class.class_id)
        energy.CommandClass['symbol'] = command_class.class_desc

        self._energy_xml = energy

    def get_energy_units(self, instance):
        node = self._get_instance(instance)
        return node['units']

    def set_energy_units(self, instance, value):
        node = self._get_instance(instance)
        data = node.attrib.pop(node['units'])
        node['units'] = value
        node[value] = data

    def get_energy_value(self, instance):
        node = self._get_instance(instance)
        return node[node['units']]

    def set_energy_value(self, instance, value):
        node = self._get_instance(instance)
        node[node['units']] = value

    def get_energy_usage(self, instance):
        return EnergyUsage(self, self._get_instance(instance))

    def _get_instance(self, instance):
        for node in self._energy_xml:
            if node.tag == 'CommandClass':
                continue

            if node['instance'] == instance:
                return node

        return self._new_instance(instance)

    def _new_instance(self, instance):
        instance_xml = xml_handler.XMLElement('Instance')
        instance_xml['instance'] = instance
        instance_xml['units'] = self._energy_xml['units']
        instance_xml[self._energy_xml['units']] = 0
        instance_xml['next_id'] = 0
        self._energy_xml.append(instance_xml)

        return instance_xml


class UsageEntry(object):

    @utils.logit
    def __init__(self, parent, xml_data):
        self._xml = xml_data
        self._parent = parent

    @property
    def parent(self):
        return self._parent

    @property
    def id(self):
        return self._xml['id']

    @property
    def start(self):
        secs = float(self._xml.Start.text)
        # secs = time.localtime(secs)
        date_time = datetime.datetime.fromtimestamp(secs)
        return date_time

    @start.setter
    def start(self, value):
        secs = time.mktime(value.timetuple())
        self._xml.Start.text = str(secs)

    @property
    def stop(self):
        secs = float(self._xml.Stop.text)

        if secs == 0:
            return None

        # secs = time.localtime(secs)
        date_time = datetime.datetime.fromtimestamp(secs)
        return date_time

    @stop.setter
    def stop(self, value):
        secs = time.mktime(value.timetuple())
        self._xml.Stop.text = str(secs)

    @property
    def duration(self):
        start = time.mktime(self.start.timetuple())

        stop = self.stop
        if stop is None:
            return 0
        else:
            stop = time.mktime(stop.timetuple())

        return stop - start

    @property
    def calculated_hour_units(self):
        units = self.units
        if units.lower().startswith('watt'):
            units = 'kwh'
        elif units.lower().startswith('btu'):
            units = 'btuh'
        elif units.lower().startswith('amp'):
            units = 'ah'
        else:
            units = ''

        return units

    @property
    def calculated_hour_total(self):
        duration = self.duration
        if duration == 0:
            stop = time.mktime(datetime.datetime.now().timetuple())
            start = time.mktime(self.start.timetuple())
            duration = stop - start

        energy = self.energy_used
        units = self.units

        if units.lower().startswith('watt'):
            kw = energy / 1000.0
            kwh = (kw / (60.0 * 60.0)) * duration

            return kwh
        elif units.lower().startswith('btu'):
            btuh = (energy / (60.0 * 60.0)) * duration
            return btuh

        elif units.lower().startswith('amp'):
            ah = (energy / (60.0 * 60.0)) * duration
            return ah

        return 0.0

    @property
    def energy_used(self):
        return self._xml['energy_used']

    @energy_used.setter
    def energy_used(self, value):
        value = '{0:.2f}'.format(float(value))
        self._xml['energy_used'] = value

    @property
    def units(self):
        return self._parent._xml['units']

    def __eq__(self, other):
        return object.__eq__(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(repr(self))


class EnergyUsage(list):

    def __init__(self, parent, xml):
        self.__parent = parent
        self._xml = xml
        self._id_count = self._xml['next_id']

        list.__init__(self)

    def __eq__(self, other):
        return object.__eq__(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(repr(self))

    @property
    def daily_consumption(self):
        res = []

        for entry in self:
            start = entry.start
            date = start.date()
            consumption = entry.calculated_hour_total
            units = entry.calculated_hour_units

            if not units:
                continue

            for i, (d, total, unts) in enumerate(res):
                if d == date:
                    total += consumption
                    res[i] = [d, total, unts]
                    break
            else:
                res += [[date, consumption, units]]

        for i, (date, total, units) in enumerate(res):
            res[i] = [date.isoformat(), total, units]

        return res

    def new(self):

        usage_entry = xml_handler.XMLElement('Useage')
        usage_entry['energy_used'] = 0
        usage_entry['id'] = self._id_count

        self._id_count += 1
        self._xml['next_id'] = self._id_count

        usage_entry.Start = xml_handler.XMLElement('Start')
        usage_entry.Stop = xml_handler.XMLElement('Stop')
        usage_entry.Start.text = '0'
        usage_entry.Stop.text = '0'

        self._xml.append(usage_entry)

        return UsageEntry(self, self._xml[-1])

    def __iter__(self):
        for node in self._xml:
            yield UsageEntry(self, node)

    def __contains__(self, item):
        return item.parent == self

    def remove(self, item):
        for i, node in enumerate(list(self._xml)[:]):
            if i == item.index:
                self._xml.remove(node)
                return

        raise ValueError('Item not in {0}'.format(repr(self)))

    def __len__(self):
        return len(self._xml)

    def __getitem__(self, item):
        try:
            return list(self)[item]
        except IndexError:
            raise IndexError('Index out of range ({0})'.format(item))

    def __setitem__(self, key, value):
        raise RuntimeError(
            'object is write protected, use the "new" method when adding'
        )

    def clear(self):
        self._xml.clear()
