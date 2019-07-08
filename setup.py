#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

setup(
    name='ks33requests',
    description='适用于金山云对象存储(KS3)的简单 Python3 客户端',
    author="Liu Xue Yan",
    author_email="liu_xue_yan@foxmail.com",
    long_description=(2 * os.linesep).join(
        open(file, encoding='utf-8').read().strip()
        for file in ('README.md', 'CHANGELOG.md', 'CONTRIBUTING.md', 'AUTHORS.md')
    ),
    long_description_content_type='text/markdown',
    license='Apache Software License',
    url='https://github.com/tanbro/ks33requests',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5',
    setup_requires=[
        'setuptools_scm',
        'setuptools_scm_git_archive',
    ],
    use_scm_version={
        # guess-next-dev:	automatically guesses the next development version (default)
        # post-release:	generates post release versions (adds postN)
        'version_scheme': 'guess-next-dev',
        'write_to': 'src/ks33requests/_scm_version.py',
    },
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'requests<3.0,>=2.0',
        'lxml<5.0,>=4.0',
    ],
    tests_require=[
        'python-dotenv',
    ],
)
