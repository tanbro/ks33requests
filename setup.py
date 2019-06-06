#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""setuptools script of this package

see:

* https://packaging.python.org/
* https://setuptools.readthedocs.io/
"""

from setuptools import find_packages as find, setup


setup(
    name='ks33requests',
    url='https://github.com/tanbro/ks33requests',

    packages=find('src'),
    package_dir={'': 'src'},

    description="A simple client SDK in Python3 language for ksyun's KS3 object storage service",

    install_requires=[
        'requests',
        'lxml',
    ],

    use_scm_version={
        # guess-next-dev:	automatically guesses the next development version (default)
        # post-release:	generates post release versions (adds postN)
        'version_scheme': 'guess-next-dev',
        'write_to': 'src/ks33requests/_scm_version.py',
    },
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],

    author='liu xue yan',
    author_email='liu_xue_yan@foxmail.com',
    long_description=open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
)
