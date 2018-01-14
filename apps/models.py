# coding: utf-8
"""
这里仅用来定义数据结构以及初始化建表，不在web中使用，且不做migrate,
若需要中途修改表结构，记得在这里添加相应字段，然后自己动手修改数据库表
"""

import datetime

from peewee import Model, DateTimeField, IntegerField, PrimaryKeyField, \
    CharField, SqliteDatabase, BigIntegerField, ForeignKeyField

from utils import Constant


db = SqliteDatabase(Constant.sqlitedb)


class BaseModel(Model):
    class Meta:
        database = db


class Role(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=255, unique=True, index=True)
    permission = BigIntegerField(default=0)


class User(BaseModel):
    """表名都用单数"""
    id = PrimaryKeyField()
    password = CharField(max_length=128)
    name = CharField(max_length=255, verbose_name="user's name", index=True, unique=True)
    # email = CharField(max_length=128, unique=True, index=True)
    # age = IntegerField(null=False, verbose_name="user's age")
    # sex = CharField(max_length=16, verbose_name="user's sex")
    # city = CharField(verbose_name='city for user')
    # create_time = DateTimeField(verbose_name='create time',
                                # default=datetime.datetime.utcnow)
    # role_id = ForeignKeyField(Role, related_name="user")

    class Meta:
        db_table = 'user'


def createTable(tables):
    db.connect()
    db.create_tables(tables)
    db.commit()


def createAllTables():
    tables = [User, Role]
    createTable(tables)


class S(object):
    """SQL"""

    username = User.name.db_column
    user_table = User._meta.db_table
    password = User.password.db_column

    s_username = f"select id, {username} from {user_table} where {username} = ? limit 1"
    s_alluser = f"select id, {username} from {user_table}"
    i_user = f"insert into {user_table} ({username}, {password}) values (?, ?)"
