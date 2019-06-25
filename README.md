# ks33requests

[![PyPI](https://img.shields.io/pypi/v/ks33requests.svg)](https://pypi.org/project/ks33requests/)
[![Documentation Status](https://readthedocs.org/projects/ks33requests/badge/?version=stable)](https://ks33requests.readthedocs.io/zh_CN/stable/?badge=stable)
[![PyPI - License](https://img.shields.io/pypi/l/ks33requests.svg)](https://pypi.org/project/ks33requests/)
[![codecov](https://codecov.io/gh/tanbro/ks33requests/branch/master/graph/badge.svg)](https://codecov.io/gh/tanbro/ks33requests)
[![PyPI - Format](https://img.shields.io/pypi/format/ks33requests.svg)](https://pypi.org/project/ks33requests/)
[![PyPI - Status](https://img.shields.io/pypi/status/ks33requests.svg)](https://pypi.org/project/ks33requests/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ks33requests.svg)](https://pypi.org/project/ks33requests/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/ks33requests.svg)](https://pypi.org/project/ks33requests/)

## 概述

一个很简单的、适用于 [金山云][] 对象存储([KS3][])的 [Python][]3 客户端。

[金山云][] 官方提供了 [KS3][] 的 [Python][] SDK，但在我启动这个项目(2019-06-10)时，仅提供 [Python][]2 SDK。

考虑到 [Python][]2 已经接近其生命周期的终点，我制作了这个简单的 [Python]3 [KS3][] 客户端用于相关项目。

## 安装

- [pip][] 安装

  ```bash
  pip install ks33requests
  ```

- 源代码安装

  ```bash
  python setuptools.py install
  ```

- [Pipenv][] 安装

  ```bash
  pipenv install ks33requests
  ```

## 如何使用

参见 [notebooks](notebooks) 中的笔记

[Python]: https://python.org/
[virtual environment]: https://packaging.python.org/glossary/#term-virtual-environment "An isolated Python environment that allows packages to be installed for use by a particular application, rather than being installed system wide."
[pip]: https://packaging.python.org/key_projects/#pip "A tool for installing Python packages."
[Pipenv]: https://packaging.python.org/key_projects/#pipenv "Pipenv is a project that aims to bring the best of all packaging worlds to the Python world."
[venv]: https://packaging.python.org/key_projects/#venv "A package in the Python Standard Library (starting with Python 3.3) for creating Virtual Environments."
[conda]: https://packaging.python.org/key_projects/#conda "conda is the package management tool for Anaconda Python installations."
[S3]: https://aws.amazon.com/s3/
[金山云]: https://www.ksyun.com/
[KS3]: https://www.ksyun.com/post/product/KS3 "金山对象存储（Kingsoft Standard Storage Service，简称KS3）"
[generateDS]: https://pypi.org/project/generateDS/
