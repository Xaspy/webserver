# Xaspy's webserver Xio version 0.2
~~Try to create the most lightweight web-framework~~
___
This is a simple web-framework, which realised routes, but without arguing.
This program can handle requests.

For using web-framework you should:
```
from webserver import Xio
```

Further create object of webserver with his name by first argument:
```
app = Xio(__name__)
```

Create routes to your project, firstly choose path to thing, secondly choose methods available for this (`default: 
methods= ('GET', 'POST', 'DELETE', 'PUT')`):
```
@app.route('/some-path', ['GET'])
def some_throw():
    return 'Hello, my friend!'
```
Nextly runs server! You can choose one optional argument `is_debug`, `host`, `port`  which provides you some info while
server works (`default: is_debug= False, host='localhost', port=80`):
```
app.run(is_debug=True, host='127.0.0.1')
```
___
_Contacts:_

_Voice:_ +79527326662

_VK:_ vk.com/xaspy

_E-mail:_ 20kolpakov01@gmail.com
