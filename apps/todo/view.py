# -*- coding: utf-8 -*-

import logging

from sanic import Blueprint
from .. import app
from ..models import S, User
from ..auth import login_required
from ..baseview import BaseView
from .forms import postTodoListView
from utils import RetCode, webJson, Constant, requestParam, safeInt, datetime2str

logger = logging.getLogger(__name__)
todo_bp = Blueprint("todo")


class TodoView(BaseView):
    decorators = [login_required]

    async def get(self, request, todo_id, **kwargs):
        """获取用户单条todo"""
        user_id = request[Constant.auth_info][Constant.user_id]
        # user_id = request.get("user_id") # 还需求证一下，request共用于同一个线程，还需考虑一个协程在await时，另一个协程去认证，造成前一个协程的user_id被改变
        # 应该不会有上面的问题，因为每个request的args都是不同的, request其实只在sanic/app.handle_request中处理
        # 经过大量的并发实验，该方案可行
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(S.s_user_todo, (user_id, todo_id))
                todo = await cur.fetchone()
                todo = formatTodoInfo(todo)
        return webJson(data=todo)

    async def delete(self, request, todo_id, **kwargs):
        """删除用户单条todo"""
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
        """获取某用户所有todo或者获取所有用户的所有todo"""
        user_id_args = request.args.get("user_id")
        user_id = request[Constant.auth_info][Constant.user_id]
        logger.info("user_id: %s, user_id_args: %s", user_id, user_id_args)
        # 查看自己的用户信息
        if user_id_args:
            if user_id_args == str(user_id):
                async with request.app.db.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(S.s_user_todos, (user_id_args))
                        data = await cur.fetchall()
                        data = formatTodosInfo(data)
                return webJson(data=data)
        # 管理员查看信息
        is_admin = False
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(S.s_user_permission, (user_id))
                data = await cur.fetchone()
                if data:
                    is_admin = User.checkIfAdmin(data.permission)
                if not is_admin:
                    return webJson(RetCode.FORBIDDEN)
                # 如果传入参数有user_id, 那就只看该id信息
                if user_id_args:
                    await cur.execute(S.s_user_todos, (user_id_args))
                    data = await cur.fetchall()
                else:
                    await cur.execute(S.s_all_todo)
                    data = await cur.fetchall()
                data = formatTodosInfo(data)
        return webJson(data=data)

    async def post(self, request, **kwargs):
        """创建todo"""
        form = postTodoListView(request)
        user_id = request[Constant.auth_info][Constant.user_id]
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                logger.info("check if title exists")
                await cur.execute(S.s_todo_title, (form.title, user_id))
                todo = await cur.fetchone()
                if todo:
                    return webJson(RetCode.PARAMETER_ERROR, data=("title exists"))
                logger.info("start to insert todo")
                await cur.execute(
                    S.i_todo, (user_id, form.title, form.detail,
                               form.created_time, form.updated_time))
            await conn.commit()
        return webJson(data=form.title)


def formatTodoInfo(data):
    """data是一个字典"""
    if data:
        data.created_time = datetime2str(data.created_time)
        data.updated_time = datetime2str(data.updated_time)
        return data
    return {}


def formatTodosInfo(data):
    """data是一个列表"""
    if data:
        for i in range(len(data)):
            data[i] = formatTodoInfo(data[i])
        return data
    return {}


todo_bp.add_route(TodoListView.as_view(), '/')
todo_bp.add_route(TodoView.as_view(), "/<todo_id:int>")
