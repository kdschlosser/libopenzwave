# -*- coding: utf-8 -*-

import os
from distutils import log as LOG

from . import library_base


class Library(library_base.Library):

    @property
    def prefix(self):
        return '/opt/local'

    @property
    def libraries(self):
        return ['-lresolv', '-liconv', '-lusb-1.0']

    @libraries.setter
    def libraries(self, _):
        pass

    @property
    def sources(self):
        sources = library_base.get_sources(
            os.path.join(self.openzwave, 'cpp'),
            ignore=[
                'windows',
                'winrt',
                'mac',
                'hidapi',
                'examples',
                'test'
            ]
        )
        return sources

    @sources.setter
    def sources(self, _):
        pass

    @property
    def ld_flags(self):
        ld_flags = library_base.parse_flags(os.environ['LDFLAGS'])

        if not self.builder.static:
            if '-shared' not in ld_flags:
                ld_flags.append('-shared')

        return ld_flags

    @property
    def c_flags(self):
        c_flags = library_base.parse_flags('CFLAGS') + [
            '-c',
            '-Wall',
            '-Wno-unknown-pragmas',
            '-Werror',
            '-Wno-error=sequence-point',
            '-Wno-sequence-point',
            '-O3',
            '-fPIC',
        ]

        return c_flags

    @property
    def include_dirs(self):
        includes = library_base.Library.include_dirs.fget(self)

        includes.append('-I "/usr/local/include/libusb-1.0"')

        return includes

    def clean(self, command_class):
        LOG.info(
            "Clean OpenZwave in {0} ... be patient ...".format(
                self.build_path
            )
        )
        command_class.spawn(
            ['make', 'PREFIX=/opt/local', 'clean'],
            cwd=self.openzwave
        )
