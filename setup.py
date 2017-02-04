#!/usr/bin/env python

import re

from setuptools import setup


packages = ['entitas']
requires = ['pytest']

with open('entitas/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open('README.rst') as f:
    readme = f.read()

setup(
    name='Entitas',
    version=version,
    description='Entitas ECS implementation in Python',
    long_description=readme,
    author='Fabien Nouaillat',
    author_email='aenyhm@gmail.com',
    url='https://github.com/aenyhm/entitas-python',
    packages=packages,
    include_package_data=True,
    install_requires=requires,
    license='MIT'
)
