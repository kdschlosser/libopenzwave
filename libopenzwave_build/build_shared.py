# -*- coding: utf-8 -*-

import sys
from .build import build as _build
import libopenzwave_version
from .get_openzwave import get_openzwave


class build_shared(_build):
    backend = 'cython'
    openzwave = 'openzwave-shared'
    flavor = 'release_shared'
    static = False
    install_openzwave_so = True

    def finalize_options(self):
        _build.finalize_options(self)

        if self.dev_repo is None:
            self.dev_repo = (
                'https://codeload.github.com/OpenZWave/open-zwave/zip/master'
            )

        if sys.platform.startswith('win'):
            build_config = self.distribution.get_command_obj('build_config')
            build_config.ensure_finalized()

    def get_openzwave_dev(self):
        get_openzwave(
            self.openzwave,
            self.dev_repo
        )

    def get_openzwave(self):
        url = 'http://old.openzwave.com/downloads/'
        import requests

        response = requests.get(self.url)
        if sys.version_info[0] == 2:
            response = response.content.split('\n')
            for line in response:
                if '<a href=openzwa' in line:
                    break
            else:
                raise RuntimeError('Unable to locate openzwave')

            lines = line.replace('<tr>', '').split('</tr>')

            download_url = None
            download_version = 0

            for line in lines:
                line = line.strip()
                line = line.replace('<td>', '').split('</td>')
                version = line[0][line[0].find('>') + 1:]
                download_file_name = line[2].replace('<a href= ', '')

                version = tuple(
                    int(ver) for ver in version.split('.') if ver.isdigit()
                )

                if version[:2] == libopenzwave_version.libopenzwave_version:
                    if version[2] > download_version:
                        download_version = version[2]
                        download_url = url + download_file_name

            if download_url is None:
                raise RuntimeError(
                    'unable to locate suitable openzwave download')

        else:
            response = response.content.split(b'\n')
            for line in response:
                if b'<a href=openzwa' in line:
                    break
            else:
                raise RuntimeError('Unable to locate openzwave')

            lines = line.replace(b'<tr>', b'').split(b'</tr>')

            download_url = None
            download_version = 0

            for line in lines:
                line = line.strip()
                line = line.replace(b'<td>', b'').split(b'</td>')
                version = line[0][line[0].find(b'>') + 1:]
                download_file_name = line[2].replace(b'<a href= ', b'')

                version = tuple(
                    int(ver) for ver in version.split(b'.') if ver.isdigit()
                )

                if version[:2] == libopenzwave_version.libopenzwave_version:
                    if version[2] > download_version:
                        download_version = version[2]
                        download_url = url + download_file_name

            if download_url is None:
                raise RuntimeError(
                    'unable to locate suitable openzwave download')

        get_openzwave(self.openzwave, download_url)
