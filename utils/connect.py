# -*- coding: utf-8 -*-

import aiomysql
from aiomysql.cursors import DictCursor, Cursor
from . import AttrDict


class AttrDictCursor(DictCursor):
    dict_type = AttrDict


async def createMysqlPool(loop, config):
    "传入字典格式的配置"
    pool = await aiomysql.create_pool(
        loop=loop,
        host=config.get('HOST'),
        port=config.get('PORT'),
        user=config.get("USER"),
        password=config.get("PASSWORD"),
        db=config.get("DB"),
        maxsize=config.get("POOLSIZE", 10),
        cursorclass=AttrDictCursor
    )
    return pool


class RedisPool(object):
    pass
