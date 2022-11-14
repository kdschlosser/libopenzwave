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
:synopsis: ZWave Object (the base class for all ZWave classes)

.. moduleauthor:: Kevin G Schlosser
"""

import logging

from .singleton import InstanceSingleton
from . import xml_handler  # NOQA


logger = logging.getLogger(__name__)


class ZWaveObject(object, metaclass=InstanceSingleton):
    """
    Represents a ZWave object. Values, nodes, ...
    """

    _command_classes = []

    def __init__(self, object_id, network=None, xml_data=None):
        """
        Initialize a ZWave object

        :param object_id: ID of the object
        :type object_id: int, None

        :param network: The network object to access the manager
        :type network: ZWaveNetwork, optional

        :param xml_data:
        :type xml_data: xml_handler.XMLElement, optional
        """
        self._network = network
        self._last_update = None
        self._outdated = True
        self._object_id = object_id
        self._xml_handler = xml_data
        self._dataset_loaded = False

    @property
    def xml_handler(self):
        """
        :rtype: xml_handler.XMLElement, None
        """
        return self._xml_handler

    def __eq__(self, other):
        """
        :param other:
        :type other: int, "ZWaveObject"

        :rtype: bool
        """
        if isinstance(other, ZWaveObject):
            return object.__eq__(self, other)

        if isinstance(other, int):
            if hasattr(self, '_cls_ids'):
                return other in self._cls_ids

        try:
            other.class_id in self._command_classes
        except AttributeError:
            pass

        try:
            return self.command_class == other  # NOQA
        except AttributeError:
            return False

    def __ne__(self, other):
        """
        :param other:
        :type other: int, "ZWaveObject"

        :rtype: bool
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        :rtype: hash
        """
        return hash(str(self))

    @property
    def id(self):
        """
        The id of the node.

        :rtype: int
        """
        return self._object_id

    @property
    def home_id(self):
        """
        The home_id of the node.

        :rtype: int
        """
        return self._network.object_id if self._network is not None else None

    @property
    def network(self):
        """
        The network of the node.
        """
        return self._network

    @property
    def object_id(self):
        """
        The id of the object.
        object_id could be None, when creating a scene for example.

        :rtype: int
        """
        return self._object_id
