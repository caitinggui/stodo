# -*- coding: utf-8 -*-

import os


BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Constant(object):
    basedir = BASEDIR
    # 通过token认证后传给handle的参数的键值，也就是token中的信息
    auth_info = "user_info"
    # 存在token中的键，值为用户id
    token_id = "token_id"


class AppConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
