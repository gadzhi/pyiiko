from test.settings import iiko

token = iiko.token()

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