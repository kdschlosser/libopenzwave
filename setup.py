# -*- coding: utf-8 -*-
# **libopenzwave** is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# **libopenzwave** is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with libopenzwave. If not, see http://www.gnu.org/licenses.

"""
This file is part of the **libopenzwave** project

:platform: Unix, Windows, OSX
:license: GPL(v3)
:synopsis: Install/Build program
    To use this module you can run it directly using python or it can be run
    using easy_install (setuptools) or pip.

    * primary parameters:

        * build: compiles the program output is in the directory `build` where
          this file is located
        * build_embed: builds a pre compiled version
        * build_shared: builds using a shared openzwave library
        * install: compiles and installs the program
        * install_embed: installs a pre compiled version
        * install_shared: builds and installs a shared openzwave library
          version
        * bdist_wheel: builds the standard version or development version and
          packages it into a wheel file. This is useful for multiple
          installations on say a raspberry pi where ti could take a long time
          to compile on each one of them.
        * bdist_egg:  builds the standard version into an egg file. similar
          to bdist_wheel
        * build_docs: builds the documentation

    * secondary parameters:

        * --dev {path to github zipball file (optional)}: the --dev switch can
          be added to any of the above commands. the --dev switch will download
          the master branch of openzwave to use or optionally the zipball
          provided. If the --dev parameter is not specified then the latest
          release of openzwave that is supported by this version of the library
          will be used.

    There are 2 optional modules included with libopenzwave. These can be
    installed using the following command line parameters

    * optional modules:

        * --service:  Run libopenzwave as a service (Windows, OSX, Linux)
        * --manager: GUI based manager (Windows, OSX, Linux)
        * --remote_access: The remote access allows you to use a client/server
          arrangement. There is very minimal code changes needed to use this
          feature

.. moduleauthor:: Kevin G Schlosser
"""

sphinx_extra_lines = '''
# uncomment all of the lines below to have it build a new node_types rst file
# node_types_doc = []
# 
# def gen_doc(name):
#     from libopenzwave import node_types
# 
#     header = ['-' * len(name)]
#     header += [name]
#     header += [header[0]]
#     header += ['']
#     
#     def get_key(val):
#         for k, v in node_types.__dict__.items():
#             if v == val:
#                 return k
# 
#     items = getattr(node_types, name.replace(' ', '_').upper())
#     for item in items:
#         key = get_key(item)
#         if key is None:
#             continue
#         
#         header += ['.. py:data:: libopenzwave.node_types.' + key]
#         header += ['']
#         header += ['    * `str(' + key + ')`: ' + str(item)]
#         header += ['    * `int(' + key + ')`: 0x' + hex(int(item))[2:].upper()]
#         
#         if name == 'Generic Types':
#         
#             if not item.specific_types:
#                 header += ['    * Specific Types: `None`']
#                 header += ['', '']
#                 continue
#                 
#             header += ['    * Specific Types:']
#             header += ['']
#                 
#             for specific_type in item.specific_types:
#                 key = get_key(specific_type)
#                 if key is None:
#                     continue
#                    
#                 header += ['        * `' + key + '`: ']
#                 header += ['']
#                 header += ['            * `str(' + key + ')`: ' + str(specific_type)]
#                 header += ['            * `int(' + key + ')`: 0x' + hex(int(specific_type))[2:].upper()]
#                 header += ['']
#                 
#             header += ['']
#                 
#         header += ['', '']
# 
#     header += ['', '']
#     header = '\\n'.join(header)
#     node_types_doc.append(header)
# 

def setup(app):
    # gen_doc('Basic Types')
    # gen_doc('Generic Types')
    # gen_doc('Role Types')
    # gen_doc('Device Types')
    # gen_doc('Node Types')
    # 
    # with open('docs/libopenzwave/node_types.rst', 'w') as f:
    #     f.write('========================\\n')
    #     f.write('Node Types documentation\\n')
    #     f.write('========================\\n\\n\\n')
    #     f.write('\\n'.join(node_types_doc))

    app.add_stylesheet('css/libopenzwave.css')
'''  # NOQA

if __name__ == '__main__':
    import os
    import sys

    print(sys.argv)

    if '--DISTUTILS_DEBUG' in sys.argv:
        os.environ['DISTUTILS_DEBUG'] = '1'
        sys.argv.remove('--DISTUTILS_DEBUG')

    for arg in sys.argv[:]:
        if arg.startswith('--bdist-dir'):
            bdist_dir = arg.split('=', 1)[-1]
            sys.argv.remove(arg)
            break
    else:
        bdist_dir = None

    if 'clean' in sys.argv:
        import shutil

        sys.argv.remove('clean')

        base_path = os.path.abspath(os.path.dirname(__file__))

        build_path = os.path.join(base_path, 'build')
        ozw_path = os.path.join(base_path, 'openzwave')
        lib_path = os.path.join(
            base_path,
            '_libopenzwave',
            '_libopenzwave.cpp'
        )

        if os.path.exists(build_path):
            shutil.rmtree(build_path)

        if os.path.exists(ozw_path):
            shutil.rmtree(ozw_path)

        if os.path.exists(lib_path):
            os.remove(lib_path)

        print('Clean Finished!')

        if len(sys.argv) == 1:
            sys.exit(0)


    import builder  # NOQA

    builder.setup()

    if '--no_deps' in sys.argv:
        sys.argv.remove('--no_deps')

    dev_repo = None
    if '--dev' in sys.argv:
        next_arg_index = sys.argv.index('--dev') + 1
        if len(sys.argv) > next_arg_index:
            if sys.argv[next_arg_index].startswith('http'):
                dev_repo = sys.argv.pop(next_arg_index)

    #
    # # set the wheel output folder if a wheel is being generated
    # if 'bdist_wheel' in sys.argv:
    #     sys.argv[sys.argv.index('bdist_wheel')] = 'wheel'

    install_requires = [
        'pyserial',
        'pycryptodome',
        'lxml',
    ]

    _verbose = '--verbose' in sys.argv

    import distutils.file_util  # NOQA
    import version  # NOQA

    _copy_file = distutils.file_util.copy_file  # NOQA


    def copy_file(
        src,
        dst,
        preserve_mode=1,
        preserve_times=1,
        update=0,
        link=None,
        verbose=1,  # NOQA
        dry_run=0
    ):
        return _copy_file(
            src,
            dst,
            preserve_mode=preserve_mode,
            preserve_times=preserve_times,
            update=update,
            link=link,
            verbose=int(_verbose),
            dry_run=dry_run
        )


    distutils.file_util.copy_file = copy_file  # NOQA

    from setuptools import setup, find_packages # NOQA

    if '--dev' in sys.argv:
        sys.argv.remove('--dev')
        options = dict(
            build_docs=dict(dev=True),
            bdist_egg=dict(dev=True, bdist_dir=bdist_dir),
            build=dict(dev=True, dev_repo=dev_repo),
            install=dict(dev=True),
        )

    else:
        options = dict(
            bdist_egg=dict(bdist_dir=bdist_dir),
        )

    if '--cython' in sys.argv:
        sys.argv.remove('--cython')

        if 'build' in options:
            options['build']['cython'] = True
        else:
            options['build'] = dict(
                cython=True
            )

    if 'build_docs' in sys.argv:
        options['build_docs'] = options.get('build_docs', dict())
        bd = options['build_docs']
        bd['full_traceback'] = True

        for arg in sys.argv[:]:
            for switch in ('--source-path', '--builder-name'):
                if arg.startswith(switch):
                    name, value = list(item.strip() for item in arg.split('='))
                    name = name[2:].replace('-', '_')
                    bd[name] = value
                    sys.argv.remove(arg)

        if '--full-traceback' in sys.argv:
            sys.argv.remove('--full-traceback')

        for key, value in (
            ('source_path', 'docs'),
            ('builder_name', 'html'),
        ):
            bd[key] = bd.get(key, value)

        sphinx_conf = builder.build_docs.ConfigOptions()
        builder.build_docs.sphinx_conf = sphinx_conf

        # -- GENERAL options ---------------------------------------------------
        sphinx_conf.suppress_warnings = ['image.nonlocal_uri']
        sphinx_conf.extensions = [
            'sphinx.ext.autodoc',
            'sphinx.ext.todo',
            'sphinx.ext.doctest',
            'sphinx.ext.viewcode',
            'sphinx.ext.autosummary',
            'sphinxcontrib.blockdiag',
            'sphinxcontrib.nwdiag',
            'sphinxcontrib.actdiag',
            'sphinxcontrib.seqdiag',
            'sphinxcontrib.fulltoc',
            'sphinx_sitemap',
            'sphinx.ext.graphviz',
            'sphinx.ext.inheritance_diagram'
        ]

        if sys.platform.startswith('win'):
            sphinx_conf.blockdiag_fontpath = os.path.join(
                os.path.expandvars('%WINDIR%'),
                'Fonts',
                'Arial.ttf'
            )
        else:
            sphinx_conf.blockdiag_fontpath = (
                '/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf'
            )
        sphinx_conf.templates_path = ['_templates']
        sphinx_conf.source_suffix = '.rst'
        sphinx_conf.master_doc = 'index'
        sphinx_conf.version = version.libopenzwave_version_short
        sphinx_conf.release = version.libopenzwave_version
        sphinx_conf.exclude_patterns = ['_build']
        sphinx_conf.add_function_parentheses = True
        sphinx_conf.show_authors = True
        sphinx_conf.pygments_style = 'sphinx'
        sphinx_conf.add_module_names = True

        # -- Options for HTML output -------------------------------------------
        sphinx_conf.html_baseurl = '/docs/'
        sphinx_conf.html_theme = 'groundwork'
        sphinx_conf.html_theme_options = {
            "sidebar_width": '240px',
            "stickysidebar": True,
            "stickysidebarscrollable": True,
            "contribute": True,
            "github_fork": "kdschlosser/libopenzwave",
            "github_user": "kdschlosser",
        }
        sphinx_conf.html_theme_path = ["_themes"]
        sphinx_conf.html_title = 'libopenzwave'
        sphinx_conf.html_logo = '_static/images/logo.png'
        sphinx_conf.html_static_path = ['_static']
        sphinx_conf.html_domain_indices = True
        sphinx_conf.html_use_index = True
        sphinx_conf.html_split_index = False
        sphinx_conf.html_show_sourcelink = True
        sphinx_conf.html_sourcelink_suffix = '.py'
        sphinx_conf.html_experimental_html5_writer = True
        sphinx_conf.html_show_sphinx = False
        sphinx_conf.html_copy_source = True
        sphinx_conf.html_show_copyright = True
        sphinx_conf.htmlhelp_basename = 'libopenzwave'
        sphinx_conf.html_sidebars = {
            '**': [
                'globaltoc.html',
                'sourcelink.html',
                'searchbox.html'
            ],
            'using/windows': [
                'windowssidebar.html',
                'searchbox.html'
            ],
        }

        # -- Options for LATEX output ------------------------------------------
        sphinx_conf.latex_elements = {}
        sphinx_conf.latex_documents = [
          ('index', 'libopenzwave.tex', u'libopenzwave Documentation',
           u'kdschlosser', 'manual'),
        ]

        # -- Options for MAN PAGES output --------------------------------------
        sphinx_conf.man_pages = [
            ('index', 'libopenzwave', u'libopenzwave Documentation',
             [u'kdschlosser'], 1)
        ]

        # -- Options for TEXT INFO output --------------------------------------
        sphinx_conf.texinfo_documents = [
            (
                'index',
                'libopenzwave',
                'libopenzwave Documentation',
                'kdschlosser',
                'libopenzwave',
                'One line description of project.',
                'Miscellaneous'
            ),
        ]

        sphinx_conf.additional_lines = sphinx_extra_lines

    packages = []
    package_dir = dict(
        libopenzwave='libopenzwave',
        _libopenzwave='_libopenzwave'
    )

    entry_points = dict()

    if '--manager' in sys.argv:
        install_requires += ['wxPython>=4.0.2']
        sys.argv.remove('--manager')
        package_dir['libopenzwave_man'] = 'libopenzwave_man'
        packages += [
            'libopenzwave.scripts'
        ]

        entry_points['console_scripts'] = [
            'libopenzwave_manager=libopenzwave.scripts.'
            'libopenzwave_manager:main'
        ]
    if '--service' in sys.argv:
        sys.argv.remove('--service')
        install_requires += [
            "pywin32>=223;sys_platform=='win32'",
            "sdnotify;sys_platform!='win32'"
        ]

        cs = entry_points.get('console_scripts', [])
        cs.append(
            'libopenzwave_service=libopenzwave.scripts.'
            'libopenzwave_service:main'
        )

        if 'libopenzwave.scripts' not in packages:
            packages.append('libopenzwave.scripts')

        entry_points['console_scripts'] = cs

    setup(
        name='libopenzwave',
        author='Kevin G. Schlosser',
        author_email='',
        version=version.libopenzwave_version,
        zip_safe=False,
        options=options,
        url='https://github.com/kdschlosser/libopenzwave',
        ext_modules=[builder.extension],
        libraries=[builder.library],
        install_requires=install_requires,
        cmdclass=dict(
            build_clib=builder.build_clib,
            build_docs=builder.build_docs,
            bdist_egg=builder.bdist_egg,
            build=builder.build,
            install=builder.install,
            build_ext=builder.build_ext,
            build_config=builder.build_config,
            build_stub=builder.build_stub,
        ),
        packages=packages,
        entry_points=entry_points,
        package_dir=package_dir,
        description=(
            'libopenzwave is a python wrapper for the openzwave c++ library.'
        ),
        long_description=(
            'A full API to map the ZWave network in Python objects. '
            'Look at examples at : https://github.com/kdschlosser/libopenzwave'
        ),
        keywords=['openzwave', 'zwave'],
        classifiers=[
            "Topic :: Home Automation",
            "Topic :: System :: Hardware",
            "Topic :: System :: Hardware :: Hardware Drivers",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
            "Operating System :: POSIX :: BSD",
            "Programming Language :: C++",
            "Programming Language :: Cython",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            (
                "License :: OSI Approved :: "
                "GNU General Public License v3 or later (GPLv3+)"
            ),
        ],
    )

    print('FINISHED!!')
