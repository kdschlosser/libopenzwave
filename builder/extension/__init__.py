# -*- coding: utf-8 -*-

import sys
from distutils import log as LOG


LOG.info('Getting Extension for platform {0}'.format(sys.platform))

if sys.platform.startswith('win'):
    from .windows import Extension

elif sys.platform.startswith("cygwin"):
    from .cygwin import Extension

elif sys.platform.startswith("darwin"):
    from .darwin import Extension

elif sys.platform.startswith('freebsd'):
    from .freebsd import Extension

elif sys.platform.startswith('sunos'):
    from .sunos import Extension

elif sys.platform.startswith('linux'):
    from .linux import Extension

else:
    raise RuntimeError(
        "No Extension available for platform {0}".format(sys.platform)
    )

extension = Extension()
