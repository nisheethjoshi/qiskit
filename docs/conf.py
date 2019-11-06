# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2018.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import sphinx_rtd_theme


# -- Project information -----------------------------------------------------
from distutils import dir_util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import warnings

project = 'Qiskit'
copyright = '2019, Qiskit Development Team'
author = 'Qiskit Development Team'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = '0.15.0'

# Elements with api doc sources
qiskit_elements = ['qiskit-ignis', 'qiskit-terra', 'qiskit-aer',
                   'qiskit-aqua', 'qiskit-ibmq-provider']
apidocs_exists = False


def _get_current_versions(app):
    versions = {}
    setup_py_path = os.path.join(os.path.dirname(app.srcdir), 'setup.py')
    with open(setup_py_path, 'r') as fd:
        setup_py = fd.read()
        for package in qiskit_elements:
            version_regex = re.compile(package + '[=|>]=(.*)\"')
            match = version_regex.search(setup_py)
            if match:
                ver = match[1]
                versions[package] = ver
    return versions


def _git_copy(package, sha1, api_docs_dir):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            github_source = 'https://github.com/Qiskit/%s' % package
            subprocess.run(['git', 'clone', github_source, temp_dir],
                           capture_output=True)
            subprocess.run(['git', 'checkout', sha1], cwd=temp_dir,
                           capture_output=True)
            shutil.copytree(os.path.join(temp_dir, 'docs'),
                            os.path.join(api_docs_dir, package))
    except FileNotFoundError:
        warnings.warn('Copy from git failed for %s at %s, skipping...' %
                      (package, sha1), RuntimeWarning)


def load_api_sources(app):
    api_docs_dir = os.path.join(app.srcdir, 'apidoc')
    if os.path.isdir(api_docs_dir):
        global apidocs_exists
        apidocs_exists = True
        warnings.warn('docs/apidocs already exists skipping source clone')
        return
    meta_versions = _get_current_versions(app)
    for package in qiskit_elements:
        _git_copy(package, meta_versions[package], api_docs_dir)


def clean_api_source(app, exc):
    global apidocs_exists
    if apidocs_exists:
        return
    api_docs_dir = os.path.join(app.srcdir, 'apidoc')
    shutil.rmtree(api_docs_dir)

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx.ext.viewcode',
    'sphinx.ext.extlinks',
    'sphinx_tabs.tabs',
    'sphinx_automodapi.automodapi',
    'jupyter_sphinx.execute',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['theme/']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# If true, figures, tables and code-blocks are automatically numbered if they
# have a caption.
numfig = True

# A dictionary mapping 'figure', 'table', 'code-block' and 'section' to
# strings that are used for format of figure numbers. As a special character,
# %s will be replaced to figure number.
numfig_format = {
    'table': 'Table %s'
}
# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# For Adding Locale
locale_dirs = ['locale/']   # path is example but recommended.
gettext_compact = False     # optional.

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'colorful'

# A boolean that decides whether module names are prepended to all object names
# (for object types where a “module” of some kind is defined), e.g. for
# py:function directives.
add_module_names = False

# A list of prefixes that are ignored for sorting the Python module index
# (e.g., if this is set to ['foo.'], then foo.bar is shown under B, not F).
# This can be handy if you document a project that consists of a single
# package. Works only for the HTML builder currently.
modindex_common_prefix = ['qiskit.']

# -- Configuration for extlinks extension ------------------------------------
# Refer to https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html

extlinks = {
    'pull_terra': ('https://github.com/Qiskit/qiskit-terra/pull/%s', '#'),
    'pull_aqua': ('https://github.com/Qiskit/qiskit-aqua/pull/%s', '#'),
    'pull_aer': ('https://github.com/Qiskit/qiskit-aer/pull/%s', '#'),
    'pull_ignis': ('https://github.com/Qiskit/qiskit-ignis/pull/%s', '#'),
    'pull_ibmq-provider': ('https://github.com/Qiskit/qiskit-ibmq-provider/pull/%s', '#')
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

html_theme_path = ['.', sphinx_rtd_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
    'style_nav_header_background': '#212121',

}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['theme/static/']

html_logo = 'theme/static/img/logo.png'
html_favicon = 'theme/static/img/favicon.ico'

html_last_updated_fmt = '%Y/%m/%d'

html_copy_source = False

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'Qiskitdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Qiskit.tex', 'Qiskit Documentation',
     'Qiskit Development Team', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'qiskit', 'Qiskit Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Qiskit', 'Qiskit Documentation',
     author, 'Qiskit', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

autosummary_generate = True

autodoc_default_options = {
    'inherited-members': None,
}

autoclass_content = 'both'
# -- Extension configuration -------------------------------------------------

# Elements with api doc sources
qiskit_elements = ['qiskit-ignis', 'qiskit-terra', 'qiskit-aer',
                   'qiskit-aqua', 'qiskit-ibmq-provider']
apidocs_exists = False
apidocs_master = None


def _get_current_versions(app):
    versions = {}
    setup_py_path = os.path.join(os.path.dirname(app.srcdir), 'setup.py')
    with open(setup_py_path, 'r') as fd:
        setup_py = fd.read()
        for package in qiskit_elements:
            version_regex = re.compile(package + '[=|>]=(.*)\"')
            match = version_regex.search(setup_py)
            if match:
                ver = match[1]
                versions[package] = ver
    return versions


def _install_from_master():
    github_url = [
        'git+https://github.com/Qiskit/%s' %
        package for package in qiskit_elements]
    cmd = [sys.executable, '-m', 'pip', 'install', '-U']
    cmd += github_url
    subprocess.run(cmd)


def _git_copy(package, sha1, api_docs_dir):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            github_source = 'https://github.com/Qiskit/%s' % package
            subprocess.run(['git', 'clone', github_source, temp_dir],
                           capture_output=True)
            subprocess.run(['git', 'checkout', sha1], cwd=temp_dir,
                           capture_output=True)
            dir_util.copy_tree(
                os.path.join(temp_dir, 'docs', 'apidocs'),
                api_docs_dir)
    except FileNotFoundError:
        warnings.warn('Copy from git failed for %s at %s, skipping...' %
                      (package, sha1), RuntimeWarning)


def load_api_sources(app):
    api_docs_dir = os.path.join(app.srcdir, 'apidoc')
    if os.getenv('DOCS_FROM_MASTER'):
        global apidocs_master
        apidocs_master = tempfile.mkdtemp()
        shutil.move(api_docs_dir, apidocs_master)
        _install_from_master()
        for package in qiskit_elements:
            _git_copy(package, 'HEAD', api_docs_dir)
        return
    elif os.path.isdir(api_docs_dir):
        global apidocs_exists
        apidocs_exists = True
        warnings.warn('docs/apidocs already exists skipping source clone')
        return
    meta_versions = _get_current_versions(app)
    for package in qiskit_elements:
        _git_copy(package, meta_versions[package], api_docs_dir)


def clean_api_source(app, exc):
    api_docs_dir = os.path.join(app.srcdir, 'apidoc')
    global apidocs_exists
    global apidocs_master
    if apidocs_exists:
        return
    elif apidocs_master:
        shutil.rmtree(api_docs_dir)
        shutil.move(os.path.join(apidocs_master, 'apidoc'), api_docs_dir)
        return
    shutil.rmtree(api_docs_dir)

# -- Extension configuration -------------------------------------------------

def setup(app):
    app.setup_extension('versionutils')
    app.add_css_file('css/theme-override.css')
    app.connect('builder-inited', load_api_sources)
    app.connect('build-finished', clean_api_source)
