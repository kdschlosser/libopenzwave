# -*- coding: utf-8 -*-

from .wheel import wheel


class wheel_embed_shared(wheel):

    def finalize_options(self):
        install_options = dict(install_lib=('setup script', self.bdist_dir))
        self.distribution.command_options['install_embed_shared'] = (
            install_options
        )

    def run_install(self):
        self.run_command('install_embed_shared')
