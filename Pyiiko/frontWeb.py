import requests


class FrontWebAPI:

    def __init__(self, url, moduleid, content_type):

        self.url = url
        self.moduleid = moduleid
        self.content_type = content_type

    def token(self):

        req = requests.get('http://' + self.url +
                           "/api/login/" + self.moduleid).content
        return req

    def quit(self, token):
        """Уничтожение токена"""
        req = requests.get('http://' + self.url +
                           "/api/logout/" + token).content
        return req

    def orders(self, token):
        """Заказы"""
        req = requests.get('http://' + self.url + "/api/orders?key=" + token,
                           headers=self.content_type).content
        return req

    def sections(self, token):
        """Отделения"""
        req = requests.get('http://' + self.url + "/api/sections?key=" + token,
                           headers=self.content_type).content
        return req

    def tables(self, token):
        """Столы"""
        req = requests.get('http://' + self.url + "/api/tables?key=" + token,
                           headers=self.content_type).content
        return req

    def products(self, token):
        """Продукты"""
        req = requests.get('http://' + self.url + "/api/products?key=" + token,
                           headers=self.content_type).content
        return req

    def product_groups(self, token):
        """Иерархическое меню"""
        req = requests.get('http://' + self.url + "/api/productgroups?key=" + token,
                           headers=self.content_type).content
        return req

    def quick_menu(self, token):
        """Быстрое меню для стола по умолчанию"""
        req = requests.get('http://' + self.url + "/api/quickmenu?key=" + token,
                           headers=self.content_type).content
        return req

    def users(self, token):
        """Пользователи"""
        req = requests.get('http://' + self.url + "/api/users?key=" + token,
                           headers=self.content_type).content
        return req

    def deliveries(self, token):
        """Доставки"""
        req = requests.get('http://' + self.url + "/api/deliveries?key=" + token,
                           headers=self.content_type).content
        return req

    def kitchen(self, token):
        """Кухонные заказы"""
        req = requests.get('http://' + self.url + "/api/kitchenorders?key=" + token,
                           headers=self.content_type).content
        return req
