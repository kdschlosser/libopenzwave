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
:synopsis: Signals (callback notifications)

.. moduleauthor:: Kevin G Schlosser


Before you had to know what version of Python the user was running your
application in to import the proper signaling module (louie or pydispatch).
You no longer have to worry about that. Everything is handled internally to
pyozw now.

This was the old way to go about registering a callback to a signal.

.. code-block:: python

    dispatcher.connect(
        self.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD,
        some_callback_function
    )


This is now the new way.

.. code-block:: python

    libopenzwave.SIGNAL_NETWORK_READY(some_callback_function)


This does not seem like a HUGE change. But when you have to key in a whole mess
of registrations it is far less code you have to add. Plus it is easier to read

There has been a large change to the Signals.. You can now register a signal
to a callback for a specific object. This is a great mechanism to provide
scenes with. Or if you want to update the GUI for a specific node or value
that a user has in focus.

.. code-block:: python

    node = network.nodes[10]

    def value_changed_callback(*args, **kwargs):
        print(args, kwargs)

    for value in node:

        libopenzwave.SIGNAL_VALUE_CHANGED.register(
            value_changed_callback,
            sender=value
        )


to unregister a callback from a signal you would change the `register` to
`unregister`


.. code-block:: python

    node = network.nodes[10]

    def value_changed_callback(*args, **kwargs):
        print(args, kwargs)

    for value in node:
        libopenzwave.SIGNAL_VALUE_CHANGED.register(
            value_changed_callback,
            sender=value
        )

    for value in node:
        libopenzwave.SIGNAL_VALUE_CHANGED.unregister(
            value_changed_callback,
            sender=value
        )


These are the SIGNAL constants:


* Network Signals:

    * `SIGNAL_NETWORK_FAILED`
    * `SIGNAL_NETWORK_READY`
    * `SIGNAL_NETWORK_RESET`
    * `SIGNAL_NETWORK_STARTED`
    * `SIGNAL_NETWORK_STOPPED`
    * `SIGNAL_NETWORK_MANUFACTURER_DB_READY`
    * `SIGNAL_NETWORK_CONTROLLER_COMMAND`

* Alert Signals:

    * `SIGNAL_USER_ALERTS`
    * `SIGNAL_ALERT_DNS_ERROR`
    * `SIGNAL_ALERT_UNSUPPORTED_CONTROLLER`
    * `SIGNAL_ALERT_APPLICATION_STATUS_RETRY`
    * `SIGNAL_ALERT_APPLICATION_STATUS_QUEUED`
    * `SIGNAL_ALERT_APPLICATION_STATUS_REJECTED`
    * `SIGNAL_ALERT_CONFIG_OUT_OF_DATE`
    * `SIGNAL_ALERT_MFS_OUT_OF_DATE`
    * `SIGNAL_ALERT_CONFIG_FILE_DOWNLOAD_FAILED`
    * `SIGNAL_ALERT_RELOAD_REQUIRED`

* Value Signals:

    * `SIGNAL_VALUE_LOADING_STARTED`
    * `SIGNAL_VALUE_LOADING_CACHED`
    * `SIGNAL_VALUE_READY`
    * `SIGNAL_VALUE_CHANGED`
    * `SIGNAL_VALUE_REFRESHED`
    * `SIGNAL_VALUE_REMOVED`

* Node Signals:

    * `SIGNAL_NODE_ADDED`
    * `SIGNAL_NODE_LOADING_STARTED`
    * `SIGNAL_NODE_LOADING_CACHED`
    * `SIGNAL_NODE_LOADING_ESSENTIAL`
    * `SIGNAL_NODE_READY`
    * `SIGNAL_NODE_REMOVED`
    * `SIGNAL_NODE_RESET`
    * `SIGNAL_NODE_BUTTON_OFF`
    * `SIGNAL_NODE_BUTTON_ON`
    * `SIGNAL_NODE_CREATE_BUTTON`
    * `SIGNAL_NODE_DELETE_BUTTON`
    * `SIGNAL_NODE_ASSOCIATION_GROUP`
    * `SIGNAL_NODE_CONTROLLER_COMMAND`
    * `SIGNAL_NODE_POLLING_DISABLED`
    * `SIGNAL_NODE_POLLING_ENABLED`
    * `SIGNAL_NODE_EVENT`
    * `SIGNAL_NODE_NAMING`
    * `SIGNAL_NODE_PROTOCOL_INFO`

* Misc Signals:

    * `SIGNAL_NODES_LOADED`
    * `SIGNAL_NODES_LOADED_SOME_DEAD`
    * `SIGNAL_NODES_LOADED_AWAKE`
    * `SIGNAL_NODES_LOADED_ALL`
    * `SIGNAL_NOTIFICATION`
    * `SIGNAL_MSG_COMPLETE`


There are several signals that we want to make sure you fully understand the
purpose of. and also proper use. The proper use is what is going to give the
user the best experience.

Some of these signals are going to only be seen when the network first starts
or when a new node is added to the network. If the network has already been
set up and the program is just starting up libopenzwave has a very large
database of cached information and information that is not actually stored in
the device.
This cached data is ready to be accessed almost instantly and quite a bit of
information is available. There is enough information for you to be able to
display a GUI representing the network and it's nodes. You are not going to be
able to query the network or any of the nodes/values for any dynamic
information until the node has fully loaded. But there is no need to have
your program sit and wait for this to happen.

* `SIGNAL_NETWORK_STARTED`: When the network gets started.
* `SIGNAL_NETWORK_READY`: When the network and all of the nodes in it have
  completely loaded.

These are the signals that will happen when all of the nodes on a network
have been queried for it's existence and also for any dynamic information that
may not be synced with the cached data.

* `SIGNAL_NODES_LOADED`: The node have finished being loaded. This is a
  generic signal that covers all of the signals below. This signal gets sent
  along with any of the ones listed below.
* `SIGNAL_NODES_LOADED_SOME_DEAD`: When all of the node in the network have
  loaded but some where not able to be contacted.
* `SIGNAL_NODES_LOADED_AWAKE`: all nodes have loaded and all of the nodes that
  are considered awake are sent to the callback.
* `SIGNAL_NODES_LOADED_ALL`: all nodes have loaded

These signals will occur during the node loading phase. These signals will
happen for each node that is on the network.

* `SIGNAL_NODE_ADDED`: when a node gets included into the network for the
  first time.
* `SIGNAL_NODE_LOADING_STARTED`: when the saved node data starts to load or
  when a new nodes cached data gets created.
* `SIGNAL_NODE_LOADING_CACHED`: when all of the cached data has been loaded
  for a node.
* `SIGNAL_NODE_LOADING_ESSENTIAL`: loading of essential information has
  finished.
* `SIGNAL_NODE_READY`: load has been fully loaded, this includes the node
  being contacted and dynamic data being updated

Here are the value signals that are important for startup. Value data is also
loaded from cache. and any dynamic information gets updated later on during
the startup process.

* `SIGNAL_VALUE_LOADING_STARTED`: The loading of a value has begun
* `SIGNAL_VALUE_LOADING_CACHED`: The loading of the cached data for a value as
  finished.
* `SIGNAL_VALUE_READY`: a value has been fully loaded.

Below I am going to show 2 code examples. the 2 examples are going to show
the common way an application will typically code a network startup. The
second way I am going to show you will decrease the time it takes to startup
a network by an average of 85%.

Typical Network startup design.

.. code-block:: python

    import threading
    import libopenzwave

    libopenzwave.logger.setLevel(openzwave.logger.NOTSET)

    # we no longer need to specify the device (port) The library now
    # autodetects
    # SilLabs based chips and will set the device (port) for you.
    option = libopenzwave.ZWaveOption(user_path='~/zwave')
    option.set_logging(False)
    option.lock()

    event = Threading.Event()

    def stop_callback(**kwargs):
        print(kwargs)
        print('******** FINISHED STOPPING NETWORK ********')
        event.set()

    def ready_callback(**kwargs):
        print(kwargs)
        print('******** FINISHED LOADING NETWORK ********')


        for node in network:
            print('NODE ID:', node.id)
            print('NODE NAME:', node.name)
            print('NODE LOCATION:', node.location)

        network.stop()

    def failed_callback(**kwargs):
        print(kwargs)
        print('******** NETWORK FAILED ********')
        event.set()

    libopenzwave.SIGNAL_NETWORK_READY.register(ready_callback)
    libopenzwave.SIGNAL_NETWORK_FAILED.register(failed_callback)
    libopenzwave.SIGNAL_NETWORK_STOPPED.register(stop_callback)

    network = libopenzwave.ZWaveNetwork(option)
    event.wait()


Now the above code will get the job done. But if the user has a largish
network and there are battery devices or possibly even some dead nodes on the
network you can have startup times that take several minutes or longer.

If you notice the nodes do not get enumerated until the network has completely
loaded. You will also notice the information we are accessing is actually data
that gets cached. So why do we need to wait until the end to be able to show
this information?


Here is some code for an alternate way.

.. code-block:: python

    import threading
    import libopenzwave

    libopenzwave.logger.setLevel(openzwave.logger.NOTSET)

    # we no longer need to specify the device (port) The library now
    # autodetects
    # SilLabs based chips and will set the device (port) for you.
    option = libopenzwave.ZWaveOption(user_path='~/zwave')
    option.set_logging(False)
    option.lock()

    event = Threading.Event()

    def stop_callback(**kwargs):
        print(kwargs)
        print('******** FINISHED STOPPING NETWORK ********')
        event.set()

    def ready_callback(**kwargs):
        print(kwargs)
        print('******** FINISHED LOADING NETWORK ********')
        print(
        'This is when the typical app will load the information that is '
        'needed.'
        )

        network.stop()

    def failed_callback(**kwargs):
        print(kwargs)
        print('******** NETWORK FAILED ********')
        event.set()

    def node_cached_callback(sender, **kwargs):
        print('NODE ID:', sender.id)
        print('NODE NAME:', sender.name)
        print('NODE LOCATION:', sender.location)
        print(
            'Run code to create an icon maybe with a banner indicating that '
            'the node is still loading.'
        )

    def value_cached_callback(sender, **kwargs):
        print('VALUE INDEX:', sender.index)
        print('VALUE LABEL:', value.label)
        print('VALUE_COMMAND CLASS:', value.command_class.class_desc)
        print(
            'Run code to create the GUI representation of the value '
            'with some kind of an identifier that any dynamic information is'
            'still loading.'
        )

    def node_ready_callback(sender, **kwargs):
        print('NODE ID:', sender.id)
        print(
            'run code to update the GUI so that the user knows the node has '
            'been fully loaded.'
        )

    def value_ready_callback(sender, **kwargs):
        print('VALUE LABEL:', value.label)
        print(
            'run code to update the GUI so that the user knows the value has '
            'been fully loaded.'
        )

    libopenzwave.SIGNAL_NODE_READY(node_ready_callback)
    libopenzwave.SIGNAL_VALUE_READY(value_ready_callback)
    libopenzwave.SIGNAL_NODE_LOADING_CACHED(node_cached_callback)
    libopenzwave.SIGNAL_VALUE_LOADING_CACHED(value_cached_callback)
    libopenzwave.SIGNAL_NETWORK_READY.register(ready_callback)
    libopenzwave.SIGNAL_NETWORK_FAILED.register(failed_callback)
    libopenzwave.SIGNAL_NETWORK_STOPPED.register(stop_callback)

    network = libopenzwave.ZWaveNetwork(option)
    event.wait()


"""

# noinspection PyPackageRequirements
from . import utils
import logging
import threading


class RegisteredSignal(object):

    def __init__(self, signal):
        self.__signal = signal
        self.__items = []

    def __str__(self):
        return 'Signal: "{0}", Callbacks: {1}'.format(
            self.__signal,
            self.__items
        )

    def __eq__(self, other):
        """
        :param other:
        :type other: "RegisteredSignal"

        :rtype: bool
        """
        return self.__signal == other

    def __ne__(self, other):
        """
        :param other:
        :type other: "RegisteredSignal"

        :rtype: bool
        """
        return not self.__eq__(self)

    def __contains__(self, item):
        """
        :param item:
        :type item: callable

        :rtype: bool
        """
        return item in self.__items

    def __iter__(self):
        for item in self.__items:
            yield item

    def __call__(self, sender, *args, **kwargs):
        """
        :param sender:
        :param *args:
        :param **kwargs:
        """
        for callback, obj in self:
            if obj in (None, sender):
                callback(sender=sender, signal=self.__signal, *args, **kwargs)

    def remove(self, item):
        """
        :param item:
        :type item: callable
        """
        if item in self:
            self.__items.remove(item)

    @property
    def is_empty(self):
        """
        :rtype: bool
        """
        return bool(len(self.__items))

    def __iadd__(self, other):
        """
        :param other:
        :type other: callable

        :rtype: "RegisteredSignal"
        """
        if other not in self:
            self.__items += [other]

        return self


class Dispatcher(object):

    def __init__(self):
        self.__registered = []
        self.__no_signal = []
        self.__lock = threading.RLock()

    def connect(self, receiver, signal=None, sender=None):
        """
        :param receiver:
        :param signal:
        :param sender:
        """
        with self.__lock:

            if signal is None:
                if (receiver, sender) not in self.__no_signal:
                    self.__no_signal += [(receiver, sender)]
            else:
                for reg_signal in self.__registered:
                    if reg_signal == signal:
                        break
                else:
                    reg_signal = RegisteredSignal(signal)
                    for item in self.__no_signal:
                        reg_signal += item

                    self.__registered += [reg_signal]

                reg_signal += (receiver, sender)

    def disconnect(self, receiver, signal=None, sender=None):
        """
        :param receiver:
        :param signal:
        :param sender:
        """
        with self.__lock:

            if signal is None:
                if (receiver, sender) in self.__no_signal:
                    self.__no_signal.remove((receiver, sender))

            else:
                for reg_signal in self.__registered[:]:
                    reg_signal.remove((receiver, sender))

                    if reg_signal.is_empty:
                        self.__registered.remove(reg_signal)

    def send(self, signal, sender, *args, **kwargs):
        """
        :param signal:
        :param sender:
        :param args:
        :param kwargs:
        """
        with self.__lock:
            for callback, obj in self.__no_signal:
                if obj in (None, sender):
                    callback(sender=sender, signal=signal, *args, **kwargs)

            for reg_signal in self.__registered:
                if reg_signal == signal:
                    reg_signal(sender, *args, **kwargs)


logger = logging.getLogger(__name__)


dispatcher = Dispatcher()


class _SignalMetaClass(type):

    def __new__(mcs, name, bases, dct):
        cls = (
            super(_SignalMetaClass, mcs).__new__(mcs, name, bases, dct)
        )

        if name != 'Signal':

            doc = """
            Register a callback for a signal.
            
            {params}


            For more information see.. 
            :py:func:`libopenzwave.signals.Signal.register`
            
            """

            if cls.__doc__ is None:
                doc = doc.format(params='')

            else:
                doc = doc.format(
                    params='\n'.join(
                        '        ' + d for d in cls.__doc__.split('\n')
                    ).lstrip()
                )

            def register(self, receiver, sender=None):
                Signal.register(self, receiver, sender)

            def unregister(self, receiver, sender=None):
                """
                Unregister a callback from a signal.

                For more information see..
                :py:func:`libopenzwave.signals.Signal.unregister`
                """
                Signal.unregister(self, receiver, sender)

            register.__doc__ = doc

            setattr(cls, 'register', register)
            setattr(cls, 'unregister', unregister)

        description = dct['description']

        if description:
            cls.__doc__ = description

        return cls


class Signal(str, metaclass=_SignalMetaClass):
    """
    Base class for all signals

    .. code-block:: python

        import libopenzwave

        def callback(**kwargs):
            # add code here
            pass

        libopenzwave.SIGNAL_NODE_ADDED.register(callback)


    .. code-block:: python

        import libopenzwave

        node = network.nodes[10]
        value = node.values.level

        def callback(**kwargs):
            # add code here
            pass

        libopenzwave.SIGNAL_VALUE_CHANGED.register(callback, sender=value)


    The signals run in their own thread. The way the system worked before is
    when ozw sent a notification to pyozw, pyozw would process this notification
    and generate a signal. this signal would then get processed and any
    associated callback would get called. This whole thing would be done in the
    same thread. If a callback had some lengthy code to execute. Or had to wait
    for any reason this would stall pyozw and in turn stall ozw and any network
    communications in or out would also then come to a grinding halt.

    There was a single hurdle i had to jump when I added the threads to the
    signals. This single issue was keeping value data in sync. How i decided to
    handle this issue was to collect all data from a value at the time the
    notification was received from ozw and then attach it to a signal to be
    passed as an argument to the callback.

    This is the way the old system worked.

    .. code-block:: python

        def callback(value, **kwargs):
            print(value.data)


        dispatcher.connect(callback, network.SIGNAL_VALUE_CHANGE)


    This system could no longer work because ozw would get released to go and
    do whatever it is it does before the callback ever gets called. So if
    another notification came in for the same value the first signal callback
    could print out data that is newer. If an application has any code that
    needs to get run based on a values data we want to make sure the proper
    data is gotten.

    so the new way to go about it is as follows.

    .. code-block:: python

        def callback(val_data, **kwargs):
            print(val_data.id)
            print(val_data.command_class)
            print(val_data.index)
            print(val_data.genre)
            print(val_data.type)
            print(val_data.data)
            print(val_data.label)
            print(val_data.units)
            print(val_data.is_read_only)

        libopenzwave.SIGNAL_VALUE_CHANGE.register(callback)


    you can also still get the value object if needed.

    .. code-block:: python

        def callback(sender, node, val_data, **kwargs):
            value = sender
            print(val_data.id)
            print(val_data.command_class)
            print(val_data.index)
            print(val_data.genre)
            print(val_data.type)
            print(val_data.data)
            print(val_data.label)
            print(val_data.units)
            print(val_data.is_read_only)

        libopenzwave.SIGNAL_VALUE_CHANGE.register(callback)

    """
    _instances = {}
    id = -1
    description = ''
    _callbacks = None
    _s = ''

    @classmethod
    def __new__(cls, *args, **kwargs):

        self = super(Signal, cls).__new__(*args, **kwargs)
        setattr(self, '_s', args[1])
        setattr(self, '_callbacks', [])

    @utils.logit
    def register(self, receiver, sender=None):
        """
        Register a callback for a signal.

        :param receiver: callback function
        :type receiver: callable

        :param sender: object that caused the signal to occur
        :type sender: Any

        :return: `None`
        """

        if (receiver, sender) not in self._callbacks:
            self._callbacks.append((receiver, sender))
            dispatcher.connect(receiver, self, sender)

    @utils.logit
    def unregister(self, receiver, sender=None):
        """
        Unregister a callback from a signal.

        There are a few ways to use this method.

        * `unregister(receiver=callback, sender=None)`: This will unregister
          all registrations for the supplied receiver
        * `unregister(receiver=None, sender=obj)`: This will unregister all
          registrations for the supplied sender.
        * `unregister(receiver=None, sender=None)`: This will unregister all
          registrations for this signal.
        * `unregister(receiver=callback, sender=obj)`: This will unregister the
          object and callback
        * `unregister(receiver=callback)`: This will unregister the callback


        :param receiver: same function or method used to register or `None`
        :type receiver: callable, None

        :param sender: same object that was used to register. or `None`
        :type sender: Any, None

        :return: `None`

        :raises: ValueError if there was no registration
        """
        if receiver is None and sender is None:
            for callback, obj in self._callbacks[:]:
                self._callbacks.remove((callback, obj))
                dispatcher.disconnect(callback, self, obj)

        elif receiver is not None and sender is None:
            for callback, obj in self._callbacks[:]:
                if callback == receiver:
                    self._callbacks.remove((callback, obj))
                    dispatcher.disconnect(callback, self, obj)

        elif receiver is None and sender is not None:
            for callback, obj in self._callbacks[:]:
                if obj == sender:
                    self._callbacks.remove((callback, obj))
                    dispatcher.disconnect(callback, self, obj)
        else:
            self._callbacks.remove((receiver, sender))
            dispatcher.disconnect(receiver, self, sender)

    @utils.logit
    def send(self, sender=None, *args, **kwargs):  # NOQA
        """
        Sends the signal. (internal use only)

        :param sender:
        :param args:
        :param kwargs:
        """

        for callback, obj in self._callbacks:
            if obj is None or sender == obj:
                callback(signal=self, sender=sender, *args, **kwargs)

    def __eq__(self, other):
        """
        :param other:
        :type other: int, str

        :rtype: bool
        """
        if other == self._s:
            return True

        if other == self.id:
            return True

        return False

    def __ne__(self, other):
        """
        :param other:
        :type other: int, str

        :rtype: bool
        """
        return not self.__eq__(other)

    def __int__(self):
        """
        :rtype: int
        """
        return self.id

    def __hash__(self):
        """
        :rtype: hash
        """
        return hash(str(self))

    def __str__(self):
        """
        :rtype: str
        """
        return self._s


# noinspection PyPep8Naming
class _SIGNAL_ALERT_CONFIG_OUT_OF_DATE(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 1
    description = (
        "A config file is out of date, use GetNodeId "
        "to determine which node(s) are effected."
    )


SIGNAL_ALERT_CONFIG_OUT_OF_DATE = (
    _SIGNAL_ALERT_CONFIG_OUT_OF_DATE('ConfigOutOfDate')
)


# noinspection PyPep8Naming
class _SIGNAL_ALERT_MFS_OUT_OF_DATE(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 2
    description = 'A manufacturer_specific.xml file is out of date.'


SIGNAL_ALERT_MFS_OUT_OF_DATE = _SIGNAL_ALERT_MFS_OUT_OF_DATE('MFSOutOfDate')


# noinspection PyPep8Naming
class _SIGNAL_ALERT_CONFIG_FILE_DOWNLOAD_FAILED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 3
    description = 'A config file failed to download.'


SIGNAL_ALERT_CONFIG_FILE_DOWNLOAD_FAILED = (
    _SIGNAL_ALERT_CONFIG_FILE_DOWNLOAD_FAILED('ConfigFileDownloadFailed')
)


# noinspection PyPep8Naming
class _SIGNAL_ALERT_DNS_ERROR(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
    """
    id = 4
    description = 'DNS error.'


SIGNAL_ALERT_DNS_ERROR = _SIGNAL_ALERT_DNS_ERROR('DNSError')


# noinspection PyPep8Naming
class _SIGNAL_ALERT_RELOAD_REQUIRED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 5
    description = (
        'A new config file has been discovered for this node, a node '
        'reload is required to have the new configuration take affect.'
    )


SIGNAL_ALERT_RELOAD_REQUIRED = (
    _SIGNAL_ALERT_RELOAD_REQUIRED('NodeReloadRequired')
)


# noinspection PyPep8Naming
class _SIGNAL_ALERT_UNSUPPORTED_CONTROLLER(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
    """
    id = 6
    description = 'Unsupported controller error.'


SIGNAL_ALERT_UNSUPPORTED_CONTROLLER = (
    _SIGNAL_ALERT_UNSUPPORTED_CONTROLLER('UnsupportedController')
)


# noinspection PyPep8Naming
class _SIGNAL_ALERT_APPLICATION_STATUS_RETRY(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
    """
    id = 7
    description = (
        'The Application Status Command Class returned the message '
        '"Retry Later".'
    )


SIGNAL_ALERT_APPLICATION_STATUS_RETRY = (
    _SIGNAL_ALERT_APPLICATION_STATUS_RETRY('ApplicationStatusRetry')
)


# noinspection PyPep8Naming
class _SIGNAL_ALERT_APPLICATION_STATUS_QUEUED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
    """
    id = 8
    description = 'The command has been queued for later execution.'


SIGNAL_ALERT_APPLICATION_STATUS_QUEUED = (
    _SIGNAL_ALERT_APPLICATION_STATUS_QUEUED('ApplicationStatusQueued')
)


# noinspection PyPep8Naming
class _SIGNAL_ALERT_APPLICATION_STATUS_REJECTED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
    """
    id = 9
    description = 'The command was rejected.'


SIGNAL_ALERT_APPLICATION_STATUS_REJECTED = (
    _SIGNAL_ALERT_APPLICATION_STATUS_REJECTED('ApplicationStatusRejected')
)


# noinspection PyPep8Naming
class _SIGNAL_NODES_LOADED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * sleeping: `list` of :py:class:`libopenzwave.node.ZWaveNode`
        * dead: `list` of :py:class:`libopenzwave.node.ZWaveNode`
        * awake: `list` of :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 20
    description = 'Nodes have been loaded.'


SIGNAL_NODES_LOADED = _SIGNAL_NODES_LOADED('NodesLoaded')


# noinspection PyPep8Naming
class _SIGNAL_NODES_LOADED_SOME_DEAD(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * dead: list of :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 21
    description = 'Nodes have been loaded, some are dead.'


SIGNAL_NODES_LOADED_SOME_DEAD = (
    _SIGNAL_NODES_LOADED_SOME_DEAD('NodesLoadedSomeDead')
)


# noinspection PyPep8Naming
class _SIGNAL_NODES_LOADED_AWAKE(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * awake: list of :py:class:`libopenzwave.node.ZWaveNode`
        * sleeping:  list of :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 22
    description = 'Nodes have been loaded, some are sleeping.'


SIGNAL_NODES_LOADED_AWAKE = _SIGNAL_NODES_LOADED_AWAKE('NodesLoadedAwake')


# noinspection PyPep8Naming
class _SIGNAL_NODES_LOADED_ALL(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
    """
    id = 23
    description = 'All nodes have been loaded.'


SIGNAL_NODES_LOADED_ALL = _SIGNAL_NODES_LOADED_ALL('NodesLoadedAll')


# noinspection PyPep8Naming
class _SIGNAL_NETWORK_FAILED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
    """
    id = 24
    description = 'The network has failed'


SIGNAL_NETWORK_FAILED = _SIGNAL_NETWORK_FAILED('NetworkFailed')


# noinspection PyPep8Naming
class _SIGNAL_NETWORK_READY(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
    """
    id = 25
    description = 'Network is loaded.'


SIGNAL_NETWORK_READY = _SIGNAL_NETWORK_READY('NetworkReady')


# noinspection PyPep8Naming
class _SIGNAL_NETWORK_RESET(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
    """
    id = 26
    description = 'The network has been reset.'


SIGNAL_NETWORK_RESET = _SIGNAL_NETWORK_RESET('NetworkReset')


# noinspection PyPep8Naming
class _SIGNAL_NETWORK_STARTED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
    """
    id = 27
    description = 'The network is starting.'


SIGNAL_NETWORK_STARTED = _SIGNAL_NETWORK_STARTED('NetworkStarted')


# noinspection PyPep8Naming
class _SIGNAL_NETWORK_STOPPED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
    """
    id = 28
    description = 'The network has stopped.'


SIGNAL_NETWORK_STOPPED = _SIGNAL_NETWORK_STOPPED('NetworkStopped')


# noinspection PyPep8Naming
class _SIGNAL_USER_ALERTS(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
        * user_alert: one of :py:data:`libopenzwave.PyUserAlerts`
    """
    id = 29
    description = (
        'Warnings and Notifications Generated by the library that '
        'should be displayed to the user (eg, out of date config files)'
    )


SIGNAL_USER_ALERTS = _SIGNAL_USER_ALERTS('UserAlerts')


# noinspection PyPep8Naming
class _SIGNAL_NETWORK_MANUFACTURER_DB_READY(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
    """
    id = 30
    description = 'The manufacturer specific database is loaded.'


SIGNAL_NETWORK_MANUFACTURER_DB_READY = (
    _SIGNAL_NETWORK_MANUFACTURER_DB_READY('ManufacturerSpecificDBReady')
)


# noinspection PyPep8Naming
class _SIGNAL_NETWORK_CONTROLLER_COMMAND(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * state: :py:class:`libopenzwave.state.ZWaveState`
    """
    id = 31
    description = (
        'When controller commands are executed for the network, notifications '
        'of success/failure etc are communicated via this signal.'
    )


SIGNAL_NETWORK_CONTROLLER_COMMAND = (
    _SIGNAL_NETWORK_CONTROLLER_COMMAND('NetworkControllerCommand')
)


# noinspection PyPep8Naming
class _SIGNAL_NOTIFICATION(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: ZWaveNode or :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode` or no parameter
        * notification_code: one of :py:data:`libopenzwave.PyNotifications`
    """
    id = 32
    description = 'A manager notification report.'


SIGNAL_NOTIFICATION = _SIGNAL_NOTIFICATION('Notification')


# noinspection PyPep8Naming
class _SIGNAL_VALUE_ADDED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
        * value: :py:class:`libopenzwave.value.ZWaveValue`
        * value_data: :py:class:`object` with the following attributes

            * `id`
            * `command_class`
            * `index`
            * `genre`
            * `type`
            * `data`
            * `label`
            * `units`
            * `read_only`
    """
    id = 33
    description = 'Value added to a node.'


SIGNAL_VALUE_ADDED = (
    _SIGNAL_VALUE_ADDED('NodeValueAdded')
)


# noinspection PyPep8Naming
class _SIGNAL_VALUE_DATASET_LOADED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
        * value: :py:class:`libopenzwave.value.ZWaveValue`
        * value_data: :py:class:`object` with the following attributes

            * `id`
            * `command_class`
            * `index`
            * `genre`
            * `type`
            * `data`
            * `label`
            * `units`
            * `read_only`
    """
    id = 34
    description = 'Value loaded from database.'


SIGNAL_VALUE_DATASET_LOADED = (
    _SIGNAL_VALUE_DATASET_LOADED('NodeValueDatasetLoaded')
)


# noinspection PyPep8Naming
class _SIGNAL_VALUE_READY(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
        * value: :py:class:`libopenzwave.value.ZWaveValue`
        * value_data: :py:class:`object` with the following attributes

            * `id`
            * `command_class`
            * `index`
            * `genre`
            * `type`
            * `data`
            * `label`
            * `units`
            * `read_only`
    """
    id = 35
    description = 'Value data has been loaded.'


SIGNAL_VALUE_READY = _SIGNAL_VALUE_READY('NodeValueReady')


# noinspection PyPep8Naming
class _SIGNAL_VALUE_CHANGED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.value.ZWaveValue`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
        * value: :py:class:`libopenzwave.value.ZWaveValue`
        * value_data: :py:class:`object` with the following attributes

            * `id`
            * `command_class`
            * `index`
            * `genre`
            * `type`
            * `data`
            * `label`
            * `units`
            * `read_only`
    """
    id = 36
    description = 'Value data has changed.'


SIGNAL_VALUE_CHANGED = _SIGNAL_VALUE_CHANGED('NodeValueChanged')


# noinspection PyPep8Naming
class _SIGNAL_VALUE_REFRESHED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.value.ZWaveValue`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
        * value: :py:class:`libopenzwave.value.ZWaveValue`
        * value_data: :py:class:`object` with the following attributes

            * `id`
            * `command_class`
            * `index`
            * `genre`
            * `type`
            * `data`
            * `label`
            * `units`
            * `read_only`
    """
    id = 37
    description = 'Value data has been refreshed.'


SIGNAL_VALUE_REFRESHED = _SIGNAL_VALUE_REFRESHED('NodeValueRefreshed')


# noinspection PyPep8Naming
class _SIGNAL_VALUE_REMOVED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
        * value: :py:class:`libopenzwave.value.ZWaveValue`
        * value_data: :py:class:`object` with the following attributes

            * `id`
            * `command_class`
            * `index`
            * `genre`
            * `type`
            * `data`
            * `label`
            * `units`
            * `read_only`
    """
    id = 38
    description = 'Value has been removed'


SIGNAL_VALUE_REMOVED = _SIGNAL_VALUE_REMOVED('NodeValueRemoved')


# noinspection PyPep8Naming
class _SIGNAL_NODE_ADDED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node_id: `int`
    """
    id = 39
    description = 'A node has been added to the network.'


SIGNAL_NODE_ADDED = _SIGNAL_NODE_ADDED('NodeAdded')


# noinspection PyPep8Naming
class _SIGNAL_NODE_DATASET_LOADED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 40
    description = 'The node has been loaded from the database.'


SIGNAL_NODE_DATASET_LOADED = (
    _SIGNAL_NODE_DATASET_LOADED('NodeDatasetLoaded')
)


# noinspection PyPep8Naming
class _SIGNAL_NODE_NEW(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 41
    description = 'A New node has been discovered on the network.'


SIGNAL_NODE_NEW = _SIGNAL_NODE_NEW('NodeNew')


# noinspection PyPep8Naming
class _SIGNAL_NODE_LOADING_ESSENTIAL(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 42
    description = 'The loading of essential node information has finished.'


SIGNAL_NODE_LOADING_ESSENTIAL = (
    _SIGNAL_NODE_LOADING_ESSENTIAL('NodeLoadingEssential')
)


# noinspection PyPep8Naming
class _SIGNAL_NODE_READY(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 43
    description = 'A node is no longer running from cached data.'


SIGNAL_NODE_READY = _SIGNAL_NODE_READY('NodeReady')


# noinspection PyPep8Naming
class _SIGNAL_NODE_REMOVED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 44
    description = 'A node has been removed from the network.'


SIGNAL_NODE_REMOVED = _SIGNAL_NODE_REMOVED('NodeRemoved')


# noinspection PyPep8Naming
class _SIGNAL_NODE_RESET(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 45
    description = 'A node has been reset, reloading node values.'


SIGNAL_NODE_RESET = _SIGNAL_NODE_RESET('NodeReset')


# noinspection PyPep8Naming
class _SIGNAL_NODE_BUTTON_OFF(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 46
    description = 'Handheld controller button off pressed event.'


SIGNAL_NODE_BUTTON_OFF = _SIGNAL_NODE_BUTTON_OFF('ButtonOff')


# noinspection PyPep8Naming
class _SIGNAL_NODE_BUTTON_ON(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 47
    description = 'Handheld controller button on pressed event.'


SIGNAL_NODE_BUTTON_ON = _SIGNAL_NODE_BUTTON_ON('ButtonOn')


# noinspection PyPep8Naming
class _SIGNAL_NODE_CREATE_BUTTON(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 48
    description = 'Handheld controller button event created.'


SIGNAL_NODE_CREATE_BUTTON = _SIGNAL_NODE_CREATE_BUTTON('CreateButton')


# noinspection PyPep8Naming
class _SIGNAL_NODE_DELETE_BUTTON(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 49
    description = 'Handheld controller button event deleted.'


SIGNAL_NODE_DELETE_BUTTON = _SIGNAL_NODE_DELETE_BUTTON('DeleteButton')


# noinspection PyPep8Naming
class _SIGNAL_NODE_ASSOCIATION_GROUP(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
        * group:
          :py:class:`libopenzwave.association_group.ZWaveAssociationGroup`
    """
    id = 50
    description = (
        'The associations for a node have changed. '
        'The application should rebuild any group '
        'information it holds about the node.'
    )


SIGNAL_NODE_ASSOCIATION_GROUP = _SIGNAL_NODE_ASSOCIATION_GROUP('Group')


# noinspection PyPep8Naming
class _SIGNAL_NODE_CONTROLLER_COMMAND(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
        * state: :py:class:`libopenzwave.state.ZWaveState`
    """
    id = 51
    description = (
        'When controller commands are executed for a node, notifications '
        'of success/failure etc are communicated via this signal.'
    )


SIGNAL_NODE_CONTROLLER_COMMAND = (
    _SIGNAL_NODE_CONTROLLER_COMMAND('NodeControllerCommand')
)


# noinspection PyPep8Naming
class _SIGNAL_NODE_POLLING_DISABLED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 52
    description = 'Polling of a node has been successfully turned off.'


SIGNAL_NODE_POLLING_DISABLED = _SIGNAL_NODE_POLLING_DISABLED('PollingDisabled')


# noinspection PyPep8Naming
class _SIGNAL_NODE_POLLING_ENABLED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 53
    description = 'Polling of a node has been successfully turned on.'


SIGNAL_NODE_POLLING_ENABLED = _SIGNAL_NODE_POLLING_ENABLED('PollingEnabled')


# noinspection PyPep8Naming
class _SIGNAL_NODE_EVENT(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
        * event: ???
    """
    id = 54
    description = (
        'A node has triggered an event. This is commonly caused '
        'when a node sends a Basic_Set command to the controller. '
        'The event value is stored in the notification.'
    )


SIGNAL_NODE_EVENT = _SIGNAL_NODE_EVENT('NodeEvent')


# noinspection PyPep8Naming
class _SIGNAL_NODE_NAMING(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 55
    description = (
        'One of the node names has changed (name, manufacturer, product).'
    )


SIGNAL_NODE_NAMING = _SIGNAL_NODE_NAMING('NodeNaming')


# noinspection PyPep8Naming
class _SIGNAL_NODE_PROTOCOL_INFO(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 56
    description = (
        'Basic node information has been received, such as whether the node '
        'is a listening device, a routing device and its baud rate and basic, '
        'generic and specific types. It is after this notification that you '
        'can call Manager::GetNodeType to obtain a label containing the '
        'device description.'
    )


SIGNAL_NODE_PROTOCOL_INFO = _SIGNAL_NODE_PROTOCOL_INFO('NodeProtocolInfo')


# noinspection PyPep8Naming
class _SIGNAL_MSG_COMPLETE(Signal):
    id = 57
    description = ''


SIGNAL_MSG_COMPLETE = _SIGNAL_MSG_COMPLETE('MsgComplete')


# noinspection PyPep8Naming
class _SIGNAL_NETWORK_DATASET_LOADED(Signal):
    id = 58
    description = ''


SIGNAL_NETWORK_DATASET_LOADED = (
    _SIGNAL_NETWORK_DATASET_LOADED('NetworkDatasetLoaded')
)


# noinspection PyPep8Naming
class _SIGNAL_VIRTUAL_NODE_READY(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`,
          :py:class:`libopenzwave.network.ZWaveNetwork`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 59
    description = (
        'A virtual node is ready for use. The virtual nodes represent '
        'endpoints on a multichannel node.'
    )


SIGNAL_VIRTUAL_NODE_READY = _SIGNAL_VIRTUAL_NODE_READY('VirtualNodeReady')


# noinspection PyPep8Naming
class _SIGNAL_VIRTUAL_NODE_REMOVED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 60
    description = (
        'A virtual Node has been removed.'
    )


SIGNAL_VIRTUAL_NODE_REMOVED = _SIGNAL_VIRTUAL_NODE_REMOVED('VirtualNodeRemoved')


# noinspection PyPep8Naming
class _SIGNAL_VIRTUAL_NODE_DATASET_LOADED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 61
    description = (
        'A Virtual Node has been created from the database. It is not yet '
        'known if the node actually exists.'
    )


SIGNAL_VIRTUAL_NODE_DATASET_LOADED = (
    _SIGNAL_VIRTUAL_NODE_DATASET_LOADED('VirtualNodeDatasetLoaded')
)


# noinspection PyPep8Naming
class _SIGNAL_VIRTUAL_NODE_ADDED(Signal):
    """
    Callbacks are passed these keyword arguments:

        * sender: :py:class:`libopenzwave.node.ZWaveNode`
        * network: :py:class:`libopenzwave.network.ZWaveNetwork`
        * controller: :py:class:`libopenzwave.controller.ZWaveController`
        * node: :py:class:`libopenzwave.node.ZWaveNode`
    """
    id = 62
    description = (
        'A virtual node has been added'
    )


SIGNAL_VIRTUAL_NODE_ADDED = _SIGNAL_VIRTUAL_NODE_ADDED('VirtualNodeAdded')
