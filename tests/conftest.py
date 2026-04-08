"""Shared pytest fixtures."""
import pytest
import responses as responses_lib

SERVER_URL = "http://iiko-test.local:8080"
SERVER_BASE = f"{SERVER_URL}/resto"
TRANSPORT_BASE = "https://api-ru.iiko.services"

FAKE_TOKEN = "deadbeef-1234-5678-abcd-000000000000"
FAKE_TRANSPORT_TOKEN = {"token": "transport-token-abc", "correlationId": "corr-1"}


@pytest.fixture
def mocked_responses():
    """Activate responses mock for the duration of a test."""
    with responses_lib.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps


@pytest.fixture
def server(mocked_responses):
    """IikoServer instance with mocked auth."""
    from Pyiiko import IikoServer

    mocked_responses.add(
        responses_lib.GET,
        f"{SERVER_BASE}/api/auth",
        body=FAKE_TOKEN,
        status=200,
    )
    return IikoServer(ip=SERVER_URL, login="user", password="sha1hash")


@pytest.fixture
def transport(mocked_responses):
    """Transport instance with mocked auth."""
    from Pyiiko import Transport

    mocked_responses.add(
        responses_lib.POST,
        f"{TRANSPORT_BASE}/api/1/access_token",
        json=FAKE_TRANSPORT_TOKEN,
        status=200,
    )
    return Transport(key="api-login-key")
