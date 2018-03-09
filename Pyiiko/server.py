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




