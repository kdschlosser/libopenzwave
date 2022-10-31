# -*- coding: utf-8 -*-

import os
from distutils import log as LOG

from . import library_base


class Library(library_base.Library):

    @property
    def ld(self):
        return os.environ['LD']

    @property
    def libraries(self):
        return []

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
    def obj_path(self):
        return self.openzwave + '/.lib'

    @property
    def dep_path(self):
        return self.openzwave + '/.dep'

    @property
    def ranlib(self):
        return os.environ['RANLIB']

    @property
    def ar(self):
        return os.environ['AR']

    @property
    def cc(self):
        return os.environ['CC']

    @property
    def cxx(self):
        return os.environ['CXX']

    @property
    def shared_lib_name(self):
        return 'libopenzwave.so.' + self.builder.ozw_version

    @property
    def shared_lib_no_version_name(self):
        return 'libopenzwave.so'

    @property
    def ld_flags(self):
        ld_flags = library_base.parse_flags(os.environ['LDFLAGS'])

        if not self.builder.static:
            ld_flags += [
                '-shared',
                '-lusb',
                '-Wl,',
                '-soname,',
                self.shared_lib_name
            ]
        return ld_flags

    @property
    def c_flags(self):
        c_flags = library_base.parse_flags(os.environ['CFLAGS']) + [
            '-c',
            '-Wall',
            '-Wno-unknown-pragmas',
            '-Werror',
            '-Wno-error=sequence-point',
            '-Wno-sequence-point',
            '-O3',
            '-DNDEBUG',
            '-fPIC',
            '-DSYSCONFDIR="/usr/local/etc/openzwave/"'
        ]

        command = [
            'test',
            '$(uname -U)',
            '-ge',
            '1002000;'
            'echo $?'
        ]

        from subprocess import Popen, PIPE

        p = Popen(command, stdout=PIPE, stderr=PIPE)

        if p.communicate()[0].strip() == '1':
            if not os.path.exists('/usr/local/include/iconv.h'):
                raise RuntimeError(
                    'FreeBSD pre 10.2: Please install libiconv from ports'
                )

            c_flags += '-I/usr/local/include'

        return c_flags

    @property
    def cpp_flags(self):
        cpp_flags = library_base.parse_flags(os.environ['CPPFLAGS']) + [
            '-std=c++11'
        ]

        return cpp_flags

    @property
    def include_dirs(self):
        include_dirs = [
            '-I' + os.path.join(self.openzwave, 'cpp', 'src'),
            '-I' + os.path.join(self.openzwave, 'cpp', 'tinyxml')
        ]
        return include_dirs

    @include_dirs.setter
    def include_dirs(self, _):
        pass

    def clean(self, command_class):
        LOG.info(
            "Clean OpenZwave in {0} ... be patient ...".format(
                self.build_path
            )
        )
        command_class.spawn(['gmake', 'clean'], cwd=self.openzwave)
