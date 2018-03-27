import requests
import hashlib


class IikoServer:
    def __init__(self, ip, port, login, password):

        self.ip = ip
        self.port = port
        self.login = login
        self.password = hashlib.sha1(password.encode('utf-8')).hexdigest()

    def token(self):
        """Получение токена"""
        try:
            new_token = requests.get('http://' + self.ip + ':' + self.port +
                                     "/resto/api/auth?login=" + self.login +
                                     "&" + "pass=" + self.password).text
            print("\nПолучен новый токен: " + new_token)
            return new_token

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def quit(self, token):
        """Уничтожение токена"""
        try:
            logout = requests.get('http://' + self.ip + ':' + self.port +
                                  "/resto/api/logout?key=" + token).text
            print("\nВыход осуществелен: ")
            return logout

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def departments(self, token):

        try:
            departments = requests.get(
                'http://' + self.ip + ':' + self.port +
                "/resto/api/corporation/departments?key=" + token).content
            return departments

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def groups(self, token):

        try:
            groups = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/groups?key=' + token + "&from_rev=",
                timeout=2).content
            return groups

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def terminals(self, token):
        """Терминалы"""
        try:
            terminal = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/terminals?key=' + token + "&from_rev=",
                timeout=2).content
            return terminal

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def employees(self, token):
        """Работники"""
        try:
            employees = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/employees?key=' + token,
                timeout=2).content
            return employees

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def events(self, token, revision=None):
        """События"""
        try:
            events = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/events?key=' + token + "&from_rev=" + revision,
                timeout=2).content
            return events

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def events_meta(self, token):
        """Дерево событий"""
        try:
            events = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/events/metadata?key=' + token,
                timeout=2).content
            return events

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def stores(self, token):

        try:
            stores = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/stores?key=' + token + "&from_rev=",
                timeout=2).content
            return stores

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def products(self, token):
        """Номенклатура"""
        try:
            products = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/products?key=' + token,
                timeout=2).content
            return products

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def sales(self, token, departments, date_from, date_to, dish_detail,
              all_revenue):
        """Отчет по выручке"""
        try:
            sales = requests.get(
                'http://' + self.ip + ':' + self.port +
                'resto/api/reports/sales?key=' + token + '&department=' +
                departments + '&dateFrom=' + date_from + '&dateTo=' + date_to +
                '&dishDetails=' + dish_detail + '&allRevenue=' + all_revenue,
                timeout=2).content
            return sales

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def session(self, token, start=None, end=None):
        """Информация о кассовых сменах"""
        try:
            session = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/events/sessions?key=' + token + '&from_time=' +
                start + '&to_time=' + end,
                timeout=2).content
            return session

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def close_session(self, token):
        """Номенклатура"""
        try:
            products = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/products?key=' + token,
                timeout=2).content
            return products

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)
