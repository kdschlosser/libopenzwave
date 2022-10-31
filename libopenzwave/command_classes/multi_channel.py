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
:synopsis: COMMAND_CLASS_MULTI_CHANNEL

.. moduleauthor:: Kevin G Schlosser
"""

import logging

from . import zwave_cmd_class

logger = logging.getLogger(__name__)

# Multi Channel Command Class - Active
# Transport-Encapsulation
COMMAND_CLASS_MULTI_CHANNEL = 0x60


# noinspection PyAbstractClass
class MultiChannel(zwave_cmd_class.ZWaveCommandClass):
    """
    Multi Channel Command Class

    symbol: `COMMAND_CLASS_MULTI_CHANNEL`
    """

    class_id = COMMAND_CLASS_MULTI_CHANNEL
    class_desc = 'COMMAND_CLASS_MULTI_CHANNEL'

    # noinspection PyMissingOrEmptyDocstring
    class ValueIndexes(zwave_cmd_class.ValueIndexes):
        pass

    # multichannel endpoints are added to the network as "virtual nodes"
