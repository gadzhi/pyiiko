import requests
import hashlib
import lxml
from lxml import etree
from Pyiiko.data import read_token, save_token


class Iiko:

    def __init__(self, ip, port, login, password):

        self.ip = ip
        self.port = port
        self.login = login
        self.password = hashlib.sha1(password.encode('utf-8')).hexdigest()

    def get_token(self):

        try:
            old_token = read_token()

            check = requests.get('http://' + self.ip + ':' + self.port +
                                       "/resto/api/corporation/departments?key=" + old_token)

            if (check.status_code == 400) or (check.status_code == 401) or (
                    check.status_code == 403) or (check.status_code == 402):

                new_token = requests.get('http://' + self.ip + ':' + self.port + "/resto/api/auth?login=" +
                                     self.login + "&" + "pass=" + self.password).text

                save_token(new_token)

                print("\nПолучен новый токен: " + new_token)

                return new_token

            else:
                print("\nСтарый токен валидный: " + old_token)
                return old_token

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + "\n" + self.ip + ":" + self.port)

    def get_departments(self):

        token = Iiko.get_token(self)

        departments = requests.get('http://' + self.ip + ':' + self.port +
                           "/resto/api/corporation/departments?key=" + token)

        file = lxml.etree.fromstring(departments.content)

        events = file.xpath(
            r'//corporateItemDto/type[text() = "DEPARTMENT"]/..')
        departments = {}

        for event in events:
            result = ''.join(event.xpath(r'./id/text()'))

            name = ''.join(event.xpath(r'./name/text()'))

            departments[name] = result

        return departments

