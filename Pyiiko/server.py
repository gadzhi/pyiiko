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
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                "/resto/api/corporation/departments?key=" + token).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def stores(self, token):
        """Список складов"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/stores?key=' + token,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def groups(self, token):
        """Список групп и отделений"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/groups?key=' + token + "&from_rev=",
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def terminals(self, token):
        """Терминалы"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/terminals?key=' + token + "&from_rev=",
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def departments_find(self, token, code=None):
        """Поиск подразделения"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                "/resto/api/corporation/departments/search?key=" + token +
                '&code=' + code).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def stores_find(self, token, code):
        """Список складов"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/stores/search?key=' + token +
                '&code=' + code,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def groups_find(self, token, name, department_id):
        """Поиск групп отделений"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/terminal/search?key=' + token +
                "&name=" + '&departmentId=' + department_id,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def terminals_find(self, token, anonymous=False):
        """Поиск терминала"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/terminals/search?key=' + token +
                "&anonymous=" + anonymous,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    "----------------------------------Работники----------------------------------"

    def employees(self, token):
        """Работники"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/employees?key=' + token,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    "----------------------------------События----------------------------------"

    def events(self, token, **kwargs):
        """События"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/events?key=' + token,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def events_meta(self, token):
        """Дерево событий"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/events/metadata?key=' + token,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    "----------------------------------Продукты----------------------------------"

    def products(self, token):
        """Номенклатура"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/products?key=' + token,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def products_find(self, token, **kwargs):
        """Номенклатура"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/products/search/?key=' + token,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def session(self, token, start=None, end=None):
        """Информация о кассовых сменах"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/events/sessions?key=' + token + '&from_time=' +
                start + '&to_time=' + end,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def close_session(self, token):
        """Номенклатура"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/products?key=' + token,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    "----------------------------------Поставщики----------------------------------"

    def suppliers(self, token):
        """Список всех поставщиков"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/suppliers?key=' + token,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def suppliers_find(self, token, name=None, code=None):
        """Поиск поставщика"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/suppliers?key=' + token + '&name=' + name +
                '&code=' + code,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def suppliers_price(self, token, code, date=None):
        """Поиск поставщика"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port + '/resto/api/suppliers/'
                + code + '/pricelist?key=' + token + '&date=' + date,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    "----------------------------------Отчеты----------------------------------"

    def olap(self, token, **kwargs):
        """OLAP-отчет"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/reports/olap?key=' + token,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def store_operation(self, token, **kwargs):
        """Отчет по складским операциям"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/reports/storeOperations?key=' + token,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def store_presets(self, token):
        """Пресеты отчетов по складским операциям"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/reports/storeReportPresets?key=' + token,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def product_expense(self, token, departament, **kwargs):
        """Расход продуктов по продажам"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/reports/productExpense?key=' + token +
                '&department=' + departament,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def sales(self, token, departament, **kwargs):
        """Отчет по выручке"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/reports/sales?key=' + token + '&department=' +
                departament,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def mounthly_plan(self, token, departament, **kwargs):
        """План по выручке за день"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/reports/monthlyIncomePlan?key=' + token +
                '&department=' + departament,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def ingredient_entry(self, token, departament, **kwargs):
        """Отчет о вхождении товара в блюдо"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/reports/monthlyIncomePlan?key=' + token +
                '&department=' + departament,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def olap2(self, token, **kwargs):
        """Поля OLAP-отчета"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/v2/reports/olap/columns?key=' + token,
                params=kwargs,
                timeout=2).json()

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    "----------------------------------Накладные----------------------------------"

    def in_invoice(self, token, **kwargs):
        """Выгрузка приходных накладных"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/documents/export/incomingInvoice?key=' + token,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def out_invoice(self, token, **kwargs):
        """Выгрузка расходных накладных"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/documents/export/outgoingInvoice?key=' + token,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def number_in_invoice(self, token, current_year=True, **kwargs):
        """Выгрузка приходной накладной по ее номеру"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/documents/export/incomingInvoice/byNumber?' +
                token + '&currentYear' + current_year,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def number_out_invoice(self, token, current_year=True, **kwargs):
        """Выгрузка расходной накладной по ее номеру"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/documents/export/outgoingInvoice/byNumber?key=' +
                token + '&currentYear' + current_year,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

