# -*- coding: utf-8 -*-
import requests
import hashlib
from lxml import etree
from io import StringIO


class IikoServer:
    def __init__(self, ip, port, login, password, token=None):

        self.login = login
        self.password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        self.address = 'http://' + ip + ':' + port + '/resto/'
        self._token = (token or self._token())

    def _token(self):
        """Получение токена"""

        try:
            url = self.address + 'api/auth?login=' + self.login + "&pass=" + self.password
            token = requests.get(url=url).text
            print("\nПолучен новый токен: " + token)
            return token

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def quit(self):
        """Уничтожение токена"""

        try:
            logout = requests.get(self.address + 'api/logout?key=' + self._token).text
            print("\nВыход осуществлен: ")
            return logout

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу" )

    def version(self):
        """Версия iiko"""
        try:
            ver = requests.get(self.address + '/get_server_info.jsp?encoding=UTF-8').text
            tree = etree.parse(StringIO(ver))
            version = ''.join(tree.xpath(r'//version/text()'))
            return version

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")
    "----------------------------------Корпорации----------------------------------"

    def departments(self):
        """Иерархия подразделений"""
        try:
            return requests.get(
                self.address + "/api/corporation/departments?key=" + self._token).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def stores(self):
        """Список складов"""
        try:
            ur = self.address + 'api/corporation/stores?key=' + self._token
            return requests.get(
                ur,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def groups(self):
        """Список групп и отделений"""
        try:
            ur = self.address + 'api/corporation/groups?key=' + self._token
            return requests.get(ur, timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def terminals(self):
        """Терминалы"""
        try:
            ur = self.address + 'api/corporation/terminals?key=' + self._token
            return requests.get(ur, timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def departments_find(self, **kwargs):
        """Поиск подразделения"""
        try:
            ur = self.address + 'api/corporation/departments/search?key=' + self._token
            return requests.get(
                ur, params=kwargs, timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу ")

    def stores_find(self, code):
        """Список складов"""
        try:
            ur = self.address + 'api/corporation/stores/search?key=' + self._token
            return requests.get(
                ur, params=code).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу" )

    def groups_find(self, token, name, department_id):
        """Поиск групп отделений"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/terminal/search?key=' + token +
                "&name=" + '&departmentId=' + department_id,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    def terminals_find(self, token, anonymous=False):
        """Поиск терминала"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/corporation/terminals/search?key=' + token +
                "&anonymous=" + anonymous,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    "----------------------------------Работники----------------------------------"

    def employees(self, token):
        """Работники"""
        try:
            ur = self.address + 'api/employees?key=' + token
            return requests.get(ur, timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    "----------------------------------События----------------------------------"

    def events(self, token, **kwargs):
        """События"""
        try:
            ur = self.address + 'api/events?key=' + token
            return requests.get(ur,params=kwargs, timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    def events_meta(self, token):
        """Дерево событий"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/events/metadata?key=' + token,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    "----------------------------------Продукты----------------------------------"

    def products(self, token):
        """Номенклатура"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/products?key=' + token,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    def products_find(self, token, **kwargs):
        """Номенклатура"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/products/search/?key=' + token,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    "----------------------------------Поставщики----------------------------------"

    def suppliers(self, token):
        """Список всех поставщиков"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/suppliers?key=' + token,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    def suppliers_find(self, token, name=None, code=None):
        """Поиск поставщика"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/suppliers?key=' + token + '&name=' + name +
                '&code=' + code,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    def suppliers_price(self, token, code, date=None):
        """Поиск поставщика"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port + '/resto/api/suppliers/'
                + code + '/pricelist?key=' + token + '&date=' + date,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

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
            print("Не удалось подключиться к серверу " )

    def store_operation(self, token, **kwargs):
        """Отчет по складским операциям"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/reports/storeOperations?key=' + token,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    def store_presets(self, token):
        """Пресеты отчетов по складским операциям"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/reports/storeReportPresets?key=' + token,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

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
            print("Не удалось подключиться к серверу " )

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
            print("Не удалось подключиться к серверу " )

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
            print("Не удалось подключиться к серверу " )

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
            print("Не удалось подключиться к серверу " )

    def olap2(self, token, **kwargs):
        """Поля OLAP-отчета"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/v2/reports/olap/columns?key=' + token,
                params=kwargs,
                timeout=2).json()

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    "----------------------------------Накладные----------------------------------"

    def invoice_in(self, token, **kwargs):
        """Выгрузка приходных накладных"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/documents/export/incomingInvoice?key=' + token,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    def invoice_out(self, token, **kwargs):
        """Выгрузка расходных накладных"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/documents/export/outgoingInvoice?key=' + token,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    def invoice_number_in(self, token, current_year=True, **kwargs):
        """Выгрузка приходной накладной по ее номеру"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/documents/export/incomingInvoice/byNumber?' +
                token + '&currentYear' + current_year,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    def invoice_number_out(self, token, current_year=True, **kwargs):
        """Выгрузка расходной накладной по ее номеру"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/documents/export/outgoingInvoice/byNumber?key=' +
                token + '&currentYear' + current_year,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    def production_doc(self, token, xml):
        """Загрузка акта приготовления"""
        try:
            target_url = self.address + '/api/documents/import/productionDocument?key' + token
            headers = {'Content-type': 'text/xml'}
            return requests.post(target_url, body=xml, headers=headers, timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    "----------------------------------Получение данных по кассовым сменам:----------------------------------"

    def close_session(self, token, **kwargs):
        """Список кассовых смен"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                'resto/api/closeSession/list?key=' +
                token,
                params=kwargs,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )

    def session(self, token, start=None, end=None):
        """Информация о кассовых сменах"""
        try:
            return requests.get(
                'http://' + self.ip + ':' + self.port +
                '/resto/api/events/sessions?key=' + token + '&from_time=' +
                start + '&to_time=' + end,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " )
