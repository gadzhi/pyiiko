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

    def token(self):

        try:

            new_token = requests.get('http://' + self.ip + ':' + self.port + "/resto/api/auth?login=" +
                                     self.login + "&" + "pass=" + self.password).text
            print("\nПолучен новый токен: " + new_token)

            return new_token

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" + self.port)

    def quit(self, token):

        try:

            logout = requests.get('http://' + self.ip + ':' + self.port + "/resto/api/logout?key=" +
                                     token).text
            print("\nВыход осуществелен: ")

            return logout

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" + self.port)

    def departments(self, token):

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

    def employees(self, token):

        try:

            employees = requests.get('http://' + self.ip + ':' + self.port + '/resto/api/employees?key=' +
                                     token, timeout=5).content

            return employees

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" + self.port)

    def events(self, token):

        try:

            events = requests.get('http://' + self.ip + ':' + self.port + '/resto/api/events?key=' + token +
                                  "&from_rev=", timeout=5).content

            return events

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" + self.port)

    def stores(self, token):

        try:

            stores = requests.get('http://' + self.ip + ':' + self.port + '/resto/api/corporation/stores?key=' + token +
                                  "&from_rev=", timeout=2).content

            return stores

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" + self.port)

    def groups(self, token):

        try:

            groups = requests.get('http://' + self.ip + ':' + self.port + '/resto/api/corporation/groups?key=' + token +
                                  "&from_rev=", timeout=2).content

            return groups

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" + self.port)

    def olap(self, token):
        try:

            olap = requests.get('http://' + self.ip + ':' + self.port + '/resto/api/v2/reports/olap/columns?key='
                                  + token + "&reportType=SALES", timeout=2).content

            return olap

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" + self.port)


