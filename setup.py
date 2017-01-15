#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

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
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ephe = epherousa.__init__:main',
            'epherousa = epherousa.__init__:main',
        ]
    },
    install_requires=[
        'colorama>=0.3.7',
        'backports.csv>=1.0.2',
        'beautifulsoup4>=4.5.1',
        'future>=0.16.0',
        'Logbook>=1.0.0',
        'lxml>=3.6.4',
        'requests>=2.11.1'
    ]
)
