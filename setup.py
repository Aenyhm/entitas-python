#!/usr/bin/env python

import os

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

required = []
packages = ['entitas']

# About dict to store version and package info
about = dict()
version_path = os.path.join(here, 'entitas', '__version__.py')
with open(version_path, 'r', encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name='Entitas',
    version=about['__version__'],
    description='Entitas ECS implementation in Python.',
    long_description=long_description,
    author='Fabien Nouaillat',
    author_email='aenyhm@gmail.com',
    url='https://github.com/aenyhm/entitas-python',
    packages=packages,
    install_requires=required,
    license='MIT',
)
