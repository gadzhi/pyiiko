from .settings import iiko

def test_token():
    return iiko.token()


g = iiko.products_find(token=test_token(), num=1)
print(g)