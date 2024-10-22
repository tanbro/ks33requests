import requests
from lxml import etree  # nosec

__all__ = ['Ks3Error', 'raise_for_ks3_status']

SUPPORTED_ERROR_HTTP_STATUES = [400, 403, 404, 405, 408, 409, 413, 416, 418, 500, 501]


class Ks3Error(Exception):
    """KS3 返回的 HTTP 响应带有 HTTP 错误状态码
    """

    def __init__(self, **kwargs):
        self._status = kwargs.get('status')
        self._code = kwargs.get('code')
        self._message = kwargs.get('message')
        self._resource = kwargs.get('resource')
        self._request_id = kwargs.get('request_id')
        super().__init__()

    def __repr__(self):
        return '{}(status={!r}, code={!r}, message={!r}, resource={!r}, request_id={!r})'.format(
            self.__class__.__qualname__, self._status, self._code, self._message, self._resource, self._request_id
        )

    def __str__(self):
        return self._message

    @property
    def status(self):
        """HTTP 状态码

        :rtype: int
        """
        return self._status

    @property
    def code(self):
        """错误编码

        :rtype: int
        """
        return self._code

    @property
    def message(self):
        """错误信息

        :rtype: str
        """
        return self._message

    @property
    def resource(self):
        """引起错误的资源

        :rtype: str
        """
        return self._resource

    @property
    def request_id(self):
        """引起错误的资源 ID

        :rtype: str
        """
        return self._request_id


def raise_for_ks3_status(resp: requests.Response):
    """检查 KS3 返回的 HTTP 响应，如果状态码可以识别为错误信息，则抛出异常

    :param requests.Response resp: 要检查的 HTTP 响应对象
    :raises Ks3Error: 如果检查到了 KS3 定义的 HTTP 错误状态码

    .. warning::
        这个函数仅检查可几个按照 KS3 文档定义的 HTTP 错误状态码，并 **不检查其它错误** 状态编码 。
        可调用 :meth:`requests.Response.raise_for_status` 检查其它 HTTP 错误状态码。
    """
    status = resp.status_code
    if status in SUPPORTED_ERROR_HTTP_STATUES:
        if resp.content:
            root = etree.fromstring(resp.content)  # nosec
            if root.tag != 'Error':
                raise ValueError('Expect tag of root xml node is "Error", actual is %r', root.tag)
            kv_args = {child.tag.strip().lower(): child.text.strip() for child in root}
            kv_args['status'] = status
            raise Ks3Error(**kv_args)
