# -*- coding: utf-8 -*-
'''返回代码以及错误提示'''

from sanic.response import json as jsonify


class RetCode:
    """第一个是http status，第二个是返回的json中显示的status，第三个是显示的状态说明"""

    CODE = "code"
    MSG = "msg"
    DATA = "data"

    SUCCESS = (200, 0, "请求成功")

    # 传入的参数异常都以10开头
    PARAMETER_NOT_ENOUGH = (400, 1001, "参数不足")
    PARAMETER_ERROR = (400, 1002, "参数错误")
    PAGE_ERROR = (400, 1003, "页码错误")

    # 20表示处理过程中有问题
    CANT_FIND_ANSWER = (200, 2001, "找不到合适答案")

    FORBIDDEN = (403, 403, "抱歉，您权限不足")
    NOT_FOUND = (404, 404, "无此页面")
    REQUEST_TIMEOUT = (408, 408, "请求超时")
    NEED_LOGIN = (401, 401, "抱歉，您需要先登陆")
    AUTH_HEADER_ERROR = (401, 4001, "认证header有误")
    TOKEN_ERROR = (401, 4002, "token错误")

    # 50表示影响系统的异常
    REDIS_ERROR = (500, 5001, "redis出错")
    MONGO_ERROR = (500, 5002, "mongo连接出错")
    SERVER_ERROR = (500, 500, "服务器错误, 紧急修复中...")

    @staticmethod
    def retBase(f, d, e):
        result = {
            RetCode.CODE: e[1],
            RetCode.MSG: e[2],
            RetCode.DATA: d
        }
        return f(result)


def webJson(mystatus=RetCode.SUCCESS, data='', **kwargs):
    """jsonify自带有status参数，所以这里用mystatus避免冲突"""
    result = {
        RetCode.CODE: mystatus[1],
        RetCode.MSG: mystatus[2],
        RetCode.DATA: data
    }
    return jsonify(result, status=mystatus[0], **kwargs)


class ParamsError(Exception):
    def __init__(self, data=None, *args, **kwargs):
        """这个data和返回结果的data有关"""
        super(ParamsError, self).__init__(self, *args, **kwargs)
        self.data = data


class TokenError(Exception):
    def __init__(self, data=None, *args, **kwargs):
        super(TokenError, self).__init__(self, *args, **kwargs)
        self.data = data
