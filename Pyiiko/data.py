import shelve
import os
basedir = os.path.abspath(os.path.dirname(__file__))

def save_token(token):
    db = shelve.open("Pyiiko/file")
    db['token'] = [token]
    db.close()


def read_token():
    db = shelve.open("Pyiiko/file")
    token = db['token']

    return token[0]

