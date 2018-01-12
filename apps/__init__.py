# -*- coding: utf-8 -*-

import os
import logging
import logging.config


from sanic import Sanic
from configs import configs, log_config


BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)


app = Sanic(__name__)


def createApp():
    # from .user.view import user_bp
    from .main.view import main_bp
    # app.blueprint(user_bp, url_prefix='/user')
    app.blueprint(main_bp)
    return app


