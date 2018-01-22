# -*- coding: utf-8 -*-

import logging
import re

from ..models import User

from utils import AttrDict, ParamsError, safeInt, Constant


logger = logging.getLogger(__name__)

EMAIL_PATTERN = re.compile(
    "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")


def getTokenView(request):
    """处理TokenView的get方法的表单"""
    pass


def postTokenView(request):
    pass


def postUserListView(request):
    name = request.form.get("name")
    password = request.form.get("password")
    if None in (name, password):
        raise(ParamsError)
    if len(name) > User.name.max_length:
        raise(ParamsError("name too long"))
    if len(password) < Constant.password_min_length or len(password) > Constant.password_max_length:
        raise ParamsError("password length must between %s and %",
                          Constant.password_min_length, Constant.password_max_length)
    password = User.generalPassword(password)

    email = request.form.get("email")
    if email:
        if len(email) > User.email.max_length or not EMAIL_PATTERN.match(email):
            raise(ParamsError("email error"))
    else:
        email = User.email.default

    age = safeInt(request.form.get("age", User.age.default))
    if age < Constant.age_range[0] or age > Constant.age_range[1]:
        raise(ParamsError("age error"))
    # 先不给默认值
    sex = request.form.get("sex")
    if sex:
        if sex not in User.sex.choices:
            raise(ParamsError("sex error"))
    else:
        sex = User.sex.choices.unknown
    city = request.form.get("city", User.city.default)
    if len(city) > User.city.max_length:
        raise(ParamsError("city length error"))
    signature = request.form.get("signature", User.signature.default)
    if len(signature) > User.signature.max_length:
        raise(ParamsError("signature too long"))

    created_time = updated_time = last_login = User.created_time.default()

    form = {
        "name": name,
        "password": password,
        "email": email,
        "age": age,
        "sex": sex,
        "city": city,
        "signature": signature,
        "created_time": created_time,
        "updated_time": updated_time,
        "last_login": last_login
    }
    return AttrDict(form)
