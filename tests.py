from Pyiiko.server import IikoServer

i = IikoServer('operaderbent.iiko.it', '8080', 'admin', 'resto#test')

print(i.get_events(i.get_token()))
