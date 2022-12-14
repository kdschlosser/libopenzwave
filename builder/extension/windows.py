# -*- coding: utf-8 -*-

import os
import sys
from . import extension_base
from builder import environment

DEBUG_BUILD = os.path.splitext(sys.executable)[0].endswith('_d')


class Extension(extension_base.Extension):

    def __call__(self, build_ext):

        if float(environment.win_env.visual_c.version.rsplit('.')[0]) > 10.0:
            # these compiler flags are not valid on
            # Visual C++ version 10.0 and older

            self.extra_compile_args += [  # NOQA
                # Forces writes to the program database (PDB) file to be
                # serialized through MSPDBSRV.EXE.
                '/FS',
                # Specifies standard behavior
                '/Zc:inline'
            ]

        self.libraries += environment.win_env.python.libraries  # NOQA

        extension_base.Extension.__call__(self, build_ext)

        cpp_path = os.path.join(self.openzwave, 'cpp')
        src_path = os.path.join(cpp_path, 'src')
        if self.static:
            # this is a really goofy thing to have to do. But distutils will
            # pitch a fit if we try to run the linker without a PyInit
            # expression. it does absolutely nothing. Decoration I guess.
            build_clib = build_ext.distribution.get_command_obj('build_clib')

            self.extra_objects += [  # NOQA
                os.path.join(build_clib.build_clib, 'OpenZWave.lib')
            ]

            self.include_dirs += [  # NOQA
                build_clib.build_clib,
                os.path.join(cpp_path, 'build', 'windows'),
            ]

        else:
            self.libraries += ["OpenZWave"]  # NOQA
            self.extra_compile_args += [  # NOQA
                src_path,
                os.path.join(src_path, 'value_classes'),
                os.path.join(src_path, 'platform'),
            ]

        self.extra_link_args += ['/NODEFAULTLIB:LIBCMT', '/debug:full']  # NOQA
        self.report_config()

    def __init__(self):
        extra_objects = []
        define_macros = []
        sources = []
        include_dirs = ['_libopenzwave']

        libraries = []
        extra_compile_args = [
            # Enables function-level linking.
            '/Gy',
            # Creates fast code.
            '/O2',
            # Uses the __cdecl calling convention (x86 only).
            '/Gd',
            # Omits frame pointer (x86 only).
            '/Oy',
            # Generates intrinsic functions.
            '/Oi',
            # Specify floating-point behavior.
            '/Zi',
            '/Ox',
            '/fp:precise',
            # Specifies standard behavior
            '/Zc:wchar_t',
            # Specifies standard behavior
            '/Zc:forScope',
            # I cannot remember what this does. I do know it does get rid of
            # a compiler warning
            '/EHsc',
            # compiler warnings to ignore
            '/wd4996',
            '/wd4244',
            '/wd4005',
            '/wd4800',
            '/wd4351',
            '/wd4273'
        ]

        if DEBUG_BUILD:
            define_macros += [('_DEBUG', 1)]
            libraries += ["setupapi", "msvcrtd", "ws2_32", "dnsapi"]
        else:
            libraries += ["setupapi", "msvcrt", "ws2_32", "dnsapi"]

        extension_base.Extension.__init__(
            self,
            extra_objects=extra_objects,
            sources=sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            libraries=libraries,
            extra_compile_args=extra_compile_args,
        )
