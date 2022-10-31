# -*- coding: utf-8 -*-

from . import library_base
import os


class Library(library_base.Library):

    @property
    def ld(self):
        if 'LD' in os.environ:
            return os.environ['LD']
        return 'ld'

    @property
    def libraries(self):
        return ['-lresolv']

    @libraries.setter
    def libraries(self, _):
        pass

    @property
    def sources(self):
        sources = library_base.get_sources(
            os.path.join(self.openzwave, 'cpp'),
            ignore=[
                'windows',
                'build',
                'winrt',
                'mac',
                'hidapi',
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
        return os.path.join(self.openzwave, '.lib')

    @property
    def dep_path(self):
        return os.path.join(self.openzwave, '.dep')

    @property
    def ranlib(self):
        if 'RANLIB' in os.environ:
            return os.environ['RANLIB']
        return 'ranlib'

    @property
    def ar(self):
        if 'AR' in os.environ:
            return os.environ['AR']
        return 'ar'

    @property
    def cc(self):
        if 'CC' in os.environ:
            return os.environ['CC']
        return 'gcc'

    @property
    def cxx(self):
        if 'CXX' in os.environ:
            return os.environ['CXX']
        return 'g++'

    @property
    def shared_lib_name(self):
        return 'libopenzwave.so.' + self.ozw_version_string.rsplit('.', 1)[0]

    @property
    def shared_lib_no_version_name(self):
        return 'libopenzwave.so'

    @property
    def ld_flags(self):
        ld_flags = library_base.parse_flags('LDFLAGS')

        if not self.builder.static:
            ld_flags += [
                '-shared',
                '-Wl,',
                '-soname,' + self.shared_lib_name
            ]
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
            '-DNDEBUG',
            '-fPIC'
        ]

        return c_flags

    @property
    def cpp_flags(self):
        cpp_flags = library_base.parse_flags('CPPFLAGS') + [
            ' -std=c++11'
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

    def __call__(self, openzwave):
        library_base.Library.__call__(self, openzwave)

    def __init__(self):
        define_macros = []
        library_dirs = []
        libraries = []
        extra_compile_args = []
        include_dirs = []
        extra_link_args = []

        library_base.Library.__init__(
            self,
            define_macros=define_macros,
            libraries=libraries,
            library_dirs=library_dirs,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            include_dirs=include_dirs
        )

    @property
    def packages(self):

        args = [
            'pkg-config',
            'build-essential',
            'libudev-dev',
            'g++',
            'libyaml-dev',
            'libstdc++6',
            'libudev1',
            'libc6',

        ]

        command = [
            'apt-get',
            'install',
            '--assume-yes'
        ] + args

        return command
