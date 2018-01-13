# -*- coding: utf-8 -*-

import logging
import time
import functools
from functools import update_wrapper
from datetime import timedelta


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
