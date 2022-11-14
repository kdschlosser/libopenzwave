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
# You should have received a copy of the GNU General Public License
# along with libopenzwave. If not, see http://www.gnu.org/licenses.

"""
This file is part of the **libopenzwave** project

:platform: Unix, Windows, OSX
:license: GPL(v3)

.. moduleauthor:: Kevin G Schlosser
"""

__license__ = """

This file is part of **libopenzwave** project

License : GPL(v3)

**libopenzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**libopenzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.
"""

__copyright__ = "Copyright © 2022 Kevin G Schlosser"
__author__ = 'Kevin G Schlosser'
__email__ = ''


def ui(argv):
    import wx

    app = wx.App()

    from . import ui_manager
    import libopenzwave
    import threading

    network_start_event = threading.Event()

    def network_ready(*_, **__):
        network_start_event.set()

    libopenzwave.SIGNAL_NETWORK_READY.register(network_ready)

    if argv.host:
        device = '{0}:{1}'.format(argv.host, argv.port)
        options = libopenzwave.ZWaveOption(device=device)
        options.admin_password = argv.password
    elif argv.device:
        options = libopenzwave.ZWaveOption(device=argv.device)
    else:
        options = libopenzwave.ZWaveOption()  # user_path=r'C:\ProgramData\.openzwave')

    options.save_log_level = 'None'
    options.logging = False
    options.console_outut = False
    options.poll_interval = 30
    options.interval_between_polls = False
    options.save_configuration = True
    options.single_notification_handler = False

    options.lock()

    manager = ui_manager(options)

    network_start_event.wait()

    manager.Show()
    app.MainLoop()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='libopenzwave service entry point'
    )

    parser.add_argument(
        '--password',
        dest='admin_password',
        action='store',
        type=str,
        required=False,
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
        dest='server_port',
        action='store',
        default=61611,
        type=int,
        help='network port'
    )

    parser.add_argument(
        '--device',
        dest='device',
        action='store',
        default='',
        type=str,
        help='serial port of the UZB stick'
    )

    argv = parser.parse_args()

    ui(argv)


if __name__ == '__main__':
    main()
