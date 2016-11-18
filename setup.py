#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup

version = {}
with open('untitled/version.py') as f:
    exec(f.read(), version)

setup(
    name='untitled',
    version=version['__version__'],
    description='Vulnerability searcher',
    # author='',
    # author_email='',
    # url='',
    packages=[
        'untitled',
        'untitled.searchers',
    ]
)
