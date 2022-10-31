# -*- coding: utf-8 -*-

import sys

print('Getting Library for platform {0}'.format(sys.platform))

if sys.platform.startswith('win'):
    from .windows import Library
elif sys.platform.startswith("cygwin"):
    from .cygwin import Library
elif sys.platform.startswith("darwin"):
    from .darwin import Library
elif sys.platform.startswith('freebsd'):
    from .freebsd import Library
elif sys.platform.startswith('sunos'):
    from .sunos import Library
elif sys.platform.startswith('linux'):
    from .linux import Library
else:
    raise RuntimeError(
        "No Library available for platform {0}".format(sys.platform)
    )

library = Library()
