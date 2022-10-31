# -*- coding: utf-8 -*-

import os
from . import extension_base


class Extension(extension_base.Extension):

    def __call__(self, build_ext):
        build_ext.distribution.has_c_libraries = self.has_c_libraries

        extension_base.Extension.__call__(self, build_ext)

        if self.static:
            self.libraries += ['usb']
            self.extra_objects += [
                os.path.join(self.openzwave, 'libopenzwave.a')
            ]
            self.include_dirs += [
                os.path.join(self.openzwave, 'cpp', 'build', 'linux')
            ]
        else:
            self.libraries += ['openzwave']

        self.report_config()

    def __init__(self):
        libraries = []
        include_dirs = []
        extra_objects = []

        os.environ['CPPFLAGS'] = '-Wno-unused-private-field'

        define_macros = []
        sources = []
        extra_compile_args = [
            '-Wmacro-redefined',
            '-Wdeprecated-declarations'
        ]

        extension_base.Extension.__init__(
            self,
            extra_objects=extra_objects,
            sources=sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            libraries=libraries,
            extra_compile_args=extra_compile_args
        )
