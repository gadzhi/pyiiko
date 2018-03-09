import requests
import hashlib
import lxml
from lxml import etree


class IikoServer:

    def __init__(self, ip, port, login, password):

        self.ip = ip
        self.port = port
        self.login = login
        self.password = hashlib.sha1(password.encode('utf-8')).hexdigest()

    def get_token(self):

        try:

            new_token = requests.get('http://' + self.ip + ':' + self.port + "/resto/api/auth?login=" +
                                     self.login + "&" + "pass=" + self.password).text

            print("\nПолучен новый токен: " + new_token)

            return new_token

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" + self.port)

    def get_departments(self, token):

        try:

            departments = requests.get('http://' + self.ip + ':' + self.port
                                       +"/resto/api/corporation/departments?key=" + token)

            file = lxml.etree.fromstring(departments.content)

            events = file.xpath(
                r'//corporateItemDto/type[text() = "DEPARTMENT"]/..')
            departments = {}

            for event in events:
                result = ''.join(event.xpath(r'./id/text()'))

                name = ''.join(event.xpath(r'./name/text()'))

                departments[name] = result

            return departments

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" + self.port)

    def get_employees(self, token):

        try:

            employees = requests.get('http://' + self.ip + ':' + self.port + '/resto/api/employees?key=' +
                                     token, timeout=5).content

            return employees

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" + self.port)

    def get_events(self, token):

        try:

            events = requests.get('http://' + self.ip + ':' + self.port + '/resto/api/events?key=' + token +
                                  "&from_rev=", timeout=5).content

            return events

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" + self.port)


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
            print("Не получить список организаций " + "\n" + self.login)

    def get_courier(self, token, org):

        try:
            courier = requests.get('https://iiko.biz:9900/api/0/rmsSettings/getCouriers?access_token=' + token +
                               '&organization=' + org).json()
            return courier

        except requests.exceptions.ConnectTimeout:
            print("Не получить курьеров " + "\n" + self.login)

    def get_orders(self, token, org, courier):

        try:
            orders = requests.get('https://iiko.biz:9900/api/0/orders/get_courier_orders?access_token=' + token +
                                  '&organization=' + org + '&courier=' + courier + '&request_timeout=00%3A02%3A00').json()
            return orders

        except requests.exceptions.ConnectTimeout:
            print("Не получить заказы " + "\n" + self.login)

