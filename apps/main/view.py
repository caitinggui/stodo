# -*- coding: utf-8 -*-

from sanic import Blueprint
from sanic.response import text
from .. import app

main_bp = Blueprint("main")


@main_bp.get("/")
def index(request):
    info = """
    "{main_url}"  show all the url for this app
    """
    return text(info.format(main_url=app.url_for("main.index")))
