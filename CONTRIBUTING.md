# CONTRIBUTING

> ℹ **注意:**
>
> 这个项目需要 [Python][] `3.5` 及以上版本。

## 复刻项目代码

复刻项目代码到工作目录，然后切换到项目的目录：

```bash
cd path/to/your/workspace/directory/
git clone https://github.com/tanbro/ks33requests.git
cd ks33requests
```

## 准备开发环境

强烈建议在 [virtual environment][] 中进行开发工作。

- 如果使用标准库:

  使用标准库的 [venv][] 与 [pip][] 直接新建名为`venv`的虚拟环境目录，将本项目以“开发模式”安装到这个环境，并安装开发工作所要使用的包：

  ```bash
  path/of/your/python -m venv venv
  venv/bin/python setup.py develop
  venv/bin/python -m pip install -r requires/dev.txt
  ```

- 如果使用 [Pipenv][]:

  使用 [Pipenv][] 命令直接安装:

  ```bash
  pipenv install --dev
  ```

- 如果使用 [conda][]

  使用 [conda][] 从配置文件新建一个专用于这个项目的、名为`ks33requests-dev`的环境，然后激活它，将本项目以“开发模式”安装到这个环境：

  ```bash
  conda env create -f environment.yml
  conda activate ks33requests-dev
  python setup.py develop
  ```

### XML Schema

[金山云][] [KS3][] 的 WebAPI 数据结构有许多与[S3]兼容。
所以，这个项目直接使用考虑来自 <http://s3.amazonaws.com/doc/2006-03-01/AmazonS3.xsd> 的 Schema。

我们使用 [generateDS][] 工具，从`xsd`文件生成 [Python][] 类型定义：

```bash
mkdir -p schemas
wget http://s3.amazonaws.com/doc/2006-03-01/AmazonS3.xsd -P schemas
generateDS.py -f -o s3_api.py -s s3_sub.py --super=s3_api  schemas/AmazonS3.xsd
```

生成的源代码文件复制到名称空间 `ks33requests.schemas` 中，小幅修改 `s3_sub.py` 即可使用。

### 运行测试用例

```bash
python setup.py test
```

测试用例很少，陆续补充中...

### Docs

如果模块有增减，需要删除原来的 [Sphinx-Docs][] API 自动文档并重新生成:

```bash
rm -rf docs/ks3requests.rst docs/api
sphinx-apidoc -e -f -o docs/api src/ks33requests src/ks33requests/schemas/s3_*.py
```

[Python]: https://python.org/
[virtual environment]: https://packaging.python.org/glossary/#term-virtual-environment "An isolated Python environment that allows packages to be installed for use by a particular application, rather than being installed system wide."
[pip]: https://packaging.python.org/key_projects/#pip "A tool for installing Python packages."
[Pipenv]: https://packaging.python.org/key_projects/#pipenv "Pipenv is a project that aims to bring the best of all packaging worlds to the Python world."
[venv]: https://packaging.python.org/key_projects/#venv "A package in the Python Standard Library (starting with Python 3.3) for creating Virtual Environments."
[conda]: https://packaging.python.org/key_projects/#conda "conda is the package management tool for Anaconda Python installations."
[S3]: https://aws.amazon.com/s3/
[Sphinx-Docs]: https://www.sphinx-doc.org "Sphinx is a tool that makes it easy to create intelligent and beautiful documentation"
[金山云]: https://www.ksyun.com/
[KS3]: https://www.ksyun.com/post/product/KS3 "金山对象存储（Kingsoft Standard Storage Service，简称KS3）"
[generateDS]: https://pypi.org/project/generateDS/
