import io
import typing as t
from hashlib import md5

import requests

from .auth import make_canonical_resource_string, generate_auth_headers
from .errors import raise_for_errors
from .schemas import s3_sub


class Client:
    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 endpoint: str = 'kss.ksyun.com',
                 session: requests.Session = None,
                 use_https: bool = True
                 ):
        self._endpoint = endpoint.strip()
        self._access_key = access_key.strip()
        self._secret_key = secret_key.strip()
        self._session = session
        self._use_https = bool(use_https)

    def call_api(self,
                 verb: str = 'GET',
                 bucket_name: str = None,
                 object_key: str = None,
                 sub_resources: t.Union[str, t.List[str]] = None,
                 data: t.Union[str, bytes, bytearray, t.Generator, t.BinaryIO, t.TextIO] = None,
                 headers: t.Dict[str, str] = None,
                 params: t.Dict[str, str] = None,
                 session: requests.Session = None
                 ) -> requests.Response:
        # http verb
        verb = verb.strip().upper()
        if verb not in ('POST', 'PUT'):
            data = None
        # Content MD5
        content_md5 = ''
        if data:
            if isinstance(data, str):
                content_md5 = md5(data.encode()).hexdigest()
            elif isinstance(data, (bytes, bytearray)):
                content_md5 = md5(data).hexdigest()
            elif isinstance(data, t.BinaryIO):
                h = md5()
                for chunk in data.read(io.DEFAULT_BUFFER_SIZE):
                    h.update(chunk)
                content_md5 = h.hexdegist()
                data.seek(0)
            elif isinstance(data, t.TextIO):
                h = md5()
                for chunk in data.read(io.DEFAULT_BUFFER_SIZE):
                    h.update(chunk.encode(encoding=data.encoding))
                content_md5 = h.hexdegist()
                data.seek(0)
        # Signature
        canonical_resource = make_canonical_resource_string(bucket_name, object_key, sub_resources)
        auth_headers = generate_auth_headers(
            http_verb=verb,
            access_key=self._access_key,
            secret_key=self._secret_key,
            canonical_resource=canonical_resource,
            content_md5=content_md5
        )
        # requests Session
        if not session:
            session = self._session
        if not session:
            session = requests
        if verb == 'GET':
            act = session.get
        elif verb == 'PUT':
            act = session.put
        elif verb == 'POST':
            act = session.post
        elif verb == 'DELETE':
            act = session.delete
        elif verb == 'HEAD':
            act = session.head
        elif verb == 'OPTIONS':
            act = session.options
        else:
            raise ValueError('Un-support HTTP verb {!r}'.format(verb))
        # url
        url = '{}://{}{}'.format(self.schema, self._endpoint, canonical_resource)
        # headers
        headers = headers or {}
        headers.update(auth_headers)
        if content_md5:
            headers['Content-MD5'] = content_md5
        # send http request
        resp = act(
            url=url,
            params=params or {},
            headers=headers,
            data=data
        )
        return resp

    def call_api_s3res(self, *args, **kwargs):
        resp = self.call_api(*args, **kwargs)
        raise_for_errors(resp)
        if resp.content:
            return s3_sub.parseString(resp.content)
        return None

    @property
    def schema(self) -> str:
        return 'https' if self._use_https else 'http'

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def session(self) -> t.Optional[requests.Session]:
        return self._session
