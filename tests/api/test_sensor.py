#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
.. module:: tests

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave Library

.. moduleauthor: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

License : GPL(v3)

**python-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**python-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.

"""

import sys, os, shutil
import time
import unittest
from pprint import pprint
import datetime
import random
import socket
import re
import libopenzwave
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from tests.common import pyozw_version
from tests.common import SLEEP
from tests.api.common import TestApi
from tests.common import TestPyZWave

class TestSensor(TestApi):

    def test_010_sensor_bool(self):
        ran = False
        for node in self.active_nodes:
            for val in self.active_nodes[node].get_sensors(type='Bool') :
                ran = True
                self.assertTrue(self.active_nodes[node].get_sensor_value(val) in [True, False])
        if ran == False :
            self.skipTest("No Bool sensor found")

    def test_110_sensor_byte(self):
        ran = False
        for node in self.active_nodes:
            for val in self.active_nodes[node].get_sensors(type='Byte') :
                ran = True
                good = True
                try :
                    newval = int(self.active_nodes[node].get_sensor_value(val))
                except :
                    good = False
                self.assertTrue(good)
        if ran == False :
            self.skipTest("No Byte sensor found")

    def test_210_sensor_short(self):
        ran = False
        for node in self.active_nodes:
            for val in self.active_nodes[node].get_sensors(type='Short') :
                ran = True
                good = True
                try :
                    newval = int(self.active_nodes[node].get_sensor_value(val))
                except :
                    good = False
                self.assertTrue(good)
        if ran == False :
            self.skipTest("No Short sensor found")

    def test_310_sensor_int(self):
        ran = False
        for node in self.active_nodes:
            for val in self.active_nodes[node].get_sensors(type='Int') :
                ran = True
                good = True
                try :
                    newval = int(self.active_nodes[node].get_sensor_value(val))
                except :
                    good = False
                self.assertTrue(good)
        if ran == False :
            self.skipTest("No Int sensor found")

    def test_410_sensor_decimal(self):
        ran = False
        for node in self.active_nodes:
            for val in self.active_nodes[node].get_sensors(type='Decimal') :
                ran = True
                good = True
                try :
                    newval = float(self.active_nodes[node].get_sensor_value(val))
                except :
                    good = False
                self.assertTrue(good)
        if ran == False :
            self.skipTest("No Decimal sensor found")
            
    def test_510_sensor_label(self):
        ran = False
        for node in self.active_nodes:
            for sensorid, sensor in self.active_nodes[node].get_sensors().items():
                ran = True
                label = sensor.label
                self.assertTrue(isinstance(label, str))
        if ran == False :
            self.skipTest("No sensor found")

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
