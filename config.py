import os
from datetime import timedelta


class Config(object):
    DEBUG = True
    # dialect+driver://username:password@host:port/database
    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = 'zy970509'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'test2'

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST
                                                                           , PORT, DATABASE)
    SECRET_KEY = os.urandom(24)  # 随机24为密码
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

