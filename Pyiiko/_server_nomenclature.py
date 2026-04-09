"""Nomenclature v2 mixin for IikoServer — keeps server.py under 800 lines."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import requests


class _NomenclatureMixin:
    """Mixin providing v2 nomenclature endpoints for IikoServer.

    Endpoints are under ``/api/v2/entities/products/...`` and require the
    user to have the **B_EN** ("Редактирование номенклатурных справочников")
    permission.
    """

    if TYPE_CHECKING:
        def _get(self, path: str, **kwargs: Any) -> requests.Response: ...
        def _post(self, path: str, **kwargs: Any) -> requests.Response: ...

    def _key(self, **extra: Any) -> dict[str, Any]:  # satisfied by IikoServer
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Элементы номенклатуры
    # ------------------------------------------------------------------

    def nomenclature_list(
        self,
        include_deleted: bool = False,
        revision_from: int = -1,
        ids: list[str] | None = None,
        nums: list[str] | None = None,
        codes: list[str] | None = None,
        types: list[str] | None = None,
        category_ids: list[str] | None = None,
        parent_ids: list[str] | None = None,
    ) -> Any:
        """Return the list of nomenclature elements (v2 API).

        :param include_deleted: Include deleted items (default ``False``).
        :param revision_from: Return only items with revision > this value
            (default ``-1`` — no revision filter).
        :param ids: Filter by element UUIDs (optional).
        :param nums: Filter by article numbers (optional).
        :param codes: Filter by fast-search codes (optional).
        :param types: Filter by product types, e.g. ``["GOODS", "DISH"]``
            (optional).
        :param category_ids: Filter by user-category UUIDs (optional).
        :param parent_ids: Filter by parent-group UUIDs (optional).
        :returns: Parsed JSON list of ProductDto.
        """
        params: list[tuple[str, Any]] = [
            ("key", self._key()["key"]),
            ("includeDeleted", str(include_deleted).lower()),
            ("revisionFrom", revision_from),
        ]
        for uid in ids or []:
            params.append(("id", uid))
        for num in nums or []:
            params.append(("num", num))
        for code in codes or []:
            params.append(("code", code))
        for t in types or []:
            params.append(("type", t))
        for cid in category_ids or []:
            params.append(("categoryId", cid))
        for pid in parent_ids or []:
            params.append(("parentId", pid))
        return self._get(
            "api/v2/entities/products/list",
            params=params,
        ).json()

    def nomenclature_save(
        self,
        payload: dict,
        generate_nomenclature_code: bool = True,
        generate_fast_code: bool = True,
    ) -> Any:
        """Create (import) a new nomenclature element.

        :param payload: Product object dict.  Required fields: ``name``,
            ``type``, ``mainUnit``.
        :param generate_nomenclature_code: Auto-generate article number
            (default ``True``).
        :param generate_fast_code: Auto-generate fast-search code
            (default ``True``).
        :returns: Parsed JSON with ``result``, ``errors``, ``response``.
        """
        return self._post(
            "api/v2/entities/products/save",
            params=self._key(
                generateNomenclatureCode=str(generate_nomenclature_code).lower(),
                generateFastCode=str(generate_fast_code).lower(),
            ),
            json=payload,
        ).json()

    def nomenclature_update(self, payload: dict) -> Any:
        """Edit an existing nomenclature element.

        :param payload: Product dict with ``id`` field and all fields to
            update.
        :returns: Parsed JSON with ``result``, ``errors``, ``response``.
        """
        return self._post(
            "api/v2/entities/products/update",
            params={"key": self._key()["key"]},
            json=payload,
        ).json()

    def nomenclature_delete(self, ids: list[str]) -> Any:
        """Delete nomenclature elements by UUID list.

        :param ids: List of element UUIDs to delete.
        :returns: Parsed JSON operation result.
        """
        return self._post(
            "api/v2/entities/products/delete",
            params={"key": self._key()["key"]},
            json=ids,
        ).json()

    def nomenclature_restore(self, ids: list[str]) -> Any:
        """Restore previously deleted nomenclature elements.

        :param ids: List of element UUIDs to restore.
        :returns: Parsed JSON operation result.
        """
        return self._post(
            "api/v2/entities/products/restore",
            params={"key": self._key()["key"]},
            json=ids,
        ).json()

    # ------------------------------------------------------------------
    # Номенклатурные группы
    # ------------------------------------------------------------------

    def nomenclature_group_list(
        self,
        include_deleted: bool = False,
        revision_from: int = -1,
        ids: list[str] | None = None,
        parent_ids: list[str] | None = None,
    ) -> Any:
        """Return the list of nomenclature groups (v2 API).

        :param include_deleted: Include deleted groups (default ``False``).
        :param revision_from: Revision filter (default ``-1``).
        :param ids: Filter by group UUIDs (optional).
        :param parent_ids: Filter by parent-group UUIDs (optional).
        :returns: Parsed JSON list of ProductGroupDto.
        """
        params: list[tuple[str, Any]] = [
            ("key", self._key()["key"]),
            ("includeDeleted", str(include_deleted).lower()),
            ("revisionFrom", revision_from),
        ]
        for uid in ids or []:
            params.append(("id", uid))
        for pid in parent_ids or []:
            params.append(("parentId", pid))
        return self._get(
            "api/v2/entities/products/group/list",
            params=params,
        ).json()

    def nomenclature_group_save(self, payload: dict) -> Any:
        """Create (import) a new nomenclature group.

        :param payload: Group object dict.  Required field: ``name``.
        :returns: Parsed JSON with ``result``, ``errors``, ``response``.
        """
        return self._post(
            "api/v2/entities/products/group/save",
            params={"key": self._key()["key"]},
            json=payload,
        ).json()

    def nomenclature_group_update(self, payload: dict) -> Any:
        """Edit an existing nomenclature group.

        :param payload: Group dict with ``id`` and fields to update.
        :returns: Parsed JSON with ``result``, ``errors``, ``response``.
        """
        return self._post(
            "api/v2/entities/products/group/update",
            params={"key": self._key()["key"]},
            json=payload,
        ).json()

    def nomenclature_group_delete(self, ids: list[str]) -> Any:
        """Delete nomenclature groups by UUID list.

        :param ids: List of group UUIDs to delete.
        :returns: Parsed JSON operation result.
        """
        return self._post(
            "api/v2/entities/products/group/delete",
            params={"key": self._key()["key"]},
            json=ids,
        ).json()

    def nomenclature_group_restore(self, ids: list[str]) -> Any:
        """Restore previously deleted nomenclature groups.

        :param ids: List of group UUIDs to restore.
        :returns: Parsed JSON operation result.
        """
        return self._post(
            "api/v2/entities/products/group/restore",
            params={"key": self._key()["key"]},
            json=ids,
        ).json()

    # ------------------------------------------------------------------
    # Пользовательские категории
    # ------------------------------------------------------------------

    def nomenclature_category_list(
        self,
        include_deleted: bool = False,
        revision_from: int = -1,
    ) -> Any:
        """Return the list of user-defined product categories (v2 API).

        :param include_deleted: Include deleted categories (default ``False``).
        :param revision_from: Revision filter (default ``-1``).
        :returns: Parsed JSON list of EntityDto.
        """
        return self._get(
            "api/v2/entities/products/category/list",
            params=self._key(
                includeDeleted=str(include_deleted).lower(),
                revisionFrom=revision_from,
            ),
        ).json()

    def nomenclature_category_save(self, payload: dict) -> Any:
        """Create a new user-defined product category.

        :param payload: Category dict.  Required field: ``name``.
        :returns: Parsed JSON with ``result``, ``errors``, ``response``.
        """
        return self._post(
            "api/v2/entities/products/category/save",
            params={"key": self._key()["key"]},
            json=payload,
        ).json()

    def nomenclature_category_update(self, payload: dict) -> Any:
        """Edit an existing user-defined product category.

        :param payload: Category dict with ``id`` and fields to update.
        :returns: Parsed JSON with ``result``, ``errors``, ``response``.
        """
        return self._post(
            "api/v2/entities/products/category/update",
            params={"key": self._key()["key"]},
            json=payload,
        ).json()

    def nomenclature_category_delete(self, ids: list[str]) -> Any:
        """Delete user-defined product categories by UUID list.

        :param ids: List of category UUIDs to delete.
        :returns: Parsed JSON operation result.
        """
        return self._post(
            "api/v2/entities/products/category/delete",
            params={"key": self._key()["key"]},
            json=ids,
        ).json()

    def nomenclature_category_restore(self, ids: list[str]) -> Any:
        """Restore previously deleted user-defined product categories.

        :param ids: List of category UUIDs to restore.
        :returns: Parsed JSON operation result.
        """
        return self._post(
            "api/v2/entities/products/category/restore",
            params={"key": self._key()["key"]},
            json=ids,
        ).json()
