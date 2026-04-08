"""iiko Server API client (on-premise)."""
from __future__ import annotations

import logging
from io import StringIO
from typing import Any

from lxml import etree

from ._base import DEFAULT_TIMEOUT, BaseIikoClient
from .exceptions import IikoAuthError

logger = logging.getLogger(__name__)


class IikoServer(BaseIikoClient):
    """Client for the iiko Server REST API (on-premise installations).

    Authenticates on construction and stores the token for subsequent calls.
    Pass a pre-existing *token* to skip the auth round-trip::

        server = IikoServer(ip="https://host:443", login="user", password="sha1hash")
        print(server.version())

    One token occupies one license slot.  Call :meth:`quit_token` when done to
    free the slot, or use the client as a context manager::

        with IikoServer(...) as server:
            data = server.departments()
    """

    def __init__(
        self,
        ip: str | None = None,
        login: str | None = None,
        password: str | None = None,
        token: str | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        base_url = (ip or "").rstrip("/") + "/resto/"
        super().__init__(base_url, timeout)
        self.login = login
        self.password = password
        self._token: str = token or self.get_token()

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def _key(self, **extra: Any) -> dict[str, Any]:
        """Return params dict containing the auth key plus any extra params."""
        params: dict[str, Any] = {"key": self._token}
        params.update({k: v for k, v in extra.items() if v is not None})
        return params

    def token(self) -> str:
        """Return the current authentication token."""
        return self._token

    def get_token(self) -> str:
        """Fetch a new authentication token from the server.

        .. note::

            Each token occupies one license slot.  If you have a single
            license and a live token, requesting a new one will fail.
            Call :meth:`quit_token` to release the slot first.
        """
        response = self._get(
            "api/auth",
            params={"login": self.login, "pass": self.password},
        )
        token = response.text.strip()
        if not token:
            raise IikoAuthError("Server returned an empty token")
        return token

    def quit_token(self) -> None:
        """Destroy the current token and release the license slot."""
        self._get("api/logout", params={"key": self._token})
        logger.info("Token destroyed: %s", self._token)

    # ------------------------------------------------------------------
    # Server info
    # ------------------------------------------------------------------

    def version(self) -> str:
        """Return the iiko server version string."""
        text = self._get(
            "get_server_info.jsp", params={"encoding": "UTF-8"}
        ).text
        tree = etree.parse(StringIO(text))
        nodes: list[Any] = tree.xpath(r"//version/text()")  # type: ignore[assignment]
        return "".join(str(x) for x in nodes)

    def server_info(self) -> Any:
        """Return server info and license status as a parsed JSON dict."""
        return self._get(
            "get_server_info.jsp", params={"encoding": "UTF-8"}
        ).json()

    # ------------------------------------------------------------------
    # Корпорации
    # ------------------------------------------------------------------

    def departments(self) -> bytes:
        """Return the department hierarchy (corporateItemDto).

        .. csv-table:: Department types
           :header: "Code", "Name"
           :widths: 20, 30

           "CORPORATION", Corporation
           "JURPERSON", Legal entity
           "ORGDEVELOPMENT", Structural unit
           "DEPARTMENT", Trading enterprise
           "MANUFACTURE", Production
           "CENTRALSTORE", Central warehouse
           "CENTRALOFFICE", Central office
           "SALEPOINT", Point of sale
           "STORE", Warehouse
        """
        return self._get("api/corporation/departments", params=self._key()).content

    def stores(self) -> str:
        """Return all warehouses as corporateItemDto XML."""
        return self._get("api/corporation/stores", params=self._key()).text

    def groups(self) -> bytes:
        """Return groups, branches, and points of sale (groupDto)."""
        return self._get("api/corporation/groups", params=self._key()).content

    def terminals(self) -> bytes:
        """Return all terminals (terminalDto)."""
        return self._get("api/corporation/terminals", params=self._key()).content

    def departments_find(self, code: str) -> bytes:
        """Search for a department by code (regex).

        :param code: Department code regex pattern.
        :returns: corporateItemDto structure.
        """
        return self._get(
            "api/corporation/departments/search",
            params=self._key(departmentCode=code),
        ).content

    def stores_find(self, code: str) -> bytes:
        """Search for a warehouse by code (regex).

        :param code: Warehouse code regex pattern.
        :returns: corporateItemDto structure.
        """
        return self._get(
            "api/corporation/stores/search",
            params=self._key(storeCode=code),
        ).content

    def groups_search(self, **kwargs: Any) -> bytes:
        """Search for branch groups.

        :param name: Group name regex.
        :param departmentId: Department GUID.
        """
        return self._get(
            "api/corporation/groups/search",
            params=self._key(**kwargs),
        ).content

    def terminals_search(self, anonymous: bool = False, **kwargs: Any) -> bytes:
        """Search for terminals.

        :param anonymous: Front terminals have ``anonymous=False``; back-office
            and system terminals have ``anonymous=True``.
        :param name: Terminal name regex (optional).
        :param computerName: Computer name regex (optional).
        :returns: List of terminalDto.
        """
        return self._get(
            "api/corporation/terminal/search",
            params=self._key(anonymous=str(anonymous).lower(), **kwargs),
        ).content

    # ------------------------------------------------------------------
    # Работники
    # ------------------------------------------------------------------

    def employees(self) -> bytes:
        """Return all employees."""
        return self._get("api/employees", params=self._key()).content

    # ------------------------------------------------------------------
    # События
    # ------------------------------------------------------------------

    def events(self, **kwargs: Any) -> bytes:
        """Return a list of events.

        :param from_time: Start time ISO ``yyyy-MM-ddTHH:mm:ss.SSS`` (optional).
        :param to_time: End time ISO (exclusive, optional).
        :param from_rev: Start revision number (optional).
        :returns: eventsList XML.
        """
        return self._get("api/events", params=self._key(**kwargs)).content

    def events_filter(self, body: str | bytes) -> bytes:
        """Return events filtered by event type and order number.

        :param body: XML filter body (application/xml).

        .. code-block:: xml

            <eventsRequestData>
                <events>
                    <event>orderPaid</event>
                </events>
                <orderNums>
                    <orderNum>175658</orderNum>
                </orderNums>
            </eventsRequestData>

        :returns: groupsList XML.
        """
        return self._post(
            "api/events",
            data=body,
            params={"key": self._token},
        ).content

    def events_meta(self) -> bytes:
        """Return event metadata tree."""
        return self._get("api/events/metadata", params=self._key()).content

    # ------------------------------------------------------------------
    # Продукты
    # ------------------------------------------------------------------

    def products(self, includeDeleted: bool = True) -> bytes:
        """Return the product catalog.

        .. csv-table:: Product element types
           :header: "Code", "Name"
           :widths: 15, 20

           "GOODS", Item
           "DISH", Dish
           "PREPARED", Preparation
           "SERVICE", Service
           "MODIFIER", Modifier

        :param includeDeleted: Include deleted items (default ``True``).
        """
        return self._get(
            "api/products",
            params=self._key(includeDeleted=str(includeDeleted).lower()),
        ).content

    def products_find(self, **kwargs: Any) -> bytes:
        """Search the product catalog.

        :param includeDeleted: Include deleted items.
        :param name: Name regex (optional).
        :param code: Quick-dial code regex (optional).
        :param mainUnit: Base unit of measure regex (optional).
        :param num: Article number regex (optional).
        :param cookingPlaceType: Cooking place type regex (optional).
        :param productGroupType: Parent group type regex (optional).
        :param productType: Product type regex (optional).
        """
        return self._get(
            "api/products/search/",
            params=self._key(**kwargs),
        ).content

    # ------------------------------------------------------------------
    # Поставщики
    # ------------------------------------------------------------------

    def suppliers(self) -> bytes:
        """Return all suppliers (employees structure)."""
        return self._get("api/suppliers", params=self._key()).content

    def suppliers_find(self, name: str = "", code: str = "") -> bytes:
        """Search suppliers by name and/or code regex.

        :param name: Supplier name regex (optional).
        :param code: Supplier code regex (optional).
        :returns: employees XML.
        """
        return self._get(
            "api/suppliers",
            params=self._key(name=name or None, code=code or None),
        ).content

    def suppliers_price(self, code: str, date: str | None = None) -> bytes:
        """Return the supplier price list.

        :param code: Supplier GUID.
        :param date: Price list start date ``DD.MM.YYYY`` (optional,
            defaults to latest).
        """
        return self._get(
            f"api/suppliers/{code}/pricelist",
            params=self._key(date=date),
        ).content

    # ------------------------------------------------------------------
    # Отчеты
    # ------------------------------------------------------------------

    def olap(
        self,
        report: str | None = None,
        data_from: str | None = None,
        data_to: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Return an OLAP report.

        :param report: Report type — ``SALES``, ``TRANSACTIONS``,
            ``DELIVERIES``, or ``STOCK``.
        :param data_from: Start date-time ISO.
        :param data_to: End date-time ISO.
        :param groupRow: Row grouping fields, e.g. ``WaiterName``.
        :param groupCol: Column grouping fields.
        :param agr: Aggregation fields.
        :returns: Report XML/text.
        """
        return self._get(
            "api/reports/olap",
            params={
                "key": self._token,
                "report": report,
                "from": data_from,
                "to": data_to,
                **{k: v for k, v in kwargs.items() if v is not None},
            },
        ).text

    def store_operation(
        self,
        stores: str | None = None,
        documentTypes: str | None = None,
        productDetalization: bool = True,
        showCostCorrections: bool = True,
        presetId: str | None = None,
        **kwargs: Any,
    ) -> bytes:
        """Return a warehouse operations report.

        :param stores: Warehouse GUID filter (optional, all if omitted).
        :param documentTypes: Document type filter (optional, all if omitted).
        :param productDetalization: Include per-product rows (default ``True``).
        :param showCostCorrections: Include cost corrections (default ``True``).
        :param presetId: Preset report GUID (optional).
        """
        return self._get(
            "api/reports/storeOperations",
            params=self._key(
                stores=stores,
                documentTypes=documentTypes,
                productDetalization=productDetalization,
                showCostCorrections=showCostCorrections,
                presetId=presetId,
                **kwargs,
            ),
        ).content

    def store_presets(self) -> bytes:
        """Return warehouse report presets (storeReportPresets)."""
        return self._get("api/reports/storeReportPresets", params=self._key()).content

    def product_expense(self, departament: str, **kwargs: Any) -> bytes:
        """Return a product consumption by sales report.

        :param departament: Department GUID.
        :param dateFrom: Start date ``DD.MM.YYYY``.
        :param dateTo: End date ``DD.MM.YYYY``.
        :param hourFrom: Start hour (default -1, full day).
        :param hourTo: End hour (default -1, full day).
        :returns: dayDishValue XML.
        """
        return self._get(
            "api/reports/productExpense",
            params=self._key(department=departament, **kwargs),
        ).content

    def sales(
        self,
        departament: str,
        dishDetails: bool = False,
        allRevenue: bool = True,
        **kwargs: Any,
    ) -> bytes:
        """Return a revenue report.

        :param departament: Department GUID.
        :param dateFrom: Start date ``DD.MM.YYYY``.
        :param dateTo: End date ``DD.MM.YYYY``.
        :param dishDetails: Include per-dish breakdown (default ``False``).
        :param allRevenue: All payment types if ``True``, revenue only if
            ``False`` (default ``True``).
        :returns: dayDishValue XML.
        """
        return self._get(
            "api/reports/sales",
            params=self._key(
                department=departament,
                dishDetails=dishDetails,
                allRevenue=allRevenue,
                **kwargs,
            ),
        ).content

    def mounthly_plan(self, departament: str, **kwargs: Any) -> bytes:
        """Return the monthly revenue plan.

        :param departament: Department GUID.
        :param dateFrom: Start date ``DD.MM.YYYY``.
        :param dateTo: End date ``DD.MM.YYYY``.
        :returns: budgetPlanItemDtoes XML.
        """
        return self._get(
            "api/reports/monthlyIncomePlan",
            params=self._key(department=departament, **kwargs),
        ).content

    def ingredient_entry(
        self,
        departament: str,
        includeSubtree: bool = False,
        **kwargs: Any,
    ) -> bytes:
        """Return an ingredient-in-dish report.

        :param departament: Department GUID.
        :param includeSubtree: Include sub-tree rows (default ``False``).
        :param dateFrom: Start date ``DD.MM.YYYY``.
        :param dateTo: End date ``DD.MM.YYYY``.
        :param productArticle: Product article (search priority over product).
        :returns: budgetPlanItemDtoes XML.
        """
        return self._get(
            "api/reports/ingredientEntry",
            params=self._key(
                department=departament,
                includeSubtree=includeSubtree,
                **kwargs,
            ),
        ).content

    def olap2(self, body: dict) -> Any:
        """Return OLAP report data using the v2 JSON API.

        :param body: Report request dict.  See API docs for the full schema::

            {
                "reportType": "SALES",
                "buildSummary": "true",
                "groupByRowFields": ["OpenDate.Typed", "Department"],
                "aggregateFields": ["DishDiscountSumInt.withoutVAT"],
                "filters": { ... }
            }

        :returns: Parsed JSON response.
        """
        return self._post(
            "api/v2/reports/olap",
            params={"key": self._token},
            json=body,
        ).json()

    def reports_balance(
        self,
        timestamp: str,
        account: str | None = None,
        counteragent: str | None = None,
        department: str | None = None,
    ) -> Any:
        """Return account, counteragent, and department balances.

        :param timestamp: Accounting date-time ``yyyy-MM-dd'T'HH:mm:ss``.
        :param account: Account GUID filter (optional, repeatable).
        :param counteragent: Counteragent GUID filter (optional).
        :param department: Department GUID filter (optional).
        :returns: Parsed JSON with quantity and monetary balances.
        """
        return self._get(
            "reports/balance/counteragents",
            params=self._key(
                timestamp=timestamp,
                account=account,
                counteragent=counteragent,
                department=department,
            ),
        ).json()

    # ------------------------------------------------------------------
    # Накладные
    # ------------------------------------------------------------------

    def invoice_in(self, **kwargs: Any) -> bytes:
        """Export incoming invoices.

        :param from: Start date ``YYYY-MM-DD`` (inclusive).
        :param to: End date ``YYYY-MM-DD`` (inclusive, time ignored).
        :param supplierId: Supplier GUID filter (optional).
        :returns: Incoming invoice XSD.
        """
        return self._get(
            "api/documents/export/incomingInvoice",
            params=self._key(**kwargs),
        ).content

    def invoice_out(self, **kwargs: Any) -> bytes:
        """Export outgoing invoices.

        :param from: Start date ``YYYY-MM-DD`` (inclusive).
        :param to: End date ``YYYY-MM-DD`` (inclusive, time ignored).
        :param supplierId: Supplier GUID filter (optional).
        :returns: Outgoing invoice XSD.
        """
        return self._get(
            "api/documents/export/outgoingInvoice",
            params=self._key(**kwargs),
        ).content

    def invoice_number_in(self, current_year: bool = True, **kwargs: Any) -> bytes:
        """Export an incoming invoice by document number.

        :param number: Document number.
        :param current_year: Restrict to current year (default ``True``).
            When ``False``, *from* and *to* must be provided.
        :param from: Start date ``YYYY-MM-DD`` (required when
            ``current_year=False``).
        :param to: End date ``YYYY-MM-DD`` (required when
            ``current_year=False``).
        """
        return self._get(
            "api/documents/export/incomingInvoice/byNumber",
            params=self._key(
                currentYear=str(current_year).lower(), **kwargs
            ),
        ).content

    def invoice_number_out(self, current_year: bool = True, **kwargs: Any) -> bytes:
        """Export an outgoing invoice by document number.

        :param number: Document number.
        :param current_year: Restrict to current year (default ``True``).
            When ``False``, *from* and *to* must be provided.
        :param from: Start date ``YYYY-MM-DD`` (required when
            ``current_year=False``).
        :param to: End date ``YYYY-MM-DD`` (required when
            ``current_year=False``).
        """
        return self._get(
            "api/documents/export/outgoingInvoice/byNumber",
            params=self._key(
                currentYear=str(current_year).lower(), **kwargs
            ),
        ).content

    def production_doc(self, xml: str | bytes) -> bytes:
        """Upload a production act (акт приготовления).

        :param xml: XML document body.
        """
        return self._post(
            "api/documents/import/productionDocument",
            params={"key": self._token},
            data=xml,
            headers={"Content-type": "text/xml"},
        ).content

    # ------------------------------------------------------------------
    # Кассовые смены
    # ------------------------------------------------------------------

    def close_session(
        self,
        dateFrom: str | None = None,
        dateTo: str | None = None,
    ) -> bytes:
        """Return a list of cash register sessions.

        :param dateFrom: Start date ``DD.MM.YYYY``.
        :param dateTo: End date ``DD.MM.YYYY``.
        :returns: CloseSessionDto list.
        """
        return self._get(
            "api/closeSession/list",
            params=self._key(dateFrom=dateFrom, dateTo=dateTo),
        ).content

    def session(
        self,
        from_time: str | None = None,
        to_time: str | None = None,
    ) -> bytes:
        """Return cash register session details.

        :param from_time: Start ISO ``yyyy-MM-ddTHH:mm:ss.SSS``.
        :param to_time: End ISO (exclusive).
        :returns: Session information.
        """
        return self._get(
            "api/events/sessions",
            params=self._key(**{"from": from_time, "to": to_time}),
        ).content

    # ------------------------------------------------------------------
    # EDI
    # ------------------------------------------------------------------

    def edi(
        self,
        edi: str,
        gln: str | None = None,
        inn: str | None = None,
        kpp: str | None = None,
        name: str | None = None,
    ) -> bytes:
        """Return EDI orders for a participant and supplier.

        :param edi: EDI system GUID (EdiSystem identifier).
        :param gln: Supplier GLN (required if *inn* is absent).
        :param inn: Supplier INN (required if *gln* is absent).
        :param kpp: Supplier KPP (optional).
        :param name: Supplier name (optional).
        :returns: EDI order list.
        """
        return self._get(
            f"edi/{edi}/orders/bySeller",
            params=self._key(gln=gln, inn=inn, kpp=kpp, name=name),
        ).content
