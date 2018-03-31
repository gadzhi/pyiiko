import requests


class FrontWebAPI:
    def __init__(self, url, moduleid, content_type):

        self.url = url
        self.moduleid = moduleid
        self.content_type = content_type

    def token(self):

        return requests.get(
            'http://' + self.url + "/api/login/" + self.moduleid).content


    def quit(self, token):
        """Уничтожение токена"""
        return requests.get(
            'http://' + self.url + "/api/logout/" + token).content

    def orders(self, token):
        """Заказы"""
        return requests.get(
            'http://' + self.url + "/api/orders?key=" + token,
            headers=self.content_type).content

    def sections(self, token):
        """Отделения"""
        return requests.get(
            'http://' + self.url + "/api/sections?key=" + token,
            headers=self.content_type).content

    def tables(self, token):
        """Столы"""
        return requests.get(
            'http://' + self.url + "/api/tables?key=" + token,
            headers=self.content_type).content

    def products(self, token):
        """Продукты"""
        return requests.get(
            'http://' + self.url + "/api/products?key=" + token,
            headers=self.content_type).content

    def product_groups(self, token):
        """Иерархическое меню"""
        return requests.get(
            'http://' + self.url + "/api/productgroups?key=" + token,
            headers=self.content_type).content

    def quick_menu(self, token):
        """Быстрое меню для стола по умолчанию"""
        return requests.get(
            'http://' + self.url + "/api/quickmenu?key=" + token,
            headers=self.content_type).content

    def users(self, token):
        """Пользователи"""
        return requests.get(
            'http://' + self.url + "/api/users?key=" + token,
            headers=self.content_type).content

    def deliveries(self, token):
        """Доставки"""
        return requests.get(
            'http://' + self.url + "/api/deliveries?key=" + token,
            headers=self.content_type).content

    def kitchen(self, token):
        """Кухонные заказы"""
        return requests.get(
            'http://' + self.url + "/api/kitchenorders?key=" + token,
            headers=self.content_type).content
