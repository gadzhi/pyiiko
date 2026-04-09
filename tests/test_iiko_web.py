"""Unit tests for IikoWeb."""
import json

import pytest
import responses

from Pyiiko import IikoAPIError, IikoAuthError, IikoWeb
from tests.conftest import FAKE_WEB_TOKEN, WEB_BASE

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


@responses.activate
def test_get_token_returns_dict():
    responses.add(responses.POST, f"{WEB_BASE}/auth", json=FAKE_WEB_TOKEN, status=200)
    client = IikoWeb(api_key="test-api-key")
    assert client.token() == FAKE_WEB_TOKEN
    assert client.token()["token"] == "eyJtest.token.abc"


@responses.activate
def test_get_token_raises_on_empty_token():
    responses.add(
        responses.POST,
        f"{WEB_BASE}/auth",
        json={"token": "", "expires_in": 0},
        status=200,
    )
    with pytest.raises(IikoAuthError):
        IikoWeb(api_key="bad-key")


@responses.activate
def test_get_token_raises_api_error_on_http_error():
    responses.add(responses.POST, f"{WEB_BASE}/auth", status=401)
    with pytest.raises(IikoAPIError) as exc_info:
        IikoWeb(api_key="bad-key")
    assert exc_info.value.status_code == 401


@responses.activate
def test_pre_provided_token_skips_auth():
    client = IikoWeb(token=FAKE_WEB_TOKEN)
    assert client.token() == FAKE_WEB_TOKEN
    assert len(responses.calls) == 0


@responses.activate
def test_auth_request_sends_api_key():
    responses.add(responses.POST, f"{WEB_BASE}/auth", json=FAKE_WEB_TOKEN, status=200)
    IikoWeb(api_key="my-key")
    body = json.loads(responses.calls[0].request.body)
    assert body["api_key"] == "my-key"
    assert "app_id" not in body


@responses.activate
def test_auth_request_sends_optional_credentials():
    responses.add(responses.POST, f"{WEB_BASE}/auth", json=FAKE_WEB_TOKEN, status=200)
    IikoWeb(api_key="k", app_id="app1", client_secret="sec")
    body = json.loads(responses.calls[0].request.body)
    assert body["app_id"] == "app1"
    assert body["client_secret"] == "sec"


@responses.activate
def test_sends_bearer_header(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/entities/store/list",
        json={"stores": []},
        status=200,
    )
    web.stores()
    auth = responses.calls[-1].request.headers.get("Authorization", "")
    assert auth == f"Bearer {FAKE_WEB_TOKEN['token']}"


# ---------------------------------------------------------------------------
# Entities
# ---------------------------------------------------------------------------


@responses.activate
def test_stores(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/entities/store/list",
        json={"stores": []},
        status=200,
    )
    resp = web.stores()
    assert resp.status_code == 200


@responses.activate
def test_store_sends_id(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/entities/store/get",
        json={"store": {}},
        status=200,
    )
    web.store(42)
    body = json.loads(responses.calls[-1].request.body)
    assert body == {"id": 42}


@responses.activate
def test_products_empty_body_when_no_args(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/entities/products/list",
        json={"products": []},
        status=200,
    )
    web.products()
    body = json.loads(responses.calls[-1].request.body)
    assert body == {}


@responses.activate
def test_products_with_pagination(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/entities/products/list",
        json={"products": []},
        status=200,
    )
    web.products(limit=10, offset=20)
    body = json.loads(responses.calls[-1].request.body)
    assert body == {"limit": 10, "offset": 20}


@responses.activate
def test_product_categories(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/entities/product-category/list",
        json={},
        status=200,
    )
    assert web.product_categories().status_code == 200


@responses.activate
def test_product_sizes(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/entities/product-size/list",
        json={},
        status=200,
    )
    assert web.product_sizes().status_code == 200


@responses.activate
def test_users(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/entities/user/list",
        json={},
        status=200,
    )
    assert web.users().status_code == 200


@responses.activate
def test_payment_types(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/entities/payment-type/list",
        json={},
        status=200,
    )
    assert web.payment_types().status_code == 200


@responses.activate
def test_cash_flow_categories(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/entities/cash-flow-category/list",
        json={},
        status=200,
    )
    assert web.cash_flow_categories().status_code == 200


# ---------------------------------------------------------------------------
# Counteragents
# ---------------------------------------------------------------------------


@responses.activate
def test_counteragents_no_args(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/counteragents",
        json={},
        status=200,
    )
    web.counteragents()
    body = json.loads(responses.calls[-1].request.body)
    assert body == {}


@responses.activate
def test_counteragents_with_args(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/counteragents",
        json={},
        status=200,
    )
    web.counteragents(department_id="dept-guid", type=["supplier"], limit=50)
    body = json.loads(responses.calls[-1].request.body)
    assert body["departmentId"] == "dept-guid"
    assert body["type"] == ["supplier"]
    assert body["limit"] == 50


# ---------------------------------------------------------------------------
# Incoming invoice
# ---------------------------------------------------------------------------


@responses.activate
def test_incoming_invoice_export(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/incoming-invoice/export",
        json={},
        status=200,
    )
    web.incoming_invoice_export("dept-guid", "2024-01-01", "2024-01-31")
    body = json.loads(responses.calls[-1].request.body)
    assert body["departmentId"] == "dept-guid"
    assert body["dateFrom"] == "2024-01-01"


@responses.activate
def test_incoming_invoice_create(web):
    payload = {"departmentId": "dept-guid", "items": []}
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/incoming-invoice/create",
        json={},
        status=200,
    )
    web.incoming_invoice_create(payload)
    body = json.loads(responses.calls[-1].request.body)
    assert body == payload


# ---------------------------------------------------------------------------
# Document processing — spot checks
# ---------------------------------------------------------------------------


@responses.activate
def test_writeoff_create(web):
    payload = {"departmentId": "dept", "items": []}
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/writeoff-document/create",
        json={},
        status=200,
    )
    web.writeoff_create(payload)
    assert json.loads(responses.calls[-1].request.body) == payload


@responses.activate
def test_internal_transfer_create(web):
    payload = {"fromDepartmentId": "a", "toDepartmentId": "b"}
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/internal-transfer/create",
        json={},
        status=200,
    )
    web.internal_transfer_create(payload)
    assert json.loads(responses.calls[-1].request.body) == payload


@responses.activate
def test_production_doc_create(web):
    payload = {"departmentId": "dept"}
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/production-document/create-document",
        json={},
        status=200,
    )
    web.production_doc_create(payload)
    assert json.loads(responses.calls[-1].request.body) == payload


@responses.activate
def test_sales_doc_get(web):
    payload = {"id": "doc-guid"}
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/sales-document/get-document",
        json={},
        status=200,
    )
    web.sales_doc_get(payload)
    assert json.loads(responses.calls[-1].request.body) == payload


# ---------------------------------------------------------------------------
# Nomenclature
# ---------------------------------------------------------------------------


@responses.activate
def test_update_barcodes(web):
    payload = {"products": [{"id": "p1", "barcode": "123"}]}
    responses.add(
        responses.POST,
        f"{WEB_BASE}/nomenclature/update-barcodes",
        json={},
        status=200,
    )
    web.update_barcodes(payload)
    assert json.loads(responses.calls[-1].request.body) == payload


# ---------------------------------------------------------------------------
# Purchasing
# ---------------------------------------------------------------------------


@responses.activate
def test_order_create(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/purchasing/orders/create",
        json={"id": 1},
        status=200,
    )
    web.order_create(store_id=1, workflow_id=2, due_date="2024-02-01 10:00")
    body = json.loads(responses.calls[-1].request.body)
    assert body["storeId"] == 1
    assert body["workflowId"] == 2
    assert body["dueDate"] == "2024-02-01 10:00"
    assert "plannedDeliveryDate" not in body


@responses.activate
def test_order_create_with_delivery_date(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/purchasing/orders/create",
        json={"id": 1},
        status=200,
    )
    web.order_create(1, 2, "2024-02-01 10:00", planned_delivery_date="2024-02-03 10:00")
    body = json.loads(responses.calls[-1].request.body)
    assert body["plannedDeliveryDate"] == "2024-02-03 10:00"


@responses.activate
def test_order_get(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/purchasing/orders/get",
        json={},
        status=200,
    )
    web.order_get(99)
    assert json.loads(responses.calls[-1].request.body) == {"id": 99}


@responses.activate
def test_order_task_status(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/purchasing/orders/task-status",
        json={"status": "done"},
        status=200,
    )
    web.order_task_status("task-abc-123")
    assert json.loads(responses.calls[-1].request.body) == {"taskId": "task-abc-123"}


@responses.activate
def test_workflow_activate(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/purchasing/workflows/activate",
        json={},
        status=200,
    )
    web.workflow_activate(5)
    assert json.loads(responses.calls[-1].request.body) == {"id": 5}


@responses.activate
def test_workflow_deactivate(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/purchasing/workflows/deactivate",
        json={},
        status=200,
    )
    web.workflow_deactivate(5)
    assert json.loads(responses.calls[-1].request.body) == {"id": 5}


@responses.activate
def test_workflow_get(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/purchasing/workflows/get",
        json={},
        status=200,
    )
    web.workflow_get(3)
    assert json.loads(responses.calls[-1].request.body) == {"id": 3}


@responses.activate
def test_workflows_list_empty_body(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/purchasing/workflows/list",
        json={},
        status=200,
    )
    web.workflows_list()
    assert json.loads(responses.calls[-1].request.body) == {}


# ---------------------------------------------------------------------------
# HTTP error propagation
# ---------------------------------------------------------------------------


@responses.activate
def test_api_error_on_500(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/entities/store/list",
        status=500,
    )
    with pytest.raises(IikoAPIError) as exc_info:
        web.stores()
    assert exc_info.value.status_code == 500


# ---------------------------------------------------------------------------
# Document processing — additional coverage
# ---------------------------------------------------------------------------


@responses.activate
def test_incoming_invoice_pay(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/incoming-invoice/pay",
        json={},
        status=200,
    )
    web.incoming_invoice_pay({"invoiceId": "inv-1"})


@responses.activate
def test_incoming_invoice_set_payment_date(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/incoming-invoice/set-payment-date",
        json={},
        status=200,
    )
    web.incoming_invoice_set_payment_date({"invoiceId": "inv-1", "date": "2024-01-15"})


@responses.activate
def test_incoming_invoice_update(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/incoming-invoice/update",
        json={},
        status=200,
    )
    web.incoming_invoice_update({"id": "inv-1"})


@responses.activate
def test_incoming_invoice_export_by_number(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/incoming-invoice/export/by-number",
        json={},
        status=200,
    )
    web.incoming_invoice_export_by_number({"number": "INV-001"})


@responses.activate
def test_incoming_service_create(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/incoming-service/create-document",
        json={},
        status=200,
    )
    web.incoming_service_create({"departmentId": "dept"})


@responses.activate
def test_incoming_service_edit(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/incoming-service/edit-document",
        json={},
        status=200,
    )
    web.incoming_service_edit({"id": "doc-1"})


@responses.activate
def test_incoming_service_export(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/incoming-service/export",
        json={},
        status=200,
    )
    web.incoming_service_export({"departmentId": "dept"})


@responses.activate
def test_incoming_service_get(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/incoming-service/get-document",
        json={},
        status=200,
    )
    web.incoming_service_get({"id": "doc-1"})


@responses.activate
def test_internal_transfer_edit(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/internal-transfer/edit",
        json={},
        status=200,
    )
    web.internal_transfer_edit({"id": "doc-1"})


@responses.activate
def test_internal_transfer_export(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/internal-transfer/export",
        json={},
        status=200,
    )
    web.internal_transfer_export({"departmentId": "dept"})


@responses.activate
def test_internal_transfer_get_by_id(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/internal-transfer/export/by-id",
        json={},
        status=200,
    )
    web.internal_transfer_get_by_id({"id": "doc-1"})


@responses.activate
def test_internal_transfer_export_by_number(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/internal-transfer/export/by-number",
        json={},
        status=200,
    )
    web.internal_transfer_export_by_number({"number": "IT-001"})


@responses.activate
def test_outgoing_invoice_create(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/outgoing-invoice/create",
        json={},
        status=200,
    )
    web.outgoing_invoice_create({"departmentId": "dept"})


@responses.activate
def test_outgoing_invoice_export(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/outgoing-invoice/export",
        json={},
        status=200,
    )
    web.outgoing_invoice_export({"departmentId": "dept"})


@responses.activate
def test_outgoing_invoice_export_by_number(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/outgoing-invoice/export/by-number",
        json={},
        status=200,
    )
    web.outgoing_invoice_export_by_number({"number": "OI-001"})


@responses.activate
def test_outgoing_invoice_cost_prices(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/outgoing-invoice/get-cost-prices",
        json={},
        status=200,
    )
    web.outgoing_invoice_cost_prices({"invoiceId": "inv-1"})


@responses.activate
def test_outgoing_invoice_pay(web):
    responses.add(
        responses.POST, f"{WEB_BASE}/document-processing/outgoing-invoice/pay", json={}, status=200
    )
    web.outgoing_invoice_pay({"invoiceId": "inv-1"})


@responses.activate
def test_outgoing_invoice_set_payment_date(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/outgoing-invoice/set-payment-date",
        json={},
        status=200,
    )
    web.outgoing_invoice_set_payment_date({"invoiceId": "inv-1", "date": "2024-01-15"})


@responses.activate
def test_outgoing_invoice_update(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/outgoing-invoice/update",
        json={},
        status=200,
    )
    web.outgoing_invoice_update({"id": "inv-1"})


@responses.activate
def test_outgoing_service_create(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/outgoing-service/create-document",
        json={},
        status=200,
    )
    web.outgoing_service_create({"departmentId": "dept"})


@responses.activate
def test_outgoing_service_edit(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/outgoing-service/edit-document",
        json={},
        status=200,
    )
    web.outgoing_service_edit({"id": "doc-1"})


@responses.activate
def test_outgoing_service_export(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/outgoing-service/export",
        json={},
        status=200,
    )
    web.outgoing_service_export({"departmentId": "dept"})


@responses.activate
def test_outgoing_service_get(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/outgoing-service/get-document",
        json={},
        status=200,
    )
    web.outgoing_service_get({"id": "doc-1"})


@responses.activate
def test_production_doc_edit(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/production-document/edit-document",
        json={},
        status=200,
    )
    web.production_doc_edit({"id": "doc-1"})


@responses.activate
def test_production_doc_export(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/production-document/export",
        json={},
        status=200,
    )
    web.production_doc_export({"departmentId": "dept"})


@responses.activate
def test_production_doc_get(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/production-document/get-document",
        json={},
        status=200,
    )
    web.production_doc_get({"id": "doc-1"})


@responses.activate
def test_sales_doc_create(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/sales-document/create-document",
        json={},
        status=200,
    )
    web.sales_doc_create({"departmentId": "dept"})


@responses.activate
def test_sales_doc_edit(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/sales-document/edit-document",
        json={},
        status=200,
    )
    web.sales_doc_edit({"id": "doc-1"})


@responses.activate
def test_sales_doc_export(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/sales-document/export",
        json={},
        status=200,
    )
    web.sales_doc_export({"departmentId": "dept"})


@responses.activate
def test_writeoff_edit(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/writeoff-document/edit",
        json={},
        status=200,
    )
    web.writeoff_edit({"id": "doc-1"})


@responses.activate
def test_writeoff_export(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/writeoff-document/export",
        json={},
        status=200,
    )
    web.writeoff_export({"departmentId": "dept"})


@responses.activate
def test_writeoff_get_by_id(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/writeoff-document/export/by-id",
        json={},
        status=200,
    )
    web.writeoff_get_by_id({"id": "doc-1"})


@responses.activate
def test_writeoff_export_by_number(web):
    responses.add(
        responses.POST,
        f"{WEB_BASE}/document-processing/writeoff-document/export/by-number",
        json={},
        status=200,
    )
    web.writeoff_export_by_number({"number": "WO-001"})


@responses.activate
def test_orders_list(web):
    responses.add(
        responses.POST, f"{WEB_BASE}/purchasing/orders/list", json={}, status=200
    )
    web.orders_list({"storeId": 1})


@responses.activate
def test_order_add_products(web):
    responses.add(
        responses.POST, f"{WEB_BASE}/purchasing/orders/products/add", json={}, status=200
    )
    web.order_add_products({"orderId": 1, "products": []})


@responses.activate
def test_order_select_supplier(web):
    responses.add(
        responses.POST, f"{WEB_BASE}/purchasing/orders/supplier/select", json={}, status=200
    )
    web.order_select_supplier({"orderId": 1, "supplierId": 2})


@responses.activate
def test_order_select_units(web):
    responses.add(
        responses.POST, f"{WEB_BASE}/purchasing/orders/units/select", json={}, status=200
    )
    web.order_select_units({"orderId": 1})


# ---------------------------------------------------------------------------
# Context manager
# ---------------------------------------------------------------------------


@responses.activate
def test_context_manager():
    responses.add(responses.POST, f"{WEB_BASE}/auth", json=FAKE_WEB_TOKEN, status=200)
    with IikoWeb(api_key="test-key") as client:
        assert client.token()["token"] == FAKE_WEB_TOKEN["token"]
