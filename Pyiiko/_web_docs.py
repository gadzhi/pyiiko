"""Document-processing mixin for IikoWeb — keeps iiko_web.py under 400 lines."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import requests


class _DocsMixin:
    """Mixin providing all document-processing endpoints for IikoWeb."""

    if TYPE_CHECKING:
        def _post(self, path: str, **kwargs: Any) -> requests.Response: ...

    def _auth(self) -> dict[str, str]:  # satisfied by IikoWeb
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Counteragents
    # ------------------------------------------------------------------

    def counteragents(
        self,
        department_id: Any = None,
        type: Any = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """Return the list of counteragents.

        :param department_id: Department identifier (optional).
        :param type: Counteragent type filter (optional).
        :param limit: Maximum number of records to return (optional).
        :param offset: Number of records to skip (optional).
        """
        body = {
            k: v
            for k, v in {
                "departmentId": department_id,
                "type": type,
                "limit": limit,
                "offset": offset,
            }.items()
            if v is not None
        }
        return self._post(
            "document-processing/counteragents",
            headers=self._auth(),
            json=body,
        )

    # ------------------------------------------------------------------
    # Incoming invoice
    # ------------------------------------------------------------------

    def incoming_invoice_create(self, payload: dict) -> Any:
        """Create an incoming invoice document.

        :param payload: Incoming invoice creation payload.
        """
        return self._post(
            "document-processing/incoming-invoice/create",
            headers=self._auth(),
            json=payload,
        )

    def incoming_invoice_export(
        self,
        department_id: Any,
        date_from: str,
        date_to: str,
        supplier_id: Any = None,
        revision_from: Any = None,
    ) -> Any:
        """Export incoming invoices filtered by department and date range.

        :param department_id: Department identifier.
        :param date_from: Start date (ISO string).
        :param date_to: End date (ISO string).
        :param supplier_id: Supplier identifier (optional).
        :param revision_from: Starting revision number (optional).
        """
        body = {
            k: v
            for k, v in {
                "departmentId": department_id,
                "dateFrom": date_from,
                "dateTo": date_to,
                "supplierId": supplier_id,
                "revisionFrom": revision_from,
            }.items()
            if v is not None
        }
        return self._post(
            "document-processing/incoming-invoice/export",
            headers=self._auth(),
            json=body,
        )

    def incoming_invoice_export_by_number(self, payload: dict) -> Any:
        """Export an incoming invoice by document number.

        :param payload: Query payload containing document number.
        """
        return self._post(
            "document-processing/incoming-invoice/export/by-number",
            headers=self._auth(),
            json=payload,
        )

    def incoming_invoice_pay(self, payload: dict) -> Any:
        """Mark an incoming invoice as paid.

        :param payload: Payment payload.
        """
        return self._post(
            "document-processing/incoming-invoice/pay",
            headers=self._auth(),
            json=payload,
        )

    def incoming_invoice_set_payment_date(self, payload: dict) -> Any:
        """Set the payment date on an incoming invoice.

        :param payload: Payload containing invoice ID and payment date.
        """
        return self._post(
            "document-processing/incoming-invoice/set-payment-date",
            headers=self._auth(),
            json=payload,
        )

    def incoming_invoice_update(self, payload: dict) -> Any:
        """Update an existing incoming invoice.

        :param payload: Updated invoice data.
        """
        return self._post(
            "document-processing/incoming-invoice/update",
            headers=self._auth(),
            json=payload,
        )

    # ------------------------------------------------------------------
    # Incoming service
    # ------------------------------------------------------------------

    def incoming_service_create(self, payload: dict) -> Any:
        """Create an incoming service document.

        :param payload: Incoming service creation payload.
        """
        return self._post(
            "document-processing/incoming-service/create-document",
            headers=self._auth(),
            json=payload,
        )

    def incoming_service_edit(self, payload: dict) -> Any:
        """Edit an existing incoming service document.

        :param payload: Updated incoming service data.
        """
        return self._post(
            "document-processing/incoming-service/edit-document",
            headers=self._auth(),
            json=payload,
        )

    def incoming_service_export(self, payload: dict) -> Any:
        """Export incoming service documents.

        :param payload: Export filter payload.
        """
        return self._post(
            "document-processing/incoming-service/export",
            headers=self._auth(),
            json=payload,
        )

    def incoming_service_get(self, payload: dict) -> Any:
        """Retrieve a single incoming service document.

        :param payload: Query payload.
        """
        return self._post(
            "document-processing/incoming-service/get-document",
            headers=self._auth(),
            json=payload,
        )

    # ------------------------------------------------------------------
    # Internal transfer
    # ------------------------------------------------------------------

    def internal_transfer_create(self, payload: dict) -> Any:
        """Create an internal transfer document.

        :param payload: Internal transfer creation payload.
        """
        return self._post(
            "document-processing/internal-transfer/create",
            headers=self._auth(),
            json=payload,
        )

    def internal_transfer_edit(self, payload: dict) -> Any:
        """Edit an existing internal transfer document.

        :param payload: Updated internal transfer data.
        """
        return self._post(
            "document-processing/internal-transfer/edit",
            headers=self._auth(),
            json=payload,
        )

    def internal_transfer_export(self, payload: dict) -> Any:
        """Export internal transfer documents.

        :param payload: Export filter payload.
        """
        return self._post(
            "document-processing/internal-transfer/export",
            headers=self._auth(),
            json=payload,
        )

    def internal_transfer_get_by_id(self, payload: dict) -> Any:
        """Retrieve an internal transfer document by ID.

        :param payload: Query payload containing document ID.
        """
        return self._post(
            "document-processing/internal-transfer/export/by-id",
            headers=self._auth(),
            json=payload,
        )

    def internal_transfer_export_by_number(self, payload: dict) -> Any:
        """Export an internal transfer document by document number.

        :param payload: Query payload containing document number.
        """
        return self._post(
            "document-processing/internal-transfer/export/by-number",
            headers=self._auth(),
            json=payload,
        )

    # ------------------------------------------------------------------
    # Outgoing invoice
    # ------------------------------------------------------------------

    def outgoing_invoice_create(self, payload: dict) -> Any:
        """Create an outgoing invoice document.

        :param payload: Outgoing invoice creation payload.
        """
        return self._post(
            "document-processing/outgoing-invoice/create",
            headers=self._auth(),
            json=payload,
        )

    def outgoing_invoice_export(self, payload: dict) -> Any:
        """Export outgoing invoice documents.

        :param payload: Export filter payload.
        """
        return self._post(
            "document-processing/outgoing-invoice/export",
            headers=self._auth(),
            json=payload,
        )

    def outgoing_invoice_export_by_number(self, payload: dict) -> Any:
        """Export an outgoing invoice by document number.

        :param payload: Query payload containing document number.
        """
        return self._post(
            "document-processing/outgoing-invoice/export/by-number",
            headers=self._auth(),
            json=payload,
        )

    def outgoing_invoice_cost_prices(self, payload: dict) -> Any:
        """Retrieve cost prices for an outgoing invoice.

        :param payload: Query payload.
        """
        return self._post(
            "document-processing/outgoing-invoice/get-cost-prices",
            headers=self._auth(),
            json=payload,
        )

    def outgoing_invoice_pay(self, payload: dict) -> Any:
        """Mark an outgoing invoice as paid.

        :param payload: Payment payload.
        """
        return self._post(
            "document-processing/outgoing-invoice/pay",
            headers=self._auth(),
            json=payload,
        )

    def outgoing_invoice_set_payment_date(self, payload: dict) -> Any:
        """Set the payment date on an outgoing invoice.

        :param payload: Payload containing invoice ID and payment date.
        """
        return self._post(
            "document-processing/outgoing-invoice/set-payment-date",
            headers=self._auth(),
            json=payload,
        )

    def outgoing_invoice_update(self, payload: dict) -> Any:
        """Update an existing outgoing invoice.

        :param payload: Updated invoice data.
        """
        return self._post(
            "document-processing/outgoing-invoice/update",
            headers=self._auth(),
            json=payload,
        )

    # ------------------------------------------------------------------
    # Outgoing service
    # ------------------------------------------------------------------

    def outgoing_service_create(self, payload: dict) -> Any:
        """Create an outgoing service document.

        :param payload: Outgoing service creation payload.
        """
        return self._post(
            "document-processing/outgoing-service/create-document",
            headers=self._auth(),
            json=payload,
        )

    def outgoing_service_edit(self, payload: dict) -> Any:
        """Edit an existing outgoing service document.

        :param payload: Updated outgoing service data.
        """
        return self._post(
            "document-processing/outgoing-service/edit-document",
            headers=self._auth(),
            json=payload,
        )

    def outgoing_service_export(self, payload: dict) -> Any:
        """Export outgoing service documents.

        :param payload: Export filter payload.
        """
        return self._post(
            "document-processing/outgoing-service/export",
            headers=self._auth(),
            json=payload,
        )

    def outgoing_service_get(self, payload: dict) -> Any:
        """Retrieve a single outgoing service document.

        :param payload: Query payload.
        """
        return self._post(
            "document-processing/outgoing-service/get-document",
            headers=self._auth(),
            json=payload,
        )

    # ------------------------------------------------------------------
    # Production document
    # ------------------------------------------------------------------

    def production_doc_create(self, payload: dict) -> Any:
        """Create a production document.

        :param payload: Production document creation payload.
        """
        return self._post(
            "document-processing/production-document/create-document",
            headers=self._auth(),
            json=payload,
        )

    def production_doc_edit(self, payload: dict) -> Any:
        """Edit an existing production document.

        :param payload: Updated production document data.
        """
        return self._post(
            "document-processing/production-document/edit-document",
            headers=self._auth(),
            json=payload,
        )

    def production_doc_export(self, payload: dict) -> Any:
        """Export production documents.

        :param payload: Export filter payload.
        """
        return self._post(
            "document-processing/production-document/export",
            headers=self._auth(),
            json=payload,
        )

    def production_doc_get(self, payload: dict) -> Any:
        """Retrieve a single production document.

        :param payload: Query payload.
        """
        return self._post(
            "document-processing/production-document/get-document",
            headers=self._auth(),
            json=payload,
        )

    # ------------------------------------------------------------------
    # Sales document
    # ------------------------------------------------------------------

    def sales_doc_create(self, payload: dict) -> Any:
        """Create a sales document.

        :param payload: Sales document creation payload.
        """
        return self._post(
            "document-processing/sales-document/create-document",
            headers=self._auth(),
            json=payload,
        )

    def sales_doc_edit(self, payload: dict) -> Any:
        """Edit an existing sales document.

        :param payload: Updated sales document data.
        """
        return self._post(
            "document-processing/sales-document/edit-document",
            headers=self._auth(),
            json=payload,
        )

    def sales_doc_export(self, payload: dict) -> Any:
        """Export sales documents.

        :param payload: Export filter payload.
        """
        return self._post(
            "document-processing/sales-document/export",
            headers=self._auth(),
            json=payload,
        )

    def sales_doc_get(self, payload: dict) -> Any:
        """Retrieve a single sales document.

        :param payload: Query payload.
        """
        return self._post(
            "document-processing/sales-document/get-document",
            headers=self._auth(),
            json=payload,
        )

    # ------------------------------------------------------------------
    # Writeoff document
    # ------------------------------------------------------------------

    def writeoff_create(self, payload: dict) -> Any:
        """Create a writeoff document.

        :param payload: Writeoff document creation payload.
        """
        return self._post(
            "document-processing/writeoff-document/create",
            headers=self._auth(),
            json=payload,
        )

    def writeoff_edit(self, payload: dict) -> Any:
        """Edit an existing writeoff document.

        :param payload: Updated writeoff document data.
        """
        return self._post(
            "document-processing/writeoff-document/edit",
            headers=self._auth(),
            json=payload,
        )

    def writeoff_export(self, payload: dict) -> Any:
        """Export writeoff documents.

        :param payload: Export filter payload.
        """
        return self._post(
            "document-processing/writeoff-document/export",
            headers=self._auth(),
            json=payload,
        )

    def writeoff_get_by_id(self, payload: dict) -> Any:
        """Retrieve a writeoff document by ID.

        :param payload: Query payload containing document ID.
        """
        return self._post(
            "document-processing/writeoff-document/export/by-id",
            headers=self._auth(),
            json=payload,
        )

    def writeoff_export_by_number(self, payload: dict) -> Any:
        """Export a writeoff document by document number.

        :param payload: Query payload containing document number.
        """
        return self._post(
            "document-processing/writeoff-document/export/by-number",
            headers=self._auth(),
            json=payload,
        )
