from test.settings import iiko
try:
    a = iiko.suppliers_find(name='21312', code='safmkdf')
    print(a)
except Exception as e:
   print("Обработать ошибку")

def test_token():
   return iiko.token()


def test_quit():
    return iiko.quit(token)


def test_version():
    return iiko.version()


def test_departments():
    return iiko.departments(token)


def test_stores():
    return iiko.stores(token)

def test_groups():
    return iiko.groups(token, '0')

def test_terminals():
    return iiko.terminals(token, '0')

def test_emploers():
   return iiko.terminals(token, '0')