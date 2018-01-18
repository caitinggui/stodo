# -*- coding: utf-8 -*-

from sanic.views import HTTPMethodView


class BaseView(HTTPMethodView):
    """For RESTful api"""
    decorators = []


class PermissionView(HTTPMethodView):
    """"""
    decorators = []
    permission = []
