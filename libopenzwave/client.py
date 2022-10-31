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
:synopsis: Socket client

.. moduleauthor:: Kevin G Schlosser
"""

import threading
import logging
import json
import socket
import ssl
import time
from uuid import uuid4
from collections import deque

from . import remote_encryption


try:
    pickle = __import__('cPickle')
except ImportError:
    import pickle

logger = logging.getLogger(__name__)


class Client(threading.Thread):
    """
    TODO: client.Client class docstring
    """

    def __init__(self, host, port, password, key, server_cert, client_cert):
        """
        
        :param host:
        :type host: str

        :param port:
        :type port: int

        :param password:
        :type password: str

        :param key:
        :type key: str

        :param server_cert:
        :type server_cert: str

        :param client_cert:
        :type client_cert: str
        """
        self.host = host
        self.port = port
        self.key = key
        self.client_cert = client_cert
        self.server_cert = server_cert
        self.socket = None
        self.network = None
        self.__aes = remote_encryption.AESCipher(password)
        self.message_cache = {}
        self.cache_lock = threading.Lock()
        self.results = {}

        self.exit_event = threading.Event()

        self.__notification_thread = threading.Thread(
            target=self.notification_loop
        )
        self.__notification_thread.daemon = True
        self.notification_event = threading.Event()
        self.notification_queue = deque()

        self.__processing_thread = threading.Thread(target=self.process_loop)
        self.__processing_thread.daemon = True
        self.processing_event = threading.Event()
        self.process_queue = deque()

        threading.Thread.__init__(self)

    def notification_loop(self):
        """
        TODO: client.Client.notification_loop docstring
        """
        while not self.exit_event.is_set():

            while self.notification_queue:
                notification, message_id = self.notification_queue.popleft()

                try:
                    signal = pickle.loads(
                        notification.encode('ISO-8859-1')
                    )
                    logger.debug(
                        'incoming notification ({0}):\n    {1}'.format(
                            self.host,
                            str(signal)
                        )
                    )
                    # noinspection PyProtectedMember
                    self.network._zwcallback(signal)
                except:  # NOQA
                    import traceback
                    logger.error(traceback.format_exc())

            self.notification_event.wait()
            self.notification_event.clear()

    def process_loop(self):
        """
        TODO: client.Client.process_loop docstring
        """
        logger.debug('client processing thread started')

        while not self.exit_event.is_set():

            while self.process_queue:
                data = self.process_queue.popleft()
                try:
                    message = json.loads(data)
                except:  # NOQA
                    continue

                if 'resend' in message:
                    # noinspection PyShadowingBuiltins
                    id = message['resend']
                    with self.cache_lock:
                        if id in self.message_cache:
                            resend_message = self.message_cache[id][0]
                            self.socket.send(resend_message)
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

                    try:
                        contents = json.loads(self.__aes.decrypt(contents))

                    except:  # NOQA
                        logger.error(
                            'bad message from server. '
                            'requesting retransmit. {0}'.format(id)
                        )

                        self.socket.send(json.dumps(dict(resend=id)) + '\n')
                    else:
                        if 'result' in contents:
                            try:
                                contents['result'] = (
                                    contents['result'].encode('ISO-8859-1')
                                )
                                contents['result'] = (
                                    pickle.loads(contents['result'])
                                )
                            except:  # NOQA
                                logger.error(
                                    'bad message from server. '
                                    'requesting retransmit. {0}'.format(id)
                                )

                                self.socket.send(
                                    json.dumps(dict(resend=id)) + '\n'
                                )

                            else:
                                output = json.dumps(
                                    contents, indent=4
                                ).split('\n')

                                output = '\n'.join(
                                    '    ' + line for line in output
                                )

                                logger.debug(
                                    'incoming result ({0}):\n{1}'.format(
                                        self.host, output
                                    )
                                )

                                if contents['id'] in self.results:
                                    event = self.results[contents['id']]
                                    self.results[contents['id']] = (
                                        contents['result']
                                    )
                                    event.set()

                        elif 'notification' in contents:
                            self.notification_queue.append(
                                (contents['notification'], id)
                            )

                            self.notification_event.set()

                        self.socket.send(json.dumps(dict(ok=id)) + '\n')

            self.processing_event.wait()
            self.processing_event.clear()

        logger.debug('client processing thread stopped')

    # noinspection PyMethodOverriding
    def start(self, network):
        """
        TODO: client.Client.start docstring
        
        :param network:
        :type network: :py:class:`libopenzwave.network.ZWaveNetwork`
        """
        logger.debug('starting client processing thread')
        self.__processing_thread.start()
        self.__notification_thread.start()

        logger.info(
            'starting client socket listener thread ({0}:{1})'.format(
                self.host,
                self.port
            )
        )

        self.network = network
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        if None not in (
            self.key,
            self.server_cert,
            self.client_cert
        ):
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_verify_locations(self.server_cert)
            context.load_cert_chain(
                certfile=self.client_cert,
                keyfile=self.key
            )

            if ssl.HAS_SNI:
                self.socket = context.wrap_socket(
                    self.socket,
                    server_hostname=self.host
                )
            else:
                self.socket = context.wrap_socket(self.socket)

        self.socket.settimeout(5.0)

        logger.debug(
            'connected to server ({0}:{1})'.format(self.host, self.port)
        )

        threading.Thread.start(self)

    def run(self):
        """
        TODO: client.Client.run docstring
        """
        data = ''

        logger.debug('client socket listener thread started')

        while not self.exit_event.is_set():
            try:
                new_data = self.socket.recv(8192)
            except socket.timeout:

                with self.cache_lock:
                    for id_, (message, timestamp) in list(
                        self.message_cache.items()
                    )[:]:

                        if time.time() - timestamp >= 5:
                            self.socket.send(message)
                            self.message_cache[id_] = (message, time.time())
                continue

            except socket.error:
                break

            if not new_data:
                break

            data += new_data

            while '\n' in data:
                message, data = data.split('\n', 1)
                self.process_queue.append(message)
                self.processing_event.set()

        try:
            self.socket.close()
        except socket.error:
            pass

        logger.info('server disconnected: ' + self.host)

        self.socket = None
        logger.debug('client socket listener thread stopped')

    def stop(self):
        """
        TODO: client.Client.stop docstring
        """
        logger.debug('stopping client processing thread')

        self.exit_event.set()
        self.process_queue.clear()
        self.processing_event.set()
        self.notification_queue.clear()
        self.notification_event.set()

        if self.__processing_thread.is_alive():
            self.__processing_thread.join()

        if self.__notification_thread.is_alive():
            self.__notification_thread.join()

        logger.debug('stopping client socket listener thread')

        if self.socket is not None:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()

        if self.is_alive():
            self.join()

    def send(self, msg):
        """
        :param msg:
        :type msg: dict
        """
        # noinspection PyShadowingBuiltins
        id = str(uuid4())
        msg['id'] = id
        output = json.dumps(msg, indent=4).split('\n')
        output = '\n'.join('    ' + line for line in output)

        logger.debug('<-- ' + output)
        msg = json.dumps(msg)
        msg = self.__aes.encrypt(msg)
        event = threading.Event()

        self.results[id] = event

        message_id = str(uuid4())
        message = json.dumps(dict(id=message_id, contents=msg)) + '\n'

        with self.cache_lock:
            self.message_cache[message_id] = (message, time.time())

        self.socket.send(message)
        event.wait()

        result = self.results.pop(id)
        return result
