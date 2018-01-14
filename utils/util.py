# -*- coding: utf-8 -*-

import time
import datetime
import logging
import string
import re
from collections import namedtuple

logger = logging.getLogger(__name__)

# 字符串转时间戳
def str2timestamp(d, f="%Y-%m-%d %H:%M:%S"):
    t = time.strptime(d, f)
    return time.mktime(t)

# 时间戳转字符串
def timestamp2str(d, f="%Y-%m-%d %H:%M:%S"):
    x = time.localtime(d)
    return time.strftime(f, x)


def safeInt(num, default=None):
    try:
        return int(num)
    except Exception:
        return default


def safeFloat(num, default=None):
    try:
        return float(num)
    except Exception:
        return default


def getDay(days=0, f="%Y-%m-%d"):
    currTime = datetime.datetime.now()
    day = currTime + datetime.timedelta(days)
    return datetime.datetime.strftime(day, f)


class AttrDict(dict):
    """Dict that can get/set attribute by dot
    当无该key时返回None(不异常)
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None

    def __setattr__(self, name, value):
        self[name] = value


def dict2namedtuple(data):
    """将字典转为namedtuple，生成的数据将不可更改，比AttrDict更节约内存"""
    Form = namedtuple('Form', field_names=data.keys())
    return Form(**data)


def requestParam(request, name, default=None):
    if name in request.args:
        param = request.args.get(name)
    else:
        param = request.form.get(name, default)
    return param
