import requests

address = 'https://api-ru.iiko.services/'
DEFAULT_TIMEOUT = 4
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}


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

            return requests.get(url=url, headers=hed, timeout=DEFAULT_TIMEOUT).json()

        except Exception as e:
            print(e)