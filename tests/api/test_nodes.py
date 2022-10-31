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
import six
if six.PY3:
    from pydispatch import dispatcher
else:
    from louie import dispatcher
from six import string_types, integer_types
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
from tests.common import TestPyZWave, json_dumps, json_loads

class TestNodes(TestApi):

    def test_000_nodes_count(self):
        self.assertTrue(isinstance(self.network.nodes_count, integer_types))
        self.assertTrue(self.network.nodes_count>0)

    def test_100_nodes_test(self):
        for node in self.active_nodes:
            self.active_nodes[node].test(5)

    def test_110_nodes_heal(self):
        for node in self.active_nodes:
            self.active_nodes[node].heal()
        for node in self.active_nodes:
            self.active_nodes[node].heal(True)

    def test_200_nodes_to_dict(self):
        for node in self.active_nodes:
            try :
                noded = self.active_nodes[node].to_dict()
                self.assertEqual(type(noded), type(dict()))
                self.assertTrue('values' in noded)
                self.assertTrue('groups' in noded)
                self.assertTrue('neighbors' in noded)
                self.assertTrue('capabilities' in noded)
                res = json_dumps(noded)
            except TypeError:
                res = None
            self.assertNotEqual(res, None)

    def test_210_controller_to_dict(self):
        try :
            nodes = self.network.controller.to_dict()
            self.assertEqual(type(nodes), type(dict()))
            res = json_dumps(nodes)
        except TypeError:
            res = None
        self.assertNotEqual(res, None)

    def test_220_nodes_groups_to_dict(self):
        for node in self.active_nodes:
            try :
                groups = self.active_nodes[node].groups_to_dict()
                self.assertTrue(type(groups), type(dict()))
                self.assertEqual(type(groups), type(dict()))
                res = json_dumps(groups)
            except TypeError:
                res = None
            self.assertNotEqual(res, None)

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
