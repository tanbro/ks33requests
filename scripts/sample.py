from ks33requests.client import Client
from ks33requests.errors import raise_for_ks3_status

ak = 'AKLToyzMEPK6RuGHFWXC1nfxlg'
sk = 'OBREz7VfDqvfqgjKJHPJl2+GKYwikVxJ3Z3jgn7CTB4JgdCfMCEt93BssvPouCbrEA=='
# bucket_name = 'huameoi-newcutter-develop'
endpoint = 'ks3-cn-shanghai.ksyun.com'

c = Client(ak, sk, endpoint=endpoint)

# 列出默认项目的第一个 bucket
result = c.call_api_s3res(params={'projectIds': '0'})
bucket_0 = result.Buckets.Bucket[0]
bucket_name = bucket_0.Name
print('Bucket 名称是：', bucket_name)

# 获取这个BUCKET 的 location:
result = c.call_api_s3res('GET', bucket_name=bucket_name, sub_resources='location')
print('区域是:', result.valueOf_)

# # 下载第一个文件
# result = c.call_s3_api('GET', bucket_name=bucket_name)
# for content in result.Contents:
#     file_name = content.Key
#     resp = c.call_api('GET', bucket_name=bucket_name, object_key=file_name)
#     raise_for_ks3_status(resp)
#     print('打印文件', file_name, '的内容 ...')
#     for chunk in resp.iter_content(io.DEFAULT_BUFFER_SIZE):
#         print(chunk.decode())
#
#     # 获取这个文件的 ACL:
#     resp = c.call_api('GET', bucket_name=bucket_name, object_key=file_name, sub_resources='acl')
#     raise_for_ks3_status(resp)
#     print('ACL: ', resp.text)
#
#     break

# # 上传一个文件
# file_name = 'Pipfile'
# with open(file_name) as fp:
#     text = fp.read()
# with open(file_name, 'rb') as fp:
#     c.call_api_s3_response('put', bucket_name=bucket_name, object_key=file_name, data=fp)
# # 下载看看文件信息!
# resp = c.call_api('get', bucket_name=bucket_name, object_key=file_name)
# raise_for_ks3_status(resp)
# assert text == resp.text


# 上传一个大文件试试看
# file_path = '/mnt/1B9074BA60C16502/works/huamei/大江传媒AI媒体数据处理/data/湖口/20190416.mp4'
# object_key = '湖口-20190416.mp4'
# with open(file_path, 'rb') as fp:
#     print('uploading ...')
#     resp = c.call_api('put', bucket_name=bucket_name, object_key=object_key, data=fp)
#     print('upload OK')
#     raise_for_ks3_status(resp)
