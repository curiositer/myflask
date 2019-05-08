# 作者mrzhao--John

## 中文题目：学生参赛与跟踪统计系统的设计与实现

## English title:Design and Implementation of Students'Participation and Tracking Statistical System

* 感谢@luhuisicnu翻译自Miguel Grinberg的blog https://blog.miguelgrinberg.com 的2017年新版The Flask Mega-Tutorial教程
https://github.com/luhuisicnu/The-Flask-Mega-Tutorial-zh *

在config.py文件中添加

    class Config(object):
        # DEBUG = False        # 调试时才设置为True，平常一定为False
 
        DIALECT = 'mysql'       # 数据库配置
        DRIVER = 'mysqldb'
        USERNAME = 'username'   # myflask
        PASSWORD = 'password'   # 123456
        HOST = '127.0.0.1'
        PORT = '3306'
        DATABASE = 'database'   # flask
        SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
        
        MAIL_SERVER = 'smtp.163.com'  # 电子邮件服务器
        MAIL_PORT = 465
        MAIL_USE_TLS = False
        MAIL_USE_SSL = True
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        ADMINS = ['your-email@example.com']   # 需要配置为自己的邮箱
                                                                   
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        PERMANENT_SESSION_LIFETIME = timedelta(days=7)
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        
        POSTS_PER_PAGE = 10     # 每页条目数量

        UPLOAD_FOLDER = 'file\\upload'      # 给出文件地址
        NOTICE_FOLDER = 'file\\notice'

        REMOTE_HOST = "https://pyecharts.github.io/assets/js"   # 获得图表pycharts的依赖

linux部署教程:https://github.com/luhuisicnu/The-Flask-Mega-Tutorial-zh/blob/master/docs/%E7%AC%AC%E5%8D%81%E4%B8%83%E7%AB%A0%EF%BC%9ALinux%E4%B8%8A%E7%9A%84%E9%83%A8%E7%BD%B2.md
