Xaspy's webserver Xio version 1 02/01/2021


GENERAL USAGE NOTES:
--------------------

This is a simple web-framework, which realised routes.
This program can handle requests.

For using web-framework you should:

	from webserver import Xio


Further create object of webserver with his name by first argument:

	app = Xio(__name__)


Create routes to your project, firstly choose path to thing, secondly choose
methods available for this (default: methods= ('GET', 'POST', 'DELETE', 'PUT')):

	@app.route('/some-path', ['GET'])
	async def some_throw():
    		return 'Hello, my friend!'

You can create parametric routes:

	@app.route('/lol/<key>')
	async def get_second_argument(key):
    		return key


Nextly runs server!:

	app.run(port=80, host='localhost', is_debug=False,
                is_comp=False, is_ssl=False, cert='selfsigned.cert',
                key='selfsigned.key', connection_timeout=0.0001)

	port - port of server
	host - address of server
 	is_debug - debug mode which can give you more information about working server
	is_comp - compress mode which can compress data by gzip
	is_ssl - creates https server
	cert - cert file for ssl
	key - key file for ssl
	connection_timeout - set timeout for connection


----------------------------------------------------------------

This script works under Linux, MacOS, Windows by Python 3.
================================================================


Contacts:

Voice: +79527326662
VK: vk.com/xaspy
E-mail: 20kolpakov01@gmail.com