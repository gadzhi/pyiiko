import requests
import json
address = 'https://api-ru.iiko.services/'
DEFAULT_TIMEOUT = 4
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
from Pyiiko.settings import order

class Transport:

    def __init__(self, key=None, token=None):

        self.key = key
        self._token = (token or self.get_token())

    def token(self):
        return self._token()

    def get_token(self):
        try:
            url = address + 'api/1/access_token'
            payload = '{"apiLogin":"' + self.key + '"}'
            return requests.post(url=url, data=payload, headers=headers, timeout=DEFAULT_TIMEOUT).json()

        except Exception as e:
            print(e)

    def organization(self):
        try:
            auth = self._token['token']
            url = address + 'api/1/organizations'
            hed = {'Authorization': 'Bearer ' + auth}

            return requests.get(url=url, headers=hed, timeout=DEFAULT_TIMEOUT)

        except Exception as e:
            print(e)

    def terminal(self, org_id, include= "false"):
        try:
            auth = self._token['token']
            url = address + 'api/1/terminal_groups'
            hed = {'Authorization': 'Bearer ' + auth}
            payload = json.loads('{"organizationIds": ["' + org_id + '"]}')

            return requests.post(url=url, json=payload, headers=hed, timeout=DEFAULT_TIMEOUT)

        except Exception as e:
            print(e)

    def regions(self, org_id):
        try:
            auth = self._token['token']
            url = address + 'api/1/regions'
            hed = {'Authorization': 'Bearer ' + auth}
            payload = json.loads('{"organizationIds": ["' + org_id + '"]}')

            return requests.post(url=url, json=payload, headers=hed, timeout=DEFAULT_TIMEOUT)

        except Exception as e:
            print(e)

    def cities(self, org_id=None):
        try:
            auth = self._token['token']
            url = address + 'api/1/cities'
            hed = {'Authorization': 'Bearer ' + auth}
            payload = json.loads('{"organizationIds": ["' + org_id + '"]}')

            return requests.post(url=url, json=payload, headers=hed, timeout=DEFAULT_TIMEOUT)

        except Exception as e:
            print(e)

    def streets_by_city(self, org_id, city):
        try:
            auth = self._token['token']
            url = address + 'api/1/streets/by_city'
            hed = {'Authorization': 'Bearer ' + auth}
            payload = json.loads('{"organizationId": "' + org_id + '","cityId": "' + city + '"}')

            return requests.post(url=url, json=payload, headers=hed, timeout=DEFAULT_TIMEOUT)

        except Exception as e:
            print(e)

    def delivery_create(self, order_info):
        try:
            auth = self._token['token']
            url = address + 'api/1/deliveries/create'
            hed = {'Authorization': 'Bearer ' + auth}
            payload = order_info

            return requests.post(url=url, json=payload, headers=hed, timeout=DEFAULT_TIMEOUT)

        except Exception as e:
            print(e)

    def check_create(self, order_info):
        try:
            auth = self._token['token']
            url = address + 'api/1/deliveries/check_create'
            hed = {'Authorization': 'Bearer ' + auth}
            payload = json.loads(order_info)

            return requests.post(url=url, json=payload, headers=hed, timeout=DEFAULT_TIMEOUT)

        except Exception as e:
            print(e)

    def by_id(self, org_id=None, order_id=None):
        try:
            auth = self._token['token']
            url = address + 'api/1/deliveries/by_id'
            hed = {'Authorization': 'Bearer ' + auth}
            payload = json.loads('{"organizationId": "' + org_id + '","orderIds": ["' + order_id + '"]}')

            return requests.post(url=url, json=payload, headers=hed, timeout=DEFAULT_TIMEOUT)

        except Exception as e:
            print(e)

    def by_delivery_date(self, org_id=None, order_id=None):
        try:
            auth = self._token['token']
            url = address + 'api/1/deliveries/by_delivery_date_and_status'
            hed = {'Authorization': 'Bearer ' + auth}
            payload = json.loads('{"organizationId": ["' + org_id + '"],"deliveryDateFrom": ["' + order_id + '"]}')

            return requests.post(url=url, json=payload, headers=hed, timeout=DEFAULT_TIMEOUT)

        except Exception as e:
            print(e)


    def by_revision(self, org_id=None, revision=None):
        try:
            auth = self._token['token']
            url = address + 'api/1/deliveries/by_revision'
            hed = {'Authorization': 'Bearer ' + auth}
            payload = json.loads('{"startRevision": "' + revision + '","organizationIds": ["' + org_id + '"]}')

            return requests.post(url=url, json=payload, headers=hed, timeout=DEFAULT_TIMEOUT)

        except Exception as e:
            print(e)
