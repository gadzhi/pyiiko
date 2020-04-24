import pytest
from Pyiiko import transport
import requests
import json
from Pyiiko.settings import i, order, org_id, city
test = transport.Transport(key=i)


def test_token():
    response = test.get_token()
    assert response['token'] != None


def test_organization():
    response = test.organization()
    assert response.status_code == 200


def test_terminal():
    response = test.terminal(org_id=org_id)
    assert response.status_code == 200


def test_regions():
    response = test.regions(org_id=org_id)
    assert response.status_code == 200


def test_cites():
    response = test.cities(org_id=org_id)
    assert response.status_code == 200


def test_streets():
    response = test.streets_by_city(org_id=org_id, city=city)
    assert response.status_code == 200


def test_order():
    response = test.delivery_create(order_info=order)
    assert response.status_code == 200


def test_id():
    response = test.by_id(org_id=org_id, order_id='dfff3083-ac61-4a6e-a554-ab37059b8dac')
    assert response.status_code == 200


def test_revision():
    response = test.by_revision(org_id=org_id, revision='1')
    assert response.status_code == 200