# -*- coding: utf-8 -*-

from .install import install as _install


class install_embed(_install):
    description = 'Install python_openzwave'

    def initialize_options(self):
        _install.initialize_options(self)
        build = self.distribution.get_command_obj('build_embed')
        self.distribution.cmdclass['build'] = build
