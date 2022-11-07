# -*- coding: utf-8 -*-

import sys

print('Getting Library for platform {0}'.format(sys.platform))

os = sys.platform.lower()

if os.startswith('win'):
    from .windows import Library
elif os.startswith("cygwin"):
    from .cygwin import Library
elif os.startswith("darwin"):
    from .darwin import Library
elif os.startswith('freebsd'):
    from .freebsd import Library
elif os.startswith('netbsd'):
    from .netbsd import Library
elif os.startswith('sunos'):
    from .sunos import Library
elif os.startswith('linux'):
    from .linux import Library
else:
    raise RuntimeError(
        "No Library available for platform {0}".format(sys.platform)
    )

library = Library()
