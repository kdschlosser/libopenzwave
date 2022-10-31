# -*- coding: utf-8 -*-

suppress_warnings = ['image.nonlocal_uri']
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.todo', 'sphinx.ext.doctest', 'sphinx.ext.viewcode', 'sphinx.ext.autosummary', 'sphinxcontrib.blockdiag', 'sphinxcontrib.nwdiag', 'sphinxcontrib.actdiag', 'sphinxcontrib.seqdiag', 'sphinxcontrib.fulltoc', 'sphinx_sitemap', 'sphinx.ext.graphviz', 'sphinx.ext.inheritance_diagram']
blockdiag_fontpath = 'C:\\Windows\\Fonts\\Arial.ttf'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
version = '0.4.9'
release = '0.4.9'
exclude_patterns = ['_build']
add_function_parentheses = True
show_authors = True
pygments_style = 'sphinx'
html_baseurl = '/docs/'
html_theme = 'groundwork'
html_theme_options = {'sidebar_width': '240px', 'stickysidebar': True, 'stickysidebarscrollable': True, 'contribute': True, 'github_fork': 'OpenZWave/python-openzwave', 'github_user': 'OpenZWave'}
html_theme_path = ['_themes']
html_title = 'python-openzwave'
html_logo = '_static/images/logo.png'
html_static_path = ['_static']
html_domain_indices = True
html_use_index = True
html_split_index = True
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True
htmlhelp_basename = 'python-openzwave'
latex_elements = {}
latex_documents = [('index', 'python-openzwave.tex', 'python-openzwave Documentation', 'bibi21000', 'manual')]
man_pages = [('index', 'python-openzwave', 'python-openzwave Documentation', ['bibi21000'], 1)]
texinfo_documents = [('index', 'python-openzwave', 'python-openzwave Documentation', 'bibi21000', 'python-openzwave', 'One line description of project.', 'Miscellaneous')]
project = 'python_openzwave'
author = 'Sébastien GALLET aka bibi2100'
copyright = '2019 python_openzwave'


def setup(app):
    app.add_stylesheet('css/python_openzwave.css')

