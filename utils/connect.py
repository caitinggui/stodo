# -*- coding: utf-8 -*-

import asiodbc


async def createSqlitePool(dsn, loop):
    pool = await asiodbc.create_pool(dsn=dsn, loop=loop)
    return pool
