import typing as t
from hashlib import md5

import requests

from .auth import generate_auth_header
from .utils import http_format_date


class Connection:
    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 host: str = 'kss.ksyun.com',
                 session: requests.Session = None,
                 use_https: bool = True
                 ):
        self._host = host.strip()
        self._access_key = access_key.strip()
        self._secret_key = secret_key.strip()
        self._session = session
        self._use_https = bool(use_https)

    def call_api(self,
                 verb: str = 'GET',
                 bucket_name: str = '',
                 object_key: str = '',
                 sub_resources: t.Optional[t.Union[str, t.List[str], t.Tuple[str]]] = None,
                 data: t.Union[str, bytes, bytearray] = None,
                 params: t.Dict[str, str] = None,
                 session: requests.Session = None
                 ) -> requests.Response:
        # http verb
        verb = verb.strip().upper()
        if verb not in ('POST', 'PUT'):
            data = None
        # Signature
        content_md5 = ''
        if data:
            if isinstance(data, str):
                b_data = data.encode()
            elif isinstance(data, (bytes, bytearray)):
                b_data = data
            else:
                raise TypeError('Invalid type {!r} of parameter `data`'.format(type(data)))
            content_md5 = md5(b_data).hexdigest()
        http_date = http_format_date()
        auth_text = generate_auth_header(
            http_verb=verb,
            http_date=http_date,
            access_key=self._access_key,
            secret_key=self._secret_key,
            bucket_name=bucket_name,
            object_key=object_key,
            sub_resources=sub_resources,
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
            raise ValueError('Un-support http verb {!r}'.format(verb))
        # send http request
        resp = act(
            '{}://{}'.format(self.schema, self._host),
            params=params or {},
            headers={'Date': http_date, 'Authorization': auth_text},
            data=data
        )
        return resp

    @property
    def schema(self) -> str:
        return 'https' if self._use_https else 'http'

    @property
    def host(self) -> str:
        return self._host

    @property
    def session(self) -> t.Optional[requests.Session]:
        return self._session
