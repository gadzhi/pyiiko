![](https://habrastorage.org/webt/bi/od/mp/biodmpylxpnkxhjtewsjro_-8ps.jpeg)

About
========

Pyiiko is the easy-to-use library for iiko ERP. This library provides a pure Python interface for the iiko Server API, iikoBiz and FrontWebApi.

iiko company development of innovative systems for HoReCa industry.

## Example:

```python
    from Pyiiko import IikoServer

    i = IikoServer(ip = 'your ip', port = 'port', login = 'login', password = 'password')
    i.token()
    
```
