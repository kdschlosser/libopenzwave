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
:synopsis: ZWave node types API

.. moduleauthor:: Kevin G Schlosser
"""

import traceback
import threading
import logging
from collections import deque

from . import utils

use_single_handler = False

logger = logging.getLogger(__name__)


class HandlerMeta(type):

    def __call__(cls, obj):
        from .network import ZWaveNetwork

        if isinstance(obj, ZWaveNetwork):
            instance = super(HandlerMeta, cls).__call__(obj)
            NotificationHandler.network_handler = instance

        elif use_single_handler:
            instance = NotificationHandler.network_handler

        else:
            instance = super(HandlerMeta, cls).__call__(obj)
            NotificationHandler.node_handlers += [instance]

        return instance


class NotificationHandler(object, metaclass=HandlerMeta):

    network_handler = None
    node_handlers = []

    def __init__(self, obj):
        self.__stop_event = threading.Event()
        self.__stall_event = threading.Event()
        self.__start_lock = threading.Lock()
        self.__queue = deque()
        self.__processing = False
        self.__obj = obj
        from .network import ZWaveNetwork

        if isinstance(obj, ZWaveNetwork):
            self.name = 'pyOZW-ThreadWorker_NetworkId:' + str(obj.id)
        else:
            self.name = 'pyOZW-ThreadWorker_NodeId:' + str(obj.id)

        self.__thread = threading.Thread(
            name=self.name,
            target=self.run
        )
        self.__thread.daemon = True

    def is_owner_object(self, obj):
        return obj == self.__obj

    def start(self):
        if self.__stop_event.is_set():
            return

        if not self.__thread.is_alive():
            self.__stall_event.clear()
            self.__thread.start()

    @property
    def is_alive(self):
        return self.__thread.is_alive()

    @property
    def is_busy(self):
        if list(self.__queue):
            return True
        return False

    def add(self, func, *args, **kwargs):
        if self.__stop_event.is_set():
            return

        worker = NotificationWorker(func, *args, **kwargs)
        self.__queue.append(worker)
        self.__stall_event.set()

    def run(self):
        while not self.__stall_event.is_set():
            if self.__stop_event.is_set() and not self.__queue:
                break

            if self == NotificationHandler.network_handler:
                if self.__obj.xml_handler.is_dirty:
                    self.__obj.xml_handler.write_file()

                for nh in NotificationHandler.node_handlers:
                    if nh.is_busy and not nh.is_alive:
                        nh.start()

            while self.__queue:
                self.__processing = True
                worker = self.__queue.popleft()
                worker.do()

                if worker.has_exception:
                    worker.log_exception()

            if self != NotificationHandler.network_handler:
                self.__processing = False
                self.__stall_event.wait(3.0)
                if not self.__stall_event.is_set():
                    break
            else:
                if self.__processing:
                    self.__processing = False
                else:
                    self.__stall_event.wait(0.1)

            self.__stall_event.clear()

        self.__stall_event.clear()
        self.__thread = threading.Thread(
            name=self.name,
            target=self.run
        )
        self.__thread.daemon = True

    def stop(self):
        self.__stop_event.set()
        self.__stall_event.set()
        if threading.current_thread() != self:
            if (
                self.__thread.is_alive() and
                self.__thread != threading.current_thread()
            ):
                self.__thread.join()

        if self == NotificationHandler.network_handler:
            NotificationHandler.network_handler = None
        elif self in NotificationHandler.node_handlers:
            NotificationHandler.node_handlers.remove(self)


class NotificationWorker(object):
    def __init__(self, func, *args, **kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs
        self.__wait_event = threading.Event()
        self.__exception = None
        self.__result = None
        self.__caller = utils.caller_name()
        self.__file_name, self.__line_no = utils.get_line_and_file(3)

    @utils.logit
    def do(self):
        try:
            self.__func(*self.__args, **self.__kwargs)
        except Exception:  # NOQA
            calling_logger = utils.calling_function_logger(self.__caller)

            if calling_logger is None:
                calling_logger = logger

            msg = '\n    File "{0}", line {1}, in  {2}\n    Traceback: \n{3}'
            msg = msg.format(
                self.__file_name,
                self.__line_no,
                self.__caller,
                '\n'.join(
                    '        ' + line
                    for line in traceback.format_exc().split('\n')
                )
            )

            self.__exception = (calling_logger, msg)

        self.__wait_event.clear()

    @property
    def has_exception(self):
        return self.__exception is not None

    def log_exception(self):
        calling_logger, msg = self.__exception
        calling_logger.error(msg)
