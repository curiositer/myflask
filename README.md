# 作者mrzhao--John

## 中文题目：学生参赛与跟踪统计系统的设计与实现

## English title:Design and Implementation of Students'Participation and Tracking Statistical System

* 感谢@luhuisicnu翻译自Miguel Grinberg的blog https://blog.miguelgrinberg.com 的2017年新版The Flask Mega-Tutorial教程
https://github.com/luhuisicnu/The-Flask-Mega-Tutorial-zh *

在config.py文件中添加

    class Config(object):
        DEBUG = True
        # dialect+driver://username:password@host:port/database
        DIALECT = 'mysql'
        DRIVER = 'mysqldb'
        USERNAME = 'username'   # myflask
        PASSWORD = 'password'   # 123456
        HOST = '127.0.0.1'
        PORT = '3306'
        DATABASE = 'database'   # flask
    
        SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST
                                                                               , PORT, DATABASE)
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        PERMANENT_SESSION_LIFETIME = timedelta(days=7)
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        POSTS_PER_PAGE = 3
        UPLOAD_FOLDER = 'upload'
        REMOTE_HOST = "https://pyecharts.github.io/assets/js"

linux部署教程:https://github.com/luhuisicnu/The-Flask-Mega-Tutorial-zh/blob/master/docs/%E7%AC%AC%E5%8D%81%E4%B8%83%E7%AB%A0%EF%BC%9ALinux%E4%B8%8A%E7%9A%84%E9%83%A8%E7%BD%B2.md
