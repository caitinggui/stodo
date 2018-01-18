# -*- coding: utf-8 -*-

import logging
import functools

from . import app
from .models import User
from utils import RetCode, webJson, Constant


logger = logging.getLogger(__name__)


def login_required(func):
    """user Bearer token to auth"""

    @functools.wraps(func)
    async def decorated(request, *args, **kwargs):
        header = request.headers.get("Authorization")
        if header:
            try:
                prefix, token = header.split(' ')
                if prefix != "Bearer":
                    return webJson(RetCode.AUTH_HEADER_ERROR)
            except Exception:
                return webJson(RetCode.AUTH_HEADER_ERROR)
            user_info = User.verifyToken(token)
            kwargs[Constant.auth_info] = user_info
            response = await func(request, *args, **kwargs)
            return response
        else:
            return webJson(RetCode.NEED_LOGIN)
    return decorated
