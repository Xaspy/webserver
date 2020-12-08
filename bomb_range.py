from webserver import Xio

app = Xio(__name__)


@app.route('/kek')
async def get_zero():
    return "234234234dfgffffffffffffsdfffffffff"


app.run(is_debug=True, host='localhost')
