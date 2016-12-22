#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup

version = {}
with open('epherousa/version.py') as f:
    exec(f.read(), version)

setup(
    name='epherousa',
    version=version['__version__'],
    description='Vulnerability searcher',
    # author='',
    # author_email='',
    # url='',
    packages=[
        'epherousa',
        'epherousa.models',
        'epherousa.modules',
        'epherousa.searchers',
    ],
    scripts=[
        'bin/ephe',
        'bin/epherousa'
    ]
)
