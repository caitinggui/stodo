# -*- coding: utf-8 -*-

import logging

from sanic import Blueprint
from .. import app
from utils import RetCode, webJson

logger = logging.getLogger(__name__)
main_bp = Blueprint("main")


@main_bp.get("/")
async def index(request):
    main_url = app.url_for("main.index")
    users = app.url_for("user.UserListView")
    user = app.url_for("user.UserView")
    todos = app.url_for("todo.TodoListView")
    info = {
        f'{main_url}': "show all the url for this app",
        f"{users}": "POST: 注册",
        f"{user}": "POST: 登陆; GET: 查看当前用户信息; PUT: 更新用户信息, DELETE: 注销用户, 非登出",
        f"{todos}": "所有计划的事情"
    }
    return webJson(data=info)
