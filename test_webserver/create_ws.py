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


def start_server(port):
    app.run(port=port)
