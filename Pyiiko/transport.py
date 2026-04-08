"""iiko Transport (Cloud) API client."""
from __future__ import annotations

import logging
from typing import Any

from ._base import BaseIikoClient, DEFAULT_TIMEOUT
from .exceptions import IikoAuthError

logger = logging.getLogger(__name__)

_API_BASE = "https://api-ru.iiko.services"


class Transport(BaseIikoClient):
    """Client for the iiko Transport Cloud API.

    Authenticates with an API login key and stores a Bearer token for
    subsequent requests::

        client = Transport(key="your-api-login-key")
        orgs = client.organization()

    Pass a pre-fetched *token* dict to skip the auth round-trip::

        client = Transport(token={"token": "...", ...})
    """

    def __init__(
        self,
        key: str | None = None,
        token: dict | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        super().__init__(_API_BASE, timeout)
        self.key = key
        self._token: dict = token if token is not None else self.get_token()

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def get_token(self) -> dict:
        """Fetch a new Bearer token using the API login key.

        :returns: Token response dict, e.g. ``{"token": "...", "correlationId": "..."}``.
        :raises IikoAuthError: If the server returns an empty token.
        """
        response = self._post(
            "api/1/access_token",
            json={"apiLogin": self.key},
            headers={"content-type": "application/json", "Accept-Charset": "UTF-8"},
        )
        data: dict = response.json()
        if not data.get("token"):
            raise IikoAuthError("Transport API returned an empty token")
        return data

    def token(self) -> dict:
        """Return the current token response dict."""
        return self._token

    def _auth(self) -> dict[str, str]:
        """Return Authorization header for the current token."""
        return {"Authorization": f"Bearer {self._token['token']}"}

    # ------------------------------------------------------------------
    # Organizations & infrastructure
    # ------------------------------------------------------------------

    def organization(self) -> Any:
        """Return the list of organizations accessible with the current key."""
        return self._get("api/1/organizations", headers=self._auth())

    def terminal(self, org_id: str, include: str = "false") -> Any:
        """Return terminal groups for an organization.

        :param org_id: Organization GUID.
        :param include: Whether to include disabled groups (default ``"false"``).
        """
        return self._post(
            "api/1/terminal_groups",
            json={"organizationIds": [org_id]},
            headers=self._auth(),
        )

    def regions(self, org_id: str) -> Any:
        """Return delivery regions for an organization.

        :param org_id: Organization GUID.
        """
        return self._post(
            "api/1/regions",
            json={"organizationIds": [org_id]},
            headers=self._auth(),
        )

    def cities(self, org_id: str | None = None) -> Any:
        """Return cities for an organization.

        :param org_id: Organization GUID.
        """
        return self._post(
            "api/1/cities",
            json={"organizationIds": [org_id]},
            headers=self._auth(),
        )

    def streets_by_city(self, org_id: str, city: str) -> Any:
        """Return streets for a city within an organization.

        :param org_id: Organization GUID.
        :param city: City GUID.
        """
        return self._post(
            "api/1/streets/by_city",
            json={"organizationId": org_id, "cityId": city},
            headers=self._auth(),
        )

    # ------------------------------------------------------------------
    # Deliveries
    # ------------------------------------------------------------------

    def delivery_create(self, order_info: dict) -> Any:
        """Create a delivery order.

        :param order_info: Delivery order payload dict.
        """
        return self._post(
            "api/1/deliveries/create",
            json=order_info,
            headers=self._auth(),
        )

    def check_create(self, order_info: dict | str) -> Any:
        """Validate a delivery order before creation.

        :param order_info: Order payload as dict or JSON string.
        """
        import json

        payload = (
            order_info
            if isinstance(order_info, dict)
            else json.loads(order_info)
        )
        return self._post(
            "api/1/deliveries/check_create",
            json=payload,
            headers=self._auth(),
        )

    def by_id(
        self,
        org_id: str | None = None,
        order_id: str | None = None,
    ) -> Any:
        """Return a delivery order by ID.

        :param org_id: Organization GUID.
        :param order_id: Order GUID.
        """
        return self._post(
            "api/1/deliveries/by_id",
            json={"organizationId": org_id, "orderIds": [order_id]},
            headers=self._auth(),
        )

    def by_delivery_date(
        self,
        org_id: str | None = None,
        delivery_date_from: str | None = None,
    ) -> Any:
        """Return deliveries filtered by date and status.

        :param org_id: Organization GUID.
        :param delivery_date_from: Start date-time ISO.
        """
        return self._post(
            "api/1/deliveries/by_delivery_date_and_status",
            json={
                "organizationId": [org_id],
                "deliveryDateFrom": [delivery_date_from],
            },
            headers=self._auth(),
        )

    def by_revision(
        self,
        org_id: str | None = None,
        revision: str | None = None,
    ) -> Any:
        """Return deliveries starting from a revision number.

        :param org_id: Organization GUID.
        :param revision: Start revision (string).
        """
        return self._post(
            "api/1/deliveries/by_revision",
            json={"startRevision": revision, "organizationIds": [org_id]},
            headers=self._auth(),
        )
