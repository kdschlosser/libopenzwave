# -*- coding: utf-8 -*-

from setuptools.command.build_clib import build_clib as _build_clib  # NOQA
import distutils.dir_util
import sys
import os
import subprocess
import threading
from distutils import log as LOG  # NOQA

DUMMY_RETURN = b''
FILE_TYPES = [b'.cpp', b'.c']
COMPILERS = ['g++', 'gcc', 'clang', 'clang++', 'cc', 'c++']


if sys.platform.startswith('win'):
    SHELL = 'cmd'
else:
    SHELL = 'bash'

# this is a thread lock for printing. I use 10 threads in the windows
# compilation of openzwave to compile it. it speeds up the build process a lot.
# but we do not want to get the output all jumbled up so before printing
# anything from the output buffer we use this lock before we print the
# output buffer to stdout or stderr. we iterate over the output buffer line
# by line so if this lock is not in place the lines that get printed would be
# out of order.
print_lock = threading.Lock()


class build_clib(_build_clib):
    is_finalized = False
    # I have created this class in a manner that will allow it to be used
    # commonly between the different OS's if you look in pyozw_win you will
    # find a subclass of this class. It will show how to setup the build
    # process for the other OS's. You can if you want to have distutils
    # handle all of the building of openzwave as i did for Windows. You will
    # need to set all of the proper compiler arguments. If you do not want to
    # do that then all you would need to do is call spawn with the proper
    # "make" to build it. either way this is a more streamlined mechanism.
    # it also allows you to easily maintain the code because the code for a
    # specific OS is all grouped together.

    def build_libraries(self, libraries):
        self.compiled_files = []  # NOQA
        self.compiler.spawn = self.spawn
        self.compiler.mkpath = self.mkpath

        for lib in self.original_libraries:
            extension = self.distribution.ext_modules[0]  # NOQA
            build = self.distribution.get_command_obj('build')  # NOQA

            if (
                len(extension.extra_objects) == 1 and
                os.path.isfile(extension.extra_objects[0])
            ):
                LOG.info(
                    'Using cached build of _libopenzwave'
                )
            else:
                LOG.info(
                    "building '{0}' library".format(lib.name)
                )
                lib.build(self, build)

    # we override this method because the original method only known how to
    # process a dict for the library information. I opted to use a class as
    # this is far easier to deal with when adding or changing any of the values
    # so here we create the dict from the class that is wanted by build_clib.
    def finalize_options(self):
        if self.is_finalized:
            return

        self.is_finalized = True
        builder = self.distribution.get_command_obj('build')  # NOQA
        builder.ensure_finalized()

        openzwave = builder.openzwave
        self.build_clib = os.path.join(
            builder.build_temp,
            'lib_build'
        )

        self.build_temp = os.path.join(
            builder.build_temp,
            'lib_build_temp'
        )

        if not os.path.exists(self.build_clib):
            os.makedirs(self.build_clib)

        if sys.platform.startswith('win'):
            self.compiler = 'msvc'
        else:
            self.compiler = 'unix'

        libraries = self.distribution.libraries  # NOQA
        self.original_libraries = libraries  # NOQA

        converted_libraries = []

        for lib in libraries:
            lib(self, openzwave)
            build_info = dict(
                sources=lib.sources,
                macros=lib.define_macros,
                include_dirs=lib.include_dirs,
            )

            converted_libraries += [(lib.name, build_info)]

        self.distribution.libraries = converted_libraries  # NOQA

        _build_clib.finalize_options(self)

    # we override the compilers mkpath so we can inject the verbose option.
    # the compilers version does not allow for setting of a verbose level
    # and distutils.dir_util.mkpath defaults to a verbose level of 1 which
    # which prints out each and every directory it makes. This congests the
    # output unnecessarily.
    def mkpath(self, name, mode=0o777):
        distutils.dir_util.mkpath(
            name,
            mode,
            dry_run=self.compiler.dry_run,
            verbose=0
        )

    # this is the workhorse of the build process. it is a mechanism i use to
    # buffer the output from subprocess.Popen and allows me to grab one line
    # at a time as it becomes available. This eliminates any jumping or long
    # pauses in information being written to the screen. This is far simpler
    # then creating additional threads and using queue to pass information off
    # to another thread to print the output. there is also no stalling the
    # thread to wait for output.

    def spawn(self, cmd, search_path=1, level=1, cwd=None):
        if isinstance(cmd, (list, tuple)):
            cmd_debug = ' '.join(str(item) for item in cmd)
        else:
            cmd_debug = cmd

        LOG.debug(cmd_debug)

        if sys.platform.startswith('win'):
            p = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                cwd=cwd
            )
        else:
            p = subprocess.Popen(
                SHELL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                cwd=cwd
            )

            cmd_debug += '\n'
            p.stdin.write(cmd_debug.encode('utf-8'))
            p.stdin.close()

        while p.poll() is None:
            with print_lock:
                for line in iter(p.stdout.readline, DUMMY_RETURN):
                    line = line.strip()
                    if line:
                        LOG.debug(line)

                        if sys.platform.startswith('win'):
                            for file_type in FILE_TYPES:
                                if line.endswith(file_type):
                                    break
                            else:
                                sys.stdout.write(
                                    line.decode('utf-8') + '\n'
                                )

                            f = line

                            new_line = b'compiling ' + f + b'...'
                            sys.stdout.write(
                                new_line.decode('utf-8') + '\n'
                            )

                        else:
                            sys.stdout.write(
                                line.decode('utf-8') + '\n'
                            )
                        #
                        #     for compiler in COMPILERS:
                        #         if cmd.startswith(compiler):
                        #             break
                        #     else:
                        #         continue
                        #
                        #     if compiler.endswith('++'):
                        #         file_type = '.cpp'
                        #     else:
                        #         file_type = '.c'
                        #
                        #     f = line.split(file_type, 1)
                        #     f = f[0].rsplit(' ', 1)[-1] + file_type
                        #     f = os.path.split(f)[1]
                        #
                        # if f in self.compiled_files:
                        #     continue
                        #
                        # self.compiled_files += [f]

                        sys.stdout.flush()

                for line in iter(p.stderr.readline, DUMMY_RETURN):
                    line = line.strip()
                    if line:
                        sys.stderr.write(line.decode('utf-8') + '\n')
                        sys.stderr.flush()

        if not p.stdout.closed:
            p.stdout.close()

        if not p.stderr.closed:
            p.stderr.close()

        sys.stdout.flush()
        sys.stderr.flush()
