from ks33requests.connection import Connection

ak = 'AKLToyzMEPK6RuGHFWXC1nfxlg'
sk = 'OBREz7VfDqvfqgjKJHPJl2+GKYwikVxJ3Z3jgn7CTB4JgdCfMCEt93BssvPouCbrEA=='

c = Connection(ak, sk)

result = c.list_buckets()
for x in result.Buckets.Bucket:
    print(x.Name)
