from test.settings import iiko

def test_token():
    return iiko.token()


g = iiko.events(token=test_token(), revision=1)
print(g)