# -*- coding: utf-8 -*-

# **python-openzwave** is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# **python-openzwave** is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with python-openzwave. If not, see http://www.gnu.org/licenses.

"""
This file is part of the **libopenzwave** project

:platform: Unix, Windows, OSX
:license: GPL(v3)

.. moduleauthor:: Kevin G Schlosser
"""

def main():
    import libopenzwave_man

    import argparse

    parser = argparse.ArgumentParser(
        description='libopenzwave service entry point'
    )

    parser.add_argument(
        '--password',
        dest='password',
        action='store',
        type=str,
        help=(
            'password that is used to connect'
        )
    )

    parser.add_argument(
        '--host',
        dest='host',
        action='store',
        default='',
        type=str,
        help='ip address of the server'
    )

    parser.add_argument(
        '--port',
        dest='port',
        action='store',
        default=61611,
        type=int,
        help='network port'
    )

    parser.add_argument(
        '--device',
        dest='device',
        action='store',
        default=None,
        type=str,
        help='path to USB zwave controller'
    )

    argv = parser.parse_args()

    if argv.host and not argv.password:
        raise RuntimeError('Password is required if connecting to a remote zwave server')

    libopenzwave_man.ui(argv)
