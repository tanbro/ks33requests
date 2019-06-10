import os

from ks33requests.client import Client
from ks33requests.errors import raise_for_errors
from ks33requests.schemas import s3_sub

ak = 'AKLToyzMEPK6RuGHFWXC1nfxlg'
sk = 'OBREz7VfDqvfqgjKJHPJl2+GKYwikVxJ3Z3jgn7CTB4JgdCfMCEt93BssvPouCbrEA=='
bucket_name = 'huameoi-newcutter-develop'
endpoint = 'ks3-cn-shanghai.ksyun.com'

c = Client(ak, sk, endpoint=endpoint)

# resp = c.call_api()
# raise_for_errors(resp)
# print(resp.text)


resp = c.call_api('GET', bucket_name=bucket_name)
raise_for_errors(resp)
result = s3_sub.parseString(resp.content)
for content in result.Contents:
    file_name = content.Key
    resp = c.call_api('GET', bucket_name=bucket_name, object_key=file_name)
    raise_for_errors(resp)
    try:
        print('下载', file_name, '...')
        with open(file_name, 'wb') as fp:
            for chunk in resp.iter_content(1024):
                fp.write(chunk)
        print('下载', file_name, ' OK.')
    finally:
        os.remove(file_name)

    resp = c.call_api('get', bucket_name=bucket_name, object_key=file_name, sub_resources='acl')
    raise_for_errors(resp)
    print(resp.text)

    break
