# -*- coding: utf-8 -*-

from setuptools.command.install import install as _install  # NOQA
from distutils.command.install import install as _install2  # NOQA


class install(_install):
    description = 'Install libopenzwave'

    user_options = [
        ('dev', None, 'use development version of OpenZWave'),
        ('no-deps', 'N', "don't install dependencies"),
        ('cython', None, 'compile library using cython')
    ] + _install.user_options

    boolean_options = ['dev', 'no-deps', 'cython'] + _install.boolean_options

    def initialize_options(self):
        self.no_deps = False
        self.dev = False
        self.cython = False
        _install2.initialize_options(self)
        self.old_and_unmanageable = None
        self.single_version_externally_managed = None

    def finalize_options(self):
        build = self.distribution.get_command_obj('build')
        build.dev = self.dev
        build.cython = self.cython
        _install.finalize_options(self)

    def run(self):
        # Explicit request for old-style install?  Just do it
        self.run_command('build')
        # self.run_command('build_py')
        self.run_command('build_scripts')
        self.run_command('build_config')
        _install.run(self)

        self.do_egg_install()
