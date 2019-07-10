# CONTRIBUTING

> ℹ **注意:**
>
> 这个项目需要 [Python][] `3.5` 及以上版本。

## 复刻项目

复刻项目源码到工作目录，然后切换到项目的目录：

```bash
cd path/to/your/workspace/directory/
git clone https://github.com/tanbro/ks33requests.git
cd ks33requests
```

## 开发环境

强烈建议在 [virtual environment][] 中进行开发工作。建议的方法有:

- 标准库:

  具体参考 <https://packaging.python.org/tutorials/installing-packages/> ，此处以`Posix`+`bash`的常见情况为例

  1. 在子目录 `<venv>` (目录名用一个变量代表，应根据实际情况选择则目录) 中创建虚拟环境

     ```bash
     path/of/your/python -m venv <venv>
     ```

  1. 激活虚拟环境

     ```bash
     source <venv>/bin/activate
     ```

  1. 将本项目以 **可编辑模式** 安装到这个环境，并安装开发工作所要使用的包

     ```base
     pip install -e ./ -r requirements/dev.txt
     ```

- [Pipenv][]:

  1. 按照 **开发模式** 为该项目安装一个新的虚拟环境

     ```bash
     pipenv install --dev
     ```

  1. 激活虚拟环境

     ```bash
     pipenv shell
     ```

- [conda][]:

  1. 从配置文件 `environment.yml` 为该项目安装一个新的虚拟环境，名为`ks33requests-dev`。本项目将以 **可编辑模式** 被安装到这个环境中。

     ```bash
     conda env create -f environment.yml
     ```

  1. 激活虚拟环境

     ```bash
     conda activate ks33requests-dev
     ```

## 编码条例

1. 代码风格遵照 [PEP 8](https://www.python.org/dev/peps/pep-0008/)
1. 版本命名遵照 [PEP 440](https://www.python.org/dev/peps/pep-0440/)
1. 使用 [git](https://git-scm.org/) 进行版本控制：
   1. 按照 [git-flow](https://nvie.com/posts/a-successful-git-branching-model/) 流程进行工作
   1. 使用 [setuptools](https://pypi.org/project/setuptools/) 的扩展 [setuptools_scm](https://pypi.org/project/setuptools-scm/) 与 [setuptools_scm_git_archive](https://pypi.org/project/setuptools-scm-git-archive/) 配合上述工作流程进行打包
1. 对外的 API 须提供 [Sphinx-Docs][] 样式的 doc comments
1. 对外 API 须提供 type hints
1. 做静态检查，不提交带有错误或许多警告的代码
1. 提供有足够覆盖面的测试用例

## XML Schema

[金山云][] [KS3][] 的 WebAPI 数据结构有许多与 [S3][] 兼容。
所以，这个项目直接使用来自 <http://s3.amazonaws.com/doc/2006-03-01/AmazonS3.xsd> 的 Schema 转换部分数据的结构。

我们使用 [generateDS][] 工具，从`xsd`文件生成 [Python][] 类型定义：

```bash
mkdir -p schemas
wget http://s3.amazonaws.com/doc/2006-03-01/AmazonS3.xsd -P schemas
generateDS.py -f -o s3_api.py -s s3_sub.py --super=s3_api  schemas/AmazonS3.xsd
```

生成的源代码文件复制到名称空间 `ks33requests.schemas` 中，小幅修改 `s3_sub.py` 的源码即可使用。

## 运行测试

```bash
python -m unittest
```

如果需要在运行测试时进行代码覆盖性检查，可运行:

```bash
python -m coverage run -m unittest
```

## 静态检查

```bash
python -m flake8
```

## 文档生成

下面的命令将构建 `HTML` 文档，输出到目录 `docs/_build`:

```bash
python -m sphinx docs/ docs/_build
```

> ℹ **说明**:
>
> 如果模块有增减，需要删除原来的 [Sphinx-Docs][] 自动API文档并重新生成:
>
> ```bash
> rm -rf docs/ks3requests.rst docs/api
> mkdir -p docs/api
> sphinx-apidoc -e -f -o docs/api src/ks33requests src/ks33requests/schemas/s3_*.py
> ```

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
