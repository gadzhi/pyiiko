import requests


class IikoBiz:
    def __init__(self, login, password):

        self.login = login
        self.password = password

    def token(self):
        try:

            token = requests.get(
                'https://iiko.biz:9900/api/0/auth/access_token?user_id=' +
                self.login + '&user_secret=' + self.password,
                timeout=5).text[1:1]
            return token

        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить токен " + "\n" + self.login)

    def organization(self, token):

        try:

            organization = requests.get(
                'https://iiko.biz:9900/api/0/organization/list?access_token=' +
                token).json()
            return organization

        except requests.exceptions.ConnectTimeout:
            print(
                "Не удалось получить список организаций " + "\n" + self.login)

    def courier(self, token, org):

        try:
            courier = requests.get(
                'https://iiko.biz:9900/api/0/rmsSettings/getCouriers?access_token='
                + token + '&organization=' + org).json()
            return courier

        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить курьеров " + "\n" + self.login)

    def orders_courier(self, token, org, courier):

        try:
            orders = requests.get(
                'https://iiko.biz:9900/api/0/orders/get_courier_orders?access_token='
                + token + '&organization=' + org + '&courier=' + courier +
                '&request_timeout=00%3A02%3A00').json()
            return orders

        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить заказы " + "\n" + self.login)

    """Все заказы"""

    def all_orders(self, token, org, data_from, data_to, status, terminal_id):

        try:
            orders = requests.get(
                'https://iiko.biz:9900/api/0/orders/deliveryOrders?access_token='
                + token + '&organization=' + org + '&dateFrom=' + data_from +
                '&dateTo=' + data_to + '&deliveryStatus=' + status +
                '&deliveryTerminalId=' + terminal_id +
                '&request_timeout=00%3A02%3A00').json()
            return orders

        except requests.exceptions.ConnectTimeout:
            print("Не получить заказы " + "\n" + self.login)

    """История заказа гостя"""

    def customer_history(self, token, org, customer):

        try:
            history = requests.get(
                'https://iiko.biz:9900/api/0/orders/deliveryHistoryByCustomerId?access_token='
                + token + '&organization=' + org + '&customerId=' + customer +
                '&request_timeout=00%3A02%3A00').json()

            return history
        except requests.exceptions.ConnectTimeout:
            print("Не получить заказы " + "\n" + self.login)

    def nomenclature(self, token, org):
        """Получить дерево номенклатуры"""
        try:
            nomenclature = requests.get('https://iiko.biz:9900/api/0/nomenclature/'
                                   + org + '?access_token=' + token).json()

            return nomenclature
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить номенклатуру " + "\n" + self.login)
    
    def cities(self, token, org):
        """Список городов"""
        try:
            cities = requests.get('https://iiko.biz:9900/api/0/cities/cities?access_token='
                                   + token + '&organization=' + org).json()
            return cities
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить номенклатуру " + "\n" + self.login)



