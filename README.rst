Описание
========

Библиотека для работы с iikoAPI Server и iikoBiz

Pyiiko is the easy-to-use library for iiko ERP. This library provides a pure Python interface for the iiko
Server API and iikoBiz. iiko company development of innovative systems for HoReCa industry.

Возможности:
1. Получение токена
2. Список подразделений
3. Список пользователей
4. Список событий


Пример:

.. code:: python

    i = Iiko('ваш ip', 'порт', 'имя пользователя', 'пароль')

    i.get_token()


