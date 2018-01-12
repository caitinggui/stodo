# coding: utf-8

from sanic import Sanic
from sanic.response import text, json
from sanic.exceptions import RequestTimeout, NotFound


app = Sanic(__name__)


@app.get('/')
def index(request):
    info = """
    "/"  show all the url for this app
    """
    return text(info)


@app.exception(RequestTimeout)
def timeout(request, exception):
    return json({'message': 'Request Timeout'}, 408)


@app.exception(NotFound)
def notfound(request, exception):
    return json(
        {'message': 'Requested URL {} not found'.format(request.url)}, 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=True)
