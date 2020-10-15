Xaspy's webserver Xio version 0.2 15/10/2020


GENERAL USAGE NOTES:
--------------------

This is a simple web-framework, which realised routes, but without arguing.
This program can handle requests.

For using web-framework you should:

	from webserver import Xio


Further create object of webserver with his name by first argument and his
address by optional second argument (default = 'localhost'):

	app = Xio(__name__, host='127.0.0.1')


Create routes to your project, firstly choose path to thing, secondly choose
methods available for this (default = ('GET', 'POST', 'DELETE', 'PUT')):

	@app.route('/some-path', ['GET'])
	def some_throw():
    		return 'Hello, my friend!'

Nextly runs server! You can choose one optional argument `is_debug` which provides you some info while server works (
default = False):

	app.run(is_debug=True)

----------------------------------------------------------------

This script works under Linux, MacOS, Windows by Python 3.
================================================================


Contacts:

Voice: +79527326662
VK: vk.com/xaspy
E-mail: 20kolpakov01@gmail.com