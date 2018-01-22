# -*- coding: utf-8 -*-

import logging
import time
import datetime

from sanic import Blueprint
from .. import app
from ..models import S, User
from ..auth import login_required
from ..baseview import BaseView
from .forms import postUserListView
from utils import RetCode, webJson, requestParam, Constant, ParamsError, datetime2str

logger = logging.getLogger(__name__)
user_bp = Blueprint("user")


class TokenView(BaseView):

    # TODO 还需添加管理员判断
    def ifOwnerOrAdmin(self, user_id, real_user_id):
        if user_id != real_user_id:
            raise ParamsError("用户id与认证不符")

    @staticmethod
    @login_required
    async def get(request, **kwargs):
        """获取登陆信息"""
        user_id = request[Constant.auth_info][Constant.user_id]
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(S.s_user_login_info, (user_id,))
                data = await cur.fetchone()
                if data:
                    data.last_login = datetime2str(data.last_login)
        return webJson(data=data)

    async def post(self, request, **kwargs):
        """登陆, 不需要权限控制"""
        name = request.form.get("name")
        password = request.form.get("password")
        if None in (name, password):
            return webJson(RetCode.PARAMETER_NOT_ENOUGH)
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(S.s_password, (name, name))
                logger.debug("sql: %s: %s", S.s_password, name)
                sql_data = await cur.fetchone()
                if not sql_data:
                    return webJson(RetCode.PARAMETER_ERROR, data="无此用户")
                logger.debug("sql data: %s", sql_data)
                if User.verifyPassword(password, sql_data.password):
                    data = {Constant.user_id: sql_data.id}
                    data = User.generalToken(data, expiration=Constant.expires_in_login)
                    return webJson(data=data)
                else:
                    return webJson(RetCode.PARAMETER_ERROR, data="用户名或者密码错误")
        return webJson()

    @staticmethod
    @login_required
    async def delete(request, **kwargs):
        """登出"""
        return webJson(RetCode.INCOMPLETE)

    @staticmethod
    @login_required
    async def put(request, **kwargs):
        """修改登陆信息"""
        return webJson(RetCode.INCOMPLETE)


class UserListView(BaseView):

    @staticmethod
    @login_required
    async def get(request, **kwargs):
        """获取群组用户列表或者当前用户信息"""
        user_id_args = request.args.get("user_id")
        user_id = request[Constant.auth_info][Constant.user_id]
        logger.info("user_id: %s, user_id_args: %s", user_id, user_id_args)
        # 查看自己的用户信息
        if user_id_args:
            if user_id_args == str(user_id):
                async with request.app.db.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(S.s_user_info, (user_id))
                        data = await cur.fetchone()
                if data:
                    data.last_login = datetime2str(data.last_login)
                    data.created_time = datetime2str(data.created_time)
                    data.updated_time = datetime2str(data.updated_time)
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
                    await cur.execute(S.s_user_info, (user_id_args))
                    data = await cur.fetchone()
                else:
                    await cur.execute(S.s_alluser)
                    data = await cur.fetchall()
        return webJson(data=data)

    async def post(self, request, **kwargs):
        """注册"""
        form = postUserListView(request)
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                if_name_exist = await ifNameExist(cur, form.name)
                if if_name_exist:
                    return webJson(RetCode.PARAMETER_ERROR, data="用户名已存在")
                logger.info("start to regist")
                await cur.execute(
                    S.i_user,
                    (form.name, form.password, form.email, form.age,\
                     form.sex, form.city, form.signature, form.created_time,
                     form.updated_time, form.last_login))
            await conn.commit()
        user = {"name": form.name}
        return webJson(data=user)

    @staticmethod
    @login_required
    async def delete(request, **kwargs):
        """注销，非登出"""
        user_id = request[Constant.auth_info][Constant.user_id]
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(S.d_user, (user_id,))
            await conn.commit()
        return webJson(data=user_id)

    @staticmethod
    @login_required
    async def put(request, **kwargs):
        """更新用户信息"""
        return webJson(RetCode.INCOMPLETE)


async def ifNameExist(cur, username):
    logger.debug("sql: %s, %s", S.s_username, username)
    await cur.execute(S.s_username, (username,))
    data = await cur.fetchone()
    if data:
        return True
    return False


user_bp.add_route(UserListView.as_view(), "/")
user_bp.add_route(TokenView.as_view(), '/token')
