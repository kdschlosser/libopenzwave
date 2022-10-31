# -*- coding: utf-8 -*-


import os
import sys
import shutil
from .build import build as _build
import libopenzwave_version
from .get_openzwave import get_openzwave


class build_embed_shared(_build):
    backend = 'cpp'
    openzwave = 'openzwave-embed-shared'
    static = False
    flavor = 'release_embed_shared'
    install_openzwave_so = True

    def finalize_options(self):
        _build.finalize_options(self)

        if self.dev_repo is None:
            self.dev_repo = (
                'https://raw.githubusercontent.com/OpenZWave/python-openzwave'
                '/master/archives/open-zwave-master-{0}.dev.zip'.format(
                    libopenzwave_version.libopenzwave_version
                )
            )


        while '' in ctx['extra_compile_args']:
            ctx['extra_compile_args'].remove('')
        extra = '-I/usr/local/include/openzwave//'
        for ssubstitute in ['/', '/value_classes/', '/platform/']:
            incl = extra.replace('//', ssubstitute)
            if not incl in ctx['extra_compile_args']:
                ctx['extra_compile_args'] += [incl]

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
