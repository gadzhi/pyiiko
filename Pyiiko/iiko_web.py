"""iiko Public Web API client."""
from __future__ import annotations

import logging
from typing import Any

from ._base import DEFAULT_TIMEOUT, BaseIikoClient
from ._web_docs import _DocsMixin
from .exceptions import IikoAuthError

logger = logging.getLogger(__name__)

_API_BASE = "https://public-api.iikoweb.ru"


class IikoWeb(_DocsMixin, BaseIikoClient):
    """Client for the iiko Public Web API.

    Authenticates with an API key (and optional app_id / client_secret) and
    stores a Bearer token for subsequent requests::

        client = IikoWeb(api_key="your-api-key")
        stores = client.stores()

    Pass a pre-fetched *token* dict to skip the auth round-trip::

        client = IikoWeb(token={"token": "...", "expires_in": ...})
    """

    def __init__(
        self,
        api_key: str | None = None,
        app_id: str | None = None,
        client_secret: str | None = None,
        token: dict | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        super().__init__(_API_BASE, timeout)
        self.api_key = api_key
        self.app_id = app_id
        self.client_secret = client_secret
        self._token: dict = token if token is not None else self.get_token()

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def get_token(self) -> dict:
        """Fetch a new Bearer token using the API key.

        :returns: Token response dict, e.g. ``{"token": "...", "expires_in": ...}``.
        :raises IikoAuthError: If the server returns an empty token.
        """
        body: dict[str, Any] = {"api_key": self.api_key}
        if self.app_id is not None:
            body = {**body, "app_id": self.app_id}
        if self.client_secret is not None:
            body = {**body, "client_secret": self.client_secret}
        response = self._post("auth", json=body)
        data: dict = response.json()
        if not data.get("token"):
            raise IikoAuthError("IikoWeb API returned an empty token")
        return data

    def token(self) -> dict:
        """Return the current token response dict."""
        return self._token

    def _auth(self) -> dict[str, str]:
        """Return Authorization header for the current token."""
        return {"Authorization": f"Bearer {self._token['token']}"}

    # ------------------------------------------------------------------
    # Entities
    # ------------------------------------------------------------------

    def stores(self) -> Any:
        """Return the list of all stores."""
        return self._post(
            "entities/store/list",
            headers=self._auth(),
            json={},
        )

    def store(self, store_id: int) -> Any:
        """Return a single store by ID.

        :param store_id: Numeric store identifier.
        """
        return self._post(
            "entities/store/get",
            headers=self._auth(),
            json={"id": store_id},
        )

    def products(
        self,
        filters: Any = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """Return the list of products with optional filtering and pagination.

        :param filters: Filter criteria dict (optional).
        :param limit: Maximum number of records to return (optional).
        :param offset: Number of records to skip (optional).
        """
        body = {
            k: v
            for k, v in {"filters": filters, "limit": limit, "offset": offset}.items()
            if v is not None
        }
        return self._post(
            "entities/products/list",
            headers=self._auth(),
            json=body,
        )

    def product_categories(
        self,
        filters: Any = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """Return the list of product categories.

        :param filters: Filter criteria dict (optional).
        :param limit: Maximum number of records to return (optional).
        :param offset: Number of records to skip (optional).
        """
        body = {
            k: v
            for k, v in {"filters": filters, "limit": limit, "offset": offset}.items()
            if v is not None
        }
        return self._post(
            "entities/product-category/list",
            headers=self._auth(),
            json=body,
        )

    def product_sizes(
        self,
        filters: Any = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """Return the list of product sizes.

        :param filters: Filter criteria dict (optional).
        :param limit: Maximum number of records to return (optional).
        :param offset: Number of records to skip (optional).
        """
        body = {
            k: v
            for k, v in {"filters": filters, "limit": limit, "offset": offset}.items()
            if v is not None
        }
        return self._post(
            "entities/product-size/list",
            headers=self._auth(),
            json=body,
        )

    def users(
        self,
        filters: Any = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """Return the list of users.

        :param filters: Filter criteria dict (optional).
        :param limit: Maximum number of records to return (optional).
        :param offset: Number of records to skip (optional).
        """
        body = {
            k: v
            for k, v in {"filters": filters, "limit": limit, "offset": offset}.items()
            if v is not None
        }
        return self._post(
            "entities/user/list",
            headers=self._auth(),
            json=body,
        )

    def payment_types(
        self,
        filters: Any = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """Return the list of payment types.

        :param filters: Filter criteria dict (optional).
        :param limit: Maximum number of records to return (optional).
        :param offset: Number of records to skip (optional).
        """
        body = {
            k: v
            for k, v in {"filters": filters, "limit": limit, "offset": offset}.items()
            if v is not None
        }
        return self._post(
            "entities/payment-type/list",
            headers=self._auth(),
            json=body,
        )

    def cash_flow_categories(
        self,
        filters: Any = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Any:
        """Return the list of cash flow categories.

        :param filters: Filter criteria dict (optional).
        :param limit: Maximum number of records to return (optional).
        :param offset: Number of records to skip (optional).
        """
        body = {
            k: v
            for k, v in {"filters": filters, "limit": limit, "offset": offset}.items()
            if v is not None
        }
        return self._post(
            "entities/cash-flow-category/list",
            headers=self._auth(),
            json=body,
        )

    # ------------------------------------------------------------------
    # Nomenclature
    # ------------------------------------------------------------------

    def update_barcodes(self, payload: dict) -> Any:
        """Update barcodes in the nomenclature.

        :param payload: Barcode update payload.
        """
        return self._post(
            "nomenclature/update-barcodes",
            headers=self._auth(),
            json=payload,
        )

    # ------------------------------------------------------------------
    # Purchasing — orders
    # ------------------------------------------------------------------

    def order_create(
        self,
        store_id: int,
        workflow_id: int,
        due_date: str,
        planned_delivery_date: str | None = None,
    ) -> Any:
        """Create a new purchasing order.

        :param store_id: Numeric store identifier.
        :param workflow_id: Numeric workflow identifier.
        :param due_date: Due date (ISO string).
        :param planned_delivery_date: Planned delivery date (ISO string, optional).
        """
        body: dict[str, Any] = {
            "storeId": store_id,
            "workflowId": workflow_id,
            "dueDate": due_date,
        }
        if planned_delivery_date is not None:
            body = {**body, "plannedDeliveryDate": planned_delivery_date}
        return self._post(
            "purchasing/orders/create",
            headers=self._auth(),
            json=body,
        )

    def order_get(self, order_id: int) -> Any:
        """Retrieve a purchasing order by ID.

        :param order_id: Numeric order identifier.
        """
        return self._post(
            "purchasing/orders/get",
            headers=self._auth(),
            json={"id": order_id},
        )

    def orders_list(self, payload: dict) -> Any:
        """Return a list of purchasing orders matching the given filters.

        :param payload: Filter and pagination payload.
        """
        return self._post(
            "purchasing/orders/list",
            headers=self._auth(),
            json=payload,
        )

    def order_add_products(self, payload: dict) -> Any:
        """Add products to an existing purchasing order.

        :param payload: Payload containing order ID and product list.
        """
        return self._post(
            "purchasing/orders/products/add",
            headers=self._auth(),
            json=payload,
        )

    def order_select_supplier(self, payload: dict) -> Any:
        """Select a supplier for a purchasing order.

        :param payload: Payload containing order ID and supplier details.
        """
        return self._post(
            "purchasing/orders/supplier/select",
            headers=self._auth(),
            json=payload,
        )

    def order_task_status(self, task_id: str) -> Any:
        """Check the status of an async purchasing order task.

        :param task_id: Task identifier string.
        """
        return self._post(
            "purchasing/orders/task-status",
            headers=self._auth(),
            json={"taskId": task_id},
        )

    def order_select_units(self, payload: dict) -> Any:
        """Select measurement units for a purchasing order.

        :param payload: Payload containing order ID and unit selections.
        """
        return self._post(
            "purchasing/orders/units/select",
            headers=self._auth(),
            json=payload,
        )

    # ------------------------------------------------------------------
    # Purchasing — workflows
    # ------------------------------------------------------------------

    def workflow_activate(self, workflow_id: int) -> Any:
        """Activate a purchasing workflow.

        :param workflow_id: Numeric workflow identifier.
        """
        return self._post(
            "purchasing/workflows/activate",
            headers=self._auth(),
            json={"id": workflow_id},
        )

    def workflow_deactivate(self, workflow_id: int) -> Any:
        """Deactivate a purchasing workflow.

        :param workflow_id: Numeric workflow identifier.
        """
        return self._post(
            "purchasing/workflows/deactivate",
            headers=self._auth(),
            json={"id": workflow_id},
        )

    def workflow_get(self, workflow_id: int) -> Any:
        """Retrieve a purchasing workflow by ID.

        :param workflow_id: Numeric workflow identifier.
        """
        return self._post(
            "purchasing/workflows/get",
            headers=self._auth(),
            json={"id": workflow_id},
        )

    def workflows_list(self, payload: dict | None = None) -> Any:
        """Return the list of purchasing workflows.

        :param payload: Optional filter payload; defaults to empty dict.
        """
        return self._post(
            "purchasing/workflows/list",
            headers=self._auth(),
            json=payload or {},
        )
