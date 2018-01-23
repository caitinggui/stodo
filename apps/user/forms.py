# -*- coding: utf-8 -*-

import logging

from ..models import User
from ..forms import checkEmail, checkPassword, checkUsername, checkSex

from utils import AttrDict, ParamsError, safeInt, Constant


logger = logging.getLogger(__name__)


def getTokenView(request):
    """处理TokenView的get方法的表单"""
    pass


def postTokenView(request):
    pass


def postUserListView(request):
    name = request.form.get("name")
    password = request.form.get("password")
    email = request.form.get("email")
    checkUsername(name)
    checkPassword(password)
    checkEmail(email)
    password = User.generalPassword(password)

    age = safeInt(request.form.get("age", User.age.default))
    if age < Constant.age_range[0] or age > Constant.age_range[1]:
        raise(ParamsError("age error"))
    # 先不给默认值
    sex = request.form.get("sex")
    if not checkSex(sex):
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
