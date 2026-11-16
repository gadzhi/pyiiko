"""iiko Transport (Cloud) API client."""
from __future__ import annotations

import json

from requests import Response

from ._base import DEFAULT_TIMEOUT, BaseIikoClient
from .exceptions import IikoAuthError

_API_BASE = "https://api-ru.iiko.services"


def _delivery_datetime(value: str) -> str:
    """Accept the documented ISO separator as well as iiko's space."""
    if value[10:11] == "T":
        return value[:10] + " " + value[11:]
    return value


class Transport(BaseIikoClient):
    """Client for the iiko Transport Cloud API.

    Authenticates with an API login key and stores a Bearer token for
    subsequent requests::

        client = Transport(key="your-api-key", app_id="app-id", client_secret="secret")
        orgs = client.organization()

    Pass a pre-fetched *token* dict to skip the auth round-trip::

        client = Transport(token={"token": "...", ...})
    """

    def __init__(
        self,
        key: str | None = None,
        token: dict | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        *,
        app_id: str | None = None,
        client_secret: str | None = None,
    ) -> None:
        super().__init__(_API_BASE, timeout)
        self.key = key
        self.app_id = app_id
        self.client_secret = client_secret
        try:
            self._token = token if token is not None else self.get_token()
        except BaseException:
            self.close()
            raise

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def get_token(self) -> dict:
        """Fetch a new Bearer token using the API login key.

        :returns: Token response dict, e.g. ``{"token": "...", "correlationId": "..."}``.
        :raises IikoAuthError: If the server returns an empty token.
        """
        if not self.key:
            raise IikoAuthError("Transport requires an API key or an existing token")
        if self.app_id is None and self.client_secret is None:
            response = self._post("api/1/access_token", json={"apiLogin": self.key})
        else:
            if not self.app_id or not self.client_secret:
                raise IikoAuthError("Cloud v2 requires both app_id and client_secret")
            response = self._post(
                "api/v2/access_token",
                json={
                    "appId": self.app_id,
                    "clientSecret": self.client_secret,
                    "apiKey": self.key,
                },
            )
        data = response.json()
        if not isinstance(data, dict) or not isinstance(data.get("token"), str):
            raise IikoAuthError("Transport API returned an invalid token response")
        if not data["token"].strip():
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

    def organization(self) -> Response:
        """Return the list of organizations accessible with the current key."""
        return self._post("api/1/organizations", retry=True, json={}, headers=self._auth())

    def terminal(self, org_id: str, include: str | bool = "false") -> Response:
        """Return terminal groups for an organization.

        :param org_id: Organization GUID.
        :param include: Include disabled groups. Accepts bools and legacy strings.
        """
        if isinstance(include, str):
            value = include.strip().lower()
            if value not in {"true", "false"}:
                raise ValueError("include must be a boolean or 'true'/'false'")
            include = value == "true"
        return self._post(
            "api/1/terminal_groups",
            retry=True,
            json={"organizationIds": [org_id], "includeDisabled": include},
            headers=self._auth(),
        )

    def regions(self, org_id: str) -> Response:
        """Return delivery regions for an organization.

        :param org_id: Organization GUID.
        """
        return self._post(
            "api/1/regions",
            retry=True,
            json={"organizationIds": [org_id]},
            headers=self._auth(),
        )

    def cities(self, org_id: str | None = None) -> Response:
        """Return cities for an organization.

        :param org_id: Organization GUID.
        """
        return self._post(
            "api/1/cities",
            retry=True,
            json={"organizationIds": [org_id]},
            headers=self._auth(),
        )

    def streets_by_city(self, org_id: str, city: str) -> Response:
        """Return streets for a city within an organization.

        :param org_id: Organization GUID.
        :param city: City GUID.
        """
        return self._post(
            "api/1/streets/by_city",
            retry=True,
            json={"organizationId": org_id, "cityId": city},
            headers=self._auth(),
        )

    # ------------------------------------------------------------------
    # Deliveries
    # ------------------------------------------------------------------

    def delivery_create(self, order_info: dict) -> Response:
        """Create a delivery order.

        :param order_info: Delivery order payload dict.
        """
        return self._post(
            "api/1/deliveries/create",
            json=order_info,
            headers=self._auth(),
        )

    def check_create(self, order_info: dict | str) -> Response:
        """Validate a delivery order before creation.

        :param order_info: Order payload as dict or JSON string.
        """
        payload = (
            order_info
            if isinstance(order_info, dict)
            else json.loads(order_info)
        )
        return self._post(
            "api/1/deliveries/check_create",
            retry=True,
            json=payload,
            headers=self._auth(),
        )

    def by_id(
        self,
        org_id: str | None = None,
        order_id: str | None = None,
    ) -> Response:
        """Return a delivery order by ID.

        :param org_id: Organization GUID.
        :param order_id: Order GUID.
        """
        return self._post(
            "api/1/deliveries/by_id",
            retry=True,
            json={"organizationId": org_id, "orderIds": [order_id]},
            headers=self._auth(),
        )

    def by_delivery_date(
        self,
        org_id: str | None = None,
        delivery_date_from: str | None = None,
        *,
        delivery_date_to: str | None = None,
        statuses: list[str] | None = None,
    ) -> Response:
        """Return deliveries filtered by date and status.

        :param org_id: Organization GUID.
        :param delivery_date_from: Start date-time, required by iiko.
        :param delivery_date_to: Optional end date-time.
        :param statuses: Optional delivery statuses.
        """
        if not org_id or not delivery_date_from:
            raise ValueError("org_id and delivery_date_from are required")
        body: dict[str, str | list[str]] = {
            "organizationIds": [org_id],
            "deliveryDateFrom": _delivery_datetime(delivery_date_from),
        }
        if delivery_date_to is not None:
            body["deliveryDateTo"] = _delivery_datetime(delivery_date_to)
        if statuses is not None:
            body["statuses"] = statuses
        return self._post(
            "api/1/deliveries/by_delivery_date_and_status",
            retry=True,
            json=body,
            headers=self._auth(),
        )

    def by_revision(
        self,
        org_id: str | None = None,
        revision: str | None = None,
    ) -> Response:
        """Return deliveries starting from a revision number.

        :param org_id: Organization GUID.
        :param revision: Start revision (string).
        """
        return self._post(
            "api/1/deliveries/by_revision",
            retry=True,
            json={"startRevision": revision, "organizationIds": [org_id]},
            headers=self._auth(),
        )
