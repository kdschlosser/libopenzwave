# -*- coding: utf-8 -*-

import sys
import os


BASE_PATH = os.path.dirname(__file__)

if not BASE_PATH:
    BASE_PATH = os.path.dirname(sys.argv[0])

if not BASE_PATH:
    BASE_PATH = os.getcwd()

build_path = os.path.join(os.path.abspath(BASE_PATH), 'build')

for d in os.listdir(build_path):

    if d.startswith('lib'):
        build_path = os.path.join(build_path, d)

sys.path.insert(0, build_path)

import threading # NOQA
import openzwave # NOQA
import time # NOQA

start_time = time.time()

openzwave.logger.setLevel(openzwave.logger.INFO)

option = openzwave.ZWaveOption()
option.admin_password = 'SOME_PASSWORD'
option.use_server = True
option.console_output = False
option.logging = False
option.lock()


def network_ready(*args, **kwargs):
    print('************* Network Ready ******************')
    end_time = time.time()

    print('Total load time:', end_time - start_time, 'seconds')
    event.set()


def network_stopped(*args, **kwargs):
    print('************* Network Stopped ******************')
    event.set()


def value_changed(node, value, *args, **kwargs):
    print('************ Value Changed *****************')
    print('timestamp:', int(round(time.time() * 1000)), '   ', node.name, '   ', value.label, ':', value.data)
    print()


def network_started(*args, **kwargs):
    print('************** Network Started *************')


openzwave.SIGNAL_NETWORK_STARTED.register(network_started)
openzwave.SIGNAL_NETWORK_READY.register(network_ready)
openzwave.SIGNAL_NETWORK_STOPPED.register(network_stopped)

event = threading.Event()
network = openzwave.ZWaveNetwork(option)

event.wait()

for node in network:
    print(node.name)
    for value in node:
        print('   ', value.label, ':', value.data)

event.clear()

openzwave.SIGNAL_VALUE_CHANGED.register(value_changed)

try:
    event.wait()
except KeyboardInterrupt:
    event.clear()
    network.stop()
    event.wait()


