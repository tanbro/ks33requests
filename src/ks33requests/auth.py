import hmac
import typing as T
from base64 import encodebytes
from hashlib import sha1
from urllib.parse import quote_plus

from .constants import HTTP_VERBS, SUB_RESOURCES


def get_auth_header(
        http_verb: str,
        http_date: str,
        access_key: str,
        secret_key: str,
        bucket_name: str = '',
        object_key: str = '',
        sub_resources: T.Optional[T.Union[str, T.List[str], T.Tuple[str]]] = None,
) -> str:
    # 参数验证
    if http_verb not in HTTP_VERBS:
        raise ValueError('Un-support http verb %r'.format(http_verb))
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
    #
    # Canonical KssHeaders
    canonical_kss_headers = ''
    #
    # Canonical Resource
    canonical_resource = '/'
    if bucket_name:
        canonical_resource += bucket_name + '/'
    if object_key:
        canonical_resource += quote_plus(object_key)
    if sub_res_text:
        canonical_resource += '?' + sub_res_text
    # String to sign
    string_to_sign = http_verb + '\n'  # HTTP-Verb
    string_to_sign += '\n'  # Content-MD5
    string_to_sign += '\n'  # Content-Type
    string_to_sign += http_date + '\n'  # Date
    string_to_sign += canonical_kss_headers + canonical_resource  # Canonical-KssHeaders + Canonical-Resource
    #
    # Signature
    hash_obj = hmac.new(secret_key.encode(), string_to_sign.encode(), sha1)
    sign = encodebytes(hash_obj.digest()).strip()
    #
    # 最终返回
    return 'KSS {}:{}'.format(access_key, sign.decode())
