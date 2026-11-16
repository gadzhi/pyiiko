# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.6.0] - 2026-11-16

### Changed

- Require Python 3.11+ and update the minimum HTTP and XML dependency versions.
- Retry read operations on transient HTTP or connection errors. Send write requests,
  token requests, and logout requests once. Reject HTTP redirects.
- Default scheme-less iiko Server addresses to HTTPS. Use an explicit HTTP URL for legacy servers.

### Added

- Support iiko Cloud v2 authentication with `Transport(key=..., app_id=..., client_secret=...)`.
- Restore GitHub Actions for tests, dependency audits, and distribution checks.

### Fixed

- Omit credentials from Pyiiko log messages and HTTP exception tracebacks.
- Release client-owned iiko Server tokens when leaving a context manager.
- Send the documented Cloud requests for organizations, terminal groups, and deliveries by date.
- Parse XML server version responses without resolving entities and send the XML events media type.
- Include the complete test suite in source distributions.

## [0.5.0] - 2026-06-21

### Added
- `_EntitiesMixin` — 2 new `IikoServer` methods for the v2 reference-data API:
  - `entities_list(root_types, ...)` — `GET /api/v2/entities/list`: retrieves
    common reference records for one or more entity types (DiscountType,
    PaymentType, TaxCategory, LocalTax, OrderType, ProductSize, Account, etc.);
    supports multiple `rootType` params, `includeDeleted`, and `revisionFrom`.
  - `entities_ids(entity_type, ...)` — `GET /api/v2/entities/{entityType}/ids`:
    returns the list of UUID identifiers for any entity type; supports
    `includeDeleted` and `revisionFrom`.
- 11 new tests for the entities v2 API.

## [0.4.0] - 2026-05-06

### Added
- `IikoWeb` — new client for the iiko Public Web API (`https://public-api.iikoweb.ru`).
  Supports JWT Bearer auth, entities (stores, products, users, payment types),
  document processing (41 methods: incoming/outgoing invoices, internal transfers,
  write-offs, production and sales acts), nomenclature barcodes, and purchasing
  workflows (11 methods).
- `_NomenclatureMixin` — 15 new `IikoServer` methods for the v2 nomenclature API
  (`/api/v2/entities/products/...`): list, save, update, delete, restore for
  product elements, groups, and user-defined categories.
- 94 new tests (75 for `IikoWeb`, 19 for nomenclature v2); total test count: 158.

### Changed
- `pyproject.toml`: license field updated to PEP 639 SPDX string (`"Apache-2.0"`).

### Removed
- Legacy `test/` folder (old integration tests that required a live server).
- `.github/` and `.idea/` directories untracked and added to `.gitignore`.
- `setup.py` removed (fully replaced by `pyproject.toml` since 0.3.0).

## [0.3.0] - 2026-04-08

### Breaking changes
- Methods now raise `IikoAPIError` (or `IikoAuthError`) on failure instead of
  silently returning `None`. Update any code that checks `if result is None`.
- `Transport.by_delivery_date` parameter renamed from `order_id` to
  `delivery_date_from` to match its actual meaning.
- `IikoServer.olap2()` returns decoded JSON. Remove `.json()` from existing calls.
- `FrontWebAPI` module removed.
- `IikoBiz` module removed.
- `Card5` module removed.

### Added
- `IikoError`, `IikoAuthError`, `IikoAPIError` — structured exception hierarchy
  exported from the top-level package.
- `BaseIikoClient` — shared HTTP session with automatic retry on 5xx errors
  (3 retries, exponential back-off).
- Context manager support for `IikoServer` and `Transport`:
  `with IikoServer(...) as server: ...`.
- `timeout` parameter on `IikoServer.__init__` and `Transport.__init__`.
- PEP 561 `py.typed` marker — the library now ships type information.
- `pyproject.toml` replacing the legacy `setup.py`.
- Unit test suite in `tests/` using `pytest` + `responses` (no live API required).
- GitHub Actions CI workflow (Python 3.9–3.12).

### Fixed
- `server_info()` was returning a method object instead of parsed JSON (`.json`
  vs `.json()`).
- `terminals_search(anonymous=True)` raised `TypeError` — boolean was
  concatenated to a URL string.
- `invoice_number_in/out(current_year=False)` raised `TypeError` — same issue.
- `production_doc` used the wrong kwarg `body=` instead of `data=` and had a
  missing `=` before the token in the URL.
- `store_operation`, `product_expense`, `sales`, `ingredient_entry`,
  `reports_balance`, `close_session`, `session` all used Python set literals
  `{a, b, c}` as `params=`, which requests cannot serialise. Converted to
  proper dicts.
- `olap()` still constructed the URL via string concatenation — moved to
  `params=`.
- `Transport.get_token()` constructed JSON via string concatenation instead of
  a proper dict.
- `Transport.token()` called `self._token()` (treating the token dict as a
  callable).
- `Transport` imported `order` from a non-existent `Pyiiko.settings` module.
- All `json.loads('{"key":"' + var + '"}')` patterns replaced with native dicts.
- All `print(e)` calls replaced with `logging.error(...)`.
- Missing `timeout` on several requests in `IikoServer` and `FrontWebAPI`.

## [0.2.15] - 2019-xx-xx

Initial public release.

[Unreleased]: https://github.com/gadzhi/pyiiko/compare/v0.6.0...HEAD
[0.6.0]: https://github.com/gadzhi/pyiiko/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/gadzhi/pyiiko/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/gadzhi/pyiiko/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/gadzhi/pyiiko/compare/v0.2.15...v0.3.0
[0.2.15]: https://github.com/gadzhi/pyiiko/releases/tag/v0.2.15
