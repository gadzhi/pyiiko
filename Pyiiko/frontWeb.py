import requests


class FrontWebAPI:

    def __init__(self, url, moduleid, content_type):

        self.url = url
        self.moduleid = moduleid
        self.content_type = content_type

    def token(self):

        req = requests.get('http://' + self.url + "/api/login/" + self.moduleid).content

        return req

    def order_all(self, token):

        req = requests.get('http://' + self.url + "/api/orders?key=" + token,
                           headers=self.content_type).content

        return req


