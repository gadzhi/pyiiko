from Pyiiko.server import Iiko

i = Iiko('operaderbent.iiko.it', '8080', 'admin', 'resto#test')

print(i.get_token())
