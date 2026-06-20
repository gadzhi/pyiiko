"""Reference-data (v2 справочники) mixin for IikoServer — keeps server.py under 800 lines."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import requests


class _EntitiesMixin:
    """Mixin providing v2 reference-data (справочники) endpoints for IikoServer.

    Two endpoints are exposed:

    * ``GET /api/v2/entities/list`` — return common reference records for one
      or more entity types (available since iiko 5.0).
    * ``GET /api/v2/entities/{entityType}/ids`` — return the list of UUIDs for
      an entity type (available since iiko 9.2.1028.0).
    """

    if TYPE_CHECKING:
        def _get(self, path: str, **kwargs: Any) -> requests.Response: ...

    def _key(self, **extra: Any) -> dict[str, Any]:  # satisfied by IikoServer
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Справочники
    # ------------------------------------------------------------------

    def entities_list(
        self,
        root_types: list[str],
        include_deleted: bool = True,
        revision_from: int = -1,
    ) -> Any:
        """Return reference data for one or more entity types (v2 API).

        :param root_types: One or more entity type names, e.g.
            ``["DiscountType", "PaymentType"]``.  Supported values include
            ``Account``, ``DiscountType``, ``PaymentType``, ``TaxCategory``,
            ``LocalTax``, ``OrderType``, ``ProductSize``, and others.
        :param include_deleted: Include deleted records (default ``True``,
            matching the API default).
        :param revision_from: Return only items whose revision is strictly
            greater than this value.  ``-1`` disables the filter (default).
        :returns: Parsed JSON list.  Each element contains ``id``,
            ``rootType``, ``deleted``, ``code``, ``name``.  Some types expose
            additional fields:

            * ``OrderType`` → ``orderServiceType``, ``defaultForServiceType``
            * ``ProductSize`` → ``shortName``
            * ``TaxCategory`` → ``vatPercent``
            * ``LocalTax`` → ``appliedVAT``, ``vatCategoryId``,
              ``ordersTypesIds``, ``allOrderTypes``, ``categoriesIds``,
              ``departmentsSettings``, ``reporting``, ``createdAt``,
              ``updatedAt``

        Available since iiko 5.0.

        Example::

            data = server.entities_list(
                ["DiscountType", "PaymentType"],
                include_deleted=False,
            )
        """
        params: list[tuple[str, Any]] = [
            ("key", self._key()["key"]),
            ("includeDeleted", str(include_deleted).lower()),
            ("revisionFrom", revision_from),
        ]
        for rt in root_types:
            params.append(("rootType", rt))
        return self._get("api/v2/entities/list", params=params).json()

    def entities_ids(
        self,
        entity_type: str,
        include_deleted: bool = True,
        revision_from: int = -1,
    ) -> Any:
        """Return the list of UUID identifiers for an entity type (v2 API).

        :param entity_type: Entity type name, e.g. ``"Account"``.
        :param include_deleted: Include deleted records (default ``True``).
        :param revision_from: Return only items whose revision is strictly
            greater than this value.  ``-1`` disables the filter (default).
        :returns: Parsed JSON list of UUID strings.

        Available since iiko 9.2.1028.0.

        Example::

            ids = server.entities_ids("Account", include_deleted=False, revision_from=10)
        """
        return self._get(
            f"api/v2/entities/{entity_type}/ids",
            params=self._key(
                includeDeleted=str(include_deleted).lower(),
                revisionFrom=revision_from,
            ),
        ).json()
