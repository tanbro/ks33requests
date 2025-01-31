import io
import os
import pathlib
import unittest

from dotenv import load_dotenv

from ks33requests import Client, Ks3Error

load_dotenv()

KSYUN_ACCESS_KEY = os.environ['KSYUN_ACCESS_KEY']
KSYUN_SECRET_KEY = os.environ['KSYUN_SECRET_KEY']
KS3_ENDPOINT = os.environ['KS3_ENDPOINT']
KS3_BUCKET = os.environ['KS3_BUCKET']


class SmallTextFileUploadTestCase(unittest.TestCase):
    KEY = 'README.md'
    ENCODING = 'utf-8'

    def setUp(self):
        self.client = Client(endpoint=KS3_ENDPOINT)

    def upload(self, *args, **kwargs):
        return self.client.send(method='put', bucket_name=KS3_BUCKET, object_key=self.KEY, *args, **kwargs)

    def test_open(self):
        with open(self.KEY, encoding=self.ENCODING) as fp:
            self.upload(data=fp)

    def test_open_binary(self):
        with open(self.KEY, 'rb') as fp:
            self.upload(data=fp)

    def test_path(self):
        data = pathlib.Path(self.KEY)
        self.upload(data=data)

    def test_string(self):
        with open(self.KEY, encoding=self.ENCODING) as fp:
            data = fp.read()
        self.upload(data=data)

    def test_bytes(self):
        with open(self.KEY, 'rb') as fp:
            data = fp.read()
        self.upload(data=data)

    def test_string_io(self):
        with open(self.KEY, encoding=self.ENCODING) as fp:
            data = io.StringIO(fp.read())
        self.upload(data=data)

    def test_bytes_io(self):
        with open(self.KEY, 'rb') as fp:
            data = io.BytesIO(fp.read())
        self.upload(data=data)

    def test_invalid_checksum(self):
        with open(self.KEY, encoding=self.ENCODING) as fp:
            with self.assertRaises(Ks3Error) as context:
                self.upload(data=fp, content_md5='invalid_checksum')
        self.assertEqual('The Content-MD5 you specified is not valid.', context.exception.message)


if __name__ == '__main__':
    unittest.main()
