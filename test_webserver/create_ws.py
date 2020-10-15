from webserver import Xio

app = Xio(__name__)


@app.route('/test-page')
def test_page():
    return 'all-right'


@app.route('/test-page-get')
def test_page():
    return 'get ok'


@app.route('/test-page-post')
def test_page():
    return 'post ok'


def start_server(port):
    app.run(port=port)


if __name__ == '__main__':
    pass
