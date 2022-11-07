# -*- coding: utf-8 -*-

from setuptools.command import bdist_egg as _bdist_egg


# We had to override this method so that setuptools would not write the
# libopenzwave bootstrap over the one we created.
def write_stub(_, __):
    pass


_bdist_egg.write_stub = write_stub


class bdist_egg(_bdist_egg.bdist_egg):
    description = 'Create an EGG.'

    user_options = [
        ('bdist-dir=', None, 'temporary install path'),
        ('dev', None, 'Use development version of OpenZWave')
    ]

    boolean_options = ['dev']

    def initialize_options(self):
        self.bdist_dir = None
        self.dev = False  # NOQA
        _bdist_egg.bdist_egg.initialize_options(self)

    def finalize_options(self):
        builder = self.distribution.get_command_obj('build')  # NOQA
        builder.ensure_finalized()
        self.bdist_dir = builder.build_lib
        _bdist_egg.bdist_egg.finalize_options(self)
        self.keep_temp = 1

    def run(self):
        self.run_command('build_py')
        self.run_command('build')
        self.run_command('build_scripts')

        _bdist_egg.bdist_egg.run(self)
