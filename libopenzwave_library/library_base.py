# -*- coding: utf-8 -*-
import os
from distutils import log as LOG  # NOQA
import subprocess
import sys
import threading
import shutil


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

            found += get_sources(src, ignore)
        elif src_f.endswith('.c') or src_f.endswith('.cpp'):
            found += [src]
    return found


class Library(object):

    def __init__(
        self,
        sources=[],
        define_macros=[],
        libraries=[],
        library_dirs=[],
        include_dirs=[],
        extra_compile_args=[],
        extra_link_args=[]
    ):
        self.openzwave = ''
        self.name = 'OpenZWave'
        self.sources = sources
        self.define_macros = define_macros
        self.libraries = libraries
        self.library_dirs = library_dirs
        self.include_dirs = include_dirs
        self.extra_compile_args = extra_compile_args
        self.extra_link_args = extra_link_args
        self.build_path = ''
        self.builder = None
        self.dest_path = None
        self.ozw_vers_major = '1'
        self.ozw_vers_minor = '6'
        self.ozw_vers_revision = '0'
        self.print_lock = threading.Lock()
        self.running_threads = {}

        packages = self.packages

        if packages:
            p = subprocess.Popen(
                packages,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            while p.poll() is None:
                for line in iter(p.stdout.readline, dummy_return):
                    line = line.strip()
                    if line:
                        sys.stdout.write(line.decode('utf-8') + '\n')
                        sys.stdout.flush()

                for line in iter(p.stderr.readline, dummy_return):
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

    @property
    def ozw_version_string(self):
        return (
            self.ozw_vers_major + '.' +
            self.ozw_vers_minor + '.' +
            self.ozw_vers_revision
        )

    @property
    def prefix(self):
        return os.path.join('/usr', 'local')

    @property
    def sys_config_path(self):
        return os.path.join(self.prefix, 'etc', 'openzwave')

    @property
    def include_path(self):
        return os.path.join(self.prefix, 'include', 'openzwave')

    @property
    def pkg_config_path(self):
        if os.path.exists('/usr/lib64'):
            return os.path.join('/usr', 'lib64', 'pkgconfig')
        else:
            return os.path.join('/usr', 'lib', 'pkgconfig')

    @property
    def lib_inst_path(self):
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
    def t_arch(self):
        return []

    @property
    def ar(self):
        return ''

    @property
    def ld_flags(self):
        return []

    @property
    def ld(self):
        return ''

    @property
    def shared_lib_name(self):
        return ''

    @property
    def shared_lib_no_version_name(self):
        return ''

    @property
    def obj_path(self):
        return ''

    @property
    def dep_path(self):
        return ''

    @property
    def ranlib(self):
        return ''

    @property
    def cc(self):
        return ''

    @property
    def cxx(self):
        return ''

    @property
    def c_flags(self):
        return []

    @property
    def cpp_flags(self):
        return []

    @property
    def libraries(self):
        return []

    @libraries.setter
    def libraries(self, _):
        pass

    @property
    def include_dirs(self):
        return []

    @include_dirs.setter
    def include_dirs(self, _):
        pass

    @property
    def so_path(self):
        import libopenzwave_pkgconfig

        ldpath = libopenzwave_pkgconfig.libs_only_l('libopenzwave')[2:]

        LOG.info(
            "Running ldconfig on {0}... be patient ...".format(ldpath)
        )

        return ldpath

    def build_version_file(self, build_clib):
        from subprocess import Popen, PIPE
        version_file = os.path.join(self.openzwave, 'cpp', 'src', 'vers.cpp')

        if os.path.exists(version_file):
            return

        with self.print_lock:
            sys.stdout.write('building vers.cpp ....\n')
            sys.stdout.flush()

        ozw_git = os.path.join(self.openzwave, '.git')

        command = ['which', 'git']
        p = Popen(command, stdout=PIPE, stderr=PIPE)

        git = p.communicate()[0].strip().decode('utf-8')

        if os.path.exists(ozw_git) and git:
            command = [
                '{git} --git-dir {ozw_git} describe --long --tags --dirty 2 '
                '> /dev/null |sed s/^v//'.format(
                    git=git,
                    ozw_git=ozw_git
                )
            ]

            p = Popen(command, stdout=PIPE, stderr=PIPE)
            git_version = p.communicate()[0].strip().decode('utf-8')
            print(repr(git_version))

            if git_version:
                command = [
                    "echo {git_version} | awk '{{split($0,a,\"-\"); "
                    "print a[2]}}'".format(git_version=git_version)
                ]
                p = Popen(command, stdout=PIPE, stderr=PIPE)
                ozw_vers_revision = p.communicate()[0].strip().decode('utf-8')
                self.ozw_vers_revision = ozw_vers_revision

                print(repr(self.ozw_vers_revision))
        else:
            self.ozw_vers_revision = '0'

        template = [
            '# include "Defs.h"',
            'uint16_t ozw_vers_major = {0};',
            'uint16_t ozw_vers_minor = {1};',
            'int16_t ozw_vers_revision = {2};',
            'char ozw_version_string[] = "{3}\\0";'
        ]

        template = '\n'.join(template)

        output = template.format(
            self.ozw_vers_major,
            self.ozw_vers_minor,
            self.ozw_vers_revision,
            self.ozw_version_string
        )

        LOG.debug(output)

        with open(version_file, 'w') as f:
            f.write(output)

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
        libopenzwave = os.path.join(self.openzwave, 'libopenzwave.a')

        if os.path.exists(libopenzwave):
            return

        with self.print_lock:
            sys.stdout.write('linking static library...\n')
            sys.stdout.flush()

        command = [self.ar, 'rc'] + [libopenzwave] + objects
        build_clib.spawn(command)

        command = [self.ranlib, libopenzwave]
        build_clib.spawn(command)

    def link_shared(self, objects, build_clib):

        libopenzwave_no_version = os.path.join(
            self.openzwave,
            self.shared_lib_no_version_name
        )
        libopenzwave_version = os.path.join(
            self.openzwave,
            self.shared_lib_name
        )

        if os.path.exists(libopenzwave_no_version):
            return

        with self.print_lock:
            sys.stdout.write('linking shared library...\n')
            sys.stdout.flush()

        command = [self.ld] + self.ld_flags + self.t_arch
        command += ['-o', libopenzwave_version]
        command += objects + self.libraries
        build_clib.spawn(command)

        command = [
            'ln',
            '-sf',
            libopenzwave_version,
            libopenzwave_no_version
        ]
        build_clib.spawn(command)
        build_clib.spawn(['ldconfig', self.so_path], cwd=self.openzwave)

    def build_pkg_config_file(self, build_clib):
        with self.print_lock:
            sys.stdout.write('building pkg-config file...\n')
            sys.stdout.flush()

        pc = os.path.join(self.openzwave, 'libopenzwave.pc')
        pc_in = os.path.join(
            self.openzwave,
            'cpp',
            'build',
            'libopenzwave.pc.in'
        )

        exec_prefix = os.path.join('/usr', 'local', 'bin')

        command = [
            "sed "
            "-e 's|[@]prefix@|{prefix}|g' "
            "-e 's|[@]exec_prefix@|{exec_prefix}|g' "
            "-e 's|[@]libdir@|{libdir}|g' "
            "-e 's|[@]includedir@|{includedir}/|g' "
            "-e 's|[@]sysconfdir@|{sysconfdir}/|g' "
            "-e 's|[@]gitversion@|{gitversion}|g' "
            "-e 's|[@]VERSION@|{version}|g' "
            "-e 's|[@]LIBS@|{libs}|g' "
            "< \"{pc_in}\" "
            "> \"{pc}\"".format(
                prefix=self.prefix,
                exec_prefix=exec_prefix,
                libdir=self.lib_inst_path,
                includedir=self.include_path,
                sysconfdir=self.sys_config_path,
                gitversion=self.ozw_version_string,
                version=self.ozw_version_string,
                libs=' '.join(lib.lstrip('l ') for lib in self.libraries),
                pc_in=pc_in,
                pc=pc
            )
        ]

        build_clib.spawn(command)

    def build_config_file(self, build_clib):
        with self.print_lock:
            sys.stdout.write('building config file...\n')
            sys.stdout.flush()

        pkgconfigfile = os.path.join(self.pkg_config_path, 'libopenzwave.pc')
        ozw_config_in = os.path.join(
            self.openzwave,
            'cpp',
            'build',
            'ozw_config.in'
        )
        ozw_config = os.path.join(self.openzwave, 'ozw_config')

        command = [
            "sed "
            "-e 's|[@]pkgconfigfile@|\"{pkgconfigfile}\"|g' "
            "< \"{ozw_config_in}\" > \"{ozw_config}\"".format(
                pkgconfigfile=pkgconfigfile,
                ozw_config_in=ozw_config_in,
                ozw_config=ozw_config
            )
        ]
        build_clib.spawn(command)

        import stat

        st = os.stat(ozw_config)
        os.chmod(ozw_config, st.st_mode | stat.S_IEXEC)
    #
    #
    # def install_shared_library(self):
    #     """
    #     	@echo "Installing Shared Library"
    # 	@install -d $(DESTDIR)/$(instlibdir)/
    # 	@cp  $(LIBDIR)/$(SHARED_LIB_NAME) $(DESTDIR)/$(instlibdir)/$(SHARED_LIB_NAME)
    # 	@ln -sf $(SHARED_LIB_NAME) $(DESTDIR)/$(instlibdir)/$(SHARED_LIB_UNVERSIONED)
    # 	@echo "Installing Headers"
    # 	@install -d $(DESTDIR)/$(includedir)
    # 	@install -m 0644 $(top_srcdir)/cpp/src/*.h $(DESTDIR)/$(includedir)
    # 	@install -d $(DESTDIR)/$(includedir)/command_classes/
    # 	@install -m 0644 $(top_srcdir)/cpp/src/command_classes/*.h $(DESTDIR)/$(includedir)/command_classes/
    # 	@install -d $(DESTDIR)/$(includedir)/value_classes/
    # 	@install -m 0644 $(top_srcdir)/cpp/src/value_classes/*.h $(DESTDIR)/$(includedir)/value_classes/
    # 	@install -d $(DESTDIR)/$(includedir)/platform/
    # 	@install -m 0644 $(top_srcdir)/cpp/src/platform/*.h $(DESTDIR)/$(includedir)/platform/
    # 	@install -d $(DESTDIR)/$(includedir)/platform/unix/
    # 	@install -m 0644 $(top_srcdir)/cpp/src/platform/unix/*.h $(DESTDIR)/$(includedir)/platform/unix/
    # 	@install -d $(DESTDIR)/$(includedir)/aes/
    # 	@install -m 0644 $(top_srcdir)/cpp/src/aes/*.h $(DESTDIR)/$(includedir)/aes/
    # 	@install -d $(DESTDIR)/$(sysconfdir)/
    # 	@echo "Installing Config Database"
    # 	@cp -r $(top_srcdir)/config/* $(DESTDIR)/$(sysconfdir)
    # 	@echo "Installing Documentation"
    # 	@install -d $(DESTDIR)/$(docdir)/
    # 	@cp -r $(top_srcdir)/docs/* $(DESTDIR)/$(docdir)
    # 	@if [ -d "$(top_builddir)/docs/html/" ]; then cp -r $(top_builddir)/docs/html/* $(DESTDIR)/$(docdir); fi
    # 	@echo "Installing Pkg-config Files"
    # 	@install -d $(DESTDIR)/$(pkgconfigdir)
    # 	@cp $(top_builddir)/libopenzwave.pc $(DESTDIR)/$(pkgconfigdir)
    # 	@install -d $(DESTDIR)/$(PREFIX)/bin/
    # 	@cp $(top_builddir)/ozw_config $(DESTDIR)/$(PREFIX)/bin/ozw_config
    # 	@chmod 755 $(DESTDIR)/$(PREFIX)/bin/ozw_config
    #
    #
    #     :return:
    #     """

    def __call__(self, openzwave):
        self.openzwave = openzwave
        self.build_path = os.path.join(self.openzwave, 'build')

    @property
    def packages(self):
        return []

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

    def clean_cython(self):
        try:
            os.remove('_libopenzwave/_libopenzwave.cpp')
        except Exception:
            pass

    def clean_config(self):
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

    def compile_c(self, c_file, build_clib):
        with self.print_lock:
            sys.stdout.write(
                'compiling ' + os.path.split(c_file)[-1] + '...\n'
            )
            sys.stdout.flush()

        c_file = os.path.abspath(c_file)
        file_name = os.path.splitext(os.path.split(c_file)[-1])[0]
        d_file = os.path.join(self.dep_path, file_name + '.d')
        tmp_file = d_file + '.tmp'
        o_file = os.path.join(self.obj_path, file_name + '.o')

        command = [self.cc, '-MM']
        command += self.c_flags
        command += self.include_dirs
        command += ['{0} > {1}'.format(c_file, d_file)]
        build_clib.spawn(command)

        shutil.move(d_file, tmp_file)

        command = [
            "sed -e 's|.*:|{0}: {1}|' < {2} > {1}".format(
                o_file,
                d_file,
                tmp_file
            )
        ]
        build_clib.spawn(command)

        command = [
            "sed -e 's/.*://' -e 's/\\$//' < {0} | fmt -1 | "
            "sed -e 's/^ *//' -e 's/$/:/' >> {1}".format(tmp_file, d_file)
        ]
        build_clib.spawn(command)

        os.remove(tmp_file)

        command = [self.cc] + self.c_flags + self.t_arch + self.include_dirs
        command += ['-o', o_file, c_file]
        build_clib.spawn(command)

        return o_file

    def compile_cpp(self, cpp_file, build_clib):
        with self.print_lock:
            sys.stdout.write(
                'compiling ' + os.path.split(cpp_file)[-1] + '...\n'
            )
            sys.stdout.flush()

        cpp_file = os.path.abspath(cpp_file)
        file_name = os.path.splitext(os.path.split(cpp_file)[-1])[0]
        d_file = os.path.join(self.dep_path, file_name + '.d')
        tmp_file = d_file + '.tmp'
        o_file = os.path.join(self.obj_path, file_name + '.o')

        command = [self.cxx, '-MM'] + self.c_flags + self.cpp_flags
        command += self.include_dirs + [cpp_file, '>', d_file]
        build_clib.spawn(command)

        shutil.move(d_file, tmp_file)

        command = [
            "sed -e 's|.*:|{0}: {1}|"
            "' < {2} > {1}".format(o_file, d_file, tmp_file)
        ]
        build_clib.spawn(command)

        command = [
            "sed -e's/.*://' -e 's/\\$//' < {0} | fmt -1 | sed -e "
            "'s/^ *//' -e 's/$/:/' >> {1}".format(tmp_file, d_file)
        ]
        build_clib.spawn(command)

        os.remove(tmp_file)

        command = [self.cxx] + self.c_flags + self.cpp_flags + self.t_arch
        command += self.include_dirs + ['-o', o_file, cpp_file]
        build_clib.spawn(command)

        return o_file

    def build(self, build_clib, build):
        self.builder = build
        self.dest_path = os.path.join(build.openzwave, 'build')

        if build.static:
            build_path = os.path.join(self.dest_path, self.lib_inst_path)
        else:
            build_path = self.lib_inst_path

        if not os.path.exists(build_path):
            LOG.debug('Creating directory ' + build_path)
            os.makedirs(build_path)

        if not os.path.exists(self.obj_path):
            LOG.debug('Creating directory ' + self.obj_path)
            os.mkdir(self.obj_path)

        if not os.path.exists(self.dep_path):
            LOG.debug('Creating directory ' + self.dep_path)
            os.mkdir(self.dep_path)

        if not os.path.exists(self.dest_path):
            LOG.debug('Creating directory ' + self.dest_path)
            os.mkdir(self.dest_path)

        self.build_version_file(build_clib)

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
            threads += [t]
            t.start()

        thread_event.wait()

        self.link_static(objects, build_clib)

        if not build.static:
            self.link_shared(objects, build_clib)
