# -*- coding: utf-8 -*-

import logging

from sanic import Blueprint
from .. import app
from utils import RetCode, webJson

logger = logging.getLogger(__name__)
user_bp = Blueprint("user")


@user_bp.get("/")
async def index(request):
    async with request.app.db.acquire() as conn:
        cur = await conn.cursor()
        await cur.execute("select * from user")
        data = await cur.fetchall()
        print(data)
    return webJson(RetCode.SUCCESS, data=data)

