#encoding: utf-8

from flask_script import Manager, Shell
from app import app, db, models
from flask_migrate import Migrate, MigrateCommand
# from models import Article

# init
# migrate
# upgrade
# 模型  ->  迁移文件  ->  表

manager = Manager(app)

# 1. 要使用flask_migrate，必须绑定app和db
migrate = Migrate(app,db)


# def make_shell_context():
#     return dict(app=app, db=db, User=User )
# 2. 把MigrateCommand命令添加到manager中
manager.add_command('db', MigrateCommand)
# manager.add_command('shell', Shell())

if __name__ == '__main__':
    manager.run()
