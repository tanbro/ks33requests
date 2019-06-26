# CHANGELOG

## 0.1.2.2

- Date: 2019-06-26

- Change:
  - 构造 `Client` 时，如果不指定密钥对，将从环境变量 `KSYUN_ACCESS_KEY` 与 `KSYUN_SECRET_KEY` 获得
  - `Client.send()` 增加 `encoding` 参数，用于对文本数据上传的支持
- New:
  - 几个测试用例
  - [Sphinx Docs](https://ks33requests.readthedocs.io)
  - [Circle CI](https://circleci.com/gh/tanbro/ks33requests)
  - [Code coverage](https://codecov.io/gh/tanbro/ks33requests)
  - `get_content_md5()`: 获取 KS3 样式的 MD5 BASE64 校验值
- Fix:
  - 几个有关文本数据上传 bug

## 0.1

- Date: 2019-06-12

这实际上还是一个 Alpha 版本，但是为了在项目中顺利使用，且给它一个稳定的版本编号。
