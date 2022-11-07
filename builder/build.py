# -*- coding: utf-8 -*-

import os
import shutil
from distutils import log as LOG
from distutils.command.build import build as _build
import setuptools
import version
from .get_openzwave import get_openzwave


class build(_build):
    backend = 'cython'
    openzwave = 'openzwave'
    flavor = 'release'
    static = True
    install_openzwave_so = False

    user_options = [
        ('cleanozw', None, 'clean OpenZwave'),
        ('dev', None, 'use development version of OpenZWave'),
        ('cython', None, 'compile library using cython')
    ] + _build.user_options

    boolean_options = ['cleanozw', 'dev', 'cython'] + _build.boolean_options

    def initialize_options(self):

        if 'DISTUTILS_DEBUG' in os.environ:
            LOG.set_threshold(LOG.DEBUG)

        _build.initialize_options(self)
        self.openzwave = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', self.openzwave)
        )
        self.dev_repo = None  # NOQA
        self.cleanozw = False  # NOQA
        self.dev = False  # NOQA
        self.cython = False  # NOQA

    def finalize_options(self):
        _build.finalize_options(self)

        if self.dev_repo is None:
            self.dev_repo = (  # NOQA
                'https://codeload.github.com/OpenZWave/open-zwave/zip/master'
            )

        if self.dev:
            self.flavor = self.flavor.replace('release', 'dev')
            self.get_openzwave = self.get_openzwave_dev  # NOQA

        if os.path.exists(self.openzwave) and self.cleanozw:
            try:
                shutil.rmtree(self.openzwave)
            except:  # NOQA
                raise RuntimeError(
                    'Unable to remove directory: ' +
                    self.openzwave
                )

        if not os.path.exists(self.openzwave):
            self.get_openzwave()

        build_config = self.distribution.get_command_obj('build_config')  # NOQA
        build_config.ensure_finalized()

        # build_clib = self.distribution.get_command_obj('build_clib')
        # build_clib.ensure_finalized()

    def run(self):
        def iter_copy(src_path, dst_path, special_file=None, exclude=None):
            for f in os.listdir(src_path):
                if f == '__pycache__':
                    continue
                if exclude is not None and f == exclude:
                    continue

                src = os.path.join(src_path, f)
                dst = os.path.join(dst_path, f)

                if os.path.isdir(src):
                    if not os.path.exists(dst):
                        LOG.info('making directory: ' + dst)
                        os.mkdir(dst)

                    iter_copy(
                        src,
                        dst,
                        special_file=special_file,
                        exclude=exclude
                    )

                elif special_file is None or special_file == f:
                    LOG.info(src + ' ---> ' + dst)
                    shutil.copyfile(src, dst)

        build_lib = os.path.join(self.build_lib, 'libopenzwave')

        if not os.path.exists(build_lib):
            LOG.info('making directory: ' + build_lib)
            os.makedirs(build_lib)

        if self.cython:
            ozw_config = os.path.join(build_lib, 'ozw_config')

            if not os.path.exists(ozw_config):
                LOG.info('making directory: ' + ozw_config)
                os.mkdir(ozw_config)

            iter_copy('libopenzwave/ozw_config', ozw_config)
            iter_copy(
                'libopenzwave',
                build_lib,
                special_file='__init__.py',
                exclude='command_classes'
            )
            self.build_cython()
        else:
            iter_copy('libopenzwave', build_lib)

        # build_config = self.distribution.get_command_obj('build_config')
        self.run_command('build_config')
        for sub_command in self.get_sub_commands():
            self.run_command(sub_command)

        #     if sub_command == 'build_py' and build_config.is_finalized:
        #         build_config.run()

    def build_cython(self):
        build_lib = os.path.join(self.build_lib, 'libopenzwave')

        cython_libopenzwave_build_path = os.path.join(
            self.build_temp,
            'cython_libopenzwave'
        )

        if not os.path.exists(cython_libopenzwave_build_path):
            LOG.info(
                'creating directory: ' + cython_libopenzwave_build_path
            )
            os.makedirs(cython_libopenzwave_build_path)

        command_classes_path = os.path.join(
            cython_libopenzwave_build_path,
            'command_classes.py'
        )

        command_classes = open(command_classes_path, 'w')

        lib_command_classes_path = 'libopenzwave/command_classes'

        cc_init_path = os.path.join(
            lib_command_classes_path,
            '__init__.py'
        )

        cc_cmd_path = os.path.join(
            lib_command_classes_path,
            'zwave_cmd_class.py'
        )

        def _strip_module(mod_data, fix_command_class=True):
            mod_doc = False
            mod_comment = True

            for lne in mod_data:
                if lne.startswith('#') and mod_comment:
                    continue

                if lne.startswith('"""'):
                    if not mod_doc:
                        mod_comment = False

                    mod_doc = not mod_doc
                    continue

                if mod_doc:
                    continue

                if fix_command_class:
                    for itm in ("'COMMAND_CLASS_", '`COMMAND_CLASS_'):
                        if itm in lne:
                            break
                    else:
                        lne = lne.replace('COMMAND_CLASS_', '_COMMAND_CLASS_')

                if lne.strip().startswith('from ..'):
                    lne = lne.replace('from ..', 'from .')

                elif lne.strip().startswith('from . ') and not lne.startswith(
                        'from . '):
                    continue
                elif lne.startswith('from .'):
                    continue

                yield lne

        with open(cc_cmd_path, 'r') as f:
            cc_cmd = f.read()

        command_classes_stub = []
        zwave_cmd_class_stub = 'class zwave_cmd_class(object):\n'

        for line in _strip_module(cc_cmd.split('\n')):
            command_classes.write(line + '\n')
            zwave_cmd_class_stub += '    ' + line + '\n'

        command_classes_stub.append(zwave_cmd_class_stub)

        names = [
            'zwave_cmd_class',
        ]

        for f in os.listdir(lib_command_classes_path):
            if f in ('__init__.py', 'zwave_cmd_class.py', '__pycache__'):
                continue

            name = os.path.splitext(f)[0]
            stub = 'class {name}(object):\n'.format(name=name)
            names.append(name)
            f = os.path.join(lib_command_classes_path, f)

            with open(f, 'r') as file:
                data = file.read()

            data = '\n'.join(_strip_module(data.split('\n')))
            data = data.replace('from . import zwave_cmd_class\n', '')
            data = data.replace('zwave_cmd_class.', '')
            command_classes.write(data + '\n')
            stub += '\n'.join('    ' + line for line in data.split('\n'))
            command_classes_stub.append(stub)

        with open(cc_init_path, 'r') as f:
            cc_init = f.read().split('\n')

        command_classes.write(
            '\n'.join(
                line for line in _strip_module(cc_init, False)
                if not line.startswith('from .')
            )
        )
        command_classes.write('\n\n')

        names = '\n'.join("    '" + name + "'," for name in names)[:-1]
        command_classes.write(IMPORT_WRAPPER.format(mod_names=names))

        command_classes.close()

        def _iter_copy(src_path, dst_path, mod_name):
            compile_sources = []
            for src_f in os.listdir(src_path):
                if src_f in ('command_classes', '__pycache__', '__init__.py'):
                    continue

                m_name = mod_name + '.' + os.path.splitext(src_f)[0]
                dst_f = os.path.join(dst_path, src_f)
                src_f = os.path.join(src_path, src_f)

                if os.path.isdir(src_f):
                    if not os.path.exists(dst_f):
                        LOG.info('creating directory: ' + dst_f)
                        os.mkdir(dst_f)

                    compile_sources.extend(_iter_copy(src_f, dst_f, m_name))
                else:
                    LOG.info(src_f + ' --> ' + dst_f)
                    shutil.copyfile(src_f, dst_f)
                    compile_sources.append([dst_f, m_name])

            return compile_sources

        sources = [[
            os.path.join(cython_libopenzwave_build_path, 'command_classes.py'),
            'libopenzwave.command_classes'
        ]]

        sources.extend(_iter_copy(
            'libopenzwave',
            cython_libopenzwave_build_path,
            'libopenzwave'
        ))

        extensions = []
        includes = set()

        for source, name in sources:
            includes.add(os.path.split(source)[0])

        for source, name in sources:
            extension = setuptools.Extension(
                name=name,
                sources=[source],
                include_dirs=list(includes)
            )
            extensions.append(extension)

        self.distribution.ext_modules.extend(extensions)  # NOQA

        def make_stubs(src_path, dst_path):
            for src_f in os.listdir(src_path):
                dst_f = os.path.join(dst_path, src_f)
                src_f = os.path.join(src_path, src_f)
                if os.path.isdir(src_f):
                    if not os.path.exists(dst_f):
                        LOG.info('creating directory ' + dst_f)
                        os.makedirs(dst_f)

                    make_stubs(src_f, dst_f)

                elif src_f.endswith('.py'):
                    dst_f += 'i'
                    LOG.info('copying ' + src_f + '-->' + dst_f)
                    shutil.copyfile(src_f, dst_f)

                    if 'command_classes' in src_f:
                        with open(dst_f, 'r') as fle:
                            dta = fle.read()

                        dta += '\n\n'
                        dta += '\n\n'.join(command_classes_stub)

                        with open(dst_f, 'w') as fle:
                            fle.write(dta)

        make_stubs(cython_libopenzwave_build_path, build_lib)

    def get_openzwave_dev(self):
        get_openzwave(
            self.openzwave,
            self.dev_repo
        )

    def get_openzwave(self):
        import requests  # NOQA

        url = b'http://old.openzwave.com/downloads/'
        response = requests.get(url)
        response = response.content.decode('utf-8').split(
            '<table border=1 class="imagetable">'
        )[1]

        lines = list(line.strip() for line in response.replace(
            '<tr>',
            ''
        ).split('</tr>')[1:-1])
        download_url = None
        download_version = (0, 0, 0)

        for line in lines:
            line = line.replace('<td>', '').split('</td>')
            vers = line[0]

            versn = vers[vers.find('>') + 1:]
            download_file_name = line[2].split('>')[-1]

            versn = tuple(
                int(ver) for ver in versn.split('.') if ver.isdigit()
            )
            if len(versn) < 3:
                versn += (0,)

            if versn[:2] == version.ozw_version:
                if str(versn[2]) > str(download_version[2]):
                    download_version = versn
                    download_url = url + download_file_name.encode('utf-8')

        if download_url is None:
            raise RuntimeError(
                'unable to locate suitable openzwave download'
            )

        get_openzwave(self.openzwave, download_url)
        version.OZW_VERSION_REV = download_version[2]


IMPORT_WRAPPER = '''\
_names = [
{mod_names}
]
import sys

class ImportWrapper(object):
    def __init__(self, mod_name):
        mod = sys.modules[__name__]
        mod_name = __name__ + '.' + mod_name

        self.__doc__ = mod.__doc__
        self.__file__ = mod.__file__
        self.__loader__ = mod.__loader__
        self.__name__ = mod.__name__
        self.__package__ = mod.__package__
        self.__spec__ = mod.__spec__

        sys.modules[mod_name] = self

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in globals():
            attr = globals()[item]
            object.__setattr__(self, item, attr)

            return attr

        raise AttributeError(item)

    def __setattr__(self, item, value):
        if item.startswith('__'):
            object.__setattr__(self, item, value)
        else:
            import sys
            mod = sys.modules[__name__]
            setattr(mod, item, value)



mod = sys.modules[__name__]

for _name in _names:
    setattr(mod, _name, ImportWrapper(_name))

del _names
del ImportWrapper
del mod
del sys
'''