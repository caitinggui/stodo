# -*- coding: utf-8 -*-

import os
import logging
import logging.config

from sanic import Sanic
import aioodbc

from configs import configs, log_config
from utils import Constant, createMysqlPool, AppConfig


logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)


app = Sanec(__name__)


def createApp():
    app.config.from_object(AppConfig)
    from .user.view import user_bp
    from .main.view import main_bp
    from .todo.view import todo_bp
    app.blueprint(user_bp, url_prefix='/users')
    app.blueprint(todo_bp, url_prefix='/todos')
    app.blueprint(main_bp)
    return app


@app.listener("before_server_start")
async def beforeStart(app, loop):
    app.db = await createMysqlPool(loop, configs.get("mysql").get("mydb"))


@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    logger.info("Closing aiomysql pool")
    app.db.close()
    await app.db.wait_closed()
