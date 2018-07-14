import pytest
import Pyiiko
from .settings import i


def test_token():
    assert i.token()


def test_version():
    assert i.version()


def test_departments():
    assert i.departments()

def test_quit():
    assert i.quit_token()
