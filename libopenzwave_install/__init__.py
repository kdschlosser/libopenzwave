# -*- coding: utf-8 -*-


from .install import install as _install
from .install_shared import install_shared as _install_shared
from .install_embed import install_embed as _install_embed
from .install_embed_shared import install_embed_shared as _install_embed_shared

install = _install
install_shared = _install_shared
install_embed = _install_embed
install_embed_shared = _install_embed_shared
