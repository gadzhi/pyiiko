.. pyiiko documentation master file, created by
   sphinx-quickstart on Tue Mar 13 20:32:41 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyiiko's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

**Just Example**::
.. code-block::
    from Pyiiko.server import IikoServer

    i = IikoServer('ваш ip', 'порт', 'Логин', 'пароль')

    token = i.token()


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
