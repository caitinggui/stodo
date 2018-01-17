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


app = Sanic(__name__)


def createApp():
    app.config.from_object(AppConfig)
    from .user.view import user_bp
    from .main.view import main_bp
    app.blueprint(user_bp, url_prefix='/user')
    app.blueprint(main_bp)
    return app


@app.listener("before_server_start")
async def beforeStart(app, loop):
    app.db = await createMysqlPool(loop, configs.get("mysql").get("mydb"))
