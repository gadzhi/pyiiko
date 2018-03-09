import requests


class IikoBiz:

    def __init__(self, login, password):

        self.login = login
        self.password = password

    def get_token(self):
        try:

            token = requests.get('https://iiko.biz:9900/api/0/auth/access_token?user_id=' + self.login +
                                 '&user_secret=' + self.password, timeout=5).text[1:1]
            return token

        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить токен " + "\n" + self.login)

    def get_organization(self, token):

        try:

            organization = requests.get('https://iiko.biz:9900/api/0/organization/list?access_token=' + token).json()
            return organization

        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список организаций " + "\n" + self.login)

    def get_courier(self, token, org):

        try:
            courier = requests.get('https://iiko.biz:9900/api/0/rmsSettings/getCouriers?access_token=' + token +
                               '&organization=' + org).json()
            return courier

        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить курьеров " + "\n" + self.login)

    def get_orders_courier(self, token, org, courier):

        try:
            orders = requests.get('https://iiko.biz:9900/api/0/orders/get_courier_orders?access_token=' + token +
                                  '&organization=' + org + '&courier=' + courier + '&request_timeout=00%3A02%3A00').json()
            return orders

        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить заказы " + "\n" + self.login)

    def get_all_orders(self, token, org, data_from, data_to, status, terminal_id):

        try:
            orders = requests.get('https://iiko.biz:9900/api/0/orders/deliveryOrders?access_token=' + token +
                                  '&organization=' + org + '&dateFrom=' + data_from + '&dateTo=' + data_to +
                                  '&deliveryStatus=' + status + '&deliveryTerminalId=' + terminal_id +
                                                     '&request_timeout=00%3A02%3A00').json()
            return orders

        except requests.exceptions.ConnectTimeout:
            print("Не получить заказы " + "\n" + self.login)