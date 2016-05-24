#!/usr/bin/env python

from setuptools import setup

setup(name="sentaku",
      use_scm_version=True,
      author="RonnyPfannschmidt",
      author_email="opensource@ronnypfannschmidt.de",
      description="variadic ux implemntation for testing",
      license="GPLv3",
      keywords=["testing"],
      url="https://github.com/RonnyPfannschmidt/Sentaku",
      packages=["sentaku"],
      package_dir={'': 'src'},
      setup_requires=[
          'setuptools_scm',
      ],
      classifiers=[
          "Topic :: Utilities",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Intended Audience :: Developers",
          "Development Status :: 4 - Beta",
      ])
