import codecs
import io
import os
import sys
from base64 import b64encode
from functools import partial
from hashlib import md5
from pathlib import Path
from typing import Dict, List, Union, Generator, Optional, BinaryIO, TextIO

import requests

from .auth import make_canonical_resource_string, generate_auth_headers
from .errors import raise_for_ks3_status
from .schemas import s3_sub
from .utils import b64md5_bytes

__all__ = ['get_s3obj', 'Client']


def get_s3obj(resp: requests.Response):
    return s3_sub.parseString(resp.content, True) if resp.content else None


class Client:
    """KS3 的“客户端”

    它提供了对 金山云对象存储(KS3)的 HTTP API 的简单封装，轻微提升了操作方便性。

    API 详见 https://docs.ksyun.com/documents/2321
    """

    def __init__(
            self,
            access_key: str = None,
            secret_key: str = None,
            endpoint: str = 'kss.ksyun.com',
            session: requests.Session = None,
            use_https: bool = True
    ):
        """
        :param str access_key: `KS3` 颁发给您的 `AccessKey` （长度为20个字符的ASCII字符串）。用于标识客户的身份。
        :param str secret_key: `KS3` 颁发给您的 `SecretKey` （长度为40个字符的ASCII字符串）。作为私钥形式存放于客户服务器不在网络中传递。
        :param str endpoint: endpoint 对应 Region（区域）
        :param requests.Session session: :mod:`requests` 会话。如果不指定，将由 :mod:`requests` 自动管理。
        :param bool use_https: 是否使用 `HTTPS`。默认启用。
        """
        self._endpoint = endpoint.strip()
        self._access_key = (access_key or '').strip() or os.environ.get('KSYUN_ACCESS_KEY', '')
        self._secret_key = (secret_key or '').strip() or os.environ.get('KSYUN_SECRET_KEY', '')
        self._session = session
        self._use_https = bool(use_https)

    def send(
            self,
            method: str = 'get',
            bucket_name: str = None,
            object_key: str = None,
            sub_resources: Union[str, List[str]] = None,
            data: Union[
                bytes, bytearray, str, Generator, Path,
                BinaryIO, TextIO,
                io.BytesIO, io.StringIO,
                io.BufferedIOBase, io.TextIOBase
            ] = None,
            encoding=None,
            content_md5: str = None,
            headers: Dict[str, str] = None,
            params: Dict[str, str] = None,
            check_status: bool = True,
            session: requests.Session = None,
            **kwargs
    ) -> requests.Response:
        """向 KS3 发送一个 HTTP API 请求，并返回对应的 HTTP 响应对象

        :param str method: HTTP 方法

        :param str bucket_name: Bucket是存放Object的容器，所有的Object都必须存放在特定的Bucket中。

            每个用户最多可以创建30个Bucket，每个Bucket中可以存放无限多个Object。
            Bucket不能嵌套，每个Bucket中只能存放Object，不能再存放Bucket，Bucket下的Object是一个平级的结构。
            Bucket的名称全局唯一且命名规则与DNS命名规则相同：

                - 仅包含小写英文字母（`a-z`），数字，点（`.`），中线，即： `abcdefghijklmnopqrstuvwxyz0123456789.-`
                - 必须由字母或数字开头
                - 长度在3和63个字符之间
                - 不能是IP的形式，类似 `192.168.0.1`
                - 不能以 `kss` 开头


        :param str object_key: 在KS3中，用户操作的基本数据单元是Object。

            单个Object允许存储0~50TB的数据。
            Object 包含key和data。
            其中，key是Object的名字；data是Object 的数据。
            key为UTF-8编码，且编码后的长度不得超过1024个字节。

        :param Union[str,List[str]] sub_resources: 用户请求的子资源

            把URL参数中的::

                "acl","lifecycle","location","logging","notification","partNumber","policy","requestPayment","torrent","uploadId","uploads","versionId","versioning","versions","website","delete","thumbnail","cors","queryadp","adp","asyntask","querytask","domain","response-content-type","response-content-language","response-expires","response-cache-control","response-content-disposition","response-content-encoding"

            筛选出来，将这些查询字符串及其请求值(不做URL编码的请求值)按照字典序，从小到大排列，以&为分隔符排列，即可得到SubResource。

            使用时，可以直接传入计算好了的 `SubResource` 字符串，也可以传入子资源的字符串列表。

        :param Union[bytes,bytearray,str,Generator,Path,BinaryIO,TextIO] data: 上传内容

            如要上传的文件，要设置的 ACL 规则等。

            .. note:: 仅在 ``method`` 参数 为 ``"PUT"`` 和 ``"POST"`` 时有效。

        :param str encoding: 上传内容编码。默认使用操作系统设置。

            .. note:: 如果 `data` 是字符串，则该参数必须指定。

        :param str content_md5: 上传内容的 MD5 散列值对应的 BASE64 字符串。默认自动计算。

            .. note:: 默认值为 ``None`` ，将自动计算。但是，如果传入空字符串 (``""``) ，将以空字符串覆盖校验值。

        :param Dict[str,str] headers: 自定义 HTTP 头
        :param Dict[str,str] params: 自定义 URL 参数
        :param bool check_status: 是否在收到 HTTP 回复的第一行时检查状态码
        :param requests.Session session: 使用指定的会话发送 API 请求。默认自动分配。
        :param kwargs: 其它传给 :mod:`requests` 的参数

        :return: HTTP 响应对象

            .. warning:: 此时尚未接收 HTTP 响应的内容，可使用 :class:`requests.Response` 的一系列方法/属性获取正文，如:

                - :attr:`requests.Response.content`
                - :meth:`requests.Response.iter_content`
                - :meth:`requests.Response.iter_lines`
                - :meth:`requests.Response.json`

        :rtype: requests.Response
        """
        # http verb
        method = method.strip().lower()
        if method in ('post', 'put'):
            # 预处理 data 编码问题，顺便进行b64md5计算
            # text 转 bytes
            if isinstance(data, str):
                data = data.encode(encoding=encoding or sys.getdefaultencoding())
            # text io 转 bytes io
            elif isinstance(data, io.TextIOBase):
                if not encoding:
                    try:
                        encoding = getattr(data, 'encoding')
                    except AttributeError:
                        pass
                new_data = io.BytesIO()
                if content_md5 is None:
                    h = md5()
                else:
                    h = None
                for chunk in iter(partial(data.read, io.DEFAULT_BUFFER_SIZE), ''):
                    chunk = codecs.encode(chunk, encoding=encoding or sys.getdefaultencoding())
                    new_data.write(chunk)
                    if content_md5 is None:
                        h.update(chunk)
                if content_md5 is None:
                    content_md5 = b64encode(h.digest()).decode()
                new_data.seek(0)
                data = new_data
            if content_md5 is None:
                if isinstance(data, (bytes, bytearray)):
                    content_md5 = b64md5_bytes(data)
                elif isinstance(data, io.BufferedIOBase):
                    h = md5()
                    for chunk in iter(partial(data.read, io.DEFAULT_BUFFER_SIZE), b''):
                        h.update(chunk)
                    content_md5 = b64encode(h.digest()).decode()
                    data.seek(0)
                elif isinstance(data, Path):
                    with data.open('rb') as fp:
                        h = md5()
                        for chunk in iter(partial(fp.read, io.DEFAULT_BUFFER_SIZE), b''):
                            h.update(chunk)
                        content_md5 = b64encode(h.digest()).decode()
                else:
                    content_md5 = ''
        else:
            data = None
            content_md5 = ''
        # Signature
        canonical_resource = make_canonical_resource_string(bucket_name, object_key, sub_resources)
        auth_headers = generate_auth_headers(
            http_verb=method,
            access_key=self._access_key,
            secret_key=self._secret_key,
            canonical_resource=canonical_resource,
            content_md5=content_md5
        )
        # requests Session
        if not session:
            session = self._session
        if session:
            request = session.request
        else:
            request = requests.request
        # url
        url = '{}://{}{}'.format('https' if self._use_https else 'http', self._endpoint, canonical_resource)
        # headers
        headers = headers or {}
        headers.update(auth_headers)
        if content_md5:
            headers['Content-MD5'] = content_md5
        # send http request
        # 文件路径的，要特殊处理！
        if isinstance(data, Path):
            with data.open('rb') as fp:
                resp = request(method, url=url, params=params or {}, headers=headers, data=fp, **kwargs)
        else:
            resp = request(method, url=url, params=params or {}, headers=headers, data=data, **kwargs)
        # read response status code
        if check_status:
            raise_for_ks3_status(resp)
            resp.raise_for_status()
        # return
        setattr(resp, 's3obj', lambda: get_s3obj(resp))
        return resp

    @property
    def use_https(self) -> bool:
        """是否启用 HTTPS

        :rtype: bool
        """
        return self._use_https

    @property
    def endpoint(self) -> str:
        """Endpoint

        :rtype: str
        """
        return self._endpoint

    @property
    def session(self) -> Optional[requests.Session]:
        """用户指定的 :class:`requests.Session`

        :rtype: requests.Session
        """
        return self._session
