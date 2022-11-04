# -*- coding: utf-8 -*-

from . import library_base
import os


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

        self._define_macros.extend([
            ('SYSCONFDIR', '"\\"{0}"\\"'.format(self.sys_config_path)),
            ('NDEBUG',)
        ])

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
            '-Werror',
            '-Wno-error=sequence-point',
            '-Wno-sequence-point',
            '-O3',
            '-fPIC'
        ):
            if flag not in c_flags:
                c_flags.append(flag)

        return c_flags

    def __call__(self, openzwave):
        library_base.Library.__call__(self, openzwave)
