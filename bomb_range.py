from webserver import Xio
from flask import Flask

app = Xio(__name__)
app2 = Flask(__name__)


@app.route('/lol/<key>')
async def get_zero(key):
    return key


app.run(host='localhost')
