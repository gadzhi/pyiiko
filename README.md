<p align="center"><img src="https://habrastorage.org/webt/bi/od/mp/biodmpylxpnkxhjtewsjro_-8ps.jpeg" height="180"></p>
<p align="center">
<a href="https://badge.fury.io/py/Pyiiko"><img src="https://badge.fury.io/py/Pyiiko.svg" alt="PyPI version" height="18"></a>
<a href="https://app.codeship.com/projects/291583"><img src="https://app.codeship.com/projects/d54f0350-4280-0136-4bbb-762c3d000702/status?branch=master" alt="PyPI version" height="18"></a>
<a href="https://www.apache.org/licenses/LICENSE-2.0"><img src="https://img.shields.io/pypi/l/requests.svg" alt="PyPI version" height="18"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/pypi/pyversions/Django.svg" alt="PyPI version" height="18"></a>


   

# About

Pyiiko is the easy-to-use library for iiko ERP. This library provides a pure Python interface for the iiko Server API, iikoBiz and FrontWebApi.

iiko company development of innovative systems for HoReCa industry.

## Example:

```python
    from Pyiiko import IikoServer

    i = IikoServer(ip = 'your ip', port = 'port', login = 'login', password = 'password')
    i.token()
    
```
