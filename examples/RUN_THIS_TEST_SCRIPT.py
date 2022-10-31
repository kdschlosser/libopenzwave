# -*- coding: utf-8 -*-

# ****************** READ COMMENTS STARTING AT LINE 31 ************************

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
:synopsis: Test Script

.. moduleauthor:: Kevin G Schlosser
"""


# This is a simple test script. It is only designed to show you some of the
# changes made. and also how easy it is to now use the new system. There are
# some options to set so scroll down a but to set them. If you are using a
# new set of user config files the startup is going to be slower the first
# time around because the program has to populate all of the cached data to
# build the files. running the script more then a single time should be done.

# you need not worry about telling the program what serial port your ZStick
# is on. It does all of this automatically now.

import logging


# Set this variable to the user config folder. If you leave this blank it is
# going to make one for you
# Windows = programdata/.python-openzwave, others = ~/.python-openzwave
USER_CONFIG = r''

# set this to one of the following, setting this to DEBUG is going to slow
# down the program. This is because of the logging routine I wrote that
# prints out the filename and line number of where a function was called from
# and also where the function is located. It also times the execution time of
# the called function and displays any arguments passed as well as any
# return data.
# logging.NOTSET
# logging.DEBUG
# logging.INFO

# you optionally have these 3 to use as well and I think the names describe
# them pretty well.
# openzwave.LOGGING_DATA_PATH
# openzwave.LOGGING_DATA_PATH_WITH_RETURN
# openzwave.LOGGING_TIME_FUNCTION_CALLS
POZW_LOGGING = logging.NOTSET

# set this to either True or False
OZW_LOGGING = False


# This option changes the notification system to use a single thread to
# handle all notifications or to create a new thread for each node. Now I use
# that term create per node. and it does do this. But if there are no
# notifications being processed or queued to be processed the thread shuts
# down. when a notification comes in then a new thread gets created. This
# process gets done either way. This is going to give you an idea of the
# changes in performance from what it used to be and what it is now. It is
# not 100% because the whole system is designed to not stall OZW. so the
# difference you see using this is going to be 10 times more if it was the
# old way vs the new
SINGLE_NOTIFICATION_HANDLER = True

import sys
import os
import openzwave
import threading

if not USER_CONFIG:
    if sys.platform.startswith('win'):
        USER_CONFIG = os.path.join(os.path.expandvars('%programdata%'), '.python-openzwave')
    else:
        USER_CONFIG = os.path.join(os.path.expanduser('~'), '.python-openzwave')

    if not os.path.exists(USER_CONFIG):
        os.mkdir(USER_CONFIG)


openzwave.logger.setLevel(POZW_LOGGING)
option = openzwave.ZWaveOption(user_path=USER_CONFIG)
option.set_logging(OZW_LOGGING)
option.set_console_output(OZW_LOGGING)

option.lock()
event = threading.Event()


def stop_callback(**kwargs):
    print('******** FINISHED STOPPING NETWORK ********')
    event.set()


def ready_callback(**kwargs):
    print('******** FINISHED LOADING NETWORK ********')
    print(
        'This is when the typical app will load the information that is '
        'needed.'
    )
    event.set()


def failed_callback(**kwargs):
    print('******** NETWORK FAILED ********')
    event.set()


def node_cached_callback(sender, **kwargs):
    print('------ NODE CACHED')
    print('NODE ID:', sender.id)
    print('NODE NAME:', sender.name)
    print('NODE LOCATION:', sender.location)
    print(
        'Run code to create an icon maybe with a banner indicating that '
        'the node is still loading.'
    )

    print('\n\n')


def value_cached_callback(value, node, **kwargs):
    print('------ VALUE CACHED')
    print('NODE ID:', node.id)
    print('NODE NAME:', node.name)
    print('VALUE ID:', value.id)
    print('VALUE INDEX:', value.index)
    print('VALUE LABEL:', value.label)
    print('VALUE_COMMAND CLASS:', value.command_class.class_desc)
    print(
        'Run code to create the GUI representation of the value '
        'with some kind of an identifier that any dynamic information is'
        'still loading.'
    )

    print('\n\n')


def node_ready_callback(sender, **kwargs):
    print('------ NODE READY')
    print('NODE ID:', sender.id)
    print('NODE NAME:', sender.name)
    print('NODE LOCATION:', sender.location)
    print(
        'run code to update the GUI so that the user knows the node has '
        'been fully loaded.'
    )
    print('\n\n')


def value_ready_callback(node, value, **kwargs):
    print('------ VALUE READY')
    print('NODE ID:', node.id)
    print('NODE NAME:', node.name)
    print('VALUE INDEX:', value.index)
    print('VALUE LABEL:', value.label)
    print('VALUE_COMMAND CLASS:', value.command_class.class_desc)
    print(
        'run code to update the GUI so that the user knows the value has '
        'been fully loaded.'
    )

    print('\n\n')

def value_changed_callback(node, value, value_data, **kwargs):
    print('------ VALUE CHANGED')
    print('NODE ID:', node.id)
    print('NODE NAME:', node.name)
    print('VALUE INDEX:', value.index)
    print('VALUE LABEL:', value.label)
    print('VALUE COMMAND CLASS:', value.command_class.class_desc)
    print('VALUE DATA (caused signal):', value_data.data)
    print('VALUE DATA (from value):', value.data)
    print(
        'You may or may not see a difference in the value data. '
        'You will always want to use value_data.data to get the data that '
        'is associated with the signal.'
    )

    print('\n\n')


openzwave.SIGNAL_NODE_READY.register(node_ready_callback)
openzwave.SIGNAL_VALUE_READY.register(value_ready_callback)

# comment the next line to import startup performance. This causes a heap of
# extra network activity because of using value.data in the callback.
# It does this for every single value for every single node on the network
openzwave.SIGNAL_VALUE_CHANGED.register(value_changed_callback)

openzwave.SIGNAL_NODE_LOADING_CACHED.register(node_cached_callback)
openzwave.SIGNAL_VALUE_LOADING_CACHED.register(value_cached_callback)
openzwave.SIGNAL_NETWORK_READY.register(ready_callback)
openzwave.SIGNAL_NETWORK_FAILED.register(failed_callback)
openzwave.SIGNAL_NETWORK_STOPPED.register(stop_callback)

network = openzwave.ZWaveNetwork(
    option,
    single_notification_handler=SINGLE_NOTIFICATION_HANDLER
)

event.wait()

for node in network:
    stats = node.stats

    print(stats.sentCnt.doc, ':', stats.sentCnt)
    print(stats.sentFailed.doc, ':', stats.sentFailed)
    print(stats.retries.doc, ':', stats.retries)
    print(stats.receivedCnt.doc, ':', stats.receivedCnt)
    print(stats.receivedDups.doc, ':', stats.receivedDups)
    print(stats.receivedUnsolicited.doc, ':', stats.receivedUnsolicited)
    print(stats.sentTS.doc, ':', stats.sentTS)
    print(stats.receivedTS.doc, ':', stats.receivedTS)
    print(stats.lastRequestRTT.doc, ':', stats.lastRequestRTT)
    print(stats.averageRequestRTT.doc, ':', stats.averageRequestRTT)
    print(stats.lastResponseRTT.doc, ':', stats.lastResponseRTT)
    print(stats.averageResponseRTT.doc, ':', stats.averageResponseRTT)
    print(stats.quality.doc, ':', stats.quality)
    print(stats.lastReceivedMessage.doc, ':', stats.lastReceivedMessage)
    print(stats.txStatusReportSupported.doc, ':', stats.txStatusReportSupported)
    print(stats.txStatusReportSupported.doc, ':', stats.txStatusReportSupported)
    print(stats.txTime.doc, ':', stats.txTime)
    print(stats.hops.doc, ':', stats.hops)
    print(stats.rssi_1.doc, ':', stats.rssi_1)
    print(stats.rssi_2.doc, ':', stats.rssi_2)
    print(stats.rssi_3.doc, ':', stats.rssi_3)
    print(stats.rssi_4.doc, ':', stats.rssi_4)
    print(stats.rssi_5.doc, ':', stats.rssi_5)
    print(stats.ackChannel.doc, ':', stats.ackChannel)
    print(stats.lastTxChannel.doc, ':', stats.lastTxChannel)
    print(stats.routeScheme.doc, ':', stats.routeScheme)
    print(stats.routeUsed.doc, ':', stats.routeUsed)
    print(stats.routeSpeed.doc, ':', stats.routeSpeed)
    print(stats.routeTries.doc, ':', stats.routeTries)
    print(stats.lastFailedLinkFrom.doc, ':', stats.lastFailedLinkFrom)
    print(stats.lastFailedLinkTo.doc, ':', stats.lastFailedLinkTo)

    print(stats.ccData.doc, ':')

    for ccd in stats.ccData:
        print('   ', ccd.commandClassId.doc, ':', ccd.commandClassId)
        print('   ', ccd.sentCnt.doc, ':', ccd.sentCnt)
        print('   ', ccd.receivedCnt.doc, ':', ccd.receivedCnt)


event.clear()
print('********* STOPPING NETWORK *************')
network.stop()
event.wait()
