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

    "----------------------------------Корпорации----------------------------------"

    def departments(self, token):
        """Иерархия подразделений"""
        try:
            departments = requests.get(
                'http://' + self.ip + ':' + self.port +
                "/resto/api/corporation/departments?key=" + token).content
            return departments

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def stores(self, token):
        """Список складов"""
        try:
            stores = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/stores?key=' + token,
                timeout=2).content
            return stores

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def groups(self, token):
        """Список групп и отделений"""
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

    def departments_find(self, token, code=None):
        """Поиск подразделения"""
        try:
            departments = requests.get(
                'http://' + self.ip + ':' + self.port +
                "/resto/api/corporation/departments/search?key=" + token +
                '&code=' + code).content
            return departments

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def stores_find(self, token, code):
        """Список складов"""
        try:
            stores = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/stores/search?key=' + token +
                '&code=' + code,
                timeout=2).content
            return stores

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def groups_find(self, token, name, department_id):
        """Поиск групп отделений"""
        try:
            groups = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/terminal/search?key=' + token +
                "&name=" + '&departmentId=' + department_id,
                timeout=2).content
            return groups

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def terminals_find(self, token, anonymous=False):
        """Поиск терминала"""
        try:
            terminal = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/terminals/search?key=' + token +
                "&anonymous=" + anonymous,
                timeout=2).content
            return terminal

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    "----------------------------------Работники----------------------------------"

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
    
    "----------------------------------События----------------------------------"
    
    def events(self, token, **kwargs):
        """События"""
        try:
            events = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/events?key=' + token, params = kwargs, 
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
    
    "----------------------------------Продукты----------------------------------"
    
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

    def products_find(self, token, **kwargs):
        """Номенклатура"""
        try:
            products = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/products/search/?key=' + token, params = kwargs,
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

    "----------------------------------Поставщики----------------------------------"

    def suppliers(self, token):
        """Список всех поставщиков"""
        try:
            suppliers = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/suppliers?key=' + token,
                timeout=2).content
            return suppliers

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def suppliers_find(self, token, name=None, code=None):
        """Поиск поставщика"""
        try:
            suppliers = requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/suppliers?key=' + token + '&name=' + name +
                '&code=' + code,
                timeout=2).content
            return suppliers

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def suppliers_price(self, token, code, date=None):
        """Поиск поставщика"""
        try:
            suppliers = requests.get(
                'http://' + self.ip + ':' + self.port + '/resto/api/suppliers/'
                + code + '/pricelist?key=' + token + '&date=' + date,
                timeout=2).content
            return suppliers

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)
