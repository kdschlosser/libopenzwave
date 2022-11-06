# -*- coding: utf-8 -*-

import os
from . import extension_base


class Extension(extension_base.Extension):

    def __call__(self, build_ext):
        build_ext.distribution.has_c_libraries = self.has_c_libraries

        extension_base.Extension.__call__(self, build_ext)

        if self.static:
            self.libraries += ['resolv']

            build_clib = build_ext.distribution.get_command_obj('build_clib')
            self.extra_objects += [
                os.path.join(build_clib.build_clib, 'libopenzwave.a')
            ]

            self.include_dirs += [
                os.path.join(self.openzwave, 'cpp', 'build', 'linux')
            ]

        else:
            import libopenzwave_pkgconfig

            self.libraries += ["openzwave"]
            extra = libopenzwave_pkgconfig.cflags('libopenzwave')
            if extra != '':
                for ssubstitute in ['', 'value_classes', 'platform']:
                    self.extra_compile_args += [
                        os.path.normpath(os.path.join(extra, ssubstitute))
                    ]

        self.report_config()

    def __init__(self):
        libraries = []
        include_dirs = []
        extra_objects = []

        define_macros = []
        sources = []

        extra_link_args = [
            '-std=c++11'
        ]
        extra_compile_args = [
            '-std=c++11',
            '-Wno-builtin-macro-redefined',
            '-Wno-deprecated-declarations',
            '-Wno-deprecated',
            '-Wno-unreachable-code-fallthrough'
        ]

        extension_base.Extension.__init__(
            self,
            extra_link_args=extra_link_args,
            extra_objects=extra_objects,
            sources=sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            libraries=libraries,
            extra_compile_args=extra_compile_args
        )
