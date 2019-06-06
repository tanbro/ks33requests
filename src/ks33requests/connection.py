import requests

from .auth import get_auth_header

from .utils import get_format_date, s3_obj


class Connection:
    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 host: str = 'kss.ksyun.com',
                 use_https: bool = True
                 ):
        self._host = host
        self._access_key = access_key
        self._secret_key = secret_key
        self._use_https = use_https

    @property
    def schema(self):
        return 'https' if self._use_https else 'http'

    def list_buckets(self):
        http_date = get_format_date()
        auth_text = get_auth_header('GET', http_date, self._access_key, self._secret_key)
        r = requests.get(
            '{}://{}'.format(self.schema, self._host),
            headers={
                'Date': http_date,
                'Authorization': auth_text,
            }
        )
        r.raise_for_status()
        return s3_obj(r.content)
