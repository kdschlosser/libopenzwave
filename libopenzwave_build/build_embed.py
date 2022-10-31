# -*- coding: utf-8 -*-

import os
import shutil
from .build import build as _build
import libopenzwave_version
from .get_openzwave import get_openzwave


class build_embed(_build):
    backend = 'cpp'
    openzwave = 'openzwave-embed'
    flavor = 'release_embed'
    static = True
    install_openzwave_so = False

    def finalize_options(self):
        _build.finalize_options(self)

        if self.dev_repo is None:
            self.dev_repo = (
                'https://raw.githubusercontent.com/OpenZWave/python-openzwave'
                '/master/archives/open-zwave-master-{0}.dev.zip'.format(
                    libopenzwave_version.libopenzwave_version
                )
            )

        build_config = self.distribution.get_command_obj('build_config')
        build_config.ensure_finalized()

    def get_openzwave_dev(self):
        get_openzwave(self.openzwave, self.dev_repo)

        src = os.path.join(
            self.openzwave,
            'python-openzwave',
            'openzwave.vers.cpp'
        )

        dst = os.path.join(self.openzwave, 'cpp', 'src', 'vers.cpp')
        shutil.copyfile(src, dst)

    def get_openzwave(self):
        url = (
            'https://raw.githubusercontent.com/OpenZWave/python-openzwave'
            '/master/archives/open-zwave-master-{0}.zip'.format(
                libopenzwave_version.libopenzwave_version
            )
        )
        get_openzwave(self.openzwave, url)

        src = os.path.join(
            self.openzwave,
            'python-openzwave',
            'openzwave.vers.cpp'
        )

        dst = os.path.join(self.openzwave, 'cpp', 'src', 'vers.cpp')
        shutil.copyfile(src, dst)
