import requests


class FrontWebAPI():
    def __init__(self, login, url,moduleid):

        self.login = login
        self.url = url
        self.moduleid = moduleid

    def token(self):

        req = requests.get('http://' + self.url + "/api/login/" + self.moduleid).content

        return req

    def order_all(self, token):

        req = requests.get('http://' + self.url + "/api/orders?key=" + token).content

        return req

