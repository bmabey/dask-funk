#!/usr/bin/env python

from os.path import exists
from setuptools import setup

import versioneer

setup(
    name='dask-funk',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=('daskfunk',),
    setup_requires=['pytest-runner'],
    install_requires=('dask>=0.8.0', 'toolz>=0.8.0'),
    tests_require=('pytest>=3.0.3', 'pytest-pythonpath', 'pytest-flake8',
                   'pytest-isort', 'flake8-print', 'flake8-todo', 'pep8-naming'),
    description="Composable keyword function graphs",
    long_description=(open('README.rst').read() if exists('README.rst')
                      else ''),
    author="Ben Mabey",
    author_email="ben@benmabey.com",
    url="http://github.com/Savvysherpa/dask-funk",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
    ],
)
