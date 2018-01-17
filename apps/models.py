# coding: utf-8
"""
这里仅用来定义数据结构以及初始化建表，不在web中使用，且不做migrate,
若需要中途修改表结构，记得在这里添加相应字段，然后自己动手修改数据库表
一些记录:
  1. 不要用mysql的enum,因为不好迁移, 且不在严格模式时，插入错误数据不报错
  2. 要不要Field使用`constraints=[SQL("default 0")]`设定数据库的默认值：
    2.1 peewee的default是在orm转换的时候用的，不作用在数据库中
    2.2 要设置数据库default: eg:) CharField(constraints=[SQL("default ''")])
    2.3 设置或者不设置数据库default对性能几乎没有损失
    2.4 设置数据库default，能够很好的避免null，一般建议在NOT NULL时设置default
    2.5 peewee开发者任务设置数据库default后，如果更改默认值会比较复杂，所以default只作用于python端
    2.6 可以参考:https://stackoverflow.com/questions/8010036/should-mysql-columns-always-have-default-values
    2.7 这里default和constraints都设置，显式的采用default，而constraints可以避免每个insert都需要插入全部的值
"""

import datetime
import logging
import hashlib

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from peewee import Model, DateTimeField, IntegerField, PrimaryKeyField, \
    CharField, MySQLDatabase, BigIntegerField, ForeignKeyField, TextField,\
    BooleanField, SQL, SmallIntegerField

from utils import Constant, AttrDict
from configs import configs
from . import app


logger = logging.getLogger(__name__)

db = MySQLDatabase(
    database=configs["mysql"]["mydb"]["DB"],
    user=configs["mysql"]["mydb"]["USER"],
    password=configs["mysql"]["mydb"]["PASSWORD"],
)

serializer = Serializer(app.config['SECRET_KEY'])

def setDefault(default):
    return [SQL("default {}".format(default))]


class BaseModel(Model):
    class Meta:
        database = db


class Role(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=255, unique=True, index=True)
    permission = BigIntegerField(default=0, constraints=setDefault(0))


class User(BaseModel):
    """表名都用单数"""
    id = PrimaryKeyField()
    password = CharField(max_length=128)
    name = CharField(max_length=255, verbose_name="user's name",
                     index=True, unique=True)
    # email = CharField(max_length=128, unique=True, index=True)
    # 0表示未设置
    age = SmallIntegerField(
        default=0, constraints=setDefault(0), verbose_name="user's age")
    # 用"<3"就可以过滤出已填性别的人
    sex = SmallIntegerField(choices=AttrDict(male=1, female=2, unknown=3))
    # city = CharField(verbose_name='city for user')
    created_time = DateTimeField(default=datetime.datetime.utcnow)
    # constraints=setDefault("CURRENT_TIMESTAMP"), MySQL 5.6版本支持设置
    updated_time = DateTimeField(default=datetime.datetime.utcnow)
    role = ForeignKeyField(Role, related_name="user")

    class Meta:
        db_table = 'user'

    @staticmethod
    def generalPassword(password):
        password = bytes(password + app.config["SECRET_KEY"], encoding='utf-8')
        hash_password = hashlib.new("md5", data=password)
        return hash_password.hexdigest()

    @staticmethod
    def verifyPassword(password, password_hash):
        return User.generalPassword(password) == password_hash

    @staticmethod
    def generateToken(data, expiration=600):
        """生成token频率不高且有效期可能不同，所以serializer实时生成"""
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps(data)

    @staticmethod
    def verifyToken(token):
        """校验token不涉及到有效期，所以提前生成serializer"""
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return {}    # valid token, but expired
        except Exception:
            return {}    # invalid token
        return data


class Todo(BaseModel):
    """要做的事情"""
    id = PrimaryKeyField()
    title = CharField(max_length=255, index=True)
    detail = TextField(null=True, help_text="要做的事的具体内容或步骤")
    is_completed = BooleanField(constraints=setDefault(0), default=False)
    user = ForeignKeyField(User, related_name="todo")

    class Meta:
        db_table = 'todo'


def createTable(tables):
    db.connect()
    db.create_tables(tables)
    db.commit()


def createAllTables():
    tables = [User, Role, Todo]
    createTable(tables)


class S(object):
    """SQL"""

    username = User.name.db_column
    user_table = User._meta.db_table
    password = User.password.db_column

    s_username = f"select id, {username} from {user_table} where {username} = %s limit 1"
    s_alluser = f"select id, {username} from {user_table}"
    i_user = f"insert into {user_table} ({username}, {password}) values (%s, %s)"
