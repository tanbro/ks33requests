import typing as T
from datetime import datetime
from email.utils import formatdate
from time import mktime

from .schemas import amazon_s3


def get_format_date():
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return formatdate(timeval=stamp, localtime=False, usegmt=True)


def s3_obj(content: T.Union[bytes, str]):
    if isinstance(content, str):
        content = content.encode()
    if isinstance(content, bytes):
        return amazon_s3.parseString(content)
    raise TypeError('Invalid data type {!r} of argument `content`'.format(type(content)))
