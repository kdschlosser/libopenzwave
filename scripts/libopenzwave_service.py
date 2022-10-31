# -*- coding: utf-8 -*-
"""
Service control entry point (Windows/Linux/Mac)
"""

import os
import sys
import threading
import subprocess


if sys.platform.startswith('win'):

    if __name__ != '__main__':

        log_path = os.path.join(
            os.path.expandvars('%programdata%'),
            '.openzwave'
        )

        if not os.path.exists(log_path):
            os.mkdir(log_path)

        import logging

        class LoggingFilter(logging.Filter):

            def filter(self, record):
                return True

        filter = LoggingFilter()

        log_file = open(
            os.path.join(log_path, 'libopenzwave.log'),
            'w'
        )

        handler = logging.StreamHandler(log_file)
        handler.addFilter(filter)

        root_logger = logging.getLogger()
        root_logger.addHandler(handler)

    try:
        from pip import get_installed_distributions
    except ImportError:
        from pip._internal.utils.misc import get_installed_distributions

    base_path = os.path.dirname(sys.executable)

    path_items = set(item for item in os.environ['PATH'].split(';') if item.strip())

    for p in get_installed_distributions():
        if p.project_name == 'pywin32':
            site_packages = p.location
            sys32_path = os.path.join(site_packages, 'pywin32_system32')
            win32_path = os.path.join(site_packages, 'win32')

            path_items.add(sys32_path)
            path_items.add(win32_path)
            path_items.add(base_path)

            proc = subprocess.Popen(
                'setx /M PATH "{0}"'.format(';'.join(item for item in path_items)),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            proc.communicate()
            break
    else:
        raise RuntimeError('pywin32 is not installed.')

    import win32serviceutil  # NOQA
    import win32service  # NOQA
    import servicemanager  # NOQA

    try:
        import _winreg
    except ImportError:
        import winreg as _winreg

    # noinspection PyPep8Naming
    class LibopenzwaveService(win32serviceutil.ServiceFramework):
        _svc_name_ = 'libopenzwave'
        _svc_display_name_ = 'libopenzwave'
        _svc_description_ = 'Python service wrapper for OpenZWave'

        # noinspection PyUnusedLocal
        def __init__(self, args):
            self.__options = None
            self.__network = None
            self.__stop_event = threading.Event()

            win32serviceutil.ServiceFramework.__init__(self, args)

        def SvcStop(self):
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STOPPING,
                (self._svc_name_, '')
            )

            event = threading.Event()

            def network_stopped(*_, **__):
                servicemanager.LogMsg(
                    servicemanager.EVENTLOG_INFORMATION_TYPE,
                    servicemanager.PYS_SERVICE_STOPPED,
                    (self._svc_name_, '')
                )

                event.set()

            self.__stop_event.set()

            if self.__network is not None:
                libopenzwave.SIGNAL_NETWORK_STOPPED.register(network_stopped)
                event.wait(60)
                libopenzwave.SIGNAL_NETWORK_STOPPED.unregister(network_stopped)

                if not event.is_set():
                    servicemanager.LogErrorMsg(
                        servicemanager.EVENTLOG_ERROR_TYPE,
                        0xF000,
                        ('Critical error when stopping service', '')
                    )

                    self.ReportServiceStatus(
                        win32service.SERVICE_ERROR_CRITICAL
                    )
                    self.ReportServiceStatus(win32service.SERVICE_STOPPED)
                    servicemanager.LogMsg(
                        servicemanager.EVENTLOG_INFORMATION_TYPE,
                        servicemanager.PYS_SERVICE_STOPPED,
                        (self._svc_name_, '')
                    )

                self.__stop_event.set()

        # def SvcPause(self):
        #     self.ReportServiceStatus(win32service.SERVICE_PAUSED)
        #
        # def SvcContinue(self):
        #     self.ReportServiceStatus(win32service.SERVICE_RUNNING)

        def SvcDoRun(self):
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTING,
                (self._svc_name_, '')
            )

            self.__stop_event.clear()

            try:
                reg_key = _winreg.OpenKey(
                    _winreg.HKEY_LOCAL_MACHINE,
                    'System\\CurrentControlSet\\Services\\' + self._svc_name_
                )

                def get_reg_value(name):
                    value = _winreg.QueryValueEx(reg_key, name)[0]

                    if value == 'None':
                        return None
                    if value == 'True':
                        return True
                    if value == 'False':
                        return False
                    if value.isdigit():
                        return int(value)
                    return value

                append_log_file = get_reg_value('append_logfile')
                log_level = get_reg_value('log_level').title()
                user_path = get_reg_value('user_path')

                import libopenzwave
                
                if log_level == 'None':
                    ll = logging.NOTSET
                elif log_level == 'Error':
                    ll = logging.ERROR
                elif log_level == 'Warning':
                    ll = logging.WARNING
                elif log_level == 'Info':
                    ll = logging.INFO
                elif log_level == 'Detail':
                    ll = libopenzwave.logger.LOGGING_DATA_PATH_WITH_RETURN
                elif log_level == 'Debug':
                    ll = logging.DEBUG

                libopenzwave.logger.setLevel(ll)

                self.__options = options = libopenzwave.ZWaveOption(
                    device=get_reg_value('device'),
                    config_path=get_reg_value('config_path'),
                    user_path=user_path
                )

                options.use_server = True
                options.console_output = False
                options.append_log_file = append_log_file
                options.admin_password = get_reg_value('admin_password')
                options.associate = get_reg_value('associate')
                options.server_ip = get_reg_value('server_ip')
                options.server_port = get_reg_value('server_port')
                options.ssl_key_path = get_reg_value('ssl_key_path')
                options.notify_transactions = (
                    get_reg_value('notify_transactions')
                )
                options.ssl_server_cert_path = (
                    get_reg_value('ssl_server_cert_path')
                )
                options.ssl_client_cert_path = (
                    get_reg_value('ssl_client_cert_path')
                )
                options.include_instance_label = (
                    get_reg_value('include_instance_label')
                )
                options.suppress_value_refresh = (
                    get_reg_value('suppress_value_refresh')
                )

                security_strategy = get_reg_value('security_strategy')
                if security_strategy is not None:
                    options.security_strategy = security_strategy

                custom_secured_cc = get_reg_value('custom_secured_cc')
                if custom_secured_cc is not None:
                    options.custom_secured_cc = custom_secured_cc

                poll_interval = get_reg_value('poll_interval')
                if poll_interval is not None:
                    options.poll_interval = poll_interval

                interval_between_polls = (
                    get_reg_value('interval_between_polls')
                )
                if interval_between_polls is not None:
                    options.interval_between_polls = interval_between_polls

                reload_nodes_after_config_update = (
                    get_reg_value('reload_nodes_after_config_update')
                )
                if reload_nodes_after_config_update is not None:
                    options.reload_nodes_after_config_update = (
                        reload_nodes_after_config_update
                    )

                options.logging = False if log_level == 'None' else True

                options.lock()

                self.__network = libopenzwave.ZWaveNetwork(
                    options,
                    single_notification_handler=False
                )

                servicemanager.LogMsg(
                    servicemanager.EVENTLOG_INFORMATION_TYPE,
                    servicemanager.PYS_SERVICE_STARTED,
                    (self._svc_name_, '')
                )

                self.__stop_event.wait()
                self.__stop_event.clear()

                self.__network.stop()
                self.__stop_event.wait()
                self.__options = None
                self.__network = None

            except:
                import traceback

                msg = traceback.format_exc()
                servicemanager.LogMsg(
                    servicemanager.EVENTLOG_ERROR_TYPE,
                    0xF000,
                    (msg, '')
                )
                self.ReportServiceStatus(win32service.SERVICE_ERROR_CRITICAL)
                self.ReportServiceStatus(win32service.SERVICE_STOPPED)


script_running = 'libopenzwave_service.py'


is_main = (
    __name__ == '__main__' or
    sys.argv[0].lower().endswith(os.path.join('scripts', 'libopenzwave_service'))
)


if is_main:
    import argparse # NOQA

    parser = argparse.ArgumentParser(
        description='libopenzwave service entry point'
    )

    parser.add_argument(
        '--password',
        dest='admin_password',
        action='store',
        default=None,
        type=str,
        help=(
            'password that is used to connect to the service - '
            'required with --install and --update'
        )

    )

    parser.add_argument(
        '--host',
        dest='server_ip',
        action='store',
        default='127.0.0.1',
        type=str,
        help='network interface ip address to bind to'
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
        '--cert-key',
        dest='ssl_key_path',
        action='store',
        default=None,
        type=str,
        help=(
            'ca cert key file location. using this options also '
            'requires the use of --server-cert and --client-cert'
        )
    )

    parser.add_argument(
        '--server-cert',
        dest='ssl_server_cert_path',
        action='store',
        default=None,
        type=str,
        help=(
            'server ca cert file location. using this options also '
            'requires the use of --cert-key and --client-cert'
        )
    )

    parser.add_argument(
        '--client-cert',
        dest='ssl_client_cert_path',
        action='store',
        default=None,
        type=str,
        help=(
            'client ca cert file location. using this options also '
            'requires the use of --cert-key and --server-cert'
        )
    )

    parser.add_argument(
        '--user-path',
        dest='user_path',
        action='store',
        default=None,
        type=str,
        help='directory where you want to save user config files to'
    )

    parser.add_argument(
        '--config-path',
        dest='config_path',
        action='store',
        default=None,
        type=str,
        help='directory where the device configuration files are located'
    )

    parser.add_argument(
        '--device',
        dest='device',
        action='store',
        default=None,
        type=str,
        help=(
            'the serial port of the USB Stick.\n'
            'only use this setting if the auto detection feature\n'
            'does not work properly.'
        )
    )

    parser.add_argument(
        '--append-logfile',
        dest='append_logfile',
        action='store_true',
        default=False,
        help='append to the log files. (default = False'
    )

    parser.add_argument(
        '--log-level',
        dest='log_level',
        choices=['none', 'error', 'warning', 'info', 'detail', 'debug'],
        default='error',
        help=(
            'Logging level (default = error).\n'
            '\n'
            'none: Disable all logging.\n'
            'error: A serious issue with the library or the network.\n'
            'warning: A minor issue from which the library should '
            'be able to recover.\n'
            'info: Everything Is working fine... These messages provide '
            'streamlined feedback on each message.\n'
            'detail: Detailed information on the progress of each message.\n'
            'debug: Very detailed information on progress that will '
            'create a huge log file quickly.\n'
        )
    )

    parser.add_argument(
        '--include-instance-label',
        dest='include_instance_label',
        action='store_true',
        default=False,
        help='prepend instance label to the label of a value (default = False)'
    )

    parser.add_argument(
        '--associate',
        dest='associate',
        action='store_true',
        default=False,
        help=(
            'enable automatic association of the controller with '
            'group one of every device. (default = False)'
        )
    )

    parser.add_argument(
        '--notify-transactions',
        dest='notify_transactions',
        action='store_true',
        default=False,
        help=(
            'notifications when transaction complete is '
            'reported. (default = False)'
        )
    )

    parser.add_argument(
        '--poll-interval',
        dest='poll_interval',
        action='store',
        default=None,
        type=int,
        help=(
            'value polling interval (in seconds).'
        )
    )

    parser.add_argument(
        '--interval-between-polls',
        dest='interval_between_polls',
        action='store',
        default=None,
        type=int,
        help=(
            'interval between polling loops (in seconds).'
        )
    )

    parser.add_argument(
        '--suppress-value-refresh',
        dest='suppress_value_refresh',
        action='store_true',
        default=False,
        help=(
            'suppress notifications for value refresh if the value '
            'data has not changed (default = False)'
        )
    )

    parser.add_argument(
        '--reload-nodes-after-config-update',
        dest='reload_nodes_after_config_update',
        choices=['never', 'immediate', 'awake'],
        default='awake',
        help=(
            'Reload a node if it\'s config file has been updated. '
            '(default = awake)\n'
            '\n'
            'never: Never Reload a Node after updating the Config File. '
            'Manual Reload is Required.\n'
            'immediate: Reload the Node Immediately after downloading '
            'the latest revision.\n'
            'awake: Reload Nodes only when they are awake '
            '(Always-On Nodes will reload immediately, Sleeping '
            'Nodes will reload when they wake up)\n'
        )
    )

    parser.add_argument(
        '--security-strategy',
        dest='security_strategy',
        choices=['SUPPORTED', 'ESSENTIAL', 'CUSTOM'],
        default=None,
        help=(
            'Reload a node if it\'s config file has been updated.\n'
            'if CUSTOM is set custom_secured_cc must also be used'
        )
    )

    parser.add_argument(
        '--custom-secured-cc',
        dest='custom_secured_cc',
        action='store',
        default=None,
        type=str,
        help=(
            'What List of Custom CC should we always encrypt if '
            '--security-strategy is CUSTOM.\n'
            'example: "0x62,0x4c,0x63"'
        )
    )

    parser.add_argument(
        '--install',
        dest='install',
        action='store_true',
        default=False,
        help='install the service'
    )

    parser.add_argument(
        '--remove',
        dest='remove',
        action='store_true',
        default=False,
        help='remove the service'
    )

    parser.add_argument(
        '--update',
        dest='update',
        action='store_true',
        default=False,
        help='update the service with the supplied new parameters'
    )

    parser.add_argument(
        '--start',
        dest='start',
        action='store_true',
        default=False,
        help='starts the service'
    )

    parser.add_argument(
        '--stop',
        dest='stop',
        action='store_true',
        default=False,
        help='stops the service'
    )

    parser.add_argument(
        '--restart',
        dest='restart',
        action='store_true',
        default=False,
        help='restarts the service'
    )


    def check_arguments():

        if (
            argv.custom_secured_cc is not None and
            argv.security_strategy != 'CUSTOM'
        ):
            raise RuntimeError(
                'If using the --custom-secured-cc parameter '
                'you must have --security-strategy set to "CUSTOM"'
            )

        cert_check = (
            argv.ssl_key_path,
            argv.ssl_server_cert_path,
            argv.ssl_client_cert_path
        )

        if (
            cert_check != (None, None, None) and
            None in cert_check
        ):
            raise RuntimeError(
                'To use SSL you need to provide\n'
                '--ssl_key_path\n'
                '--ssl_server_cert_path\n'
                '--ssl_client_cert_path'
            )

        if True in (argv.install, argv.update):
            if argv.admin_password is None:
                raise RuntimeError(
                    'password is required to install or update service'
                )

else:
    def check_arguments():
        pass

    argparse = None
    parser = None

if sys.platform.startswith('win'):
    if is_main:
        import pywintypes  # NOQA

        parser.add_argument(
            '--interactive',
            dest='interactive',
            action='store_true',
            default=False,
            help=(
                'service can interact with user - requires'
                ' --install or --update parameters'
            )
        )

        parser.add_argument(
            '--startup',
            dest='startup',
            action='store',
            default='auto',
            type=str,
            help=(
                'service startup type - '
                ' --install or --update parameters'
            )
        )
        parser.add_argument(
            '--service-username',
            dest='service_username',
            action='store',
            default='',
            type=str,
            help=(
                'service startup type - '
                ' --install or --update parameters'
            )
        )

        parser.add_argument(
            '--service-password',
            dest='service_password',
            action='store',
            default='',
            type=str,
            help=(
                'service startup type - '
                ' --install or --update parameters'
            )
        )

        argv = parser.parse_args()
        check_arguments()
        start = argv.start
        stop = argv.stop
        restart = argv.restart
        interactive = argv.interactive
        startup = argv.startup
        install = argv.install
        remove = argv.remove
        update = argv.update

        def write_reg_values():
            key = _winreg.CreateKey(
                _winreg.HKEY_LOCAL_MACHINE,
                (
                    'System\\CurrentControlSet\\Services\\' +
                    LibopenzwaveService._svc_name_
                )
            )

            def write_value(attr_name):
                _winreg.SetValueEx(
                    key,
                    attr_name,
                    0,
                    _winreg.REG_SZ,
                    str(getattr(argv, attr_name))
                )

            try:
                attrs = [
                    'admin_password',
                    'server_ip',
                    'server_port',
                    'ssl_key_path',
                    'ssl_server_cert_path',
                    'ssl_client_cert_path',
                    'user_path',
                    'config_path',
                    'device',
                    'append_logfile',
                    'include_instance_label',
                    'associate',
                    'notify_transactions',
                    'poll_interval',
                    'interval_between_polls',
                    'suppress_value_refresh',
                    'reload_nodes_after_config_update',
                    'security_strategy',
                    'custom_secured_cc',
                    'log_level'
                ]

                for attr in attrs:
                    write_value(attr)
            finally:
                _winreg.CloseKey(key)


        def wait_for_service(new_state):
            """Waits for the service to return the specified status.  You
            should have already requested the service to enter that state"""
            event = threading.Event()

            while True:
                sys.stdout.write('.')

                now_state = win32serviceutil.QueryServiceStatus(
                    LibopenzwaveService._svc_name_
                )[1]
                if now_state == new_state:
                    print()
                    break
                if now_state == win32service.SERVICE_ERROR_CRITICAL:
                    print()
                    raise RuntimeError('Service Error Critical')
                event.wait(1.0)

        if len(sys.argv) == 1:
            try:
                status = win32serviceutil.QueryServiceStatus(
                    LibopenzwaveService._svc_name_
                )[1]

                if status == win32service.SERVICE_STOPPED:
                    print('Service is not running.')

            except pywintypes.error:
                print('Service is not installed.')

                win32serviceutil.HandleCommandLine(LibopenzwaveService, argv=argv)

                status = win32serviceutil.QueryServiceStatus(
                    LibopenzwaveService._svc_name_
                )[1]

                servicemanager.SetEventSourceName(
                    LibopenzwaveService._svc_name_,
                    True
                )

            if status == win32service.SERVICE_STOPPED:
                win32serviceutil.StartService(LibopenzwaveService._svc_name_)
                wait_for_service(win32service.SERVICE_RUNNING)

        elif remove:
            service_args = [sys.argv[0], 'remove']

            try:
                status = win32serviceutil.QueryServiceStatus(
                    LibopenzwaveService._svc_name_
                )[1]

                if status != win32service.SERVICE_STOPPED:
                    win32serviceutil.StopService(LibopenzwaveService._svc_name_)
                    wait_for_service(win32service.SERVICE_STOPPED)

                _winreg.DeleteKey(
                    _winreg.HKEY_LOCAL_MACHINE,
                    (
                        'System\\CurrentControlSet\\Services\\' +
                        LibopenzwaveService._svc_name_
                    )
                )

                win32serviceutil.HandleCommandLine(
                    LibopenzwaveService,
                    argv=service_args
                )
                print('Service removed.')

            except pywintypes.error:
                print('Service is not installed.')

        elif update:
            try:
                status = win32serviceutil.QueryServiceStatus(
                    LibopenzwaveService._svc_name_
                )[1]

                if status != win32service.SERVICE_STOPPED:
                    service_was_running = True
                    print('Stopping service....')
                    win32serviceutil.StopService(LibopenzwaveService._svc_name_)

                    wait_for_service(win32service.SERVICE_STOPPED)
                else:
                    service_was_running = False

            except pywintypes.error:
                raise RuntimeError('Service not installed')

            write_reg_values()

            service_args = [sys.argv[0], '--startup=' + argv.startup]

            if argv.service_username:
                service_args += ['--username=' + argv.service_username]

            if argv.service_password:
                service_args += ['--password=' + argv.service_password]

            if argv.interactive:
                service_args += ['--interactive']

            service_args += ['update']


            win32serviceutil.HandleCommandLine(LibopenzwaveService, argv=service_args)

            if service_was_running:
                print('Starting service....')
                servicemanager.SetEventSourceName(
                    LibopenzwaveService._svc_name_,
                    True
                )

                win32serviceutil.StartService(LibopenzwaveService._svc_name_)
                wait_for_service(win32service.SERVICE_RUNNING)

        elif argv.install:

            try:
                status = win32serviceutil.QueryServiceStatus(
                    LibopenzwaveService._svc_name_
                )[1]
                raise RuntimeError('Service is already installed')

            except pywintypes.error:
                pass

            write_reg_values()

            service_args = [sys.argv[0], '--startup=' + argv.startup]

            if argv.service_username:
                service_args += ['--username=' + argv.service_username]

            if argv.service_password:
                service_args += ['--password=' + argv.service_password]

            if argv.interactive:
                service_args += ['--interactive']

            service_args += ['install']

            win32serviceutil.HandleCommandLine(LibopenzwaveService, argv=service_args)

            print('Starting service....')
            servicemanager.SetEventSourceName(
                LibopenzwaveService._svc_name_,
                True
            )

            win32serviceutil.StartService(LibopenzwaveService._svc_name_)
            wait_for_service(win32service.SERVICE_RUNNING)

        elif start:
            try:
                status = win32serviceutil.QueryServiceStatus(
                    LibopenzwaveService._svc_name_
                )[1]

                if status == win32service.SERVICE_RUNNING:
                    raise RuntimeError('Service is already started.')

                print('Starting service....')
                servicemanager.SetEventSourceName(
                    LibopenzwaveService._svc_name_,
                    True
                )

                win32serviceutil.StartService(LibopenzwaveService._svc_name_)
                wait_for_service(win32service.SERVICE_RUNNING)

            except pywintypes.error:
                raise RuntimeError('Service is not installed')

            pass

        elif stop:
            try:
                status = win32serviceutil.QueryServiceStatus(
                    LibopenzwaveService._svc_name_
                )[1]

                if status == win32service.SERVICE_STOPPED:
                    raise RuntimeError('Service is already stopped')

                print('Stopping service...')
                win32serviceutil.StopService(LibopenzwaveService._svc_name_)

                wait_for_service(win32service.SERVICE_STOPPED)

            except pywintypes.error:
                raise RuntimeError('Service is not installed')
            pass

        elif restart:
            try:
                status = win32serviceutil.QueryServiceStatus(
                    LibopenzwaveService._svc_name_
                )[1]

                if status != win32service.SERVICE_STOPPED:
                    print('Stopping service...')
                    win32serviceutil.StopService(LibopenzwaveService._svc_name_)
                    wait_for_service(win32service.SERVICE_STOPPED)

                else:
                    print('Service was already stopped.')

                print('Starting service....')
                servicemanager.SetEventSourceName(
                    LibopenzwaveService._svc_name_,
                    True
                )

                win32serviceutil.StartService(LibopenzwaveService._svc_name_)
                wait_for_service(win32service.SERVICE_RUNNING)

            except pywintypes.error:
                raise RuntimeError('Service is not installed')
            pass

else:
    try:
        import sdnotify
    except ImportError:
        raise RuntimeError('The sdnotify library is required.')

    parser.add_argument(
        '--run',
        dest='run',
        action='store_true',
        default=False,
        type=bool
    )

    argv = parser.parse_args()
    check_arguments()

    start = argv.start
    stop = argv.stop
    restart = argv.restart
    install = argv.install
    remove = argv.remove
    update = argv.update
    run = argv.run

    service_file = '/etc/systemd/system/libopenzwave.service'
    service_exists = os.path.exists(service_file)

    if not install and not service_exists:
        raise RuntimeError('Service is not installed.')

    elif install and service_exists:
        raise RuntimeError('Service is already installed')

    service_template = (
        '[Unit]\n'
        'Description=libopenzwave\n'
        'After=network-online.target multi-user.target\n'
        'Wants=network-online.target\n'
        '\n'
        '[Service]\n'
        'Type=notify\n'
        'Environment=PYTHONUNBUFFERED=true\n'
        'ExecStart={executable} {args}\n'
        'WatchdogSec=30\n'
        'Restart=on-watchdog\n'
        'NotifyAccess=all\n'
        'WorkingDirectory={working_directory}\n'
        'KillSignal=SIGINT\n'
        '\n'
        '[Install]\n'
        'WantedBy=multi-user.target\n'
    )

    def systemctl(*args):
        proc = subprocess.Popen(
            ['systemctl'] + list(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        out, err = proc.communicate()
        print(out)
        if err:
            raise RuntimeError(err)


    if run:
        # sys.stderr = StdReplacement()
        # sys.stdout = StdReplacement()

        import libopenzwave  # NOQA
        import logging  # NOQA

        systemd = sdnotify.SystemdNotifier()
        exit_event = threading.Event()

        from signal import signal, SIGINT, SIGABRT

        def sigint_shutdown_handler(signum, frame):
            systemd.notify("STOPPING=1")

            def network_stopped(*_, **__):
                exit_event.set()

            libopenzwave.SIGNAL_NETWORK_STOPPED.register(network_stopped)

            network.stop()

        def sigabrt_shutdown_handler(signum, frame):
            exit_event.set()

        signal(SIGINT, sigint_shutdown_handler)
        signal(SIGABRT, sigabrt_shutdown_handler)

        systemd.notify("STATUS=Setting Options")
        options = libopenzwave.ZWaveOption(
            device=argv.device,
            user_path=argv.user_path,
            config_path=argv.config_path
        )

        options.admin_password = argv.admin_password
        options.server_ip = argv.server_ip
        options.server_port = argv.server_port
        options.ssl_key_path = argv.ssl_key_path
        options.ssl_server_cert_path = argv.ssl_server_cert_path
        options.ssl_client_cert_path = argv.ssl_client_cert_path
        options.append_log_file = argv.append_logfile
        options.include_instance_label = argv.include_instance_label
        options.associate = argv.associate
        options.notify_transactions = argv.notify_transactions

        poll_interval = argv.poll_interval
        if poll_interval is not None:
            options.poll_interval = poll_interval

        interval_between_polls = argv.interval_between_polls
        if interval_between_polls is not None:
            options.interval_between_polls = interval_between_polls

        options.suppress_value_refresh = argv.suppress_value_refresh

        reload_nodes_after_config_update = (
            argv.reload_nodes_after_config_update
        )
        if reload_nodes_after_config_update is not None:
            options.reload_nodes_after_config_update = (
                reload_nodes_after_config_update
            )

        security_strategy = argv.security_strategy
        if security_strategy is not None:
            options.security_strategy = security_strategy

        custom_secured_cc = argv.custom_secured_cc
        if custom_secured_cc is not None:
            options.custom_secured_cc = custom_secured_cc

        systemd.notify("STATUS=Setting Logging")
        log_level = argv.log_level.title()

        options.save_log_level = log_level
        options.queue_log_level = log_level
        options.dump_trigger_level = log_level
        options.logging = False if log_level == 'None' else True

        if log_level == 'None':
            log_level = logging.NOTSET
        elif log_level == 'Error':
            log_level = logging.ERROR

        elif log_level == 'Warning':
            log_level = logging.WARNING

        elif log_level == 'Info':
            log_level = logging.INFO

        elif log_level == 'Detail':
            log_level = libopenzwave.logger.LOGGING_DATA_PATH_WITH_RETURN

        elif log_level == 'Debug':
            log_level = logging.DEBUG

        logging.basicConfig(
            filename=os.path.join(options.user_path, 'service.log'),
        )

        libopenzwave.logger.setLevel(log_level)

        write_type = 'a' if options.append_log_file else 'w'

        stdout_file = open(
            os.path.join(options.user_path, 'stdout.log'),
            write_type
        )

        stderr_file = open(
            os.path.join(options.user_path, 'stderr.log'),
            write_type
        )

        with sys.stdout.lock:
            sys.stdout.log_file = stdout_file

        with sys.stderr.lock:
            sys.stderr.log_file = stderr_file

        systemd.notify("STATUS=Starting Network")

        network = libopenzwave.ZWaveNetwork(options)

        systemd.notify("READY=1")
        while not exit_event.is_set():
            exit_event.wait(28)
            if network.manager.is_alive():
                systemd.notify("WATCHDOG=1")

        with sys.stdout.lock:
            sys.stdout.log_file.close()
            sys.stdout.log_file = None

        with sys.stderr.lock:
            sys.stderr.log_file.close()
            sys.stderr.log_file = None

    elif install:
        args = sys.argv[:]
        args.remove('--install')

        base_path = os.path.abspath(os.path.dirname(__file__))
        args[0] = os.path.abspath(__file__)

        for i, arg in enumerate(args):
            if arg.startswith('--'):
                continue

            if arg.isdigit():
                continue

            args[i] = '"' + arg + '"'

        args.insert(1, '--run')

        template = service_template.format(
            executable=sys.executable,
            args=' '.join(args),
            working_directory=base_path,
        )

        with open(service_file, 'w') as f:
            f.write(template)

        os.chmod(service_file, 644)

        systemctl('daemon-reload')
        systemctl('enable', 'libopenzwave')
        systemctl('start', 'libopenzwave')

        pass

    elif update:
        args = sys.argv[:]
        args.remove('--update')

        base_path = os.path.abspath(os.path.dirname(__file__))
        args[0] = os.path.abspath(__file__)

        for i, arg in enumerate(args):
            if arg.startswith('--'):
                continue

            if arg.isdigit():
                continue

            args[i] = '"' + arg + '"'

        args.insert(1, '--run')

        template = service_template.format(
            executable=sys.executable,
            args=' '.join(args),
            working_directory=base_path,
        )

        systemctl('stop', 'libopenzwave')
        systemctl('disable', 'libopenzwave')

        with open(service_file, 'w') as f:
            f.write(template)

        systemctl('daemon-reload')
        systemctl('enable', 'libopenzwave')
        systemctl('start', 'libopenzwave')

    elif remove:
        systemctl('stop', 'libopenzwave')
        systemctl('disable', 'libopenzwave')

        os.remove(service_file)

        systemctl('daemon-reload')
        systemctl('reset-failed')

    elif restart:
        systemctl('restart', 'libopenzwave')

    elif start:
        systemctl('start', 'libopenzwave')

    elif stop:
        systemctl('stop', 'libopenzwave')


def main():
    pass
