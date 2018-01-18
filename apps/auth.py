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
        if request.token:
            user_info = User.verifyToken(request.token)
            kwargs[Constant.auth_info] = user_info
            response = await func(request, *args, **kwargs)
            return response
        else:
            return webJson(RetCode.NEED_LOGIN)
    return decorated
