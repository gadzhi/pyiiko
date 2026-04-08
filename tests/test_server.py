"""Unit tests for IikoServer."""
import pytest
import responses

from Pyiiko import IikoAPIError, IikoAuthError, IikoServer
from tests.conftest import FAKE_TOKEN, SERVER_BASE, SERVER_URL

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


# ---------------------------------------------------------------------------
# Corporation — remaining methods
# ---------------------------------------------------------------------------


@responses.activate
def test_groups(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/corporation/groups",
        body=b"<groups/>",
        status=200,
    )
    assert server.groups() == b"<groups/>"


@responses.activate
def test_terminals(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/corporation/terminals",
        body=b"<terminals/>",
        status=200,
    )
    assert server.terminals() == b"<terminals/>"


@responses.activate
def test_departments_find(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/corporation/departments/search",
        body=b"<dep/>",
        status=200,
    )
    result = server.departments_find("DEPT-001")
    assert result == b"<dep/>"
    assert "departmentCode=DEPT-001" in responses.calls[0].request.url


@responses.activate
def test_stores_find(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/corporation/stores/search",
        body=b"<store/>",
        status=200,
    )
    result = server.stores_find("STR-01")
    assert result == b"<store/>"
    assert "storeCode=STR-01" in responses.calls[0].request.url


@responses.activate
def test_groups_search(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/corporation/groups/search",
        body=b"<groups/>",
        status=200,
    )
    result = server.groups_search(name="Main")
    assert result == b"<groups/>"
    assert "name=Main" in responses.calls[0].request.url


# ---------------------------------------------------------------------------
# Employees & events
# ---------------------------------------------------------------------------


@responses.activate
def test_employees(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/employees",
        body=b"<employees/>",
        status=200,
    )
    assert server.employees() == b"<employees/>"


@responses.activate
def test_events(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/events",
        body=b"<events/>",
        status=200,
    )
    result = server.events(from_time="2024-01-01T00:00:00.000")
    assert result == b"<events/>"
    assert "from_time=2024-01-01" in responses.calls[0].request.url


@responses.activate
def test_events_filter(server):
    xml_body = b"<eventsRequestData><events><event>orderPaid</event></events></eventsRequestData>"
    responses.add(
        responses.POST,
        f"{SERVER_BASE}/api/events",
        body=b"<result/>",
        status=200,
    )
    result = server.events_filter(xml_body)
    assert result == b"<result/>"
    assert responses.calls[0].request.body == xml_body


@responses.activate
def test_events_meta(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/events/metadata",
        body=b"<meta/>",
        status=200,
    )
    assert server.events_meta() == b"<meta/>"


# ---------------------------------------------------------------------------
# Products — find
# ---------------------------------------------------------------------------


@responses.activate
def test_products_find(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/products/search/",
        body=b"<products/>",
        status=200,
    )
    result = server.products_find(name="Burger", productType="DISH")
    assert result == b"<products/>"
    url = responses.calls[0].request.url
    assert "name=Burger" in url
    assert "productType=DISH" in url


# ---------------------------------------------------------------------------
# Suppliers
# ---------------------------------------------------------------------------


@responses.activate
def test_suppliers(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/suppliers",
        body=b"<suppliers/>",
        status=200,
    )
    assert server.suppliers() == b"<suppliers/>"


@responses.activate
def test_suppliers_find_with_params(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/suppliers",
        body=b"<suppliers/>",
        status=200,
    )
    server.suppliers_find(name="Acme")
    assert "name=Acme" in responses.calls[0].request.url


@responses.activate
def test_suppliers_find_empty_params_omitted(server):
    """Empty strings must not appear as name= or code= in the URL."""
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/suppliers",
        body=b"<suppliers/>",
        status=200,
    )
    server.suppliers_find()
    url = responses.calls[0].request.url
    assert "name=" not in url
    assert "code=" not in url


@responses.activate
def test_suppliers_price(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/suppliers/supplier-guid/pricelist",
        body=b"<price/>",
        status=200,
    )
    result = server.suppliers_price("supplier-guid", date="01.01.2024")
    assert result == b"<price/>"
    assert "date=01.01.2024" in responses.calls[0].request.url


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------


@responses.activate
def test_store_operation(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/reports/storeOperations",
        body=b"<report/>",
        status=200,
    )
    result = server.store_operation(stores="store-guid", presetId="preset-guid")
    assert result == b"<report/>"
    url = responses.calls[0].request.url
    assert "stores=store-guid" in url
    assert "presetId=preset-guid" in url


@responses.activate
def test_store_operation_filters_none_params(server):
    """None values must not appear as query params."""
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/reports/storeOperations",
        body=b"<report/>",
        status=200,
    )
    server.store_operation()
    url = responses.calls[0].request.url
    assert "stores=" not in url
    assert "presetId=" not in url


@responses.activate
def test_store_presets(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/reports/storeReportPresets",
        body=b"<presets/>",
        status=200,
    )
    assert server.store_presets() == b"<presets/>"


@responses.activate
def test_product_expense(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/reports/productExpense",
        body=b"<report/>",
        status=200,
    )
    result = server.product_expense("dept-guid", dateFrom="01.01.2024", dateTo="31.01.2024")
    assert result == b"<report/>"
    url = responses.calls[0].request.url
    assert "department=dept-guid" in url
    assert "dateFrom=01.01.2024" in url


@responses.activate
def test_sales(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/reports/sales",
        body=b"<report/>",
        status=200,
    )
    result = server.sales("dept-guid", dishDetails=True, allRevenue=False)
    assert result == b"<report/>"
    url = responses.calls[0].request.url
    assert "department=dept-guid" in url
    assert "dishDetails=True" in url


@responses.activate
def test_mounthly_plan(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/reports/monthlyIncomePlan",
        body=b"<plan/>",
        status=200,
    )
    result = server.mounthly_plan("dept-guid", dateFrom="01.01.2024")
    assert result == b"<plan/>"
    assert "department=dept-guid" in responses.calls[0].request.url


@responses.activate
def test_ingredient_entry(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/reports/ingredientEntry",
        body=b"<report/>",
        status=200,
    )
    result = server.ingredient_entry("dept-guid", includeSubtree=True)
    assert result == b"<report/>"
    url = responses.calls[0].request.url
    assert "department=dept-guid" in url
    assert "includeSubtree=True" in url


@responses.activate
def test_reports_balance(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/reports/balance/counteragents",
        json={"balances": []},
        status=200,
    )
    result = server.reports_balance("2024-01-31T23:59:59", account="acc-guid")
    assert result == {"balances": []}
    url = responses.calls[0].request.url
    assert "timestamp=2024-01-31" in url
    assert "account=acc-guid" in url


@responses.activate
def test_reports_balance_none_params_omitted(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/reports/balance/counteragents",
        json={},
        status=200,
    )
    server.reports_balance("2024-01-01T00:00:00")
    url = responses.calls[0].request.url
    assert "account=" not in url
    assert "counteragent=" not in url


# ---------------------------------------------------------------------------
# Invoices
# ---------------------------------------------------------------------------


@responses.activate
def test_invoice_in(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/documents/export/incomingInvoice",
        body=b"<invoice/>",
        status=200,
    )
    result = server.invoice_in(**{"from": "2024-01-01", "to": "2024-01-31"})
    assert result == b"<invoice/>"
    url = responses.calls[0].request.url
    assert "from=2024-01-01" in url


@responses.activate
def test_invoice_out(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/documents/export/outgoingInvoice",
        body=b"<invoice/>",
        status=200,
    )
    result = server.invoice_out(**{"from": "2024-01-01", "to": "2024-01-31"})
    assert result == b"<invoice/>"


@responses.activate
def test_invoice_number_out_current_year_param(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/documents/export/outgoingInvoice/byNumber",
        body=b"<invoice/>",
        status=200,
    )
    server.invoice_number_out(current_year=True, number="OUT-001")
    assert "currentYear=true" in responses.calls[0].request.url


@responses.activate
def test_production_doc(server):
    xml = b"<productionDocument/>"
    responses.add(
        responses.POST,
        f"{SERVER_BASE}/api/documents/import/productionDocument",
        body=b"OK",
        status=200,
    )
    result = server.production_doc(xml)
    assert result == b"OK"
    assert responses.calls[0].request.body == xml
    assert responses.calls[0].request.headers["Content-type"] == "text/xml"


# ---------------------------------------------------------------------------
# Cash register sessions
# ---------------------------------------------------------------------------


@responses.activate
def test_close_session(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/closeSession/list",
        body=b"<sessions/>",
        status=200,
    )
    result = server.close_session(dateFrom="01.01.2024", dateTo="31.01.2024")
    assert result == b"<sessions/>"
    url = responses.calls[0].request.url
    assert "dateFrom=01.01.2024" in url
    assert "dateTo=31.01.2024" in url


@responses.activate
def test_session(server):
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/api/events/sessions",
        body=b"<sessions/>",
        status=200,
    )
    result = server.session(from_time="2024-01-01T00:00:00.000", to_time="2024-01-02T00:00:00.000")
    assert result == b"<sessions/>"
    url = responses.calls[0].request.url
    assert "from=2024-01-01" in url
    assert "to=2024-01-02" in url


# ---------------------------------------------------------------------------
# EDI
# ---------------------------------------------------------------------------


@responses.activate
def test_edi(server):
    edi_guid = "edi-system-guid"
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/edi/{edi_guid}/orders/bySeller",
        body=b"<orders/>",
        status=200,
    )
    result = server.edi(edi_guid, gln="1234567890123", inn="7700000000")
    assert result == b"<orders/>"
    url = responses.calls[0].request.url
    assert "gln=1234567890123" in url
    assert "inn=7700000000" in url


@responses.activate
def test_edi_none_params_omitted(server):
    edi_guid = "edi-system-guid"
    responses.add(
        responses.GET,
        f"{SERVER_BASE}/edi/{edi_guid}/orders/bySeller",
        body=b"<orders/>",
        status=200,
    )
    server.edi(edi_guid)
    url = responses.calls[0].request.url
    assert "gln=" not in url
    assert "inn=" not in url
