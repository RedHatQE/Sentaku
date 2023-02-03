from __future__ import annotations
import sys
import os
import importlib.metadata

sys.path.insert(0, os.path.abspath("../examples"))

__distribution = importlib.metadata.distribution("Sentaku")

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

# General information about the project.
project = __distribution.metadata["Name"]
copyright = "2016, Ronny Pfannschmidt"
author = "Ronny Pfannschmidt"

release = __distribution.version
version = ".".join(release.split(".")[:2])

exclude_patterns: list[str] = []

pygments_style = "sphinx"
todo_include_todos = False

html_theme = "haiku"
html_static_path: list[str] = []

htmlhelp_basename = "sentakudoc"
