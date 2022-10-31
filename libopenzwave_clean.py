# -*- coding: utf-8 -*-

from distutils.command.clean import clean as _clean


class clean(_clean):
    def run(self):
        if getattr(self, 'all', False):
            current_template.clean_all()
        else:
            current_template.clean()
        _clean.run(self)
