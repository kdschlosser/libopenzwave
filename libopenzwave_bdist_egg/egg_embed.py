# -*- coding: utf-8 -*-

from .egg import egg


class egg_embed(egg):

    def finalize_options(self):
        builder = self.distribution.get_command_obj('build_embed')
        builder.ensure_finalized()

        egg.finalize_options(self)
