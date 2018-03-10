from Pyiiko.server import IikoServer
import requests
#i = IikoServer('operaderbent.iiko.it', '8080', 'admin', 'resto#test')

#print(i.get_events(i.get_token()))


re1 = requests.post('http://localhost:3199/create').content
string = {'name': 2}
re = requests.get('http://localhost:3199/44c5afcd-a90a-420a-ab7c-2037ce2ee716/', string).content

print(re1)