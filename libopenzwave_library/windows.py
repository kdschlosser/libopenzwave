# -*- coding: utf-8 -*-

from distutils import log as LOG
import os
import sys
import shutil
import pyMSVC

from . import library_base

environment = pyMSVC.setup_environment()
print(environment)

# read further down as to what this is for
DLL_MAIN = '''

void PyInit_OpenZwave() {}

'''

# this is an easy macro to tell if a debugging version of python is what is
# running if it is what is running then we want to build a debugging version
# of openzwave. the use of this will allow you to set any preprocessor
# macros to build a debugging version of openzwave
DEBUG_BUILD = os.path.splitext(sys.executable)[0].endswith('_d')


# in order to have distutils handle the building of openzwave there has to be
# a call to PyInit so we create a cpp file and place the call in it. The call
# actually does nothing except allow openzwave to be built.

# When running a build on linux the makefile handles the creation of the
# openzwave version file. if you build openzwave using visual studio the same
# is done. Since we are letting distutils handle the compiling of openzwave
# we need to create that version file ourselves.
# that is what this function does.

class Library(library_base.Library):

    def build_dll_main(self):
        dll_main_path = self.openzwave + '\\cpp\\dllmain.cpp'
        with open(dll_main_path, 'w') as f:
            f.write(DLL_MAIN)

    def build_version_file(self):

        template = (
            'unsigned short ozw_vers_major = {major};\n' 
            'unsigned short ozw_vers_minor = {minor};\n' 
            'unsigned short ozw_vers_revision = {revision};\n' 
            'char ozw_version_string[] = "{version}.{revision}\0";'
        )

        import libopenzwave_version

        minor = libopenzwave_version.OZW_VERSION_MIN
        major = libopenzwave_version.OZW_VERSION_MAJ
        version = libopenzwave_version.OZW_VERSION
        revision = libopenzwave_version.OZW_VERSION_REV
        if revision == -1:
            revision = 0

        template = template.format(
            minor=minor,
            major=major,
            version=version,
            revision=revision
        )

        version_dir = os.path.abspath(
            os.path.join(
                self.openzwave,
                'cpp',
                'build',
                'windows',
            )
        )
        version_file = os.path.join(
            version_dir,
            'winversion.cpp'
        )

        with open(version_file, 'w') as f:
            f.write(template)

        self.build_dll_main()

    @property
    def sources(self):
        return library_base.get_sources(
            os.path.join(self.openzwave, 'cpp'),
            ignore=[
                'unix',
                'winrt',
                'mac',
                'linux',
                'examples',
                'libusb',
                'test'
            ]
        )

    @sources.setter
    def sources(self, _):
        pass

    @property
    def include_dirs(self):
        cpp_path = os.path.join(os.path.relpath(self.openzwave), 'cpp')
        includes = [
            '/I{0}'.format(os.path.join(cpp_path, 'src')),
            '/I{0}'.format(os.path.join(cpp_path, 'tinyxml')),
            '/I{0}'.format(os.path.join(cpp_path, 'hidapi', 'hidapi'))
        ]
        includes += list(
            '/I{0}'.format(itm) for itm in os.environ['INCLUDE'].split(';')
        )

        includes += list(
            '/I{0}'.format(itm) for itm in environment.python.libraries
        )
        return includes

    @include_dirs.setter
    def include_dirs(self, _):
        pass

    @property
    def libraries(self):
        return ['setupapi', environment.python.dependency[:-4]]

    @libraries.setter
    def libraries(self, _):
        pass

    def compile_c(self, c_file, build_clib):
        object_file = os.path.split(c_file)[-1]
        object_file = os.path.join(
            os.path.abspath(self.obj_path),
            os.path.splitext(object_file)[0] + '.obj'
        )

        command = ['cl.exe']
        command += self.extra_compile_args
        command += self.define_macros
        command += self.include_dirs
        command += ['/Tc' + c_file]
        command += ['/Fo' + object_file]

        build_clib.spawn(command)
        return object_file

    def compile_cpp(self, cpp_file, build_clib):
        object_file = os.path.split(cpp_file)[-1]
        object_file = os.path.join(
            os.path.abspath(self.obj_path),
            os.path.splitext(object_file)[0] + '.obj'
        )

        command = ['cl.exe']
        command += self.extra_compile_args
        command += self.define_macros
        command += self.include_dirs
        command += ['/Tp' + cpp_file]
        command += ['/Fo' + object_file]

        build_clib.spawn(command)
        return object_file

    def __init__(self):
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
            '/Zi',
            '/Ox',
            # Renames program database file.
            # '/Fdbuild\\lib_build\\OpenZWave.pdb'.format(self.build_path),
            # Specify floating-point behavior.
            '/fp:precise',
            # Specifies standard behavior
            '/Zc:wchar_t',
            # Specifies standard behavior
            '/Zc:forScope',
            # I cannot remember what this does. I do know it does get rid of
            # a compiler warning
            '/EHsc',
            # compiler warnings to ignore
            '/wd4251',
            '/wd4244',
            '/wd4101',
            '/wd4267',
            '/wd4996',
            '/wd4351',
            '/c',
            '/nologo',
            '/Ox',
            '/W3',
            '/GL',
            '/MT',
        ]

        if float(environment.visual_c.version.rsplit('.', 1)[0]) > 10.0:
            # these compiler flags are not valid on
            # Visual C++ version 10.0 and older

            extra_compile_args += [
                # Forces writes to the program database (PDB) file to be
                # serialized through MSPDBSRV.EXE.
                '/FS',
                # Specifies standard behavior
                '/Zc:inline'
            ]

        self.files_to_compile = {}

        # not used but here for completeness.
        extra_link_args = [
            '/LTCG',
            '/MACHINE:' + environment.platform.upper(),
            '/NOLOGO',
            '/WX:NO',
        ]

        libraries = []
        library_dirs = []

        library_base.Library.__init__(
            self,
            libraries=libraries,
            library_dirs=library_dirs,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args
        )

        self._define_macros = [
            '/DWIN32=1',
            '/D_MBCS=1',
            '/D_LIB=1',
            '/D_MT=1',
            '/D_DLL=1',
            '/DOPENZWAVE_MAKEDLL=1'
        ]

        if DEBUG_BUILD:
            self._define_macros += ['/DDEBUG=1']
        else:
            self._define_macros += ['/DNDEBUG=1']

        if environment.platform == 'x64':
            self._define_macros += ['/DWIN64=1']

    @property
    def define_macros(self):
        return self._define_macros

    def install(self, command_class):
        pass

    def call_compiler(self, files, build_clib):
        objs = build_clib.compiler.compile(
            files,
            output_dir=build_clib.build_temp,
            macros=self.define_macros,
            include_dirs=self.include_dirs,
            extra_preargs=self.extra_compile_args,
            debug=build_clib.debug
        )

        return objs

    @property
    def lib_inst_path(self):
        return 'lib_build'

    def link_static(self, objects, build_clib):

        lib_file = os.path.join(build_clib.build_clib, self.name + '.lib')

        command = ['lib.exe']
        command += self.extra_link_args
        command += objects
        command += ['/OUT:' + lib_file]
        build_clib.spawn(command)

        # build_clib.compiler.create_static_lib(
        #     objects,
        #     self.name,
        #     output_dir=build_clib.build_clib,
        #     debug=build_clib.debug
        # )

    @property
    def dep_path(self):
        return self.obj_path

    @property
    def obj_path(self):
        path = library_base.Library.obj_path.fget(self)
        return os.path.split(path)[0]

    def link_shared(self, objects, build_clib):
        pass

    def clean(self, _):
        LOG.info(
            "Clean OpenZwave in {0} ... be patient ...".format(
                self.build_path
            )
        )
        try:
            shutil.rmtree(self.build_path)
        except OSError:
            pass
