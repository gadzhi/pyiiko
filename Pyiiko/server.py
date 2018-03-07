import requests


class Iiko:

    def __init__(self, ip, port, login, password, token, revision):

        self.ip = ip
        self.port = port
        self.login = login
        self.password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        self.token = token
        self.revision = revision

    def get_token(self):

        try:
            new_token = requests.get('http://' + self.ip + ':' + self.port + "/resto/api/auth?login=" +
                                     self.login + "&" + "pass=" + self.password)

            print(self.name + "\nПолучен новый токен: " + new_token)
            return new_token

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу " + self.name + "\n" + self.ip + ":" + self.port)
