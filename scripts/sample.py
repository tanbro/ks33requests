from ks33requests.connection import Connection
from ks33requests.errors import raise_for_error

ak = 'AKLToyzMEPK6RuGHFWXC1nfxlg'
sk = 'OBREz7VfDqvfqgjKJHPJl2+GKYwikVxJ3Z3jgn7CTB4JgdCfMCEt93BssvPouCbrEA=='

c = Connection(ak, sk)
resp = c.call_api()
raise_for_error(resp)

# result = c.list_buckets()
# print(result)
# for x in result.Buckets.Bucket:
#     print(x.Name)
