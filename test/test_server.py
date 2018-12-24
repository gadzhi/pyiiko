import pytest
import Pyiiko
import requests
from settings import i


def test_token():
    assert i.token()

def test_version():
    assert i.version()


def test_departments():
    assert i.departments()


def test_stores():
    response = i.stores()
    assert response.status_code == 200


def test_groups():
    i.groups()


def test_terminals():
    assert i.terminals()


def test_departments_find():
    assert i.departments_find("234")


def test_stores_find():
    assert i.stores_find("") == 200


def test_quit():
    assert i.quit_token()

test_stores()