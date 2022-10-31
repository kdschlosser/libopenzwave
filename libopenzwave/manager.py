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
:synopsis: wrapper for :py:class:`libopenzwave.PyManager`

.. moduleauthor:: Kevin G Schlosser
"""

import _libopenzwave
import os
import inspect
import traceback
import logging

from . import utils
from .command_classes import COMMAND_CLASSES


COMMAND_CLASS_IDS = list(
    cls.class_id for cls in COMMAND_CLASSES
    if cls.class_id <= 255
)

logger = logging.getLogger(__name__)

if 'MAKE_IDE_HAPPY' in os.environ:
    # This is here to make an IDE happy. It never actually gets run.
    ZWaveManager = _libopenzwave.PyManager

else:

    class MethodWrapper(object):
        """
        Wrapper for libopenzwave.PyManager methods.
        """

        def __init__(self, method):
            """
            :param method:
            :type method: callable
            """
            self.__dict__.update(method.__dict__)
            self.__method = method
            self.__call__ = self.__call

        def __call(self, *args, **kwargs):
            """
            :param *args:
            :param **kwargs:
            """
            try:
                res = self.__method(*args, **kwargs)
                return res
            except:  # NOQA
                logger.error(traceback.format_exc())

    # noinspection PyPep8Naming
    class ZWaveManager(object):
        """
        Wrapper around libopenzwave.PyManager.

        Exceptions that bubble up in OpenZWave was added in version 1.6. So
        to keep the program from stalling this wrapper makes it easier to
        handle the exception catching and logging.
        """
        def __init__(self, network):
            """
            :param network:
            :type network: ZWaveNetwork
            """
            self.__network = network
            self.__server = None
            self.__callback = None

            if network.options._local_connection:  # NOQA
                self.__manager = _libopenzwave.PyManager()

            else:
                pseudo_manager = PseudoManager(network)

                self.__manager = None
                self.__class__.__getattr__ = pseudo_manager.__getattr__
                self.addWatcher = pseudo_manager.addWatcher
                self.addDriver = pseudo_manager.addDriver
                self.removeWatcher = pseudo_manager.removeWatcher
                self.removeDriver = pseudo_manager.removeDriver
                self.create = pseudo_manager.create
                self.getNodeClassIds = pseudo_manager.getNodeClassIds

        def __getattr__(self, item):
            """
            :param item:
            """
            if item in self.__dict__:
                return self.__dict__[item]

            if hasattr(self.__manager, item):
                attr = getattr(self.__manager, item)

                if inspect.ismethod(attr) or inspect.isfunction(attr):
                    self.__dict__[item] = wrapper = MethodWrapper(attr)
                    return wrapper

                return attr

            raise AttributeError(item)

        def is_alive(self):
            """
            :rtype: bool
            """
            if self.__server is None:
                return False

            return self.__server.is_alive

        @utils.logit
        def getNodeClassIds(self, home_id, node_id):
            """
            :param home_id:
            :type home_id: int

            :param node_id:
            :type node_id: int

            :rtype: List[int]
            """
            cls_ids = []

            for cls_id in COMMAND_CLASS_IDS:
                if self.getNodeClassInformation(home_id, node_id, cls_id):
                    cls_ids += [cls_id]

            return cls_ids

        def addDriver(self, driver):
            """
            :param driver:
            """
            options = self.__network.options

            if self.__network.options.use_server:
                from .server import Server

                cert_check = (
                    options.ssl_key_path,
                    options.ssl_server_cert_path,
                    options.ssl_client_cert_path
                )

                if (
                    cert_check != (None, None, None) and
                    None in cert_check
                ):
                    raise RuntimeError(
                        'To use SSL you need to provide\n'
                        'cert key path\n'
                        'client cert path\n'
                        'server cert path'
                    )

                if options.admin_password is None:
                    raise RuntimeError(
                        'You need to supply a server password using\n'
                        'ZWaveOption.admin_password = password'
                    )

                self.__server = Server(
                    options.server_ip,
                    options.server_port,
                    options.admin_password,
                    options.ssl_key_path,
                    options.ssl_server_cert_path,
                    options.ssl_client_cert_path
                )

                self.__server.start(self.__network)

            self.__manager.addDriver(driver)

        def addWatcher(self, callback):
            """
            :param callback:
            :type callback: callable
            """
            if self.__server is not None:
                self.__callback = callback

                def notif_callback(notif):
                    self.__callback(notif)
                    self.__server.send(notif)

                self.__manager.addWatcher(notif_callback)
            else:
                self.__manager.addWatcher(callback)

        def removeWatcher(self, callback):
            """
            :param callback:
            :type callback: callable
            """
            if self.__callback is not None:
                self.__manager.removeWatcher(self.__callback)
                self.__callback = None
            else:
                self.__manager.removeWatcher(callback)

        def removeDriver(self, driver):
            """
            :param driver:
            """
            if self.__server is not None:
                self.__server.stop()

            self.__manager.removeDriver(driver)


class PseudoMethod(object):

    def __init__(self, method_name, client):
        self.__method_name = method_name
        self.__client = client
        self.__name__ = method_name

    @utils.logit
    def __call__(self, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """

        data = dict(
            func=self.__method_name,
            args=args,
            kwargs=kwargs
        )
        res = self.__client.send(data)
        return res


# noinspection PyPep8Naming
class PseudoManager(object):

    def __init__(self, network):
        """
        :param network:
        :type network: ZWaveNetwork
        """
        self.__network = network
        self.__client = None

    def __getattr__(self, item):
        """
        :param item:
        :type item: str
        """
        if item in self.__dict__:
            return self.__dict__[item]

        if item in _libopenzwave.PyManager.__dict__:
            attr = _libopenzwave.PyManager.__dict__[item]
            if hasattr(attr, '__call__'):
                self.__dict__[item] = PseudoMethod(item, self.__client)

                return self.__dict__[item]
            return attr

        raise AttributeError(item)

    def addDriver(self, _):
        """
        :param _:
        """
        options = self.__network.options
        from .client import Client

        host, port = options.device.split(':')
        port = int(port)

        cert_check = (
            options.ssl_key_path,
            options.ssl_server_cert_path,
            options.ssl_client_cert_path
        )

        if (
            cert_check != (None, None, None) and
            None in cert_check
        ):
            raise RuntimeError(
                'To use SSL you need to provide\n'
                'cert key path\n'
                'client cert path\n'
                'server cert path'
            )

        if options.admin_password is None:
            raise RuntimeError(
                'You need to supply a client password using\n'
                'ZWaveOption.admin_password = password.\n'
                'This password must match what is set on the remote server'
            )

        self.__client = Client(
            host,
            port,
            options.admin_password,
            options.ssl_key_path,
            options.ssl_server_cert_path,
            options.ssl_client_cert_path
        )
        self.__client.start(self.__network)

    def addWatcher(self, _):
        """
        :param _:
        """
        pass

    def removeWatcher(self, _):
        """
        :param _:
        """
        pass

    def removeDriver(self, _):
        """
        :param _:
        """
        self.__client.stop()

    def create(self):
        pass

    @utils.logit
    def getNodeClassIds(self, *args, **kwargs):
        """
        :param *args:
        :param **kwargs:
        """
        data = dict(
            func='getNodeClassIds',
            args=args,
            kwargs=kwargs
        )
        result = self.__client.send(data)
        return result
