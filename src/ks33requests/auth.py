import hmac
from base64 import encodebytes
from hashlib import sha1
from typing import Dict, List, Optional, Union
from urllib.parse import quote_plus

from .constants import HTTP_VERBS, SUB_RESOURCES
from .utils import http_format_date


def make_canonical_resource_string(
        bucket_name: str = '',
        object_key: str = '',
        sub_resources: Optional[Union[str, List[str]]] = None,
) -> str:
    result = '/'
    if sub_resources:
        if isinstance(sub_resources, str):
            sub_resources = [sub_resources]
        if isinstance(sub_resources, (tuple, list)):
            if any(s not in SUB_RESOURCES for s in sub_resources):
                raise ValueError('Invalid value in sub-resources list')
            sub_res_text = '&'.join(sorted(sub_resources))
        else:
            raise TypeError('Wrong type {!r} of argument `sub_resources`'.format(type(sub_resources)))
    else:
        sub_res_text = ''
    if bucket_name:
        result += bucket_name + '/'
    if object_key:
        result += quote_plus(object_key)
    if sub_res_text:
        result += '?' + sub_res_text
    return result


def generate_auth_headers(
        http_verb: str,
        access_key: str,
        secret_key: str,
        canonical_resource: str,
        content_md5: str = '',
) -> Dict[str, str]:
    # 参数验证
    http_verb = http_verb.strip().upper()
    if http_verb not in HTTP_VERBS:
        raise ValueError('Un-support http verb {!r}'.format(http_verb))
    # Date
    date_text = http_format_date()
    # Canonical KssHeaders
    canonical_kss_headers = ''
    # String to sign
    string_to_sign = http_verb + '\n'  # HTTP-Verb
    string_to_sign += content_md5 + '\n'  # Content-MD5
    string_to_sign += '\n'  # Content-Type
    string_to_sign += date_text + '\n'  # Date
    string_to_sign += canonical_kss_headers + canonical_resource  # Canonical-KssHeaders + Canonical-Resource
    # Signature
    hash_obj = hmac.new(secret_key.encode(), string_to_sign.encode(), sha1)
    sign = encodebytes(hash_obj.digest()).strip()
    # Authorization
    auth_text = 'KSS {}:{}'.format(access_key, sign.decode())
    # 最终返回
    return {'Date': date_text, 'Authorization': auth_text}
