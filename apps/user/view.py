# -*- coding: utf-8 -*-

import logging
import time
import datetime

from sanic import Blueprint
from .. import app
from ..models import S, User
from ..auth import login_required
from ..baseview import BaseView
from utils import RetCode, webJson, requestParam, Constant, ParamsError

logger = logging.getLogger(__name__)
user_bp = Blueprint("user")


class UserView(BaseView):

    # TODO 还需添加管理员判断
    def ifOwnerOrAdmin(self, user_id, real_user_id):
        if user_id != real_user_id:
            raise ParamsError("用户id与认证不符")

    @staticmethod
    @login_required
    async def get(request, **kwargs):
        """获取单个用户的信息"""
        real_user_id = request[Constant.auth_info][Constant.user_id]
        return webJson(data=request.get(Constant.auth_info))
        self.ifOwnerOrAdmin(user_id, real_user_id)
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(S.s_user_info, (user_id,))
                data = await cur.fetchone()
        return webJson(data=data)

    async def post(self, request, **kwargs):
        """登陆, 不需要权限控制"""
        name = requestParam(request, 'name')
        password = requestParam(request, 'password')
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(S.s_password, (name,))
                logger.debug("sql: %s: %s", S.s_password, name)
                sql_data = await cur.fetchone()
                if not sql_data:
                    return webJson(RetCode.PARAMETER_ERROR, data="无此用户")
                logger.debug("sql data: %s", sql_data)
                logger.debug(User.generalPassword(password))
                if User.verifyPassword(password, sql_data.password):
                    data = {Constant.user_id: sql_data.id}
                    # None表示永不过期，这里用于debug阶段
                    data = User.generalToken(data, expiration=None)
                    return webJson(data=data)
                else:
                    return webJson(RetCode.PARAMETER_ERROR, data="用户名或者密码错误")
        return webJson()

    @staticmethod
    @login_required
    async def delete(request, **kwargs):
        """注销，并非登出"""
        real_user_id = request[Constant.auth_info][Constant.user_id]
        self.ifOwnerOrAdmin(user_id, real_user_id)
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(S.d_user, (user_id,))
            await conn.commit()
        return webJson(data=user_id)

    @staticmethod
    @login_required
    async def put(request, **kwargs):
        """修改用户信息"""
        pass


class UserListView(BaseView):

    @staticmethod
    @login_required
    async def get(request, **kwargs):
        """获取群组用户列表"""
        # TODO 需要认证是否为管理员
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(S.s_alluser)
                data = await cur.fetchall()
        return webJson(data=data)

    async def post(self, request, **kwargs):
        """注册"""
        name = requestParam(request, 'name')
        password = requestParam(request, 'password')
        age = requestParam(request, "age", User.age.default)
        sex = requestParam(request, "sex", User.sex.choices.unknown)
        created_time = datetime.datetime.now()
        logger.info("args: %s", request.args)
        async with request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                if_name_exist = await ifNameExist(cur, name)
                if if_name_exist:
                    return webJson(RetCode.PARAMETER_ERROR, data="用户名已存在")
                logger.info("start to regist")
                password = User.generalPassword(password)
                await cur.execute(S.i_user, (name, password, age, sex, created_time))
            await conn.commit()
        user = {"name": name}
        return webJson(data=user)


async def ifNameExist(cur, username):
    logger.debug("sql: %s, %s", S.s_username, username)
    await cur.execute(S.s_username, (username,))
    data = await cur.fetchone()
    if data:
        return True
    return False


user_bp.add_route(UserView.as_view(), '/user')
user_bp.add_route(UserListView.as_view(), "/")
