import io
import pathlib
from base64 import b64encode
from codecs import encode
from datetime import datetime
from email.utils import formatdate
from functools import partial
from hashlib import md5
from sys import getdefaultencoding
from time import mktime
from typing import Any, Tuple

__all__ = ['http_format_date', 'prepare_data', 'get_content_md5']


def http_format_date(dt: datetime = None) -> str:
    """生成 HTTP 头的日期时间字符串

    :param datetime dt: 要转换的时间日期

        :default: ``None`` - 当前时间

    :return: 转换后的满足 HTTP 格式要求的时间日期字符串
    :rtype: str
    """
    if not dt:
        dt = datetime.now()
    stamp = mktime(dt.timetuple())
    return formatdate(timeval=stamp, localtime=False, usegmt=True)


def prepare_data(data, checking: bool = True, encoding: str = None) -> Tuple[Any, str]:  # noqa: C901
    """为 API 准备要进行 POST 或 PUT 的数据，包括 KS3 API 的通用请求部分所需的 `Content-MD5`。

    准备数据是为了让 :mod:`requests` 直接使用 `data` 进行 `POST` / `PUT`

    :param data: 要准备的数据

        支持的数据类型有：
        :class:`bytes`,
        :class:`bytearray`,
        :class:`str`,
        :class:`pathlib.Path`,
        :class:`io.BufferedIOBase`,
        :class:`io.TextIOBase`

        如果此参数是不支持的数据类型，该函数返回是 ``(data, "")`` ，即原样返回 `data` ，以及空字符串组成的元组

    :param bool checking: 是否计算MD5. 默认 ``True``
    :param str encoding: 如果数据是字符串，使用这个参数指定字符编码。默认自动获取。

    :rtype: Tuple[Any, str]
    :return: 返回元组形如 ``(data, md5)`` 。分别是转换后的数据，以及该数据的MD5散列值的BASE64编码结果字符串。

    .. note::
        `Content-MD5` 的算法为先对数据做MD5摘要，再将MD5摘要做Base64编码。
        中间不需要做HEX编码，由于部分语言或工具包的MD5是默认做HEX编码的，所以当MD5算出来的结果为HEX编码的，首先需要对算出来的结果做HEX解码，然后再做Base64编码。

    .. seealso:: https://docs.ksyun.com/documents/2321
    """
    hash_val = ''
    default_encoding = getdefaultencoding()

    # 字节数据 - 直接计算
    if isinstance(data, (bytes, bytearray)):
        result_data = data
        if checking:
            hash_val = b64encode(md5(data).digest()).decode()  # nosec

    # 文件路径
    elif isinstance(data, pathlib.Path):
        result_data = data  # noqa: T484
        if checking:
            with data.open('rb') as fp:
                h = md5()  # nosec
                for chunk in iter(partial(fp.read, io.DEFAULT_BUFFER_SIZE), b''):
                    h.update(chunk)
                hash_val = b64encode(h.digest()).decode()

    # 字节流
    elif isinstance(data, io.BufferedIOBase):
        result_data = data  # noqa: T484
        if checking:
            h = md5()
            p = data.tell()
            try:
                for chunk in iter(partial(data.read, io.DEFAULT_BUFFER_SIZE), b''):
                    h.update(chunk)
            finally:
                data.seek(p)
            hash_val = b64encode(h.digest()).decode()

    # 字符串
    elif isinstance(data, str):
        result_data = encode(data, encoding=encoding or default_encoding)
        if checking:
            hash_val = b64encode(md5(result_data).digest()).decode()  # nosec

    # 文本流
    elif isinstance(data, io.TextIOBase):
        if not encoding:
            try:
                encoding = getattr(data, 'encoding')
            except AttributeError:
                pass
        if checking:
            h = md5()  # nosec
        stream = io.BytesIO()
        for s in iter(partial(data.read, io.DEFAULT_BUFFER_SIZE), ''):
            chunk = encode(s, encoding=encoding or default_encoding)
            stream.write(chunk)
            if checking:
                h.update(chunk)
        stream.seek(0)
        result_data = stream  # noqa: T484
        if checking:
            hash_val = b64encode(h.digest()).decode()

    else:
        result_data = data

    return result_data, hash_val


def get_content_md5(data, encoding: str = None) -> str:
    """获取 KS3 API 的通用请求部分所需的 `Content-MD5`

    :param data: 要计算数据

        .. seealso:: 与 :func:`prepare_data` 的同名参数一致。

    :param str encoding: 字符编码

        .. seealso:: 与 :func:`prepare_data` 的同名参数一致。

    :rtype: str
    :return: 该数据的MD5散列值的BASE64编码结果字符串

    .. seealso:: https://docs.ksyun.com/documents/2321
    """
    _, result = prepare_data(data, True, encoding)
    return result
