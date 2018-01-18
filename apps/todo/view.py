# -*- coding: utf-8 -*-

import logging

from sanic import Blueprint
from .. import app
from ..models import S
from ..auth import login_required
from utils import RetCode, webJson, Constant, requestParam, safeInt

logger = logging.getLogger(__name__)
todo_bp = Blueprint("todo")


@todo_bp.get("/")
@login_required
async def index(request, **kwargs):
    user_id = kwargs[Constant.auth_info][Constant.token_id]
    async with request.app.db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(S.s_user_todos, (user_id,))
            todos = await cur.fetchall()
    return webJson(data=todos)


@todo_bp.route("/add", methods=["GET", "POST"])
@login_required
async def addTodo(request, **kwargs):
    user_id = kwargs[Constant.auth_info][Constant.token_id]
    title = requestParam(request, "title")
    detail = requestParam(request, "detail")
    async with request.app.db.acquire() as conn:
        async with conn.cursor() as cur:
            logger.info("start to insert todo")
            await cur.execute(S.i_todo, (user_id, title, detail))
        await conn.commit()
    return webJson(data=title)


@todo_bp.post("/delete")
@login_required
async def deleteTodo(request, **kwargs):
    user_id = kwargs[Constant.auth_info][Constant.token_id]
    todo_id = safeInt(request.form.get("todo_id"))
    if not todo_id:
        return webJson(RetCode.PARAMETER_ERROR, data="todo id有误")
    async with request.app.db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(S.s_user_todo, (user_id, todo_id))
            todo = await cur.fetchone()
            if todo:
                await cur.execute(S.d_user_todo, (todo.id,))
            else:
                return webJson(RetCode.PARAMETER_ERROR, data="无此todo")
        await conn.commit()
    return webJson(data=todo.title)