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
:synopsis: Remote connection encryption

.. moduleauthor:: Kevin G Schlosser
"""

import base64
import hashlib
import os

# noinspection PyPackageRequirements
from Crypto.Cipher import AES  # NOQA


class AESCipher(object):

    def __init__(self, key):
        """
        :param key:
        :type key: str
        """
        self.bs = AES.block_size
        try:
            self.key = hashlib.sha256(
                key.encode('ISO-8859-1')
            ).digest()[:self.bs]
        except:  # NOQA
            self.key = hashlib.sha256(key).digest()[:self.bs]

    def encrypt(self, raw):
        """
        :param raw:
        :type raw: str

        :rtype: str
        """
        raw = self._pad(raw)
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        """
        :param enc:
        :type enc: str

        :rtype: str
        """
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(
            cipher.decrypt(enc[16:])
        ).decode('ISO-8859-1')

    def _pad(self, s):
        return (
            s +
            (self.bs - len(s) % self.bs) *
            chr(self.bs - len(s) % self.bs)
        )

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
