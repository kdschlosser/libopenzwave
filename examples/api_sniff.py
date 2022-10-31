#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave wrapper

.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

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

import sys
import threading
import time

import libopenzwave


event = threading.Event()

log = "Debug"
sniff = 60.0
device = None

for arg in sys.argv:
    if arg.startswith("--device"):
        temp, device = arg.split("=")
    elif arg.startswith("--log"):
        temp, log = arg.split("=")
    elif arg.startswith("--sniff"):
        temp, sniff = arg.split("=")
        sniff = float(sniff)
    elif arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")

# Define some manager options

options = libopenzwave.ZWaveOption(device, user_path=".")

options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level("Debug")

# options.set_save_log_level('Info')
options.set_logging(True)
options.lock()

def network_started(network, *_, **__):
    print('//////////// ZWave network is started ////////////')
    print(
        'OpenZWave network is started : '
        'homeid {0:08x} - {1} nodes were found.'.format(
            network.home_id,
            network.nodes_count
        )
    )

    event.set()


def network_reset(*_, **__):
    print('OpenZWave network is reset.')


def network_ready(network, *_, **__):
    print('//////////// ZWave network is ready ////////////')
    print(
        'ZWave network is ready : {0} '
        'nodes were found.'.format(network.nodes_count)
    )
    print('Controller : {0}'.format(network.controller.name))

    openzwave.SIGNAL_VALUE_CHANGED.register(value_update)
    openzwave.SIGNAL_NETWORK_CONTROLLER_COMMAND.register(ctrl_message)
    openzwave.SIGNAL_NODE_COMMAND.register(node_message)

    event.set()


def value_update( node, value, val_data):
    print(
        'Node: {0} ({1}) Value update : {2}. Data:{3}'.format(
            node.name,
            node.location,
            value.label,
            val_data.data
        )
    )

def ctrl_message(state, *_, **__):
    print('Controller message : {0}.'.format(state.command.doc))

def node_message(node, state, *_, **__):
    print('Node {0} message : {1}.'.format(node.name, state.command.doc))


openzwave.SIGNAL_NETWORK_STARTED.register(network_started)
openzwave.SIGNAL_NETWORK_RESET.register(network_reset)
openzwave.SIGNAL_NETWORK_READY.register(network_ready)

#Create a network object
network = openzwave.ZWaveNetwork(options, single_notification_handler=False)

print("------------------------------------------------------------")
print("Waiting for driver : ")
print("------------------------------------------------------------")

event.wait()
event.clear()

print("Use openzwave library : {0}".format(network.controller.ozw_library_version))
print("Use python library : {0}".format(network.controller.python_library_version))
print("Use ZWave library : {0}".format(network.controller.library_description))
print("Network home id : {0}".format(network.home_id_str))
print("Controller node id : {0}".format(network.controller.node.node_id))
print("Controller node version : {0}".format(network.controller.node.version))
print("Nodes in network : {0}".format(network.nodes_count))
print("------------------------------------------------------------")
print("Waiting for network to become ready : ")
print("-----------------------------------------------------------")

event.wait()

print("------------------------------------------------------------")
print("Controller capabilities : {}".format(network.controller.capabilities))
print("Controller node capabilities : {}".format(network.controller.node.capabilities))
print("Nodes in network : {}".format(network.nodes_count))
print("Driver statistics : {}".format(network.controller.stats))
print("------------------------------------------------------------")

time.sleep(sniff)

print("")
print("------------------------------------------------------------")
print("Driver statistics : {}".format(network.controller.stats))
print("------------------------------------------------------------")

print("")
print("------------------------------------------------------------")
print("Stop network")
print("------------------------------------------------------------")
network.stop()
