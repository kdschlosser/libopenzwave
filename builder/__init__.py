
from .bdist_egg import bdist_egg as _bdist_egg
from .bdist_wheel import bdist_wheel as _bdist_wheel
from .build import build as _build
from .build_clib import build_clib as _build_clib
from .build_config import build_config as _build_config
from .build_docs import build_docs as _build_docs
from .build_ext import build_ext as _build_ext
from .build_stub import build_stub as _build_stub
from .clean import clean as _clean
from .environment import setup as _setup
from .extension import extension as _extension
from .install import install as _install
from .library import library as _library
from .get_openzwave import get_openzwave as _get_openzwave

bdist_egg = _bdist_egg
bdist_wheel = _bdist_wheel
build = _build
build_clib = _build_clib
build_config = _build_config
build_docs = _build_docs
build_ext = _build_ext
build_stub = _build_stub
clean = _clean
setup = _setup
extension = _extension
get_openzwave = _get_openzwave
install = _install
library = _library
