# -*- coding: utf-8 -*-
import requests
import hashlib
from lxml import etree
from io import StringIO


class IikoServer:
    def __init__(self, ip, port, login, password):

        self.login = login
        self.password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        self.address = 'http://' + ip + ':' + port + '/resto/'

    def token(self):
        """Получение токена"""
        try:
            url = self.address + 'api/auth?login=' + self.login + "&pass=" + self.password
            new_token = requests.get(url=url).text
            print("\nПолучен новый токен: " + new_token)
            return new_token

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def quit(self, token):
        """Уничтожение токена"""
        try:
            logout = requests.get(self.address + 'api/logout?key=' + token).text
            print("\nВыход осуществлен: ")
            return logout

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def version(self):
        """Версия iiko"""
        try:
            ver = requests.get(self.address + '/get_server_info.jsp?encoding=UTF-8').text
            tree = etree.parse(StringIO(ver))
            version = ''.join(tree.xpath(r'//version/text()'))
            return version

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)
    "----------------------------------Корпорации----------------------------------"

    def departments(self, token):
        """Иерархия подразделений"""
        try:
            return requests.get(
                self.address + "/api/corporation/departments?key=" + token).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def stores(self, token):
        """Список складов"""
        try:
            ur = self.address + 'api/corporation/stores?key=' + token
            return requests.get(
                ur,
                timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def groups(self, token, revision):
        """Список групп и отделений"""
        try:
            ur = self.address + 'api/corporation/groups?key=' + token
            return requests.get( ur, params=revision, timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def terminals(self, token, revision):
        """Терминалы"""
        try:
            ur = self.address + 'api/corporation/terminals?key=' + token
            return requests.get(ur, params=revision, timeout=2).content

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
            ur = self.address + 'api/employees?key=' + token
            return requests.get(ur, timeout=2).content

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

    def invoice_in(self, token, **kwargs):
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

    def invoice_out(self, token, **kwargs):
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
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

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
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

    def production_doc(self, token, xml):
        """Загрузка акта приготовления"""
        try:
            target_url = self.address + '/api/documents/import/productionDocument?key' + token
            headers = {'Content-type': 'text/xml'}
            return requests.post(target_url, body=xml, headers=headers, timeout=2).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" +
                  self.port)

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
