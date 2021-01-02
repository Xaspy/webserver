from webserver import Xio

app = Xio(__name__)


@app.route('/test-page')
async def test_page():
    return 'all-right'


@app.route('/test-page-get')
async def test_page():
    return 'get ok'


@app.route('/test-page-post', ['POST'])
async def test_page(data):
    return 'post ok ' + data


@app.route('/lol/<key>')
async def get_zero(key):
    return key


def start_server(port, host, is_ssl=False, cert='', key=''):
    app.run(port=port, host=host, is_ssl=is_ssl, cert=cert, key=key)
