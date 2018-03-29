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
            nomenclature = requests.get(
                'https://iiko.biz:9900/api/0/nomenclature/' + org +
                '?access_token=' + token).json()

            return nomenclature
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить номенклатуру " + "\n" + self.login)

    "-------------------Города, улицы, регионы-------------------"

    def cities(self, token, org):
        """Список городов"""
        try:
            cities = requests.get(
                'https://iiko.biz:9900/api/0/cities/cities?access_token=' +
                token + '&organization=' + org).json()
            return cities
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список городов" + "\n" + self.login)

    def cities_list(self, token, org):
        """возвращает список всех городов заданной организации"""
        try:
            cities = requests.get(
                'https://iiko.biz:9900/api/0/citiesList/cities?access_token=' +
                token + '&organization=' + org).json()
            return cities
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список городов" + "\n" + self.login)

    def streets(self, token, org, citi_id):
        """возвращает список улиц города заданной организации"""
        try:
            streets = requests.get(
                'https://iiko.biz:9900/api/0/citiesList/streets?access_token='
                + token + '&organization=' + org + '&city=' + citi_id).json()
            return streets
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список улиц" + "\n" + self.login)
    
    "--------------------------------------Стоп-листы--------------------------------------"

    def stop_list(self, token, org):
        """Получить стоп-лист по сети ресторанов"""
        try:
            return requests.get(
                'https://iiko.biz:9900/api/0/stopLists/getDeliveryStopList?access_token=' + token + 
                '&organization=' + org).json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список улиц" + "\n" + self.login)

    "--------------------------------------Журнал событий--------------------------------------"

    def events(self, token, timeout=None):
        """Получить стоп-лист по сети ресторанов"""
        try:
            return requests.get(
                'https://iiko.biz:9900/api/0/events/events?access_token=' + token + 
                '&request_timeout=' + timeout).json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список улиц" + "\n" + self.login)

    def events_meta(self, token, body, timeout=None):
        """Получить стоп-лист по сети ресторанов"""
        try:
            return requests.post(
                'https://iiko.biz:9900/api/0/events/eventsMetadata?access_token=' + token + 
                '&request_timeout=' + timeout, body=body).json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список улиц" + "\n" + self.login)

    def events_session(self, token, body, timeout=None):
        """Получить стоп-лист по сети ресторанов"""
        try:
            return requests.post(
                'https://iiko.biz:9900/api/0/events/sessions?access_token=' + token + 
                '&request_timeout=' + timeout, body=body).json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список улиц" + "\n" + self.login)