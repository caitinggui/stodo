# -*- coding: utf-8 -*-

import logging

from sanic import Blueprint
from sanic.response import text
from .. import app

logger = logging.getLogger(__name__)
main_bp = Blueprint("main")


@main_bp.get("/")
async def index(request):
    main_url = app.url_for("main.index")
    info = f"""
    "{main_url}"  show all the url for this app
    """
    return text(info)
