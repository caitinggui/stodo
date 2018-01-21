# coding: utf-8

configs = {
    "mysql": {
        "mydb": {
            "HOST": "127.0.0.1",
            "PORT": 3306,
            "USER": "user",
            "PASSWORD": "password",
            "POOLSIZE": 30,
            "DB": "Stodo"
        }
    },
    "mongodb": {
        "mydb": {
            "HOST": "127.0.0.1",
            "PORT": 27017,
            "USER": "user",
            "PASSWORD": "password",
            "MINPOOLSIZE": 20,
            "MAXPOOLSIZE": 30
        }
    },
    "redis": {
        "mydb": {
            "HOST": "127.0.0.1",
            "PORT": 6379,
            "DB": 3,
            "MAX_CONNECTIONS": 200,
            "PASSWORD": "password"
        }
    }
}

log_config = {
    "version": 1,
    "disable_existing_loggers": False,  # other loggers can log to root
    "handlers": {
        "console": {
            "formatter": "simple",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "DEBUG"
        },
        'file': {  # 可以在多进程下使用
            'formatter': 'standard',
            "filename": "logs/stodo.log",
            # 如果没有使用并发的日志处理类，在多实例的情况下日志会出现缺失
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            # 当达到100MB时分割日志
            'maxBytes': 1024 * 1024 * 100,
            # 最多保留50份文件
            'backupCount': 50,
            'level': 'DEBUG',
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': True,
        },
        # "timedfile": {  # 在多进程下会出问题
            # "formatter": "standard",
            # "filename": "logs/mylog.log",
            # "class": "logging.handlers.TimedRotatingFileHandler",
            # "level": "DEBUG",
            # "when": "midnight",  # 每天半夜切分日志
            # "backupCount": 60    # 保留60天的日志
        # },
        "socket": {
            "level": "DEBUG",
            "class": "logging.handlers.SocketHandler",
            "host": "192.168.50.46",
            "port": 8002,
            "formatter": "standard"
        },
        "http": {
            "level": "DEBUG",
            "class": "logging.handlers.HTTPHandler",
            "host": "192.168.50.46",
            "url": "/log",
            "method": "POST",
            "formatter": "standard"
        },
        "mail": {
            "level": "ERROR",
            "class": "logging.handlers.SMTPHandler",
            "mailhost": "",
            "fromaddr": "",
            "toaddrs": "",
            "subject": "",
            "credentials": "",
            "formatter": "standard"
        }
    },
    "formatters": {
        "simple": {
            "format": "%(asctime)s[%(name)s(line:%(lineno)d)%(levelname)s] %(message)s",
            'datefmt': "%H:%M:%S"
        },
        "standard": {
            "format": "%(asctime)s[%(name)s(line:%(lineno)d)%(levelname)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        }
    },
    "root": {
        "level": "WARN",
        "propagate": False,
        "handlers": ["file"]
    },
    "loggers": {
        "apps": {
            "handlers": ["file"],
            "propagate": False,
            "level": "INFO"
        },
        "utils": {
            "handlers": ["file"],
            "propagate": False,
            "level": "INFO"
        },
        "configs": {
            "handlers": ["file"],
            "propagate": False,
            "level": "INFO"
        },
        'sanic': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}
