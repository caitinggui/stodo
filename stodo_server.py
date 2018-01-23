# coding: utf-8

import logging
import click

from sanic.exceptions import RequestTimeout, NotFound, InvalidUsage

from apps import createApp
from utils import RetCode, webJson, ParamsError, TokenError


logger = logging.getLogger("apps")
app = createApp()


@app.exception(RequestTimeout)
def timeout(request, exception):
    return webJson(RetCode.REQUEST_TIMEOUT)


@app.exception(NotFound)
def notfound(request, exception):
    return webJson(RetCode.NOT_FOUND)


@app.exception(InvalidUsage)
def invalidUsage(request, exception):
    return webJson(RetCode.NOT_FOUND, data="请求方法有误")


@app.exception(ParamsError)
def paramsError(request, exception):
    return webJson(RetCode.PARAMETER_ERROR, data=exception.data)


@app.exception(TokenError)
def paramsError(request, exception):
    return webJson(RetCode.TOKEN_ERROR, data=exception.data)


@app.exception(Exception)
def serverError(request, exception):
    logger.exception(exception)
    return webJson(RetCode.SERVER_ERROR)


@click.group()
def cli():
    pass


@cli.command(help="初始化数据库")
def initdb():
    from apps.models import S
    S.createAllTables()


@cli.command(help="运行server")
@click.option("--host", default="0.0.0.0", help="The interface to bind to.")
@click.option("--port", default=8090, help="The port to bind to.")
@click.option('--debug/--no-debug', default=True, help='Run under debug or not.')
@click.option("--workers", default=1, help="The process that app used")
def run(host, port, debug, workers):
    app.run(host=host, port=port, debug=debug, access_log=False, workers=workers)


@cli.command(help="ipython命令行环境")
def ishell():
    from IPython import embed
    from apps.models import User, Role
    from apps import app
    embed()


if __name__ == "__main__":
    cli()
