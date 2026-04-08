<p align="center">
  <img src="https://habrastorage.org/webt/bi/od/mp/biodmpylxpnkxhjtewsjro_-8ps.jpeg" height="160" alt="pyiiko">
</p>

<h1 align="center">pyiiko</h1>

<p align="center">Python-библиотека для работы с API iiko ERP</p>

<p align="center">
  <a href="https://badge.fury.io/py/Pyiiko"><img src="https://badge.fury.io/py/Pyiiko.svg" alt="PyPI version"></a>
  <a href="https://github.com/gadzhi/pyiiko/actions/workflows/ci.yml"><img src="https://github.com/gadzhi/pyiiko/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://www.apache.org/licenses/LICENSE-2.0"><img src="https://img.shields.io/pypi/l/Pyiiko.svg" alt="License: Apache 2.0"></a>
  <a href="https://pypi.org/project/Pyiiko/"><img src="https://img.shields.io/pypi/pyversions/Pyiiko.svg" alt="Python versions"></a>
</p>

---

## Возможности

- **iiko Server API** — on-premise установки (складской учёт, номенклатура, отчёты OLAP, сотрудники, накладные, EDI)
- **iiko Transport API** — облачный API (организации, терминалы, доставки, города, улицы)
- Автоматический retry на 5xx ошибки (3 попытки с backoff)
- Единая иерархия исключений: `IikoError` → `IikoAuthError` / `IikoAPIError`
- Context manager для автоматического освобождения ресурсов
- Type hints, PEP 561 `py.typed`

## Установка

```bash
pip install Pyiiko
```

**Требования:** Python 3.9+

## Быстрый старт

### iiko Server (on-premise)

```python
from Pyiiko import IikoServer

# Пароль передаётся в виде SHA1-хеша
server = IikoServer(
    ip="https://your-server.example.com:443",
    login="login",
    password="da39a3ee5e6b4b0d3255bfef95601890afd80709",
)

print(server.version())          # "7.8.9"
print(server.departments())      # XML с иерархией подразделений
print(server.products())         # XML с номенклатурой
```

Использование как context manager освобождает токен (лицензионный слот) автоматически:

```python
with IikoServer(ip="...", login="...", password="...") as server:
    stores = server.stores()
    employees = server.employees()
# токен уничтожен, лицензия освобождена
```

Если токен уже получен — передайте его напрямую, чтобы не делать лишний запрос:

```python
server = IikoServer(ip="https://...", token="your-existing-token")
```

### iiko Transport (Cloud)

```python
from Pyiiko import Transport

client = Transport(key="your-api-login-key")

orgs = client.organization()
terminals = client.terminal(org_id="org-guid-...")
cities = client.cities(org_id="org-guid-...")
```

Создание доставки:

```python
order = {
    "organizationId": "org-guid-...",
    "order": {
        "phone": "+79001234567",
        "deliveryPoint": {"coordinates": {"latitude": 55.75, "longitude": 37.61}},
        "items": [{"productId": "product-guid-...", "amount": 1}],
    },
}
response = client.delivery_create(order_info=order)
```

## Обработка ошибок

```python
from Pyiiko import IikoServer, IikoAuthError, IikoAPIError

try:
    server = IikoServer(ip="...", login="user", password="wrong")
except IikoAuthError:
    print("Неверные учётные данные")

try:
    data = server.departments()
except IikoAPIError as e:
    print(f"Ошибка API: HTTP {e.status_code}")
```

| Исключение | Когда возникает |
|---|---|
| `IikoError` | Базовый класс всех ошибок pyiiko |
| `IikoAuthError` | Неверный логин/пароль, пустой токен |
| `IikoAPIError` | Сервер вернул HTTP 4xx/5xx |

## Справочник методов

### `IikoServer`

| Метод | Описание |
|---|---|
| `version()` | Версия iiko сервера |
| `server_info()` | Информация о сервере и лицензии |
| `departments()` | Иерархия подразделений |
| `stores()` | Список складов |
| `groups()` | Группы и отделения |
| `terminals()` | Список терминалов |
| `terminals_search(anonymous, **kwargs)` | Поиск терминалов |
| `employees()` | Сотрудники |
| `products(includeDeleted)` | Номенклатура |
| `products_find(**kwargs)` | Поиск по номенклатуре |
| `suppliers()` | Поставщики |
| `suppliers_find(name, code)` | Поиск поставщиков |
| `suppliers_price(code, date)` | Прайс-лист поставщика |
| `events(**kwargs)` | События |
| `events_filter(body)` | События по фильтру XML |
| `olap(report, data_from, data_to, **kwargs)` | OLAP-отчёт v1 |
| `olap2(body)` | OLAP-отчёт v2 (JSON) |
| `sales(departament, **kwargs)` | Отчёт по выручке |
| `product_expense(departament, **kwargs)` | Расход продуктов |
| `store_operation(**kwargs)` | Складские операции |
| `reports_balance(timestamp, **kwargs)` | Балансы по счетам |
| `invoice_in(**kwargs)` | Приходные накладные |
| `invoice_out(**kwargs)` | Расходные накладные |
| `invoice_number_in(current_year, **kwargs)` | Приходная накладная по номеру |
| `invoice_number_out(current_year, **kwargs)` | Расходная накладная по номеру |
| `production_doc(xml)` | Загрузка акта приготовления |
| `close_session(dateFrom, dateTo)` | Кассовые смены |
| `edi(edi, **kwargs)` | EDI заказы |
| `quit_token()` | Уничтожить токен / освободить лицензию |

### `Transport`

| Метод | Описание |
|---|---|
| `organization()` | Список организаций |
| `terminal(org_id)` | Терминальные группы |
| `regions(org_id)` | Регионы доставки |
| `cities(org_id)` | Города |
| `streets_by_city(org_id, city)` | Улицы города |
| `delivery_create(order_info)` | Создать доставку |
| `check_create(order_info)` | Валидировать заказ перед созданием |
| `by_id(org_id, order_id)` | Доставка по ID |
| `by_delivery_date(org_id, delivery_date_from)` | Доставки по дате |
| `by_revision(org_id, revision)` | Доставки с ревизии |

## Разработка

```bash
git clone https://github.com/gadzhi/pyiiko.git
cd pyiiko
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest --cov=Pyiiko
```

Тесты не требуют подключения к серверу — HTTP замокан через `responses`.

Подробности в [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

Смотрите [CHANGELOG.md](CHANGELOG.md).

## Лицензия

[Apache License 2.0](LICENSE)
