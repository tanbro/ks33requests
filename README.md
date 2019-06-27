# ks33requests

---

[![PyPI](https://img.shields.io/pypi/v/ks33requests.svg)](https://pypi.org/project/ks33requests/)
[![PyPI - License](https://img.shields.io/pypi/l/ks33requests.svg)](https://pypi.org/project/ks33requests/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ks33requests.svg)](https://pypi.org/project/ks33requests/)
[![PyPI - Status](https://img.shields.io/pypi/status/ks33requests.svg)](https://pypi.org/project/ks33requests/)
[![CircleCI](https://circleci.com/gh/tanbro/ks33requests.svg?style=svg)](https://circleci.com/gh/tanbro/ks33requests)
[![codecov](https://codecov.io/gh/tanbro/ks33requests/branch/master/graph/badge.svg)](https://codecov.io/gh/tanbro/ks33requests)
[![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/tanbro/ks33requests.svg)](https://libraries.io/github/tanbro/ks33requests)
[![Documentation Status](https://readthedocs.org/projects/ks33requests/badge/?version=stable)](https://ks33requests.readthedocs.io/zh_CN/stable/?badge=stable)

---

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

## 用法

参见: [notebooks](notebooks) 目录中的笔记

## 文档

参见: <https://ks33requests.readthedocs.io>

以及代码仓库中的:

- [CHANGELOG](CHANGELOG)
- [CONTRIBUTING](CONTRIBUTING)
- [AUTHORS](AUTHORS)

[Python]: https://python.org/
[金山云]: https://www.ksyun.com/
[KS3]: https://www.ksyun.com/post/product/KS3 "金山对象存储（Kingsoft Standard Storage Service，简称KS3）"
[pip]: https://packaging.python.org/key_projects/#pip "A tool for installing Python packages."
[Pipenv]: https://packaging.python.org/key_projects/#pipenv "Pipenv is a project that aims to bring the best of all packaging worlds to the Python world."
