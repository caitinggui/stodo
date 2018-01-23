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
    from apps.models import S, Role
    S.createAllTables()
    Role.initAdmin()


@cli.command("createSuperUser", help="创建超级管理员账号")
def createSuperUser():
    from apps.models import User, Role
    from apps.forms import checkEmail, checkUsername, checkPassword
    # 从数据库绑定admin id
    role_admin = Role.select(Role.id).where(Role.name=="admin").get().id
    if not role_admin:
        return("必须先在Role表中创建管理员角色")
    email = click.prompt("请输入邮箱")
    checkEmail(email)
    name = click.prompt("请输入用户名")
    checkUsername(name)
    password = click.prompt("请输入密码", hide_input=True, confirmation_prompt=True)
    checkPassword(password)
    password = User.generalPassword(password)
    User.create(email=email, name=name, password=password, sex=User.sex.choices.unknown, role_id=role_admin, signature="I am super admin")
    print("成功创建超级管理员账户；%s" % name)


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
