#!/usr/bin/env python

from os.path import exists
from setuptools import setup
import daskfunk._info as di

setup(
    name='dask-funk',
    version=di.__version__,
    packages=('daskfunk',),
    install_requires=('dask>=0.8.0', 'toolz'),
    tests_require=('pytest', 'pytest-benchmark', 'pytest-flake8',
                   'pytest-isort', 'flake8-print', 'flake8-todo', 'pep8-naming'),
    description="Composable keyword function graphs",
    long_description=(open('README.rst').read() if exists('README.rst')
                      else ''),
    author="Ben Mabey",
    author_email="ben@benmabey.com",
    url="http://github.com/TBD/dask-funk",
    license="MIT",
    classifiers=(
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
    ),
)
