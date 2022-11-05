# -*- coding: utf-8 -*-

import os
from distutils import log as LOG

from . import library_base
import libopenzwave_pkgconfig


class Library(library_base.Library):

    @property
    def fmt_cmd(self):
        return 'fmt -g 1'

    @property
    def include_dirs(self):
        includes = library_base.Library.include_dirs.fget(self)
        includes.append(libopenzwave_pkgconfig.cflags('libusb-1.0'))

        return includes

    @property
    def libraries(self):
        libs = [
            '-lresolv',
            libopenzwave_pkgconfig.libs('libusb-1.0')
        ]
        return libs

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
                'examples',
                'libusb',
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
        c_flags = library_base.parse_flags('CFLAGS')

        for flag in (
            '-c',
            '-Wall',
            '-Wno-unknown-pragmas',
            '-Werror',
            '-Wno-error=sequence-point',
            '-Wno-sequence-point',
            '-O3',
            '-fPIC',
        ):
            if flag not in c_flags:
                c_flags.append(flag)

        return c_flags

    def clean(self, command_class):
        LOG.info(
            "Clean OpenZwave in {0} ... be patient ...".format(
                self.build_path
            )
        )
        command_class.spawn(['gmake', 'clean'], cwd=self.openzwave)
