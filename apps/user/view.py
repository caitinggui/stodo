# -*- coding: utf-8 -*-

import logging

from sanic import Blueprint
from .. import app
from utils import RetCode, webJson, requestParam, requestGetParam

logger = logging.getLogger(__name__)
user_bp = Blueprint("user")


@user_bp.get("/", name="user_index")
async def index(request):
    async with request.app.db.acquire() as conn:
        cur = await conn.cursor()
        await cur.execute("select * from user")
        data = await cur.fetchall()
        print(data)
    return webJson(data=data)


@user_bp.route("/regist", methods=["GET", "POST"])
async def regist(request):
    name = requestParam(request, "name")
    password = requestParam(request, "password")
    logger.info("name: %s", name)
    return webJson()


@user_bp.route("/login", methods=["GET", "POST"])
async def login(request):
    return webJson()
