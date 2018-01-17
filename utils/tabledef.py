# -*- coding: utf-8 -*-

import os


BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Constant(object):
    basedir = BASEDIR
    sqlitedb = os.path.join(BASEDIR, "data.db")
    dsn = "Driver=SQLite;Database={}".format(sqlitedb)


class AppConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
