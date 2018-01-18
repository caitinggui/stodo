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
    user_url = app.url_for("user.user_index")
    regist = app.url_for("user.regist")
    login = app.url_for("user.login")
    todos = app.url_for("todo.TodoListView")
    info = {
        f'{main_url}': "show all the url for this app",
        f"{user_url}": "show all users",
        f"{regist}": "regist",
        f"{login}": "login",
        f"{todos}": "all todos for you"
    }
    return webJson(data=info)
