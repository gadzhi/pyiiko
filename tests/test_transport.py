"""Unit tests for Transport."""
import json

import pytest
import responses

from Pyiiko import IikoAPIError, IikoAuthError, Transport
from tests.conftest import FAKE_TRANSPORT_TOKEN, TRANSPORT_BASE

ORG_ID = "org-guid-0000-1111"
CITY_ID = "city-guid-aaaa"


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


@responses.activate
def test_get_token_returns_dict():
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/access_token",
        json=FAKE_TRANSPORT_TOKEN,
        status=200,
    )
    client = Transport(key="api-key")
    assert client.token() == FAKE_TRANSPORT_TOKEN
    assert client.token()["token"] == "transport-token-abc"


@responses.activate
def test_get_token_raises_on_empty_token():
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/access_token",
        json={"token": "", "correlationId": "x"},
        status=200,
    )
    with pytest.raises(IikoAuthError):
        Transport(key="bad-key")


@responses.activate
def test_get_token_raises_api_error_on_http_error():
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/access_token",
        status=401,
    )
    with pytest.raises(IikoAPIError) as exc_info:
        Transport(key="bad-key")
    assert exc_info.value.status_code == 401


@responses.activate
def test_pre_provided_token_skips_auth():
    client = Transport(token=FAKE_TRANSPORT_TOKEN)
    assert client.token() == FAKE_TRANSPORT_TOKEN
    assert len(responses.calls) == 0


# ---------------------------------------------------------------------------
# Organizations & infrastructure
# ---------------------------------------------------------------------------


@responses.activate
def test_organization(transport):
    responses.add(
        responses.GET,
        f"{TRANSPORT_BASE}/api/1/organizations",
        json={"organizations": []},
        status=200,
    )
    resp = transport.organization()
    assert resp.status_code == 200


@responses.activate
def test_organization_sends_bearer(transport):
    responses.add(
        responses.GET,
        f"{TRANSPORT_BASE}/api/1/organizations",
        json={},
        status=200,
    )
    transport.organization()
    auth_header = responses.calls[0].request.headers.get("Authorization", "")
    assert auth_header == f"Bearer {FAKE_TRANSPORT_TOKEN['token']}"


@responses.activate
def test_terminal(transport):
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/terminal_groups",
        json={"terminalGroups": []},
        status=200,
    )
    resp = transport.terminal(org_id=ORG_ID)
    assert resp.status_code == 200
    body = json.loads(responses.calls[0].request.body)
    assert body == {"organizationIds": [ORG_ID]}


@responses.activate
def test_cities(transport):
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/cities",
        json={"cities": []},
        status=200,
    )
    resp = transport.cities(org_id=ORG_ID)
    assert resp.status_code == 200
    body = json.loads(responses.calls[0].request.body)
    assert body == {"organizationIds": [ORG_ID]}


@responses.activate
def test_streets_by_city(transport):
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/streets/by_city",
        json={"streets": []},
        status=200,
    )
    resp = transport.streets_by_city(org_id=ORG_ID, city=CITY_ID)
    assert resp.status_code == 200
    body = json.loads(responses.calls[0].request.body)
    assert body == {"organizationId": ORG_ID, "cityId": CITY_ID}


# ---------------------------------------------------------------------------
# Deliveries
# ---------------------------------------------------------------------------


@responses.activate
def test_delivery_create(transport):
    order = {"organizationId": ORG_ID, "order": {"phone": "+7900"}}
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/deliveries/create",
        json={"orderInfo": {}},
        status=200,
    )
    resp = transport.delivery_create(order_info=order)
    assert resp.status_code == 200
    assert json.loads(responses.calls[0].request.body) == order


@responses.activate
def test_check_create_accepts_dict(transport):
    order = {"organizationId": ORG_ID}
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/deliveries/check_create",
        json={},
        status=200,
    )
    transport.check_create(order_info=order)
    assert json.loads(responses.calls[0].request.body) == order


@responses.activate
def test_check_create_accepts_json_string(transport):
    order = {"organizationId": ORG_ID}
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/deliveries/check_create",
        json={},
        status=200,
    )
    transport.check_create(order_info=json.dumps(order))
    assert json.loads(responses.calls[0].request.body) == order


@responses.activate
def test_by_id(transport):
    order_id = "order-guid-9999"
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/deliveries/by_id",
        json={},
        status=200,
    )
    transport.by_id(org_id=ORG_ID, order_id=order_id)
    body = json.loads(responses.calls[0].request.body)
    assert body == {"organizationId": ORG_ID, "orderIds": [order_id]}


@responses.activate
def test_by_revision(transport):
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/deliveries/by_revision",
        json={},
        status=200,
    )
    transport.by_revision(org_id=ORG_ID, revision="42")
    body = json.loads(responses.calls[0].request.body)
    assert body == {"startRevision": "42", "organizationIds": [ORG_ID]}


# ---------------------------------------------------------------------------
# HTTP error propagation
# ---------------------------------------------------------------------------


@responses.activate
def test_api_error_on_500(transport):
    responses.add(
        responses.GET,
        f"{TRANSPORT_BASE}/api/1/organizations",
        status=500,
    )
    with pytest.raises(IikoAPIError) as exc_info:
        transport.organization()
    assert exc_info.value.status_code == 500


# ---------------------------------------------------------------------------
# Regions
# ---------------------------------------------------------------------------


@responses.activate
def test_regions(transport):
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/regions",
        json={"regions": []},
        status=200,
    )
    resp = transport.regions(org_id=ORG_ID)
    assert resp.status_code == 200
    body = json.loads(responses.calls[0].request.body)
    assert body == {"organizationIds": [ORG_ID]}


# ---------------------------------------------------------------------------
# by_delivery_date
# ---------------------------------------------------------------------------


@responses.activate
def test_by_delivery_date(transport):
    date_from = "2024-01-01T00:00:00.000"
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/deliveries/by_delivery_date_and_status",
        json={},
        status=200,
    )
    transport.by_delivery_date(org_id=ORG_ID, delivery_date_from=date_from)
    body = json.loads(responses.calls[0].request.body)
    assert body == {"organizationId": [ORG_ID], "deliveryDateFrom": [date_from]}


# ---------------------------------------------------------------------------
# Context manager
# ---------------------------------------------------------------------------


@responses.activate
def test_context_manager():
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/access_token",
        json=FAKE_TRANSPORT_TOKEN,
        status=200,
    )
    with Transport(key="api-key") as client:
        assert client.token()["token"] == "transport-token-abc"
