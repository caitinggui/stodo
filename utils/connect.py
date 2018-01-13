# -*- coding: utf-8 -*-

import aioodbc


async def createSqlitePool(dsn, loop):
    pool = await asiodbc.create_pool(dsn=dsn, loop=loop)
    return pool


class RedisPool(object):
    pass
