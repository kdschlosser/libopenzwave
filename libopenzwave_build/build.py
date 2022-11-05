# -*- coding: utf-8 -*-

import sys
import os
import shutil
from distutils import log as LOG
from distutils.command.build import build as _build
import setuptools
import libopenzwave_version
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
        self.dev_repo = None
        self.cleanozw = False
        self.dev = False
        self.cython = False

    def finalize_options(self):
        _build.finalize_options(self)

        if self.dev_repo is None:
            self.dev_repo = 'https://codeload.github.com/OpenZWave/open-zwave/zip/master'

        if self.dev:
            self.flavor = self.flavor.replace('release', 'dev')
            self.get_openzwave = self.get_openzwave_dev

        if os.path.exists(self.openzwave) and self.cleanozw:
            try:
                shutil.rmtree(self.openzwave)
            except:
                raise RuntimeError(
                    'Unable to remove directory: ' +
                    self.openzwave
                )

        if not os.path.exists(self.openzwave):
            self.get_openzwave()

        for build_type in ('wheel', 'egg', 'build', 'install'):
            if build_type in sys.argv:
                build_config = self.distribution.get_command_obj('build_config')
                build_config.ensure_finalized()
                break

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

                    iter_copy(src, dst, special_file=special_file, exclude=exclude)

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
            iter_copy('libopenzwave', build_lib, special_file='__init__.py', exclude='command_classes')
            self.build_cython()
        else:
            iter_copy('libopenzwave', build_lib)

        build_config = self.distribution.get_command_obj('build_config')

        for sub_command in self.get_sub_commands():
            self.run_command(sub_command)

            if sub_command == 'build_py' and build_config.is_finalized:
                build_config.run()

    def build_cython(self):
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

        for line in _strip_module(cc_cmd.split('\n')):
            command_classes.write(line + '\n')

        names = [
            'zwave_cmd_class',
        ]

        for f in os.listdir(lib_command_classes_path):
            if f in ('__init__.py', 'zwave_cmd_class.py', '__pycache__'):
                continue

            names.append(os.path.splitext(f)[0])
            f = os.path.join(lib_command_classes_path, f)

            with open(f, 'r') as file:
                data = file.read()

            data = '\n'.join(_strip_module(data.split('\n')))
            data = data.replace('from . import zwave_cmd_class\n', '')
            data = data.replace('zwave_cmd_class.', '')
            command_classes.write(data + '\n')

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

        self.distribution.ext_modules.extend(extensions)

    def get_openzwave_dev(self):
        get_openzwave(
            self.openzwave,
            self.dev_repo
        )

    def get_openzwave(self):
        import requests

        url = b'http://old.openzwave.com/downloads/'
        response = requests.get(url)
        response = response.content.decode('utf-8').split('<table border=1 class="imagetable">')[1]

        lines = list(line.strip() for line in response.replace('<tr>', '').split('</tr>')[1:-1])
        download_url = None
        download_version = (0, 0, 0)

        for line in lines:
            line = line.replace('<td>', '').split('</td>')
            vers = line[0]

            version = vers[vers.find('>') + 1:]
            download_file_name = line[2].split('>')[-1]

            version = tuple(
                int(ver) for ver in version.split('.') if ver.isdigit()
            )
            if len(version) < 3:
                version += (0,)

            if version[:2] == libopenzwave_version.ozw_version:
                if str(version[2]) > str(download_version[2]):
                    download_version = version
                    download_url = url + download_file_name.encode('utf-8')

        if download_url is None:
            raise RuntimeError(
                'unable to locate suitable openzwave download'
            )

        get_openzwave(self.openzwave, download_url)
        libopenzwave_version.OZW_VERSION_REV = download_version[2]


IMPORT_WRAPPER = '''\
_names = [
{mod_names}
]


class ImportWrapper(object):
    def __init__(self, mod_name):
        import sys

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


for _name in _names:
    ImportWrapper(_name)

del _names
del ImportWrapper
'''