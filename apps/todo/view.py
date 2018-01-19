# -*- coding: utf-8 -*-

import logging

from sanic import Blueprint
from .. import app
from ..models import S
from ..auth import login_required
from ..baseview import BaseView
from utils import RetCode, webJson, Constant, requestParam, safeInt

logger = logging.getLogger(__name__)
todo_bp = Blueprint("todo")


class TodoView(BaseView):
    decorators = [login_required]

    async def get(self, request, todo_id, **kwargs):
        user_id = request[Constant.auth_info][Constant.user_id]
        # user_id = request.get("user_id") # 还需求证一下，request共用于同一个线程，还需考虑一个协程在await时，另一个协程去认证，造成前一个协程的user_id被改变
        # 应该不会有上面的问题，因为每个request的args都是不同的, request其实只在sanic/app.handle_request中处理
        # 经过大量的并发实验，该方案可行
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(S.s_user_todo, (user_id, todo_id))
                todo = await cur.fetchone()
        return webJson(data=todo)

    async def delete(self, request, todo_id, **kwargs):
        user_id = request[Constant.auth_info][Constant.user_id]
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

    async def put(self, request, todo_id, **kwargs):
        """待完善"""
        user_id = request[Constant.auth_info][Constant.user_id]
        form = request.json
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(S.s_user_todo, (user_id, todo_id))
                todo = await cur.fetchone()
        return webJson(data=todo)


class TodoListView(BaseView):
    decorators = [login_required]

    async def get(self, request, **kwargs):
        user_id = request[Constant.auth_info][Constant.user_id]
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(S.s_user_todos, (user_id,))
                todos = await cur.fetchall()
        return webJson(data=todos)

    async def post(self, request, **kwargs):
        user_id = request[Constant.auth_info][Constant.user_id]
        title = requestParam(request, "title")
        detail = requestParam(request, "detail")
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                logger.info("start to insert todo")
                await cur.execute(S.i_todo, (user_id, title, detail))
            await conn.commit()
        return webJson(data=title)


todo_bp.add_route(TodoListView.as_view(), '/')
todo_bp.add_route(TodoView.as_view(), "/<todo_id:int>")
