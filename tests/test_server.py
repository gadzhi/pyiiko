"""Unit tests for IikoServer."""
import pytest
import responses

from Pyiiko import IikoServer, IikoAPIError, IikoAuthError
from tests.conftest import SERVER_BASE, SERVER_URL, FAKE_TOKEN


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


@responses.activate
def test_get_token_returns_token():
    responses.add(responses.GET, f"{SERVER_BASE}/api/auth", body=FAKE_TOKEN, status=200)
    server = IikoServer(ip=SERVER_URL, login="user", password="pass")
    assert server.token() == FAKE_TOKEN


@responses.activate
def test_get_token_raises_on_empty_body():
    responses.add(responses.GET, f"{SERVER_BASE}/api/auth", body="", status=200)
    with pytest.raises(IikoAuthError):
        IikoServer(ip=SERVER_URL, login="user", password="pass")


@responses.activate
def test_get_token_raises_api_error_on_http_error():
    responses.add(responses.GET, f"{SERVER_BASE}/api/auth", status=401)
    with pytest.raises(IikoAPIError) as exc_info:
        IikoServer(ip=SERVER_URL, login="user", password="bad")
    assert exc_info.value.status_code == 401


@responses.activate
def test_pre_provided_token_skips_auth(mocked_responses):
    # No auth endpoint registered — passing token directly must not call it
    server = IikoServer(ip=SERVER_URL, token=FAKE_TOKEN)
    assert server.token() == FAKE_TOKEN
    assert len(responses.calls) == 0


@responses.activate
def test_quit_token(server):
    responses.add(responses.GET, f"{SERVER_BASE}/api/logout", status=200)
    server.quit_token()  # should not raise


# ---------------------------------------------------------------------------
# Server info
# ---------------------------------------------------------------------------

_SERVER_INFO_XML = b"<r><version>7.8.9</version></r>"


@responses.activate
def test_version(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/get_server_info.jsp",
        body=_SERVER_INFO_XML,
        status=200,
    )
    assert server.version() == "7.8.9"


@responses.activate
def test_server_info(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/get_server_info.jsp",
        json={"version": "7.8.9"},
        status=200,
    )
    info = server.server_info()
    assert info["version"] == "7.8.9"


# ---------------------------------------------------------------------------
# Corporations
# ---------------------------------------------------------------------------


@responses.activate
def test_departments(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/corporation/departments",
        body=b"<departments/>",
        status=200,
    )
    result = server.departments()
    assert result == b"<departments/>"


@responses.activate
def test_departments_passes_key(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/corporation/departments",
        body=b"<departments/>",
        status=200,
    )
    server.departments()
    assert f"key={FAKE_TOKEN}" in responses.calls[0].request.url


@responses.activate
def test_stores(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/corporation/stores",
        body="<stores/>",
        status=200,
    )
    assert server.stores() == "<stores/>"


@responses.activate
def test_terminals_search_boolean_param(server):
    """anonymous param must be sent as lowercase string, not Python bool."""
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/corporation/terminal/search",
        body=b"<terminals/>",
        status=200,
    )
    server.terminals_search(anonymous=True)
    assert "anonymous=true" in responses.calls[0].request.url


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------


@responses.activate
def test_products(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/products",
        body=b"<products/>",
        status=200,
    )
    result = server.products(includeDeleted=False)
    assert result == b"<products/>"
    assert "includeDeleted=false" in responses.calls[0].request.url


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------


@responses.activate
def test_olap(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/reports/olap",
        body="<report/>",
        status=200,
    )
    result = server.olap(report="SALES", data_from="2024-01-01", data_to="2024-01-31")
    assert result == "<report/>"
    url = responses.calls[0].request.url
    assert "report=SALES" in url
    assert "from=2024-01-01" in url
    assert "to=2024-01-31" in url


@responses.activate
def test_olap2(server):
    body = {"reportType": "SALES", "groupByRowFields": ["Department"]}
    responses.add(
        responses.POST,
        f"{SERVER_BASE}/api/v2/reports/olap",
        json={"data": []},
        status=200,
    )
    result = server.olap2(body)
    assert result == {"data": []}


# ---------------------------------------------------------------------------
# Invoices
# ---------------------------------------------------------------------------


@responses.activate
def test_invoice_number_in_current_year_param(server):
    """currentYear must be sent as lowercase string."""
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/documents/export/incomingInvoice/byNumber",
        body=b"<invoice/>",
        status=200,
    )
    server.invoice_number_in(current_year=False, number="INV-001")
    assert "currentYear=false" in responses.calls[0].request.url


# ---------------------------------------------------------------------------
# HTTP error propagation
# ---------------------------------------------------------------------------


@responses.activate
def test_api_error_on_500(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/corporation/departments",
        status=500,
    )
    with pytest.raises(IikoAPIError) as exc_info:
        server.departments()
    assert exc_info.value.status_code == 500


@responses.activate
def test_api_error_on_403(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/corporation/stores",
        status=403,
    )
    with pytest.raises(IikoAPIError) as exc_info:
        server.stores()
    assert exc_info.value.status_code == 403


# ---------------------------------------------------------------------------
# Context manager
# ---------------------------------------------------------------------------


@responses.activate
def test_context_manager():
    responses.add(responses.GET, f"{SERVER_BASE}/api/auth", body=FAKE_TOKEN, status=200)
    with IikoServer(ip=SERVER_URL, login="user", password="pass") as server:
        assert server.token() == FAKE_TOKEN
