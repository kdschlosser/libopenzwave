# -*- coding: utf-8 -*-

from . import library_base
import os


class Library(library_base.Library):

    def __init__(
        self,
        define_macros=[],  # NOQA
        library_dirs=[],  # NOQA
        libraries=[],  # NOQA
        extra_compile_args=[],  # NOQA
        include_dirs=[],  # NOQA
        extra_link_args=[]  # NOQA
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
    def ld_flags(self):
        ld_flags = library_base.parse_flags('LDFLAGS')

        if not self.builder.static:
            ld_flags.append('-shared')
            ld_flags.append('-Wl,-soname,{0}'.format(self.shared_lib_name))

        return ld_flags

    @property
    def c_flags(self):
        c_flags = library_base.parse_flags('CFLAGS')

        for flag in (
            '-c',
            '-Wall',
            '-Wno-unknown-pragmas',
            '-Wno-sequence-point',
            '-Wno-nonnull',
            '-O3',
            '-fPIC'
        ):
            if flag not in c_flags:
                c_flags.append(flag)

        return c_flags
