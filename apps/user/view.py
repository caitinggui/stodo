# -*- coding: utf-8 -*-

import logging
import time

from sanic import Blueprint
from .. import app
from ..models import S
from utils import RetCode, webJson, requestParam

logger = logging.getLogger(__name__)
user_bp = Blueprint("user")


@user_bp.get("/", name="user_index")
async def index(request):
    async with request.app.db.acquire() as conn:
        cur = await conn.cursor()
        await cur.execute(S.s_alluser)
        data = await cur.fetchall()
    return webJson(data=data)


@user_bp.route("/regist", methods=["GET", "POST"])
async def regist(request):
    name = requestParam(request, 'name')
    password = requestParam(request, 'password')
    logger.info("args: %s", request.args)
    async with request.app.db.acquire() as conn:
        async with conn.cursor() as cur:
            if_name_exist = await ifNameExist(cur, name)
            if if_name_exist:
                return webJson(RetCode.PARAMETER_ERROR, data="用户名已存在")
            await cur.execute(S.i_user, (name, password))
            await cur.commit()
    user = {"name": name}
    return webJson(data=user)


@user_bp.route("/login", methods=["GET", "POST"])
async def login(request):
    return webJson()


async def ifNameExist(cur, username):
    logger.debug("sql: %s", S.s_username)
    await cur.execute(S.s_username, (username,))
    data = await cur.fetchone()
    if data:
        return True
    return False
