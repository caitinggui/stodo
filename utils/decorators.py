# -*- coding: utf-8 -*-

import logging
import time
import functools
from functools import update_wrapper
from datetime import timedelta

from flask import make_response, request, current_app, abort


logger = logging.getLogger(__name__)


def runTime(func):
    logger = logging.getLogger(__name__)

    @functools.wraps(func)
    def wrapper(*args, **kw):
        time1 = time.time()
        result = func(*args, **kw)
        run_time = time.time() - time1
        logger.info('%s run time: %f' % (func.__name__, run_time))
        return result
    return wrapper


def ensureDone(times):
    """保证函数运行成功，不成功则反复执行times次"""
    logger = logging.getLogger(__name__)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            for i in xrange(times):
                try:
                    result = func(*args, **kw)
                    return result
                except Exception as e:
                    logger.warn("execute func: %s fail for %s times: %s",
                                func.__name__, i, e, exc_info=True)
            raise Exception(e)
        return wrapper
    return decorator


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def login_requied(f):
    """全部都返回未登录的状态"""
    def decorator():
        abort(403)
        return f()
    return decorator
