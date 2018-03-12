from Pyiiko.server import IikoServer
from Pyiiko.processing import *
import requests
i = IikoServer('operaderbent.iiko.it', '8080', 'admin', 'resto#test')

a = i.departments(i.token())


print(i.products(i.token()))

