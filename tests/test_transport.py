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
def test_v2_auth_sends_application_credentials():
    route = responses.post(f"{TRANSPORT_BASE}/api/v2/access_token", json=FAKE_TRANSPORT_TOKEN)
    client = Transport("api-key", app_id="app-id", client_secret="app-secret")
    assert client.token() == FAKE_TRANSPORT_TOKEN
    assert route.call_count == 1
    assert json.loads(route.calls[0].request.body) == {
        "appId": "app-id",
        "clientSecret": "app-secret",
        "apiKey": "api-key",
    }


@responses.activate
def test_incomplete_v2_auth_fails_without_sending_request():
    with pytest.raises(IikoAuthError, match="both app_id and client_secret"):
        Transport("api-key", app_id="app-id")
    assert not responses.calls


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
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/organizations",
        json={"organizations": []},
        status=200,
    )
    resp = transport.organization()
    assert resp.status_code == 200
    assert json.loads(responses.calls[0].request.body) == {}


@responses.activate
def test_organization_sends_bearer(transport):
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/organizations",
        json={},
        status=200,
    )
    transport.organization()
    auth_header = responses.calls[0].request.headers.get("Authorization", "")
    assert auth_header == f"Bearer {FAKE_TRANSPORT_TOKEN['token']}"


@pytest.mark.parametrize(("include", "expected"), [("false", False), ("true", True), (True, True)])
@responses.activate
def test_terminal(transport, include, expected):
    responses.add(
        responses.POST,
        f"{TRANSPORT_BASE}/api/1/terminal_groups",
        json={"terminalGroups": []},
        status=200,
    )
    resp = transport.terminal(ORG_ID, include)
    assert resp.status_code == 200
    body = json.loads(responses.calls[0].request.body)
    assert body == {"organizationIds": [ORG_ID], "includeDisabled": expected}


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
def test_api_error_on_500(transport, monkeypatch):
    monkeypatch.setattr("Pyiiko._base.sleep", lambda delay: None)
    responses.add(
        responses.POST,
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
    transport.by_delivery_date(
        ORG_ID, date_from, delivery_date_to="2024-01-02T00:00:00.000", statuses=["Closed"]
    )
    body = json.loads(responses.calls[0].request.body)
    assert body == {
        "organizationIds": [ORG_ID],
        "deliveryDateFrom": "2024-01-01 00:00:00.000",
        "deliveryDateTo": "2024-01-02 00:00:00.000",
        "statuses": ["Closed"],
    }


@responses.activate
def test_by_delivery_date_rejects_missing_arguments(transport):
    with pytest.raises(ValueError, match="org_id and delivery_date_from"):
        transport.by_delivery_date(ORG_ID)
    assert not responses.calls


@responses.activate
def test_read_only_post_retries(transport):
    url = f"{TRANSPORT_BASE}/api/1/organizations"
    responses.post(url, status=503)
    responses.post(url, json={"organizations": []})
    assert transport.organization().json() == {"organizations": []}
    assert len(responses.calls) == 2


@pytest.mark.parametrize("status", [429, 503])
@responses.activate
def test_read_only_post_respects_retry_after(transport, monkeypatch, status):
    url = f"{TRANSPORT_BASE}/api/1/organizations"
    responses.post(url, status=status, headers={"Retry-After": "5"})
    responses.post(url, json={"organizations": []})
    delays = []
    monkeypatch.setattr("Pyiiko._base.sleep", delays.append)
    assert transport.organization().json() == {"organizations": []}
    assert len(responses.calls) == 2
    assert delays == [5]


@responses.activate
def test_long_retry_after_is_left_to_caller(transport):
    url = f"{TRANSPORT_BASE}/api/1/organizations"
    route = responses.post(url, status=503, headers={"Retry-After": "120"})
    with pytest.raises(IikoAPIError) as exc_info:
        transport.organization()
    assert exc_info.value.status_code == 503
    assert route.call_count == 1


@responses.activate
def test_delivery_create_does_not_retry(transport):
    route = responses.post(f"{TRANSPORT_BASE}/api/1/deliveries/create", status=503)
    with pytest.raises(IikoAPIError) as exc_info:
        transport.delivery_create({"organizationId": ORG_ID})
    assert exc_info.value.status_code == 503
    assert route.call_count == 1


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
