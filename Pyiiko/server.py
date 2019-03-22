# -*- coding: utf-8 -*-
import requests
import hashlib
from lxml import etree
from io import StringIO

DEFAULT_TIMEOUT = 4


class IikoServer:
    """Класс отвечающий за работы с iikoSeverApi


    """

    def __init__(self, ip=None, login=None, password=None, token=None):

        self.login = login
        self.password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        self.address = 'http://' + ip + '/resto/'
        self._token = (token or self.get_token())

    def token(self):
        return self._token

    def get_token(self):
        """Метод получает новый токен
        .. note::

            при авторизации вы занимаете один слот лицензии. Token,
            который вы получаете при авторизации, можно использовать до того момента,
             пока он не протухнет ( не перестанет работать). И если у вас только одна
             лицензия сервера, а вы уже получили token, следующее обращение к серверу за
             token-ом вызовет ошибку. Если вам негде хранить token при работе с сервером API,
             рекомендуем вам разлогиниться, что приводит к отпусканию лицензии.

            """

        try:
            url = self.address + 'api/auth?login=' + self.login + "&pass=" + self.password
            return requests.get(url=url, timeout=DEFAULT_TIMEOUT).text

        except Exception as e:
            print(e)

    def quit_token(self):
        """Уничтожение токена

        """

        try:
            logout = requests.get(
                self.address + 'api/logout?key=' + self._token)
            print("\nТокен уничтожен: " + self._token)
            return logout

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def version(self):
        """Позволяет узнать версию iiko

        :returns: Версия iiko в формате string
        """
        try:
            ver = requests.get(
                self.address + 'get_server_info.jsp?encoding=UTF-8').text
            tree = etree.parse(StringIO(ver))
            version = ''.join(tree.xpath(r'//version/text()'))
            return version

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def server_info(self):
        """Вовращает json файл с информацией о сервере и статусе лицензии

                :returns: Информация о сервере в формате json
                """
        try:
            return requests.get(
                self.address + 'get_server_info.jsp?encoding=UTF-8').json

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    "----------------------------------Корпорации----------------------------------"

    def departments(self):
        """Иерархия подразделений

        .. csv-table:: Типы подразделений
           :header: "Код", "Наименование"
           :widths: 15, 20

           "CORPORATION", Корпорация
           "JURPERSON", Юридическое лицо
           ORGDEVELOPMENT, Структурное подразделение
           DEPARTMENT, Торговое предприятие
           MANUFACTURE, Производство
           CENTRALSTORE, Центральный склад
           CENTRALOFFICE, Центральный офис
           SALEPOINT, Точка продаж
           STORE, Склад


        """
        try:
            urls = self.address + "api/corporation/departments?key=" + self._token
            return requests.get(url=urls, timeout=DEFAULT_TIMEOUT).content
        except Exception as e:
            print(e)

    def stores(self):
        """Список складов

        :returns: Все склады ТП в виде структуры corporateItemDto


        """
        try:
            ur = self.address + 'api/corporation/stores?key=' + self._token
            return requests.get(ur, timeout=DEFAULT_TIMEOUT).text
        except Exception as e:
            print(e)

    def groups(self):
        """Список групп и отделений

        :returns: Все группы отделений, отделения и точки продаж ТП в виде структуры groupDto. \
                    В группе отделений может быть несколько точек продаж, но главная касса
                    (свойство groupDto/pointOfSaleDtoes/pointOfSaleDto/main=true) может быть подключена только
                    к одной из них. В iikoChain информация о кассе точки продаж
                    (groupDto/pointOfSaleDtoes/pointOfSaleDto/cashRegisterInfo) может отсутствовать.
        """
        try:
            ur = self.address + 'api/corporation/groups?key=' + self._token
            return requests.get(ur, timeout=DEFAULT_TIMEOUT)

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def terminals(self):
        """Список терминалов.

        :returns: Все терминалы ТП в виде структуры terminalDto. Как правило, интересны только фронтовые \
                    терминалы, см. поиск терминалов /corporation/terminal/search
        """
        try:
            ur = self.address + 'api/corporation/terminals?key=' + self._token
            return requests.get(ur, timeout=DEFAULT_TIMEOUT).content

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def departments_find(self, code):
        """Поиск подразделения.

        :param name: (optional) Код торгового предприятия. Значение элемента <code> из структуры corporateItemDto \
                                    Регулярное выражение. Если задать просто строку, то ищет любое вхождение этой строки в код ТП с учетом регистра


        :type code: [departmentCode]

        :returns: Структура corporateItemDto, если существует подразделение с данным кодом. \
                    Поиск торгового предприятия по коду. Имеет смысл только для подразделений с типом DEPARTMENT \
                    и в основном только в iikoChain, т.к. в рамках iikoRMS только одна сущность с таким типом
        """
        try:
            ur = self.address + 'api/corporation/departments/search?key=' + self._token
            return requests.get(
                ur, params=code, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def stores_find(self, code):
        """Список складов.


        :param code: Код склада - регулярное выражение. Если задать просто строку, то ищет любое вхождение \
                        этой строки в код склада с учетом регистра.
        :type code: [storeCode]

        :returns: corporateItemDto, если существует склад с данным кодом. Поиск склада по коду. Для работы этого \
                    метода  необходимо, чтобы коды складов в ТП были заполнены (данное поле является необязательным \
                    и по умолчанию пусто
        """
        try:
            ur = self.address + 'api/corporation/stores/search?key=' + self._token
            return requests.get(ur, params=code)

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def groups_search(self, **kwargs):
        """Поиск групп отделений.


        :param name: Название группы.
        :type name: regex
        :param departmentId: ID подразделения
        :type departmentId: string
        """
        try:
            urls = self.address + 'api/corporation/terminal/search?key=' + self._token
            return requests.get(
                url=urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def terminals_search(self, anonymous=False, **kwargs):
        """Поиск терминала.


        :param anonymous: (bool) Фронты имеют anonymous=false, бекофисы и системные терминалы — true.
        :param name: (regex) - (optional) Имя терминала в том виде, как он отображается в бекофисе.
        :param computerName: (regex) - (optional) Имя компьютера

        :return: Список terminalDto, если существуют подходящие терминалы
        """
        try:
            urls = self.address + 'api/corporation/terminal/search?key=' + self._token + '&anonymous=' + anonymous
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------Работники----------------------------------"

    def employees(self):
        """Работники"""
        try:
            urls = self.address + 'api/employees?key=' + self._token
            return requests.get(urls, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------События----------------------------------"

    def events(self, **kwargs):
        """Список событий.


        :param from_time: (yyyy-MM-ddTHH:mm:ss.SSS) - (optional) Время с которого запрашиваются события, в формате ISO: yyyy-MM-ddTHH:mm:ss.SSS, по-умолчанию – начало текущих суток.
        :param to_time: (yyyy-MM-ddTHH:mm:ss.SSS) - (optional) Время по которое (не включительно) запрашиваются \
        события в формате ISO: yyyy-MM-ddTHH:mm:ss.SSS,, по-умолчанию граница не установлена.
        :param from_rev: (int) - (optional) Ревизия, с которой запрашиваются события, число. Каждый ответ \
        содержит тэг revision, значение которого соответствует ревизии, по которую включительно отданы события; \
        при новых запросах следует использовать revision + 1 (revision из предыдущего ответа) для получения только \
        новых событий. В штатном режиме одно и тоже событие повторно с разными ревизиями не приходит, однако \
        такой гарантии не даётся. ID (UUID) события уникален, может использоваться в качестве ключа.

        :return: Список событий в формате eventsList (см. XSD Список событий)
        """
        try:
            ur = self.address + 'api/events?key=' + self._token
            return requests.get(
                ur, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def events_filter(self, body):
        """
        Список событий по фильтру событий и номеру заказа.


        :param body: Список id событий, по которым производится фильтрация (application/xml).

        Пример body

        .. code-block:: xml

            <eventsRequestData>
                <events>
                    <event>orderCancelPrecheque</event>
                    <event>orderPaid</event>
                </events>
                <orderNums>
                    <orderNum>175658</orderNum>
                </orderNums>
            </eventsRequestData>

        :return: Дерево событий в формате groupsList (см. XSD Дерево событий).
        """

        try:
            ur = self.address + 'api/events?key=' + self._token
            return requests.post(
                ur, data=body, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def events_meta(self):
        """
        Дерево событий.


        """
        try:
            urls = self.address + 'api/events/metadata?key=' + self._token
            return requests.get(urls, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------Продукты----------------------------------"

    def products(self, includeDeleted=True):
        """Номенклатура.

        .. csv-table:: Тип элемента номенклатуры
           :header: "Код", "Наименование"
           :widths: 15, 20

           "GOODS", "Товар"
           "DISH", Блюдо
           PREPARED, Заготовка
           SERVICE, Услуга
           MODIFIER, Модификатор
           OUTER, Внешние товары
           PETROL, Топливо
           RATE, Тариф

        .. csv-table:: Типы групп продукта
           :header: "Код", "Наименование", Комментарий
           :widths: 15, 20, 20

           "PRODUCTS", "Продукт",
           "MODIFIERS", Модификатор, "Используется только в номенклатуре, которая загружается /
           и выгружается в/из RKeeper/StoreHouse"


        :param includeDeleted: (bool) - (optional) Включать ли удаленные элементы номенклатуры в результат. По умолчанию false. Реализовано в 5.0 и новее.

        """
        try:
            urls = self.address + 'api/products?key=' + self._token
            return requests.get(
                urls, params=includeDeleted, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def products_find(self, **kwargs):
        """Поиск номенклатуры

        :param includeDeleted: (bool) Включать ли удаленные элементы номенклатуры в результат. По умолчанию false. Реализовано в 5.0 и новее.
        :param name: (regex) - (optional) Название.
        :param code: (regex) - (optional) Код быстрого набора в IikoFront.
        :param mainUnit: (regex) - (optional) Базовая единица измерения.
        :param num: (regex) - (optional) Артикул.
        :param cookingPlaceType: (regex) - (optional) Тип места приготовления.
        :param productGroupType: (regex) - (optional) Тип родительской группы.
        :param productType: (regex) - (optional) Тип номенклатуры.

        Выгрузка и поиск идет по всем неудаленным элементам номенклатуры. Включая товары поставщика. Т.к. сейчас нет возможности удалить товар поставщика, то выгрузка потянет все товары поставщика, даже те, которые реально не используются и не участвуют ни в одной связке товар у нас - товар поставщика.

        """
        try:
            urls = self.address + 'api/products/search/?key=' + self._token
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------Поставщики----------------------------------"

    def suppliers(self):
        """Список всех поставщиков

        :return: Список всех поставщиков. Структура employees
        """
        try:
            urls = self.address + 'api/suppliers?key=' + self._token
            return requests.get(urls, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def suppliers_find(self, name='', code=''):
        """Поиск поставщика

        :param name: (regex) - (optional) регулярное выражение имени поставщика.
        :param code: (regex) - (optional) регулярное выражение кода поставщика.

        :return: Список найденных поставщиков. Структура employees (см. XSD Сотрудники)
        """
        try:
            urls = self.address + 'api/suppliers?key=' + self._token
            payload = {'name': name, 'code': code}
            return requests.get(
                urls, params=payload, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def suppliers_price(self, code, date=None):
        """Поиск поставщика

        :param code: (date - DD.MM.YYYY) - (optional) Дата начала действия прайс-листа, необязательный. Если параметр не указан, возвращается последний прайс-лист.
        """
        try:
            urls = self.address + '/resto/api/suppliers/' + code + '/pricelist?key=' + self._token
            return requests.get(
                urls, params=date, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------Отчеты----------------------------------"

    def olap(self, report=None, **kwargs):
        """OLAP-отчет

        :param report: (Тип отчета)
            | ``SALES`` - По продажам.
            | ``TRANSACTIONS`` - По транзакциям.
            | ``DELIVERIES`` - По доставкам.
            | ``STOCK`` - Контролю хранения.
        :param groupRow: (Поля группировки) например:
            ``groupRow=WaiterName&groupRow=OpenTime.``

            Для определения списка доступных полей см.
                - Описание полей OLAP отчета по продажам.
                - Описание полей OLAP отчета по проводкам.
                - Описание полей OLAP отчета по доставкам.
            По полю можно проводить группировку, если значение в колонке Grouping для поля равно true.

        :param groupCol: Поля для выделения значений по колонкам.

            Для определения списка доступных полей см.
                - Описание полей OLAP отчета по продажам.
                - Описание полей OLAP отчета по проводкам.
                - Описание полей OLAP отчета по доставкам.
            По полю можно проводить группировку, если значение в колонке Grouping для поля равно true.

        :param agr: Поля агрегации, например: agr=DishDiscountSum&agr=VoucherNum

            Для определения списка доступных полей см.
                - Описание полей OLAP отчета по продажам.
                - Описание полей OLAP отчета по проводкам.
                - Описание полей OLAP отчета по доставкам.
            По полю можно проводить группировку, если значение в колонке Grouping для поля равно true.

        :return: Структура report

        """
        try:
            urls = self.address + '/resto/api/reports/'+ report + '?key=' + self._token
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def store_operation(self,
                        stores=None,
                        documentTypes=None,
                        productDetalization=True,
                        showCostCorrections=True,
                        presetId=None):
        """Отчет по складским операциям

        :param dateFrom: (DD.MM.YYYY) Начальная дата.
        :param dateTo: (DD.MM.YYYY) Конечная дата.
        :param stores: (GUID) - (optional) Список складов, по которым строится отчет. Если null или empty, строится по всем складам.
        :param documentTypes: () - (optional) Типы документов, которые следует включать. Если null или пуст, включаются все документы.
        :param productDetalization: (boolean) - (по умолчанию true) Если истина, отчет включает информацию по товарам, но не включает дату. Если ложь - отчет включает каждый документ одной строкой и заполняет суммы документов.
        :param showCostCorrections: (boolean) - Включать ли коррекции себестоимости. Данная опция учитывается только если задан фильтр по типам документов. В противном случае коррекции включаются.
        :param presetId: (GUID) - (optional) Id преднастроенного отчета. Если указан, то все настройки, кроме дат, игнорируются.

        :returns: Структура storeReportPresets (см. XSD Пресеты отчетов по складским операциям).

        """
        try:
            urls = self.address + '/resto/api/reports/storeOperations?key=' + self._token
            return requests.get(
                urls,
                params={
                    stores, documentTypes, productDetalization,
                    showCostCorrections, presetId
                },
                timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def store_presets(self):
        """Пресеты отчетов по складским операциям

        :returns: Структура storeReportPresets (см. XSD Пресеты отчетов по складским операциям).

        """
        try:
            urls = self.address + '/resto/api/reports/storeReportPresets?key=' + self._token
            return requests.get(urls, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def product_expense(self, departament, **kwargs):
        """Расход продуктов по продажам

        :param department: (GUID) Подразделение
        :param dateFrom: (DD.MM.YYYY) Начальная дата.
        :param dateTo: (DD.MM.YYYY) Конечная дата.
        :param hourFrom: (hh) Час начала интервала выборки в сутках (по умолчанию -1, все время), по умолчанию -1.
        :param hourTo: (hh) Час окончания интервала выборки в сутках (по умолчанию -1, все время), по умолчанию -1.

        :returns: Структура dayDishValue (см. XSD Расход продуктов по продажам)
        """
        try:
            urls = self.address + '/resto/api/reports/productExpense?key=' + self._token
            return requests.get(
                urls, params={departament, kwargs},
                timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def sales(self, departament, dishDetails=False, allRevenue=True, **kwargs):
        """Отчет по выручке

        :param department: (GUID) Подразделение
        :param dateFrom: (DD.MM.YYYY) Начальная дата.
        :param dateTo: (DD.MM.YYYY) Конечная дата.
        :param hourFrom: (hh) Час начала интервала выборки в сутках (по умолчанию -1, все время), по умолчанию -1.
        :param hourTo: (hh) Час окончания интервала выборки в сутках (по умолчанию -1, все время), по умолчанию -1.
        :param dishDetails: (boolean) Включать ли разбивку по блюдам (true/false), по умолчанию false.
        :param allRevenue: (boolean)  Фильтрация по типам оплат (true - все типы, false - только выручка), по умолчанию true.

        :returns: Структура dayDishValue (см. XSD Отчет по выручке)
        """

        try:
            urls = self.address + '/resto/api/reports/sales?key=' + self._token + \
                   '&department=' + departament
            return requests.get(
                urls,
                params={dishDetails, allRevenue, kwargs},
                timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def mounthly_plan(self, departament, **kwargs):
        """План по выручке за день

        :param department: (GUID) Подразделение
        :param dateFrom: (DD.MM.YYYY) Начальная дата.
        :param dateTo: (DD.MM.YYYY) Конечная дата.

        :returns: Структура budgetPlanItemDtoes (см. XSD План по выручке за день)


        """
        try:
            urls = self.address + '/resto/api/reports/monthlyIncomePlan?key=' + self._token + \
                   '&department=' + departament
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def ingredient_entry(self, departament, includeSubtree=False, **kwargs):
        """Отчет о вхождении товара в блюдо

        :param department: (GUID) Подразделение
        :param dateFrom: (DD.MM.YYYY) Начальная дата.
        :param dateTo: (DD.MM.YYYY) Конечная дата.
        :param productArticle: (string) Артикул продукта (приоритет поиска:productArticle, product)
        :param includeSubtree: (bool) - (optional) Включать ли в отчет строки поддеревьев (по умолчанию false)

        :returns: Структура budgetPlanItemDtoes (см. XSD План по выручке за день)
        """
        try:
            urls = self.address + '/resto/api/reports/ingredientEntry?key=' + self._token
            return requests.get(
                urls,
                params={departament, includeSubtree, kwargs},
                timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def olap2(self,
              reportType,
              groupingAllowed=False,
              filteringAllowed=False,
              json=None):
        """Поля OLAP-отчета

        :param reportType: (Тип отчета)
            | ``SALES`` - По продажам.
            | ``TRANSACTIONS`` - По транзакциям.
            | ``DELIVERIES`` - По доставкам.
        :param json: (optional) Json с полями
        :type json: json

        .. code-block:: json

           {
              "FieldName":{
                "name":"StringValue",
                "type":"StringValue",
                "aggregationAllowed":"booleanValue",
                "groupingAllowed":"booleanValue",
                "filteringAllowed":"booleanValue",
                "tags":[
                  "StringValue1",
                  "StringValue2",
                  "...",
                  "StringValueN"
                ]
              }
            }

        :param FieldName: Название колонки отчета. Именно это название используется для получения данных отчета
        :type FieldName: string
        :param name: Название колонки отчета в iikoOffice. Справочная информация.
        :type name: string
        :param type: Тип поля. Возможны следующие значения:
        :type type: string


        | ENUM - Перечислимые значения
        | STRING - Строка
        | ID - Внутренний идентификатор объекта в iiko (начиная с 5.0).
        | DATETIME - Дата и время
        | INTEGER - Целое
        | PERCENT - Процент (от 0 до 1)
        | DURATION_IN_SECONDS - Длительность в секундах
        | AMOUNT - Количество
        | MONEY - Денежная сумма

        :param aggregationAllowed: (optional) Если true, то по данной колонке можно агрегировать данные
        :type aggregationAllowed: bool
        :param groupingAllowed: (optional) Если true, то по данной колонке можно группировать данные. По умолчанию false.
        :type groupingAllowed: bool
        :param filteringAllowed: (optional) Если true, то по данной колонке можно фильтровать данные. По умолчанию false.
        :type filteringAllowed: bool
        :param tags: (optional) Список категорий отчета, к которому относится данное поле. Справочная информация. Соответствует списку в верхнем правом углу конструктора отчета в iikoOffice.
        
        :return: Json структура списка полей с информацией по возможностям фильтрации, агрегации и группировки.Устаревшие поля (deprecated) не выводятся.

        """
        try:
            urls = self.address + '/resto/api/v2/reports/olap/columns?key=' + self._token
            return requests.get(
                urls,
                params={reportType, groupingAllowed, filteringAllowed},
                json=json,
                timeout=DEFAULT_TIMEOUT).json()

        except Exception as e:
            print(e)

    def reports_balance(self,
                        timestamp,
                        account=None,
                        counteragent=None,
                        department=None):
        """
        Балансы по счетам, контрагентам и подразделениям

        :param timestamp: учетная-дата время отчета в формате yyyy-MM-dd'T'HH:mm:ss.
        :type timestamp: time
        :param account: (optional)  id счета для фильтрации (можно указать несколько).
        :type timestamp: string
        :param counteragent: (optional) id контрагента для фильтрации (необязательный, можно указать несколько).
        :department: (optional) id подразделения для фильтрации (необязательный, можно указать несколько).
        
        :return: Возвращает количественные (amount) и денежные (sum) остатки товаров (product) на складах (store) на заданную учетную дату-время.
        См. ниже пример результата.

        """
        try:
            urls = self.address + '/resto/reports/balance/counteragents?key=' + self._token
            return requests.get(
                urls,
                params={timestamp, account, counteragent, department},
                timeout=DEFAULT_TIMEOUT).json()

        except Exception as e:
            print(e)

    "----------------------------------Накладные----------------------------------"

    def invoice_in(self, **kwargs):
        """Выгрузка приходных накладных

        :param from: начальная дата (входит в интервал).
        :type from: YYYY-MM-DD
        :param to: конечная  дата (входит в интервал, время не учитывается).
        :type to: YYYY-MM-DD
        :param supplierId: Id поставщика.
        :type supplierId: GUID

        :result: XSD Приходная накладная
        """
        try:
            urls = self.address + '/resto/api/documents/export/incomingInvoice?key=' + self._token
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def invoice_out(self, **kwargs):
        """Выгрузка расходных накладных

        :param from: начальная дата (входит в интервал).
        :type from: YYYY-MM-DD
        :param to: конечная  дата (входит в интервал, время не учитывается).
        :type to: YYYY-MM-DD
        :param supplierId: Id поставщика.
        :type supplierId: (optional) GUID

        При запросе без постащиков возвращает все расходные накладные, попавшие в интервал.

        :result: XSD Приходная накладная
        """
        try:
            urls = self.address + '/resto/api/documents/export/outgoingInvoice?key=' + self._token
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def invoice_number_in(self, current_year=True, **kwargs):
        """Выгрузка приходной накладной по ее номеру

        :param number: номер документа.
        :type number: string
        :param from: (optional) начальная дата (входит в интервал).
        :type from: YYYY-MM-DD
        :param to: (optional) конечная  дата (входит в интервал, время не учитывается).
        :type to: YYYY-MM-DD
        :param currentYear: только за текущий год (по умолчанию True).
        :type supplierId: Boolean

        .. note::
            При currentYear = true, вернет документы с указанным номером документа только за текущий год. Параметры from и to должны отсутствовать.

            При currentYear = false параметры from и to должны быть указаны.


        """

        try:
            urls = self.address + '/resto/api/documents/export/incomingInvoice/byNumber?key=' \
                   + self._token + '&currentYear' + current_year
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def invoice_number_out(self, current_year=True, **kwargs):
        """Выгрузка расходной накладной по ее номеру.


        :param number: номер документа.
        :type number: string
        :param from: (optional) начальная дата (входит в интервал).
        :type from: YYYY-MM-DD
        :param to: (optional) конечная  дата (входит в интервал, время не учитывается).
        :type to: YYYY-MM-DD
        :param currentYear: только за текущий год (по умолчанию True).
        :type supplierId: Boolean

        .. note::
            При currentYear = true, вернет документы с указанным номером документа только за текущий год. Параметры from и to должны отсутствовать.

            При currentYear = false параметры from и to должны быть указаны.
        """

        try:
            urls = self.address + '/resto/api/documents/export/outgoingInvoice/byNumber?key=' \
                   + self._token + '&currentYear' + current_year
            return requests.get(
                urls, params=kwargs, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def production_doc(self, xml):
        """Загрузка акта приготовления"""
        try:
            target_url = self.address + '/api/documents/import/productionDocument?key' + self._token
            headers = {'Content-type': 'text/xml'}
            return requests.post(
                target_url, body=xml, headers=headers,
                timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------Получение данных по кассовым сменам:----------------------------------"

    def close_session(self, dateFrom=None, dateTo=None):
        """Список кассовых смен

        :param dateFrom: (DD.MM.YYYY) Начальная дата.
        :param dateTo: (DD.MM.YYYY) Конечная дата.

        :returns: Список всех кассовых смен в заданном интервале. В формате CloseSessionDto.

        """
        try:
            urls = self.address + 'resto/api/closeSession/list?key=' \
                   + self._token
            return requests.get(
                urls, params={dateFrom, dateTo},
                timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    def session(self, from_time=None, to_time=None):
        """Информация о кассовых сменах

        :param from_time: Время с которого запрашиваются данные по кассовым сменам, в формате ISO.
        :type from: yyyy-MM-ddTHH:mm:ss.SSS
        :param to_time:  Время по которое (не включительно) запрашиваются данные по кассовым сменам в формате ISO.
        :type to: yyyy-MM-ddTHH:mm:ss.SSS

        :returns: Информация о кассовых сменах

        """
        try:
            urls = self.address + '/resto/api/events/sessions?key=' \
                   + self._token
            return requests.get(
                urls, params={from_time, to_time},
                timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)

    "----------------------------------EDI----------------------------------"

    def edi(self, edi, gln=None, inn=None, kpp=None, name=None):
        """Список заказов для участника EDI senderId и поставщика seller

        :param ediSystem: Идентификатор участника EDI, подключенной к нашему REST API. Каждый участник EDI должен \
            получить свой собственный GUID ключ - идентификатор системы EDI (EdiSystem) для подключения к REST API электронного документооборота iiko. См. "Обмен данными/Системы EDI" в iikoOffce..
        :type ediSystem: GUID
        :param gln: (optional) GLN поставщика . Может отсутствовать, но тогда параметр inn должен быть заполнен.
        :type gln: String
        :param inn: (optional) ИНН (идентификационный номер налогоплательщика). Может отсутствовать, но тогда параметр gln должен быть заполнен.
        :type inn: String
        :param kpp: (optional) КПП (код причины постановки).
        :type kpp: String
        :param name: (optional) Имя поставщика
        :type name: String


        :returns: Высылает список заказов EDI для зарегистрированного в системе iiko участника ediSystem и указанного поставщика. \
                    В списке присутствуют также те отмененные на стороне iiko заказы, получение которых участник подтвердил ранее. \
                    Получение как отправленных, так и отмененных заказов требуется подтверждать, см. метод edi/{ediSystem}/orders/ack

        """

        try:
            urls = self.address + 'edi/' + edi + '/orders/bySeller'
            payload = {'gln': gln, 'inn': inn, 'kpp': kpp, 'name': name}
            return requests.get(
                urls, params=payload, timeout=DEFAULT_TIMEOUT).content

        except Exception as e:
            print(e)
