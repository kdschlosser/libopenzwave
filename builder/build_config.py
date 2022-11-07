# -*- coding: utf-8 -*-

import setuptools
from distutils import log as LOG
import sys
import os
from pkg_resources import resource_filename
import tempfile
import shutil


PYTHON_PATH = os.path.dirname(sys.executable)


class build_config(setuptools.Command):
    is_finalized = False
    description = 'Install config files from openzwave'

    user_options = [
        (
            'install-dir=',
            None,
            'the installation directory where openzwave '
            'configuration should be stored'
        ),
    ]

    def initialize_options(self):
        self.install_dir = None  # NOQA

    def finalize_options(self):
        self.is_finalized = True

        if self.install_dir is None:
            build = self.distribution.get_command_obj('build')  # NOQA
            build_dir = build.build_lib

            self.install_dir = os.path.join(  # NOQA
                build_dir,
                'libopenzwave',
                'ozw_config'
            )

    def run(self):
        build = self.distribution.get_command_obj('build')  # NOQA
        # here we are going to check to see if python_openzwave is already
        # installed.

        # if it is already installed we want to backup the config files so we
        # can iterate over them and check them against the ones being
        # installed. we do not want to remove any config files that may have
        # been updated by the user. or any they may have created.

        if not os.path.exists(self.install_dir):
            os.makedirs(self.install_dir)

            dst1 = os.path.join(self.install_dir, '__init__.py')
            src1 = os.path.abspath(
                'libopenzwave/ozw_config/__init__.py'
            )
            dst2 = os.path.abspath(
                os.path.join(self.install_dir, '..', '__init__.py')
            )
            src2 = os.path.abspath(
                'libopenzwave/__init__.py'
            )

            for dst, src in ((dst1, src1), (dst2, src2)):
                with open(dst, 'w') as f1:
                    with open(src, 'r') as f2:
                        f1.write(f2.read())

            # raise RuntimeError('Unable to locate installation folder.')

        try:
            config_path = resource_filename(
                'libopenzwave.ozw_config',
                '__init__.py'
            )
            config_path = os.path.dirname(config_path)

            if len(os.listdir(config_path)) < 3:
                raise OSError

        except:  # NOQA
            temp_dir = None
        else:
            temp_dir = os.path.join(tempfile.mkdtemp(), 'config')
            shutil.copytree(config_path, temp_dir)

        dst = self.install_dir

        if temp_dir is not None:
            shutil.rmtree(dst)
            shutil.copytree(temp_dir, dst)
            shutil.rmtree(temp_dir)

        def get_newer_config_file(old, new):
            new_revision = new.split(b'Revision="', 1)[-1]
            old_revision = old.split(b'Revision="', 1)[-1]

            new_revision = new_revision.split(b'"', 1)[0]
            old_revision = old_revision.split(b'"', 1)[0]

            if new_revision.isdigit() and old_revision.isdigit():
                if int(new_revision) > int(old_revision):
                    return new
                elif int(new_revision) < int(old_revision):
                    return old

            if len(new) > len(old):
                return new

            return old

        src = os.path.join(build.openzwave, 'config')

        def check_config(root):
            head = root
            tail = []
            while head and head != src:
                head, t = os.path.split(head)
                tail.insert(0, t)

            if tail:
                new_root = os.path.join(dst, *tail)
            else:
                new_root = dst

            files = os.listdir(root)

            for f in files:
                old_f = os.path.join(new_root, f)
                new_f = os.path.join(root, f)

                if os.path.isdir(new_f):
                    if not os.path.exists(old_f):
                        LOG.debug(
                            'Creating directory: ' +
                            old_f.replace(PYTHON_PATH, '')
                        )
                        os.mkdir(old_f)

                    check_config(new_f)
                else:
                    with open(new_f, 'rb') as tmp_f:
                        new_data = tmp_f.read()

                    if new_f.endswith('.xml') and os.path.isfile(old_f):
                        with open(old_f, 'rb') as tmp_f:
                            old_data = tmp_f.read()

                        if old_data == new_data:
                            LOG.debug(
                                'No update needed: ' +
                                old_f.replace(PYTHON_PATH, '')
                            )
                            continue

                        data = get_newer_config_file(
                            old_data,
                            new_data
                        )

                        if data != old_data:
                            LOG.debug(
                                'New config file: copying... ' +
                                new_f +
                                ' ---> ' +
                                old_f.replace(PYTHON_PATH, '')
                            )
                        else:
                            LOG.debug(
                                'Keeping existing file: ' +
                                old_f.replace(PYTHON_PATH, '')
                            )
                            continue
                    else:
                        LOG.debug(
                            'Copying file: ' +
                            new_f +
                            ' ---> ' +
                            old_f.replace(PYTHON_PATH, '')
                        )

                    with open(old_f, 'wb') as tmp_f:
                        tmp_f.write(new_data)

        check_config(src)
