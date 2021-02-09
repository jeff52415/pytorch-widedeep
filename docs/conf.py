# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os
import re
import sys

# import pytorch_sphinx_theme
from sphinx.ext.napoleon.docstring import GoogleDocstring

# this adds the equivalent of "../../" to the python path
PACKAGEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PACKAGEDIR)


# -- Project information -----------------------------------------------------

project = "pytorch-widedeep"
copyright = "2021, Javier Rodriguez Zaurin"
author = "Javier Rodriguez Zaurin"

# # The full version, including alpha/beta/rc tags
# def get_version():
#     r"""

#     Get the current version number for the library
#     Returns
#     -------
#     String
#         Of the form "<major>.<minor>.<micro>", in which "major", "minor" and "micro" are numbers

#   """
#     with open("../pytorch_widedeep/VERSION") as f:
#         return f.read().strip()
# release = get_version()

with open(os.path.join(PACKAGEDIR, "pytorch_widedeep", "version.py")) as f:
    version = re.search(r"__version__ \= \"(\d+\.\d+\.\d+)\"", f.read())
    assert version is not None, "can't parse __version__ from __init__.py"
    version = version.groups()[0]  # type: ignore[assignment]
    assert len(version.split(".")) == 3, "bad version spec"  # type: ignore[attr-defined]
    release = version

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "recommonmark",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_markdown_tables",
    "sphinx_copybutton",
    "sphinx.ext.githubpages",
]

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

autosummary_generate = True

napoleon_use_ivar = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = [".rst", ".md"]
# source_suffix = '.rst'

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [u"_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# Remove the prompt when copying examples
copybutton_prompt_text = ">>> "

autoclass_content = "init"  # 'both'
autodoc_member_order = "bysource"
# autodoc_default_flags = ["show-inheritance"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
# html_theme = "pytorch_sphinx_theme"
# html_theme_path = [pytorch_sphinx_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# This must be the name of an image file (path relative to the configuration
# directory) that is the favicon of the docs. Modern browsers use this as
# the icon for tabs, windows and bookmarks. It should be a Windows-style
# icon file (.ico).
html_favicon = "_static/img/widedeep_logo_docs.ico"
html_logo = "_static/img/widedeep_logo_docs.png"
html_theme_options = {
    "canonical_url": "https://pytorch-widedeep.readthedocs.io/en/latest/",
    "collapse_navigation": False,
    "logo_only": True,
    "display_version": True,
}
# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "pytorch_widedeepdoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {  # type: ignore[var-annotated]
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
    (
        master_doc,
        "pytorch_widedeep.tex",
        "pytorch_widedeep Documentation",
        "Javier Rodriguez Zaurin",
        "manual",
    ),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, "pytorch_widedeep", "pytorch_widedeep Documentation", [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "pytorch_widedeep",
        "pytorch_widedeep Documentation",
        author,
        "pytorch_widedeep",
        "One line description of project.",
        "Miscellaneous",
    ),
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
epub_exclude_files = ["search.html"]


def setup(app):
    # app.add_css_file("ignite_style.css")
    app.add_css_file("style.css")


# -- Extensions to the  Napoleon GoogleDocstring class ---------------------
# first, we define new methods for any new sections and add them to the class
def parse_keys_section(self, section):
    return self._format_fields("Keys", self._consume_fields())


GoogleDocstring._parse_keys_section = parse_keys_section  # type: ignore[attr-defined]


def parse_attributes_section(self, section):
    return self._format_fields("Attributes", self._consume_fields())


GoogleDocstring._parse_attributes_section = parse_attributes_section  # type: ignore[assignment]


def parse_class_attributes_section(self, section):
    return self._format_fields("Class Attributes", self._consume_fields())


GoogleDocstring._parse_class_attributes_section = parse_class_attributes_section  # type: ignore[attr-defined]


# we now patch the parse method to guarantee that the the above methods are
# assigned to the _section dict
def patched_parse(self):
    self._sections["keys"] = self._parse_keys_section
    self._sections["class attributes"] = self._parse_class_attributes_section
    self._unpatched_parse()


GoogleDocstring._unpatched_parse = GoogleDocstring._parse  # type: ignore[attr-defined]
GoogleDocstring._parse = patched_parse  # type: ignore[assignment]
