# -*- coding: utf-8 -*-

import re

from .models import User
from utils import ParamsError, Constant


EMAIL_PATTERN = re.compile(
    "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")


def checkEmail(email):
    if not email:
        raise(ParamsError("email error"))
    if len(email) > User.email.max_length or not EMAIL_PATTERN.match(email):
        raise(ParamsError('email error'))
    return True


def checkPassword(password):
    if not password:
        raise(ParamsError("password error"))
    if len(password) < Constant.password_min_length or len(password) > Constant.password_max_length:
        raise ParamsError("password length must between %s and %",
                          Constant.password_min_length, Constant.password_max_length)
    return True


def checkUsername(name):
    if not name:
        raise(ParamsError("name error"))
    if len(name) > User.name.max_length:
        raise(ParamsError("name too long"))
    return True


def checkSex(sex):
    if not sex:
        return False
    if sex not in User.sex.choices:
        raise(ParamsError("sex error"))
    return True
