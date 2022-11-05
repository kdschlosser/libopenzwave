# -*- coding: utf-8 -*-

from . import library_base
import os
import platform


DARWIN_VERSION = tuple(int(item) for item in platform.release().split('.'))

if len(DARWIN_VERSION) < 3:
    DARWIN_VERSION += (0,)

if DARWIN_VERSION >= (10, 14, 0):
    DARWIN_MOJAVE_UP = True
else:
    DARWIN_MOJAVE_UP = False


class Library(library_base.Library):

    def __init__(
        self,
        define_macros=[],
        library_dirs=[],
        libraries=[],
        extra_compile_args=[],
        include_dirs=[],
        extra_link_args=[]
    ):

        library_base.Library.__init__(
            self,
            define_macros=define_macros,
            libraries=libraries,
            library_dirs=library_dirs,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            include_dirs=include_dirs
        )

        self._define_macros.append(('DARWIN',))

    @property
    def libraries(self):
        libs = [
            '-framework IOKit',
            '-framework CoreFoundation {0}'.format(' '.join(self.t_arch)),
            '-lresolv'
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
                'examples',
                'hidapi',
                'libusb',
                'test'
            ]
        )
        return sources

    @sources.setter
    def sources(self, _):
        pass

    @property
    def ar(self):
        ar = os.environ['AR']
        for item in ['-static', '-o']:
            if item not in ar:
                ar += ' ' + item
        return ar

    @property
    def shared_lib_name(self):
        return 'libopenzwave-{0}.dylib'.format(self.ozw_version_string)

    @property
    def shared_lib_no_version_name(self):
        return 'libopenzwave.dylib'

    @property
    def ld_flags(self):
        ld_flags = library_base.parse_flags('LDFLAGS')
        install_name = os.path.join(
            self.dest_path,
            self.lib_inst_path,
            self.shared_lib_name
        )

        for flag in (
            '-dynamiclib',
            '-install_name "{0}"'.format(install_name)
        ):
            if flag not in ld_flags:
                ld_flags.append(flag)

        if not self.builder.static:
            for flag in (
                '-shared',
                '-Wl,-soname,{0}'.format(self.shared_lib_name)
            ):
                if flag not in ld_flags:
                    ld_flags.append(flag)

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
            '-fPIC'
        ):
            if flag not in c_flags:
                c_flags.append(flag)

        return c_flags

    @property
    def cpp_flags(self):
        cpp_flags = library_base.parse_flags('CPPFLAGS')

        if '-std=c++11' not in cpp_flags:
            cpp_flags.append('-std=c++11')

        return cpp_flags

    @property
    def t_arch(self):
        if DARWIN_MOJAVE_UP:
            # Newer macOS releases don't support i386 so only build 64-bit
            tarch = ['-arch x86_64']
        else:
            # Support older versions of OSX that may need to
            # build both 32-bit and 64-bit
            tarch = ['-arch i386', '-arch x86_64']

        return tarch
