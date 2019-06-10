import typing as t
from hashlib import md5
from urllib.parse import quote_plus

import requests

from .auth import make_canonical_resource_string, generate_auth_headers
from .constants import SUB_RESOURCES


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
                 bucket_name: str = '',
                 object_key: str = '',
                 sub_resources: t.Optional[t.Union[str, t.List[str]]] = None,
                 data: t.Union[str, bytes, bytearray] = None,
                 headers: t.Dict[str, str] = None,
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
        canonical_resource = '/'
        if sub_resources:
            if isinstance(sub_resources, str):
                sub_resources = [sub_resources]
            if isinstance(sub_resources, (tuple, list)):
                if any(s not in SUB_RESOURCES for s in sub_resources):
                    raise ValueError('Invalid value in sub-resources list')
                sub_res_text = '&'.join(sorted(sub_resources))
            else:
                raise TypeError('Invalid type {!r} of parameter `sub_resources`'.format(type(sub_resources)))
        else:
            sub_res_text = ''
        if bucket_name:
            canonical_resource += bucket_name + '/'
        if object_key:
            canonical_resource += quote_plus(object_key)
        if sub_res_text:
            canonical_resource += '?' + sub_res_text
        # url
        url = '{}://{}{}'.format(self.schema, self._endpoint, canonical_resource)
        # headers
        headers = headers or {}
        headers.update(auth_headers)
        # send http request
        resp = act(
            url=url,
            params=params or {},
            headers=headers,
            data=data
        )
        return resp

    @property
    def schema(self) -> str:
        return 'https' if self._use_https else 'http'

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def session(self) -> t.Optional[requests.Session]:
        return self._session
