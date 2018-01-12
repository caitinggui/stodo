# -*- coding: utf-8 -*-
'''返回代码以及错误提示'''

from sanic.response import json as jsonify


class RetCode:

    CODE = "code"
    MSG = "msg"
    DATA = "data"

    SUCCESS = (0, "请求成功")

    # 传入的参数异常都以10开头
    PARAMETER_NOT_ENOUGH = (1001, "参数不足")
    PARAMETER_ERROR = (1002, "参数错误")
    PAGE_ERROR = (1003, "页码错误")

    # 20表示处理过程中有问题
    CANT_FIND_ANSWER = (2001, "找不到合适答案")

    FORBIDDEN = (403, "抱歉，您权限不足")
    NOT_FOUND = (404, "无此页面")
    NEED_LOGIN = (401, "抱歉，您需要先登陆")

    # 50表示影响系统的异常
    REDIS_ERROR = (5001, "redis出错")
    MONGO_ERROR = (5002, "mongo连接出错")
    SERVER_ERROR = (500, "服务器错误, 紧急修复中...")

    @staticmethod
    def retBase(f, d, e):
        result = {
            RetCode.CODE: e[0],
            RetCode.MSG: e[1],
            RetCode.DATA: d
        }
        return f(result)


def webJson(status, data=''):
    result = {
        RetCode.CODE: status[0],
        RetCode.MSG: status[1],
        RetCode.DATA: data
    }
    return jsonify(result)


class ParamsError(Exception):
    def __init__(self, data=None, *args, **kwargs):
        """这个data和返回结果的data有关"""
        super(ParamsError, self).__init__(self, *args, **kwargs)
        self.data = data
