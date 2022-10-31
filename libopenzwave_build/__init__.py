# -*- coding: utf-8 -*-

from .build import build as _build
from .build_shared import build_shared as _build_shared
from .build_embed import build_embed as _build_embed
from .build_embed_shared import build_embed_shared as _build_embed_shared

build = _build
build_shared = _build_shared
build_embed = _build_embed
build_embed_shared = _build_embed_shared
