# -*- coding: utf-8 -*-

from . import library_base
import os


class Library(library_base.Library):

    @property
    def libraries(self):
        return [
            '-lresolv',
            '-framework IOKit',
            '-framework CoreFoundation',
        ]

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
    def obj_path(self):
        return self.openzwave + '/.lib'

    @property
    def dep_path(self):
        return self.openzwave + '/.dep'

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
        return 'clang'

    @property
    def cxx(self):
        if 'CXX' in os.environ:
            return os.environ['CXX']
        return 'clang++'

    @property
    def ld(self):
        if 'LD' in os.environ:
            return os.environ['LD']
        return self.cxx

    @property
    def shared_lib_name(self):
        return 'libopenzwave-{0}.dylib'.format(self.builder.ozw_version)

    @property
    def shared_lib_no_version_name(self):
        return 'libopenzwave.dylib'

    @property
    def ld_flags(self):
        ld_flags = library_base.parse_flags('LDFLAGS')

        ld_flags += [
            '-dynamiclib',
            '-install_name "{0}"'.format(
                os.path.join(
                    self.dest_path,
                    self.lib_inst_path,
                    self.shared_lib_name
                )
            )
        ]

        if not self.builder.static:
            ld_flags += [
                '-shared',
                '-Wl,',
                '-soname,',
                self.shared_lib_name
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
            '-fPIC',
            '-DDARWIN'
        ]

        return c_flags

    @property
    def cpp_flags(self):
        cpp_flags = library_base.parse_flags('CPPFLAGS') + [
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

    @property
    def t_arch(self):
        from subprocess import Popen, PIPE

        command = ['sw_vers', '-productVersion']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        darwin_version = p.communicate()[0].strip().decode('utf-8')
        mojave = float('.'.join(darwin_version.split('.')[:2])) >= 10.14

        if mojave:
            # Newer macOS releases don't support i386 so only build 64-bit
            target = ['-arch x86_64']
        else:
            target = ['-arch i386, -arch x86_64']

        return target
