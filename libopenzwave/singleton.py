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
:synopsis: Instance Singleton Meta Class

.. moduleauthor:: Kevin G Schlosser
"""

import os
import sys

# this is a replacement method for all of the classes that have a destroy
# method.
# This is to remove the instance from the instance singleton list.

# this is a very experimental setting. What this setting does is
# if you subclass any of the ZWave* classes instead of the parent class
# getting constructed by the program the subclass will get constructed instead.
# This makes it easier to perform operations for specific objects.
# This needs to be set to True in order for the plugins to work. You will need
# to make your plugin imports the first thing. All you have to do is import
# the plugins and nothing more. the plugins will subclass what it needs to
# and the process of doing this will swap out the originals for the subclassed
# versions This will make it so that multiple plugins can be loaded

REPLACE_ZWAVE_CLASSES_WITH_SUBCLASSES = False


# noinspection PyProtectedMember
def _destroy(self):
    if hasattr(self, '__instance_key__'):
        if self.__instance_key__ in self.__class__._instances:
            del self.__class__._instances[self.__instance_key__]

    self.__original_destroy__()


BASE_PATH = os.path.dirname(__file__)

_ZWAVE_MODULES = []
_ORIGINAL_ZWAVE_CLASSES = []
_REPLACED_ZWAVE_CLASSES = []
OZW_MOD_NAME = __name__.rsplit('.', 1)[0]
CC_MOD_NAME = OZW_MOD_NAME + '.command_classes'
BASE_MODULE = os.path.split(BASE_PATH)[-1]


def build_module_list(path):
    """
    :param path:
    """
    head, tail = os.path.split(path)
    mod = tail
    while not mod.startswith(BASE_MODULE):
        head, tail = os.path.split(head)
        mod = tail + '.' + mod

    for f in os.listdir(path):
        if f == 'plugins':
            continue

        if f.endswith('.py') and '__init__' not in f:
            _ZWAVE_MODULES.append(mod + '.' + f.rstrip('.py'))

        elif os.path.isdir(os.path.join(path, f)):
            build_module_list(os.path.join(path, f))


build_module_list(BASE_PATH)


class InstanceSingleton(type):
    """
    InstanceSingleton metaclass

    child = class that contains this class as a metaclass
    parent = this class

    This class gets used on 2 different occasions.
    The first occasion is when the child class gets compiled. we are able to
    get in front of that compilation because this classes `__init__` gets
    called first. We use that to set a class level variable, `_instances`.
    This variable gets created for every child of this class. The variables
    are not connected to any other child classes. so they are unique. The
    variable is a dict that holds all of the unique instances of that
    child class.

    The second time in which this class gets used is when one of the child
    classes gets constructed. the `__call__` method of this class gets called
    before the `__init__`. the `__call__` method is supposed to return a new
    instance. We do not want to do this is one already exists. So when a new
    instance is supposed to be created we use the `__call__` method to check
    for the existence of an instance. If it does not exist we create a new
    instance, if it does exist we return the already created one.

    How we are able to check if an instance already exists is actually pretty
    crafty. I use the args and kwargs that are passed when the construction of
    a new instance is supposed to take place. I iterate over a sorted list of
    the keys in kwargs and add the values to the args creating a tuple of all
    of the arguments that have been passed. A python dict is able to use a
    tuple as a key. For our use this key will be unique because each class
    that uses this metaclass makes use of an object_id.

    This is a pretty neat spin on making singletons. Singletons are typically
    used so that only a single instance of a class can exist. Our need is to
    make sure that only a single instance of a ZWave object exists, whether it
    be a node, value, controller, network, or options.

    If this library is used on multiple ZSticks at the same time the
    ZWaveOptions class is going to have to have 2 different locations supplied
    for it's user config data. For the ZWaveNetwork class an instance of
    ZWaveOptions has to be passed. and since that has to be unique it now makes
    the ZWaveNetwork instance unique. and the ZWaveNetwork instance has to be
    used on all other classes. it's a domino effect.
    """

    def __init__(cls, name, bases, dct):
        """
        InstanceSingleton metaclass constructor.

        :param name:
        :param bases:
        :param dct:
        """
        super(InstanceSingleton, cls).__init__(name, bases, dct)

        if (
            OZW_MOD_NAME in cls.__module__ and
            OZW_MOD_NAME + '.plugins' not in cls.__module__
        ):
            if not hasattr(cls, '_instances'):
                cls._instances = {}

            if (
                hasattr(cls, 'destroy') and
                not hasattr(cls, '__original_destroy__')
            ):
                setattr(cls, '__original_destroy__', cls.destroy)
                cls.destroy = _destroy

            _ORIGINAL_ZWAVE_CLASSES.append(cls)
            _REPLACED_ZWAVE_CLASSES.append(cls)
            cls.__openzwave_module__ = cls.__module__
            cls.__openzwave_name__ = cls.__name__

        else:
            for base in bases:
                if base in _REPLACED_ZWAVE_CLASSES:
                    _REPLACED_ZWAVE_CLASSES.remove(base)
                    _REPLACED_ZWAVE_CLASSES.append(cls)
                else:
                    continue

                cls.__openzwave_module__ = base.__openzwave_module__
                cls.__openzwave_name__ = base.__name__

                setattr(
                    sys.modules[base.__openzwave_module__],
                    base.__openzwave_name__,
                    cls
                )

                if CC_MOD_NAME in base.__openzwave_module__:
                    mod = sys.modules[CC_MOD_NAME]
                else:
                    mod = sys.modules[OZW_MOD_NAME]

                for item in dir(mod):
                    value = getattr(mod, item)

                    if value == base:
                        setattr(mod, item, cls)
                        mod.__dict__[item] = cls
                break

    # noinspection PyProtectedMember
    def __call__(cls, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """

        if cls.__openzwave_module__ == CC_MOD_NAME:
            return super(InstanceSingleton, cls).__call__(*args, **kwargs)

        from .node import ZWaveNode
        from .controller import ZWaveController
        from .option import ZWaveOption
        from .network import ZWaveNetwork

        if cls in (ZWaveNode, ZWaveController):
            node_id = kwargs.pop('id', None)
            network = kwargs.pop('network', None)
            args = list(args)

            if node_id is None:
                node_id = args.pop(0)

            if network is None:
                network = args.pop(0)

            if 'xml_data' in kwargs:
                xml_data = kwargs.pop('xml_data')
            else:
                xml_data = args.pop(0)

            key = (node_id, network)

            if key in cls._instances:
                return cls._instances[key]

            from .command_classes import COMMAND_CLASSES

            # we need to set the bases of the node. ZWaveNode being the
            # primary parent class.
            bases = set()

            # we then make a call to the network manager to get the
            # command classes the node supports.

            n_id = int(node_id.split('.')[0])
            if xml_data is None:
                command_class_ids = network.manager.getNodeClassIds(
                    network.home_id,
                    n_id,
                )

            else:
                command_class_ids = []

                for command_class in xml_data.CommandClasses:
                    command_class_ids += [int(command_class['id'], 16)]

            if cls == ZWaveController:
                for cc in (
                    COMMAND_CLASSES['COMMAND_CLASS_CONFIGURATION'],
                    COMMAND_CLASSES['COMMAND_CLASS_BASIC'],
                    COMMAND_CLASSES['COMMAND_CLASS_MANUFACTURER_SPECIFIC']
                ):
                    if cc.class_id not in command_class_ids:
                        command_class_ids += [cc.class_id]

            # see if a python command class id is in the list returned for
            # the node. If it is in the list then add the class to the bases.

            for class_id in command_class_ids:
                bases.add(COMMAND_CLASSES[class_id])

            # we need to supply a custom __init__ to our dynamically
            # created class in order to properly start all of the parent
            # classes

            # noinspection PyShadowingBuiltins

            # we use type to make the new class supplying it with the
            # custom __init__ and the bases. the __init__ iterates through
            # the bases and calls the constructor for each of them. at the
            # time each base class is constructed if it is a command class
            # it adds it's id to _cls_ids. this is done so we can use
            # equality testing to identify if a node supports a specific
            # command class.

            # as an example. if we wanted to turn on a light switch
            # if node == command_class.COMMAND_CLASS_BINARY_SWITCH:
            #     node.state = True

            # I found this to be a much better mechanism for testing node
            # types then having to add a method to ZWaveNode to check.
            # not to mention having ZWaveNode contain all the various
            # properties and methods for all command classes can get a wee
            # bit difficult to follow. So if a node is not a binary switch
            # then it is not going to have the property state. it removes
            # any checking that would need to be done inside of the
            # property/method to ensure the node is the proper type

            # this same equality testing also works on the values. It's a
            # simple to use mechanism. the equality test is only performed
            # against the command classes of a node/value if the object
            # passed is an int, if testing 2 nodes it will check to see if
            # the networks and ids match. because of the use of the
            # singleton only a single node instance on a network can exist

            bases = tuple(base for base in bases)

            def __init__(self, id, net, xml, *a, **k):
                self._bases = bases
                cls.__init__(self, id, net, xml, *a, **k)
                self.__name__ = 'ZWaveNode'

                class_ids = []
                for cmd_cls in self._bases:
                    class_ids += [cmd_cls.class_id]
                    cmd_cls.__init__(self)

                self._command_classes = class_ids[:]

            def __repr__(self):
                output = object.__repr__(self)
                output.replace('ZWaveNode', 'Dynamic_ZWaveNode')
                return output

            zwave_node = type(
                'ZWaveNode',
                (cls,) + bases,
                {
                    '__init__':   __init__,
                    '__repr__':   __repr__,
                    '__module__': ZWaveNode.__module__
                }
            )

            instance = zwave_node(node_id, network, xml_data, *args, **kwargs)
            instance.__instance_key__ = key

            cls._instances[key] = instance
            return cls._instances[key]

        elif cls == ZWaveOption:
            instance = super(InstanceSingleton, cls).__call__(*args, **kwargs)

            device = instance._device
            config_path = instance._config_path
            user_path = instance._user_path
            cmd_line = instance._cmd_line

            key = (device, config_path, user_path, cmd_line)
            if key not in cls._instances:
                instance.__instance_key__ = key
                instance.create()
                cls._instances[key] = instance

            return cls._instances[key]

        elif cls == ZWaveNetwork:
            instance = super(InstanceSingleton, cls).__call__(*args, **kwargs)

            options = instance._options
            auto_start = instance._auto_start

            key = (options, auto_start)

            if key not in cls._instances:
                instance.__instance_key__ = key
                cls._instances[key] = instance
                if auto_start:
                    instance.start()

            return cls._instances[key]
        
        else:
            key = args
            for k in sorted(kwargs.keys()):
                key += (kwargs[k],)
            if key:
                if key not in cls._instances:
                    instance = (
                        super(InstanceSingleton, cls).__call__(*args, **kwargs)
                    )
                    instance.__instance_key__ = key

                    cls._instances[key] = instance
                return cls._instances[key]
            else:
                return super(InstanceSingleton, cls).__call__(*args, **kwargs)


def subclass_zwave_class(*sub_classes):
    """
    This is a decorator that allows you to subclass the ZWave classes.

    The purpose to subclassing the ZWave classes is so that you are able to inject application code into the dynamic
    creation of the various python representations of zwave nodes, networks, values.... etc...

    This would mainly be used on the ZWaveNode, ZWaveNetwork and any of the classes in the
    openzwave.command_classes module.

    The reason why this decorator is needed is in Python 3 metaclasses are no longer stored in __metaclass__ and the
    metaclasses get check before type.__new__ ever gets called. To avoid metaclass conflicts we need to create a
    subclass of all of the metaclass bases. and we do this by calling type() on each of the parent classes passed
    to this decorator. Once the new metaclass has been built we use that metaclass to construct the new class
    that is decorated.

    In an ideal world this would not be needed But to avoid any complications this decorator MUST be used.
    You want to place the ZWave cklass you want to subclass as the first parameter. any additional classes that are
    not from openzwave can be added by supplying additional classes after the ZWave class

    Only ZWave classes that have a metaclass of :py:class:`libopenzwave.singleton.InstanceSingleton' can be subclassed
    using this decorator.

    One other thing. because the class being created is going to be used in the dynamic creation of other ZWave objects
    Your code is not is what is going to get used when the instance gets constructed. so you will have no control
    over the arguements passed to __init__. In order for this to work properly you will need to keep the parameters
    the same as what the parent class is. so it is always bets to use *args, **kwargs and pass those parameters when
    calling the parent classes __init__ method...

    :param *sub_classes: positional arguments each arguement would be a class that you want to subclass.
        The first argument MUST be a ZWave class that has a metaclass of openzwave.singleton.InstanceSingleton.
        all other arguments can be fill with additional classes that are to be subclassed.

    :return: dynamically assembled class

    :raises TypeError: if none of the classes supplied have a metaclass of openzwave.singleton.InstanceSingleton
    """
    meta_classes = []

    for sub_cls in sub_classes:
        if type(sub_cls) == InstanceSingleton and InstanceSingleton in meta_classes:
            raise TypeError('Only one ZWave class is allowed to be a parent class.')

        if type(sub_cls) not in meta_classes and type(sub_cls) != type:
            meta_classes += [type(sub_cls)]

    if InstanceSingleton not in meta_classes:
        raise TypeError(
            'This decorator is only to be used on ZWave classes that '
            'have a metaclass of openzwave.singleton.InstanceSingleton'
        )

    meta_classes.remove(InstanceSingleton)
    meta_classes.insert(0, InstanceSingleton)

    def _class_wrapper(cls):
        dct = {key: value for key, value in cls.__dict__.items()}

        if meta_classes:
            mcls = type(''.join(c.__name__ for c in meta_classes), tuple(meta_classes), {})
            return mcls(cls.__name__, sub_classes, dct)
        else:
            return type(
                cls.__name__,
                sub_classes,
                dct
            )

    return _class_wrapper
