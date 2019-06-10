import typing as t
from datetime import datetime
from email.utils import formatdate
from time import mktime

from .schemas import amazon_s3


def http_format_date(dt: datetime = None) -> str:
    if not dt:
        dt = datetime.now()
    stamp = mktime(dt.timetuple())
    return formatdate(timeval=stamp, localtime=False, usegmt=True)


def s3_obj(content: t.Union[bytes, str]):
    if isinstance(content, str):
        content = content.encode()
    if isinstance(content, bytes):
        return amazon_s3.parseString(content)
    raise TypeError('Invalid data type {!r} of argument `content`'.format(type(content)))
