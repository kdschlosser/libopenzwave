# -*- coding: utf-8 -*-

from .egg import egg


class egg_shared(egg):

    def finalize_options(self):
        builder = self.distribution.get_command_obj('build_shared')
        builder.ensure_finalized()

        egg.finalize_options(self)
