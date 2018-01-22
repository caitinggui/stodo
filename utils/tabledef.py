# -*- coding: utf-8 -*-

import os


BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Constant(object):
    basedir = BASEDIR
    # 通过token认证后传给handle的参数的键值，也就是token中的信息
    auth_info = "auth_info"
    # 存在token中的键，值为用户id
    user_id = "id"

    expires_in_login = 60 * 60 * 2400  # 2400 hours
    password_min_length = 8
    password_max_length = 32
    age_range = (0, 120)


class AppConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
