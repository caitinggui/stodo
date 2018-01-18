# -*- coding: utf-8 -*-

import logging
import time
import datetime

from sanic import Blueprint
from .. import app
from ..models import S, User
from ..auth import login_required
from utils import RetCode, webJson, requestParam, Constant

logger = logging.getLogger(__name__)
user_bp = Blueprint("user")


@user_bp.get("/", name="user_index")
@login_required
async def index(request, **kwargs):
    """使用@login_required后必须加**kwargs参数，因为login_required会给路由函数传入参数"""
    async with request.app.db.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(S.s_alluser)
            data = await cur.fetchall()
    return webJson(data=data)


@user_bp.route("/regist", methods=["GET", "POST"])
async def regist(request):
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


@user_bp.route("/login", methods=["GET", "POST"])
async def login(request):
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
                data = {Constant.token_id: sql_data.id}
                # None表示永不过期，这里用于debug阶段
                data = User.generalToken(data, expiration=None)
                return webJson(data=data)
            else:
                return webJson(RetCode.PARAMETER_ERROR, data="用户名或者密码错误")
    return webJson()


async def ifNameExist(cur, username):
    logger.debug("sql: %s, %s", S.s_username, username)
    await cur.execute(S.s_username, (username,))
    data = await cur.fetchone()
    if data:
        return True
    return False
