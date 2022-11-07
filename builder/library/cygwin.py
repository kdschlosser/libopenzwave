# -*- coding: utf-8 -*-

from . import library_base
#
#
# # 64 bit
# top_srcdir = 'openzwave'
#
# STATIC_LIB_NAME = 'libopenzwave.a'
# SHARED_LIB_NAME = 'libopenzwave.dll'
#
# CFLAGS = [
#     '-c',
#     '-Wall',
#     '-Wno-unknown-pragmas',
#     '-Wno-format',
#     '-Wno-attributes',
#     '-Wno-error=sequence-point',
#     '-Wno-sequence-point',
#     '-O3',
#     '-DNDEBUG',
#     '-fPIC'
# ]
#
# LDFLAGS = ['-shared', '-Wl,-soname,$(SHARED_LIB_NAME)']  #  + RELEASE_LDFLAGS
# LIBS = ['-lsetupapi']
#
# LIBDIR = '.'
# OBJDIR = '.'
#
# INCLUDES = ['-I "openzwave/cpp/src"', '-I "openzwave/cpp/tinyxml/"',
# '-I "openzwave/cpp/hidapi/hidapi/"']
#
#
# # 32bit
# CFLAGS = ['-c', '-Wall', '-Wno-unknown-pragmas', '-Wno-format',
# '-DMINGW', '-O3']
#
# LIBDIR = 'openzwave/cpp/lib/windows-mingw32'
# INCLUDES = [
#     '-I "openzwave/cpp/src"',
#     '-I "openzwave/cpp/src/command_classes"',
#     '-I "openzwave/cpp/src/aes"',
#     '-I "openzwave/cpp/src/value_classes"',
#     '-I "openzwave/cpp/src/platform"',
#     '-I "openzwave/cpp/src/platform/windows"',
#     '-I "openzwave/cpp/tinyxml"',
#     '-I "openzwave/cpp/hidapi/hidapi"'
# ]


class Library(library_base.Library):
    pass
