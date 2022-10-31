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
:synopsis: Socket server

.. moduleauthor:: Kevin G Schlosser
"""

import ssl
import json
import logging
from .remote_encryption import AESCipher
from .import utils
import socket
import threading
import time
from uuid import uuid4

try:
    pickle = __import__('cPickle')
except ImportError:
    import pickle


logger = logging.getLogger(__name__)


class Server(object):
    """
    TODO: server.Server class Docstring
    """

    def __init__(self, host, port, password, key, server_cert, client_cert):
        self.clients = []
        self.key = key
        self.server_cert = server_cert
        self.client_cert = client_cert
        self.__aes = AESCipher(password)
        self.password = password
        self.__client = None
        self.network = None
        self.port = port
        self.host = host
        self.socket = None
        self.event = threading.Event()
        self.thread = None
        self.client = None
        self.message_cache = {}
        self.cache_lock = threading.Lock()
        self.client_address = ''
        self.watchdog_timer = 0

    @property
    def is_alive(self):
        """
        TODO: server.Server.is_alive docstring
        :return:
        """
        if self.thread is None or not self.thread.is_alive():
            return False

        return time.time() - self.watchdog_timer <= 30

    def start(self, network):
        """
        TODO: server.Server.start docstring
        """
        if self.thread is None:
            logger.info('starting server: ' + self.host + ':' + str(self.port))
            self.network = network
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def run(self):
        """
        TODO: server.Server.run docstring
        """
        while not self.event.is_set():
            self.watchdog_timer = time.time()
            try:
                client, client_address = self.socket.accept()

                client.settimeout(5.0)
                if None not in (
                    self.key,
                    self.server_cert,
                    self.client_cert
                ):

                    client = ssl.wrap_socket(
                        client,
                        server_side=True,
                        ca_certs=self.client_cert,
                        certfile=self.server_cert,
                        keyfile=self.key,
                        cert_reqs=ssl.CERT_REQUIRED,
                        ssl_version=ssl.PROTOCOL_TLSv1_2
                    )

                self.client = client
                self.client_address = client_address[0]

                logger.info('client connected: ' + self.client_address)
                self.new_client()

                data = ''
                while True:
                    self.watchdog_timer = time.time()
                    try:
                        new_data = client.recv(8192)
                    except socket.timeout:
                        with self.cache_lock:
                            for id_, (message, timestamp) in list(
                                self.message_cache.items()
                            )[:]:
                                if time.time() - timestamp >= 5:
                                    client.send(message)
                                    self.message_cache[id_] = (
                                        message,
                                        time.time()
                                    )
                        continue
                    except socket.error:
                        break

                    if not new_data:
                        break

                    data += new_data

                    while '\n' in data:
                        message, data = data.split('\n', 1)
                        message = json.loads(message)

                        if 'resend' in message:
                            # noinspection PyShadowingBuiltins
                            id = message['resend']
                            with self.cache_lock:
                                if id in self.message_cache:
                                    resend_message = self.message_cache[id][0]
                                    client.send(resend_message)
                                    self.message_cache[id] = (
                                        resend_message,
                                        time.time()
                                    )

                        elif 'ok' in message:
                            # noinspection PyShadowingBuiltins
                            id = message['ok']
                            with self.cache_lock:
                                if id in self.message_cache:
                                    del self.message_cache[id]
                        else:
                            # noinspection PyShadowingBuiltins
                            id = message['id']
                            contents = message['contents']

                            # noinspection PyPep8
                            try:
                                contents = self.__aes.decrypt(contents)
                                message = json.loads(contents)
                                client.send(json.dumps(dict(ok=id)) + '\n')
                            except:  # NOQA
                                logger.debug(
                                    'bad message from client. '
                                    'requesting retransmit. {0}'.format(id)
                                )
                                client.send(json.dumps(dict(resend=id)) + '\n')
                                continue

                            output = json.dumps(message, indent=4).split('\n')
                            output = '\n'.join(
                                '    ' + line for line in output
                            )

                            logger.debug(
                                'incoming message ({0}): \n{1}'.format(
                                    self.client_address,
                                    output
                                )
                            )

                            message_id = str(uuid4())

                            # noinspection PyPep8
                            try:
                                func = getattr(
                                    self.network.manager, message['func']
                                )
                                res = func(
                                    *message['args'],
                                    **message['kwargs']
                                )

                            except:  # NOQA
                                import traceback
                                logging.error(traceback.format_exc())

                                res = None

                            res = pickle.dumps(res, 2).decode('ISO-8859-1')

                            contents = dict(id=message['id'], result=res)
                            contents = self.__aes.encrypt(json.dumps(contents))

                            res = dict(id=message_id, contents=contents)
                            res = json.dumps(res) + '\n'

                            with self.cache_lock:
                                self.message_cache[message_id] = (
                                    res,
                                    time.time()
                                )

                            client.send(res)

                try:
                    client.close()
                except socket.error:
                    pass

                logger.info('client disconnected: ' + self.client_address)

                self.client_address = ''
                self.client = None

            except socket.timeout:
                continue

            except socket.error:
                import traceback
                traceback.print_exc()
                break

        try:
            self.socket.close()
        except socket.error:
            pass

        self.client_address = ''
        self.client = None
        self.socket = None
        self.thread = None
        logger.info('server stopped')

    def stop(self):
        """
        TODO: server.Server.stop docstring
        """
        logger.info('stopping server: {0}:{1}'.format(self.host, self.port))
        self.event.set()

        if self.socket is not None:
            self.socket.shutdown(socket.SHUT_RDWR)

            try:
                self.socket.close()
            except socket.error:
                pass

        if self.thread is not None and self.thread.is_alive():
            self.thread.join()

    @utils.logit
    def send(self, n):
        """
        TODO: server.Server.send docstring
        """
        if self.client is not None:
            message_id = str(uuid4())

            data = dict(notification=pickle.dumps(n, 2).decode('ISO-8859-1'))
            data = self.__aes.encrypt(json.dumps(data))

            message = json.dumps(dict(id=message_id, contents=data)) + '\n'

            try:
                self.client.send(message)
                with self.cache_lock:
                    self.message_cache[message_id] = (message, time.time())

                return message_id
            except socket.error:
                pass

    def new_client(self):
        """
        TODO: server.Server.new_client docstring
        """

        # noinspection PyArgumentList
        @utils.logit
        def _do():

            try:
                if self.network.controller is None:
                    return

                def send_notif(n):
                    message_id = self.send(n)

                    if message_id is None:
                        return False

                    return True

                from _libopenzwave import (
                    PyNotifications,
                    Value,
                    ZWaveNotification,
                    PyNotificationCodes
                )

                notif = ZWaveNotification(
                    PyNotifications.DriverReady,
                    self.network.home_id,
                    self.network.controller.id
                )

                if not send_notif(notif):
                    return

                notif = ZWaveNotification(
                    PyNotifications.ManufacturerSpecificDBReady,
                    self.network.home_id,
                    0
                )
                if not send_notif(notif):
                    return

                sleeping_nodes = False
                dead_nodes = False

                for node in self.network:
                    logger.debug('NUM_VALUES: ' + str(len(list(node))))

                for node_id in sorted(list(self.network.nodes.keys())[:]):
                    node = self.network.nodes[node_id]

                    notif = ZWaveNotification(
                        PyNotifications.NodeAdded,
                        self.network.home_id,
                        node_id
                    )
                    if not send_notif(notif):
                        return

                    notif = ZWaveNotification(
                        PyNotifications.NodeProtocolInfo,
                        self.network.home_id,
                        node_id
                    )
                    if not send_notif(notif):
                        return

                    notif = ZWaveNotification(
                        PyNotifications.EssentialNodeQueriesComplete,
                        self.network.home_id,
                        node_id
                    )
                    if not send_notif(notif):
                        return

                    for value in node:
                        notif = ZWaveNotification(
                            PyNotifications.ValueAdded,
                            self.network.home_id,
                            node_id
                        )

                        notif.value = Value(value.id)
                        notif.value.command_class = (
                            value.command_class.class_id
                        )
                        notif.value.instance = value.instance
                        notif.value.index = value.index
                        notif.value.genre = value.genre
                        notif.value.type = value.type
                        notif.value.data = value.data
                        notif.value.label = value.label
                        notif.value.units = value.units
                        notif.value.is_read_only = value.is_read_only

                        if not send_notif(notif):
                            return

                    if node.is_ready:
                        notif = ZWaveNotification(
                            PyNotifications.NodeNaming,
                            self.network.home_id,
                            node_id
                        )
                        if not send_notif(notif):
                            return

                        if node_id != self.network.controller.id:
                            notif = ZWaveNotification(
                                PyNotifications.Notification,
                                self.network.home_id,
                                node_id
                            )
                            notif.notification_code = (
                                PyNotificationCodes.NoOperation
                            )

                            if not send_notif(notif):
                                return

                        notif = ZWaveNotification(
                            PyNotifications.NodeQueriesComplete,
                            self.network.home_id,
                            node_id
                        )
                        if not send_notif(notif):
                            return

                    if node.is_sleeping:
                        sleeping_nodes = True

                    if node.is_failed:
                        dead_nodes = True

                if self.network.state == self.network.STATE_READY:
                    if dead_nodes:
                        notif = ZWaveNotification(
                            PyNotifications.AllNodesQueriedSomeDead,
                            self.network.home_id,
                            0
                        )

                    elif sleeping_nodes:
                        notif = ZWaveNotification(
                            PyNotifications.AwakeNodesQueried,
                            self.network.home_id,
                            0
                        )
                    else:
                        notif = ZWaveNotification(
                            PyNotifications.AllNodesQueried,
                            self.network.home_id,
                            0
                        )

                    if not send_notif(notif):
                        return
            except:  # NOQA
                import traceback

                logger.error(traceback.format_exc())

        t = threading.Thread(target=_do)
        t.daemon = True
        t.start()
