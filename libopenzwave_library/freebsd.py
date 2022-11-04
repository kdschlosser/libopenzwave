# -*- coding: utf-8 -*-

import os
from distutils import log as LOG

from . import library_base
import platform


FREEBSD_VERSION = tuple(int(item) for item in platform.release().split('.'))

if len(FREEBSD_VERSION) < 3:
    FREEBSD_VERSION += (0,)

if FREEBSD_VERSION >= (10, 2, 0):
    FREEBSD_10_2_UP = True
else:
    FREEBSD_10_2_UP = False


class Library(library_base.Library):

    @property
    def include_dirs(self):
        includes = library_base.Library.include_dirs.fget(self)

        if not FREEBSD_10_2_UP:
            includes.append('-I "/usr/local/include"')

        return includes

    @property
    def libraries(self):
        libs = ['-lresolv', '-lusb']
        # if not FREEBSD_10_2_UP:
        #     libs.append('-liconv')

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
            ld_flags.append('-shared')
            ld_flags.append('-Wl,-soname,{0}'.format(self.shared_lib_name))

        # if not FREEBSD_10_2_UP:
        #     ld_flags += ['-L "/usr/local/lib"']

        return ld_flags

    @property
    def c_flags(self):
        c_flags = library_base.parse_flags(os.environ['CFLAGS'])

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
