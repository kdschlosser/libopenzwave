# -*- coding: utf-8 -*-

import sys
import os


BASE_PATH = os.path.dirname(__file__)

if not BASE_PATH:
    BASE_PATH = os.path.dirname(sys.argv[0])

if not BASE_PATH:
    BASE_PATH = os.getcwd()

#
# build_path = os.path.join(os.path.abspath(BASE_PATH), 'build')
#
# for d in os.listdir(build_path):
#
#     if d.startswith('lib'):
#         build_path = os.path.join(build_path, d)
#
# sys.path.insert(0, build_path)

import threading # NOQA
import openzwave # NOQA
import time # NOQA

start_time = time.time()
openzwave.logger.setLevel(openzwave.logger.INFO)

device = '127.0.0.1'

option = openzwave.ZWaveOption(device=device)
option.admin_password = 'SOME_PASSWORD'
option.lock()

def network_ready(*args, **kargs):
    print('************ Network Ready *****************')
    end_time = time.time()

    print('Total load time:', end_time - start_time, 'seconds')
    print()
    event.set()


def value_changed(node, value, *args, **kwargs):
    print('************ Value Changed *****************')
    print('timestamp:', int(round(time.time() * 1000)), '   ', node.name, '   ', value.label, ':', value.data)
    print()


def network_stopped(*args, **kwargs):
    print('************** Network Stopped *************')
    event.set()

def network_started(*args, **kwargs):
    print('************** Network Started *************')

openzwave.SIGNAL_NETWORK_STARTED.register(network_started)
openzwave.SIGNAL_NETWORK_READY.register(network_ready)
openzwave.SIGNAL_NETWORK_STOPPED.register(network_stopped)

event = threading.Event()
network = openzwave.ZWaveNetwork(option, single_notification_handler=False)

event.wait()

start_time = time.time()

node_count = 0
value_count = 0
for node in network:
    node_count += 1
    print(node.name, '(' + str(node.id) + ')')
    for value in node:
        value.refresh()
        value_count += 1
        print('   ', value.label, '(index: ' + str(value.index) + '):', value.data, )

end_time = time.time()
duration = end_time - start_time
print('Node and Value Enumeration duration (with value refresh):', duration * 1000, 'ms')

print('Number of nodes:', node_count, 'values:', value_count)
print('Average query time per value:', (duration / value_count) * 1000, 'ms')
print('Average node value enumeration time:', (duration / node_count) * 1000, 'ms')


openzwave.SIGNAL_VALUE_CHANGED.register(value_changed)

try:
    event.wait()
except KeyboardInterrupt:
    event.clear()
    network.stop()
    event.wait()
