# coding: utf-8

import logging

from sanic import Sanic
from sanic.exceptions import RequestTimeout, NotFound

from apps import createApp
from utils import RetCode, webJson


logger = logging.getLogger("apps")
app = createApp()


@app.exception(RequestTimeout)
def timeout(request, exception):
    return webJson(RetCode.REQUEST_TIMEOUT)


@app.exception(NotFound)
def notfound(request, exception):
    return webJson(RetCode.NOT_FOUND)


@app.exception(Exception)
def serverError(request, exception):
    logger.exception(exception)
    return webJson(RetCode.SERVER_ERROR)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=True)
