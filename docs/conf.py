# -*- coding: utf-8 -*-
import sys
import os
import pkg_resources

sys.path.insert(0, os.path.abspath('../examples'))

__distribution = pkg_resources.get_distribution('Sentaku')

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

# General information about the project.
project = __distribution.project_name
copyright = u'2016, Ronny Pfannschmidt'
author = u'Ronny Pfannschmidt'

release = __distribution.version
version = '.'.join(release.split('.')[:2])

exclude_patterns = []

pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'haiku'
html_static_path = ['_static']

htmlhelp_basename = 'sentakudoc'
