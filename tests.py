from Pyiiko.server import IikoServer
import requests
i = IikoServer('operaderbent.iiko.it', '8080', 'admin', 'resto#test')

print(i.stores(i.token()))


