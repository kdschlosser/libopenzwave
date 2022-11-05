# -*- coding: utf-8 -*-

import sys
import os
import platform
from setuptools.command.easy_install import find_executable  # NOQA


AR = None
RANLIB = None
C = None
CPP = None
LD = None
MAKE = None
PACKAGE_CONFIG = None


def check_packages(*needed_packages):
    global PACKAGE_CONFIG

    pkg_config = find_executable("pkg-config")

    if pkg_config:
        PACKAGE_CONFIG = pkg_config
        print("Found pkg-config : {0}".format(pkg_config))

        import libopenzwave_pkgconfig

        packages = libopenzwave_pkgconfig.list_all()

        for package in needed_packages:
            if package not in packages:
                raise RuntimeError('Missing package "{0}"'.format(package))

            print('Found Package "{0}"'.format(package))


def setup():
    global AR
    global RANLIB
    global C
    global CPP
    global LD
    global MAKE

    os_ = sys.platform.lower()

    if os_.startswith('win'):
        import libopenzwave_library  # NOQA

    elif os_.startswith("cygwin"):
        gcc = find_executable("gcc")
        gpp = find_executable("g++")
        ar = find_executable('ar')
        ld = find_executable('ld')
        ranlib = find_executable('ranlib')
        cc = os.environ.get('CC', '')
        cxx = os.environ.get('CXX', '')
        ar_env = os.environ.get('AR', '')
        ld_env = os.environ.get('LD', '')
        ranlib_env = os.environ.get('RANLIB', '')

        if ld:
            if ld != ld_env and 'ld' in ld_env:
                ld = ld_env
        elif 'ld' in ld_env:
            ld = ld_env
        else:
            raise RuntimeError('Unable to locate ld')

        if ranlib:
            if ranlib != ranlib_env and 'ranlib' in ranlib_env:
                ranlib = ranlib_env
        elif 'ranlib' in ranlib_env:
            ranlib = ranlib_env
        else:
            raise RuntimeError('Unable to locate ranlib')

        if ar:
            if ar != ar_env and 'ar' in ar_env:
                ar = ar_env
        elif 'ar' in ar_env:
            ar = ar_env
        else:
            raise RuntimeError('Unable to locate ar')

        if gcc:
            if gcc != cc and 'gcc' in cc:
                gcc = cc
        elif 'gcc' in cc:
            gcc = cc
        else:
            raise RuntimeError('Unable to locate gcc')

        if gpp:
            if gpp != cxx and 'g++' in cxx:
                gpp = cxx
        elif 'g++' in cxx:
            gpp = cxx
        else:
            raise RuntimeError('Unable to locate g++')

        AR = ar
        C = gcc
        CPP = gpp
        RANLIB = ranlib
        LD = ld

        print("Found gcc : {0}".format(gcc))
        print("Found g++ : {0}".format(gpp))
        print("Found ar : {0}".format(ar))
        print("Found ld : {0}".format(ld))
        print("Found ranlib : {0}".format(ranlib))

        os.environ['CC'] = gcc
        os.environ['CXX'] = gpp
        os.environ['AR'] = ar
        os.environ['RANLIB'] = ranlib
        os.environ['LD'] = ld

        check_packages()

    elif os_.startswith("darwin"):
        clang = find_executable("clang")
        clang_pp = find_executable("clang++")
        ar = find_executable('libtool')
        ld = clang_pp
        ranlib = find_executable('ranlib')
        cc = os.environ.get('CC', '')
        cxx = os.environ.get('CXX', '')
        ar_env = os.environ.get('AR', '')
        ld_env = os.environ.get('LD', '')
        ranlib_env = os.environ.get('RANLIB', '')

        if ranlib:
            if ranlib != ranlib_env and 'ranlib' in ranlib_env:
                ranlib = ranlib_env
        elif 'ranlib' in ranlib_env:
            ranlib = ranlib_env
        else:
            raise RuntimeError('Unable to locate ranlib')

        if ar:
            if ar != ar_env and 'libtool' in ar_env:
                ar = ar_env
        elif 'libtool' in ar_env:
            ar = ar_env
        else:
            raise RuntimeError('Unable to locate ar')

        if clang:
            if clang != cc and 'clang' in cc:
                clang = cc
        elif 'clang' in cc:
            clang = cc
        else:
            raise RuntimeError('Unable to locate clang')

        if clang_pp:
            if clang_pp != cxx and 'clang++' in cxx:
                clang_pp = cxx
        elif 'clang++' in cxx:
            clang_pp = cxx
        else:
            raise RuntimeError('Unable to locate clang++')

        if ld:
            if ld != ld_env and 'clang++' in ld_env:
                ld = ld_env
        elif 'clang++' in ld_env:
            ld = ld_env
        else:
            ld = clang_pp

        AR = ar
        C = clang
        CPP = clang_pp
        RANLIB = ranlib
        LD = ld

        print("Found clang : {0}".format(clang))
        print("Found clang++ : {0}".format(clang_pp))
        print("Found ar : {0}".format(ar))
        print("Found ld : {0}".format(ld))
        print("Found ranlib : {0}".format(ranlib))

        os.environ['CXX'] = clang_pp
        os.environ['AR'] = ar
        os.environ['LD'] = ld
        os.environ['CC'] = clang
        os.environ['RANLIB'] = ranlib

        check_packages()

    elif os_.startswith('freebsd'):

        c = find_executable("cc")
        cpp = find_executable("c++")

        gmake = find_executable("gmake")

        cc = os.environ.get('CC', '')
        cxx = os.environ.get('CXX', '')

        ar = find_executable("ar")
        ar_env = os.environ.get('AR', '')

        ranlib = find_executable("ranlib")
        ranlib_env = os.environ.get('RANLIB', '')

        ld_env = os.environ.get('LD', '')

        if c:
            if c != cc and 'cc' in cc:
                c = cc
        elif 'cc' in cc:
            c = cc
        else:
            raise RuntimeError('Unable to locate cc')

        if cpp:
            if cpp != cxx and 'c++' in cxx:
                cpp = cxx
        elif 'c++' in cxx:
            cpp = cxx
        else:
            raise RuntimeError('Unable to locate c++')

        if ar:
            if ar != ar_env and 'ar' in ar_env:
                ar = ar_env
        elif 'ar' in ar_env:
            ar = ar_env
        else:
            raise RuntimeError('Unable to locate ar')

        if ranlib:
            if ranlib != ranlib_env and 'ranlib' in ranlib_env:
                ranlib = ranlib_env
        elif 'ranlib' in ranlib_env:
            ranlib = ranlib_env
        else:
            raise RuntimeError('Unable to locate ranlib')

        if ld_env:
            if ld_env != cpp and 'c++' in ld_env:
                ld = ld_env
            else:
                ld = cpp
        else:
            ld = cpp

        AR = ar
        C = c
        CPP = cpp
        RANLIB = ranlib
        LD = ld
        MAKE = gmake

        print("Found cc : {0}".format(c))
        print("Found c++ : {0}".format(cpp))
        print("Found ranlib : {0}".format(ranlib))
        print("Found ld : {0}".format(ld))
        print("Found ar : {0}".format(ar))
        print("Found gmake : {0}".format(gmake))

        os.environ['CXX'] = cpp
        os.environ['CC'] = c
        os.environ['LD'] = ld
        os.environ['AR'] = ar
        os.environ['RANLIB'] = ranlib

        packages = ['libresolv', 'libusb-1.0', 'e2fsprogs-libuuid']

        version = tuple(
            int(item) for item in platform.release().split('.'))

        if len(version) < 3:
            version += (0,)

        if version < (10, 2, 0):
            packages.append('libiconv')

        check_packages(*packages)

    elif os_.startswith('netbsd'):

        c = find_executable("gcc")
        cpp = find_executable("g++")

        gmake = find_executable("gmake")

        cc = os.environ.get('CC', '')
        cxx = os.environ.get('CXX', '')

        ar = find_executable("ar")
        ar_env = os.environ.get('AR', '')

        ranlib = find_executable("ranlib")
        ranlib_env = os.environ.get('RANLIB', '')

        ld_env = os.environ.get('LD', '')

        if c:
            if c != cc and 'gcc' in cc:
                c = cc
        elif 'gcc' in cc:
            c = cc
        else:
            raise RuntimeError('Unable to locate cc')

        if cpp:
            if cpp != cxx and 'g++' in cxx:
                cpp = cxx
        elif 'g++' in cxx:
            cpp = cxx
        else:
            raise RuntimeError('Unable to locate c++')

        if ar:
            if ar != ar_env and 'ar' in ar_env:
                ar = ar_env
        elif 'ar' in ar_env:
            ar = ar_env
        else:
            raise RuntimeError('Unable to locate ar')

        if ranlib:
            if ranlib != ranlib_env and 'ranlib' in ranlib_env:
                ranlib = ranlib_env
        elif 'ranlib' in ranlib_env:
            ranlib = ranlib_env
        else:
            raise RuntimeError('Unable to locate ranlib')

        if ld_env:
            if ld_env != cpp and 'c++' in ld_env:
                ld = ld_env
            else:
                ld = cpp
        else:
            ld = cpp

        AR = ar
        C = c
        CPP = cpp
        RANLIB = ranlib
        LD = ld
        MAKE = gmake

        print("Found cc : {0}".format(c))
        print("Found c++ : {0}".format(cpp))
        print("Found ranlib : {0}".format(ranlib))
        print("Found ld : {0}".format(ld))
        print("Found ar : {0}".format(ar))
        print("Found gmake : {0}".format(gmake))

        os.environ['CXX'] = cpp
        os.environ['CC'] = c
        os.environ['LD'] = ld
        os.environ['AR'] = ar
        os.environ['RANLIB'] = ranlib

        packages = ['libresolv', 'libusb-1.0']

        check_packages(*packages)

    elif os_.startswith('sunos'):

        gcc = find_executable("gcc")
        gpp = find_executable("g++")
        make = find_executable("make")
        cc = os.environ.get('CC', '')
        cxx = os.environ.get('CXX', '')

        if not make:
            raise RuntimeError('Unable to locate make')

        if gcc:
            if gcc != cc and cc.endswith('gcc'):
                gcc = cc
        elif cc.endswith('gcc'):
            gcc = cc
        else:
            raise RuntimeError('Unable to locate gcc')

        if gpp:
            if gpp != cxx and cxx.endswith('g++'):
                gpp = cxx

        elif cxx.endswith('g++'):
            gpp = cxx
        else:
            raise RuntimeError('Unable to locate g++')

        AR = 'ar'
        C = gcc
        CPP = gpp
        RANLIB = 'ranlib'
        LD = gpp
        MAKE = make

        os.environ['CC'] = gcc
        os.environ['LD'] = gpp
        os.environ['AR'] = 'ar'
        os.environ['RANLIB'] = 'ranlib'
        os.environ['CXX'] = gpp

        print("Found gcc : {0}".format(gcc))
        print("Found g++ : {0}".format(gpp))
        print("Found make : {0}".format(make))
        check_packages('libresolv', 'libiconv', 'libusb-1.0')

    elif os_.startswith('linux'):

        gcc = find_executable("gcc")
        gpp = find_executable("g++")
        ar = find_executable('ar')
        ld = find_executable('ld')
        ranlib = find_executable('ranlib')
        cc = os.environ.get('CC', '')
        cxx = os.environ.get('CXX', '')
        ar_env = os.environ.get('AR', '')
        ld_env = os.environ.get('LD', '')
        ranlib_env = os.environ.get('RANLIB', '')

        if ranlib:
            ranlib = 'ranlib'
            if ranlib != ranlib_env and ranlib_env.endswith('ranlib'):
                ranlib = ranlib_env
            else:
                os.environ['RANLIB'] = 'ranlib'
        elif ranlib_env.endswith('ranlib'):
            ranlib = ranlib_env
        else:
            raise RuntimeError('Unable to locate ranlib')

        if ar:
            if ar != ar_env and ar_env.endswith('ar'):
                ar = ar_env
            else:
                os.environ['AR'] = 'ar'
        elif ar_env.endswith('ar'):
            ar = ar_env
        else:
            raise RuntimeError('Unable to locate ar')

        if gcc:
            if gcc != cc and cc.endswith('gcc'):
                gcc = cc
            else:
                os.environ['CC'] = 'gcc'
        elif cc.endswith('gcc'):
            gcc = cc
        else:
            raise RuntimeError('Unable to locate gcc')

        print("Found gcc : {0}".format(gcc))

        if gpp:
            if gpp != cxx and cxx.endswith('g++'):
                gpp = cxx
            else:
                os.environ['CXX'] = 'g++'
        elif cxx.endswith('g++'):
            gpp = cxx
        else:
            raise RuntimeError('Unable to locate g++')

        if ld:
            if ld != ld_env and ar_env.endswith('ld'):
                ld = ld_env
            else:
                os.environ['LD'] = 'ld'
        elif ld_env.endswith('ld'):
            ld = ld_env
        else:
            ld = gpp
            os.environ['LD'] = 'g++'

        AR = ar
        C = gcc
        CPP = gpp
        RANLIB = ranlib
        LD = ld

        print("Found gcc : {0}".format(gcc))
        print("Found g++ : {0}".format(gpp))
        print("Found ar : {0}".format(ar))
        print("Found ld : {0}".format(ld))
        print("Found ranlib : {0}".format(ranlib))

        check_packages('libusb-1.0', 'liconv', 'libudev-dev')

    else:
        raise RuntimeError(
            "No Library available for platform {0}".format(sys.platform)
        )
