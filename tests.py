from Pyiiko.server import IikoServer
import requests
i = IikoServer('operaderbent.iiko.it', '8080', 'admin', 'resto#test')

print(i.get_events(i.get_token()))


re = requests.post('https://kurtuba.ru/create').content
print(re)