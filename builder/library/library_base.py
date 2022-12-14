# -*- coding: utf-8 -*-
import os
from distutils import log as LOG
import sys
import threading
import shutil

from builder import environment
import version

dummy_return = b''


def parse_flags(env_param):
    if env_param in os.environ:
        flags = os.environ[env_param]
    else:
        flags = ''

    out_flags = []
    single_quote_count = 0
    double_quote_count = 0

    last_char = ''
    for char in list(flags):
        if char == '"':
            if last_char == '\\':
                continue

            if double_quote_count:
                double_quote_count -= 1
            else:
                double_quote_count += 1

        elif char == "'":
            if last_char == '\\':
                continue
            if single_quote_count:
                single_quote_count -= 1
            else:
                single_quote_count += 1
        elif (
            char == ' ' and
            not single_quote_count and
            not double_quote_count
        ):
            out_flags += ['']
            continue

        out_flags[len(out_flags) - 1] += char

    return out_flags


def get_sources(src_path, ignore):
    found = []
    for src_f in os.listdir(src_path):
        src = os.path.join(src_path, src_f)
        if os.path.isdir(src):
            if src_f.lower() in ignore:
                continue
            if src.lower() in ignore:
                continue

            found += get_sources(src, ignore)
        elif src_f.endswith('.c') or src_f.endswith('.cpp'):
            found += [src]
    return found


class Library(object):

    def __init__(
        self,
        sources=[],  # NOQA
        define_macros=[],  # NOQA
        libraries=[],  # NOQA
        library_dirs=[],  # NOQA
        include_dirs=[],  # NOQA
        extra_compile_args=[],  # NOQA
        extra_link_args=[]  # NOQA
    ):
        self.openzwave = ''
        self.name = 'OpenZWave'
        self.sources = sources
        self._define_macros = define_macros
        self.libraries = libraries
        self.library_dirs = library_dirs
        self._include_dirs = include_dirs
        self.extra_compile_args = extra_compile_args
        self.extra_link_args = extra_link_args
        self.build_path = ''
        self.builder = None
        self.dest_path = None
        self.print_lock = threading.Lock()
        self.running_threads = {}
        self.build_path = ''
        self.build_temp_path = ''

        self._define_macros.extend([
            ('SYSCONFDIR', '"\\"{0}"\\"'.format(self.sys_config_path)),
            ('NDEBUG',)
        ])

        # packages = self.packages
        #
        # if packages:
        #     p = subprocess.Popen(
        #         packages,
        #         stdout=subprocess.PIPE,
        #         stderr=subprocess.PIPE
        #     )
        #
        #     while p.poll() is None:
        #         for line in iter(p.stdout.readline, dummy_return):
        #             line = line.strip()
        #             if line:
        #                 sys.stdout.write(line.decode('utf-8') + '\n')
        #                 sys.stdout.flush()
        #
        #         for line in iter(p.stderr.readline, dummy_return):
        #             line = line.strip()
        #             if line:
        #                 sys.stderr.write(line.decode('utf-8') + '\n')
        #                 sys.stderr.flush()
        #
        #     if not p.stdout.closed:
        #         p.stdout.close()
        #
        #     if not p.stderr.closed:
        #         p.stderr.close()
        #
        #     sys.stdout.flush()
        #     sys.stderr.flush()

    @property
    def include_dirs(self):
        includes = []

        include_dirs = self._include_dirs

        for include in (
            os.path.join(self.openzwave, 'cpp', 'src'),
            os.path.join(self.openzwave, 'cpp', 'tinyxml')
        ):
            if include not in include_dirs:
                include_dirs.append(include)

        for include in include_dirs:
            includes.append('-I "{0}"'.format(include))

        return includes

    @property
    def make(self):
        return environment.MAKE

    @property
    def ar(self):
        return environment.AR

    @property
    def ld(self):
        return environment.LD

    @property
    def ranlib(self):
        return environment.RANLIB

    @property
    def cc(self):
        return environment.C

    @property
    def cxx(self):
        return environment.CPP

    @property
    def pkg_config_path(self):
        return environment.PACKAGE_CONFIG

    @property
    def ozw_version_string(self):
        vers = [
            version.OZW_VERSION_MAJ,
            version.OZW_VERSION_MIN,
            version.OZW_VERSION_REV
        ]
        return '.'.join(vers)

    @property
    def prefix(self):
        return os.path.join('/usr', 'local')

    @property
    def sys_config_path(self):
        return os.path.join('etc', 'openzwave')

    @property
    def include_path(self):
        return os.path.join(self.prefix, 'include', 'openzwave')

    @property
    def shared_lib_name(self):
        return 'libopenzwave.so.{0}'.format(self.ozw_version_string)

    @property
    def shared_lib_no_version_name(self):
        return 'libopenzwave.so'

    @property
    def lib_inst_path(self):
        if os.path.exists('openzwave/build/lib_build'):
            return 'openzwave/build/lib_build'

        if os.path.exists('/usr/lib64'):
            path = 'lib64'
        else:
            path = 'lib'

        path += '.' + self.machine
        if self.builder.static:
            return path
        else:
            return os.path.join(self.prefix, path)

    @property
    def machine(self):
        if sys.maxsize ** 32 > 64:
            return 'x86_64'
        else:
            return 'i686'

    @property
    def define_macros(self):
        macros = []
        for macro in self._define_macros:
            if len(macro) == 2:
                macros.append('-D{0}={1}'.format(*macro))
            else:
                macros.append('-D' + macro[0])
        return macros

    @property
    def t_arch(self):
        return []

    @property
    def ld_flags(self):
        return parse_flags('LDFLAGS')

    @property
    def c_flags(self):
        return parse_flags('CFLAGS')

    @property
    def cpp_flags(self):
        cpp_flags = parse_flags('CPPFLAGS')

        if version.OZW_VERSION >= (1, 7):
            if '-std=c++20' not in cpp_flags:
                cpp_flags.append('-std:c++20')
        elif '-std=c++11' not in cpp_flags:
            cpp_flags.append('-std=c++11')

        return cpp_flags

    @property
    def libraries(self):
        return ['-lresolv']

    @libraries.setter
    def libraries(self, _):
        pass

    @property
    def obj_path(self):
        return os.path.join(self.build_temp_path, '.lib')

    @property
    def dep_path(self):
        return os.path.join(self.build_temp_path, '.dep')

    @property
    def so_path(self):
        if self.pkg_config_path is not None:
            from builder import pkgconfig

            LOG.info(
                "Running ldconfig on libopenzwave... be patient ..."
            )

            ldpath = pkgconfig.libs_only_l('libopenzwave')[2:]

            return ldpath
        return ''

    def build_version_file(self):
        version_file = os.path.join(self.openzwave, 'cpp', 'src', 'vers.cpp')

        with self.print_lock:
            LOG.info('generating {0} ...'.format(version_file))

        template = [
            '#include "Defs.h"',
            'uint16_t ozw_vers_major = {VERSION_MAJ};',
            'uint16_t ozw_vers_minor = {VERSION_MIN};',
            'uint16_t ozw_vers_revision = {VERSION_REV};',
            'char ozw_version_string[] = "{VERSION_STRING}";'
        ]

        template = '\n'.join(template)

        template = template.format(
            VERSION_MAJ=version.OZW_VERSION_MAJ,
            VERSION_MIN=version.OZW_VERSION_MIN,
            VERSION_REV=version.OZW_VERSION_REV,
            VERSION_STRING=self.ozw_version_string,
        )

        with open(version_file, 'w') as f:
            f.write(template)

    def build_spec_file(self):
        spec_in = os.path.join(self.openzwave, 'dist', 'openzwave.spec.in')
        spec_out = spec_in.rsplit('.', 1)[0]

        with self.print_lock:
            LOG.info('generating {0} ...'.format(spec_out))

        with open(spec_in, 'r') as f:
            spec = f.read()

        spec = spec.replace('@VERSION@', self.ozw_version_string)

        with open(spec_out, 'w') as f:
            f.write(spec)

    def update_value_indexes(self, build_clib):
        with self.print_lock:
            sys.stdout.write('updating value index definitions ....\n')
            sys.stdout.flush()

        value_index_defines = os.path.join(
            self.openzwave,
            'cpp',
            'src',
            'ValueIDIndexesDefines'
        )

        command = [self.cxx, '-E', '-P', '-o']
        command += [value_index_defines + '.h']
        command += ['-x', 'c++', value_index_defines + '.def']
        build_clib.spawn(command)

    def link_static(self, objects, build_clib):
        libopenzwave = '"' + os.path.join(
            self.build_path,
            'libopenzwave.a'
        ) + '"'

        if os.path.exists(libopenzwave):
            return

        with self.print_lock:
            LOG.info('linking static library...')

        objects = list('"' + obj + '"' for obj in objects)

        command = [self.ar, libopenzwave] + objects

        build_clib.spawn(command)

        command = [self.ranlib, libopenzwave]

        build_clib.spawn(command)

    def link_shared(self, objects, build_clib):
        libopenzwave_lib_no_version = os.path.join(
            self.build_temp_path,
            self.shared_lib_no_version_name
        )

        libopenzwave_lib = os.path.join(
            self.build_temp_path,
            self.shared_lib_name
        )

        if os.path.exists(libopenzwave_lib_no_version):
            return

        with self.print_lock:
            LOG.info('linking shared library...')

        command = [self.ld] + self.ld_flags + self.t_arch
        command += ['-o', libopenzwave_lib]
        command += objects + self.libraries
        build_clib.spawn(command)

        command = [
            'ln',
            '-sf',
            libopenzwave_lib,
            libopenzwave_lib_no_version
        ]
        build_clib.spawn(command)
        build_clib.spawn(['ldconfig', self.so_path], cwd=self.build_temp_path)

    def build_pkg_config_file(self):
        pc_path = os.path.join(self.openzwave, 'libopenzwave.pc')
        pc_in_path = os.path.join(
            self.openzwave,
            'cpp',
            'build',
            'libopenzwave.pc.in'
        )

        with self.print_lock:
            LOG.info('generating {0} ...'.format(pc_path))

        exec_prefix = os.path.join(self.prefix, 'bin')

        with open(pc_in_path, 'r') as f:
            pc = f.read()

        replacements = [
            ('@prefix@', self.prefix),
            ('@exec_prefix@', exec_prefix),
            ('@libdir@', self.lib_inst_path),
            ('@includedir@', self.include_path),
            ('@sysconfdir@', self.sys_config_path),
            ('@gitversion@', self.ozw_version_string),
            ('@VERSION@', self.ozw_version_string),
            ('@LIBS@', ' '.join(lib[2:] for lib in self.libraries))
        ]

        for pattern, value in replacements:
            pc = pc.replace(pattern, value)

        with open(pc_path, 'w') as f:
            f.write(pc)

    def build_config_file(self):
        if self.pkg_config_path is None:
            with self.print_lock:
                LOG.info('skipping config file generation ...')

            return

        config_in_path = os.path.join(
            self.openzwave,
            'cpp',
            'build',
            'ozw_config.in'
        )

        config_path = config_in_path.rsplit('.', 1)[0]

        with self.print_lock:
            LOG.info('generating {0} ...'.format(config_path))

        with open(config_in_path, 'r') as f:
            config = f.read()

        pkgconfig_path = os.path.join(self.pkg_config_path, 'libopenzwave.pc')
        config = config.replace('@pkgconfigfile@', pkgconfig_path)

        with open(config_path, 'w') as f:
            f.write(config)

        import stat

        st = os.stat(config_path)
        os.chmod(config_path, st.st_mode | stat.S_IEXEC)

    def __call__(self, build_clib, openzwave):
        self.build_path = build_clib.build_clib
        self.build_temp_path = build_clib.build_temp

        self.openzwave = openzwave

    @property
    def packages(self):
        packages = [
            'build-essential',
            'libudev-dev',
            'g++',
            'libyaml-dev',
            'libstdc++6',
            'libudev1',
            'libc6',
            'libresolv'
        ]

        return packages

    def clean_openzwave(self):
        LOG.info(
            'Removing {0}'.format(self.openzwave)
        )
        try:
            shutil.rmtree(self.openzwave)
            LOG.info(
                'Successfully removed {0}'.format(self.openzwave)
            )
        except OSError:
            LOG.error(
                'Failed to remove {0}'.format(self.openzwave)
            )
        return True

    def clean_cython(self):  # NOQA
        try:
            os.remove('_libopenzwave/_libopenzwave.cpp')
        except Exception:  # NOQA
            pass

    def clean_config(self):  # NOQA
        LOG.info('Cleaning OpenZWave config files.')

        try:
            from pkg_resources import resource_filename
            dirn = resource_filename(
                'openzwave.ozw_config',
                '__init__.py'
            )
            dirn = os.path.dirname(dirn)
        except ImportError:
            return

        for f in os.listdir(dirn):
            if '__init__' in f:
                continue

            f = os.path.join(dirn, f)

            try:
                if os.path.isfile(f):
                    os.remove(f)

                elif os.path.isdir(f):
                    shutil.rmtree(f)
            except OSError:
                continue

    # these next 3 methods you would override accordingly. If you check in
    # pyozw_win you will see the use of these methods
    def clean(self, build_clib):
        LOG.info(
            "Clean OpenZwave in {0} ... be patient ...".format(
                self.build_path
            )
        )
        build_clib.spawn(['make', 'clean'], cwd=self.openzwave)

    @property
    def fmt_cmd(self):
        return 'fmt -1'

    def compile_c(self, c_file, build_clib):
        cmd = [
            'echo "compiling {c_filename}..."',
            (
                "{CC} -MM {CFLAGS} {MACROS} {INCLUDES} "
                "{c_file} > {DEPDIR}/{filename}.d"
            ),
            "mv -f {DEPDIR}/{filename}.d {DEPDIR}/{filename}.d.tmp",
            (
                "sed -e 's|.*:|{OBJDIR}/{filename}.o: {DEPDIR}/{filename}.d|' "
                "< {DEPDIR}/{filename}.d.tmp > {DEPDIR}/{filename}.d;"
            ),
            (
                "sed -e 's/.*://' -e 's/\\\\$//' < {DEPDIR}/{filename}.d.tmp "
                "| {FMTCMD} | sed -e 's/^ *//' -e 's/$/:/' >> "
                "{DEPDIR}/.{filename}.d;"
            ),
            "rm -f {DEPDIR}/{filename}.d.tmp",
            "{CC} {CFLAGS} {TARCH} {INCLUDES} -o {o_file} {c_file}"
        ]

        c_file = os.path.abspath(c_file)
        filename = os.path.splitext(os.path.split(c_file)[-1])[0]
        o_file = os.path.join(self.obj_path, filename + '.o')

        cmd = '\n'.join(cmd)
        cmd = cmd.format(
            c_filename=os.path.split(c_file)[-1],
            CC=self.cc,
            CFLAGS=' '.join(self.c_flags),
            MACROS=' '.join(self.define_macros),
            INCLUDES=' '.join(self.include_dirs),
            DEPDIR=self.dep_path,
            OBJDIR=self.obj_path,
            FMTCMD=self.fmt_cmd,
            TARCH=' '.join(self.t_arch),
            c_file=c_file,
            filename=filename,
            o_file=o_file
        )

        for command in cmd.split('\n'):
            build_clib.spawn(command)

        return o_file

    def compile_cpp(self, cpp_file, build_clib):
        cmd = [
            'echo "compiling {cpp_filename}..."',
            (
                "{CXX} -MM {CFLAGS} {CPPFLAGS} {MACROS} {INCLUDES} "
                "{cpp_file} > {DEPDIR}/{filename}.d"
            ),
            "mv -f {DEPDIR}/{filename}.d {DEPDIR}/{filename}.d.tmp",
            (
                "sed -e 's|.*:|{OBJDIR}/{filename}.o: {DEPDIR}/{filename}.d|' "
                "< {DEPDIR}/{filename}.d.tmp > {DEPDIR}/{filename}.d;"
            ),
            (
                "sed -e 's/.*://' -e 's/\\\\$//' < "
                "{DEPDIR}/{filename}.d.tmp | {FMTCMD} | sed -e 's/^ *//' -e "
                "'s/$/:/' >> {DEPDIR}/.{filename}.d;"
            ),
            "rm -f {DEPDIR}/{filename}.d.tmp",
            (
                "{CXX} {CFLAGS} {CPPFLAGS} {TARCH} "
                "{INCLUDES} -o {o_file} {cpp_file}"
            ),
        ]
        cpp_file = os.path.abspath(cpp_file)
        filename = os.path.splitext(os.path.split(cpp_file)[-1])[0]
        o_file = os.path.join(self.obj_path, filename + '.o')

        cmd = '\n'.join(cmd)
        cmd = cmd.format(
            cpp_filename=os.path.split(cpp_file)[-1],
            CXX=self.cxx,
            CFLAGS=' '.join(self.c_flags),
            CPPFLAGS=' '.join(self.cpp_flags),
            MACROS=' '.join(self.define_macros),
            INCLUDES=' '.join(self.include_dirs),
            DEPDIR=self.dep_path,
            OBJDIR=self.obj_path,
            FMTCMD=self.fmt_cmd,
            TARCH=' '.join(self.t_arch),
            cpp_file=cpp_file,
            filename=filename,
            o_file=o_file
        )

        for command in cmd.split('\n'):
            build_clib.spawn(command)

        return o_file

    def build(self, build_clib, build):
        self.builder = build
        self.dest_path = os.path.join(build.openzwave, 'build')

        if build.static:
            build_path = self.build_path
        else:
            build_path = self.lib_inst_path

        if not os.path.exists(build_path):
            LOG.info('Creating directory ' + build_path)
            os.makedirs(build_path)

        if not os.path.exists(self.obj_path):
            LOG.info('Creating directory ' + self.obj_path)
            os.makedirs(self.obj_path)

        if not os.path.exists(self.dep_path):
            LOG.info('Creating directory ' + self.dep_path)
            os.makedirs(self.dep_path)

        if not os.path.exists(self.dest_path):
            LOG.info('Creating directory ' + self.dest_path)
            os.makedirs(self.dest_path)

        self.build_version_file()
        self.build_pkg_config_file()
        self.build_config_file()
        self.build_spec_file()

        objects = []
        thread_event = threading.Event()

        def do(files):
            objs = []

            while files:
                f = files.pop(0)
                check_f = os.path.join(
                    self.obj_path,
                    os.path.split(f)[-1]
                )

                check_f = os.path.splitext(check_f)[0]

                for ext in ('.o', '.obj'):
                    if os.path.exists(check_f + ext):
                        obj = check_f + ext
                        break
                else:
                    if not files:
                        evt = self.running_threads[threading.current_thread()]
                        evt.set()

                    if f.endswith('cpp'):
                        obj = self.compile_cpp(f, build_clib)
                    else:
                        obj = self.compile_c(f, build_clib)

                objs.append(obj)

            objects.extend(objs)

            threads.remove(threading.current_thread())

            if not threads:
                thread_event.set()

        sources = self.sources[:]

        split_files = []

        thread_count = os.cpu_count()
        num_files = int(round(len(sources) / thread_count))

        while sources:
            try:
                split_files += [sources[:num_files]]
                sources = sources[num_files:]
            except IndexError:
                split_files += [sources[:]]
                del sources[:]

        threads = []

        for fls in split_files:
            t = threading.Thread(target=do, args=(fls,))
            t.daemon = True
            self.running_threads[t] = threading.Event()
            threads.append(t)
            t.start()

        thread_event.wait()

        self.link_static(objects, build_clib)

        if not build.static:
            self.link_shared(objects, build_clib)
