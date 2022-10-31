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
:synopsis: ZWave network API

.. moduleauthor:: Kevin G Schlosser
"""


class State(object):

    def __init__(self, node, command, state, error):
        """
        :param node:
        :param command:
        :param state:
        :param error:
        """
        self.node = node
        self.command = command
        self.state = state
        self.error = error

        self.label = ''

        for char in list(command):
            if self.label and char.isupper():
                self.label += ' '
            self.label += char


class StateItem(int):
    doc = ''

    def __eq__(self, other):
        """
        :param other:
        :type other: int, str

        :rtype: bool
        """
        if isinstance(other, int):
            return other == int(self)

        return other == self.doc

    def __ne__(self, other):
        """
        :param other:
        :type other: int, str

        :rtype: bool
        """
        return self.__eq__(other)

    def __int__(self):
        """
        :rtype: int
        """
        return super(StateItem, self).__int__()

    def set(self, doc):
        """
        :param doc:
        :type doc: str

        :rtype: "StateItem"
        """
        self.doc = doc
        return self

    def __str__(self):
        """
        :rtype: str
        """
        return str(self.__int__()) + ' : ' + self.doc


STATE_STOPPED = StateItem(0).set('Network Stopped')
STATE_FAILED = StateItem(1).set('Network Failed')
STATE_RESET = StateItem(3).set('Network Reset')
STATE_STARTED = StateItem(5).set('Network Started')
STATE_AWAKE = StateItem(7).set('Network Awake')
STATE_READY = StateItem(10).set('Network Ready')
