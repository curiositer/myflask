from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

import jwt                  # 用于重置密码
from time import time

# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))


from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, index=True, primary_key=True, unique=True)
    username = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    tel_num = db.Column(db.String(20))
    password_hash = db.Column(db.String(128), nullable=True)
    type = db.Column(db.String(10), default='student', nullable=True)

    __mapper_args__ = {         # 表示继承
        # 'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    @property       # 将该方法作为其中的一个属性，只能用self.id来调用
    def id(self):       # 为适应login_user中字段id，进行转换
        return self.user_id

    def __repr__(self):     # 格式化此模块输出
        return '<User {}>'.format(self.username)

    def set_password(self, password):       # 获取密码对应的哈希值
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):     # 确定密码是否匹配
        """verify the password whether matched
        #         :return True:if matched
        #                 False:if not matched or hash isn't exist"""
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):     # 载入头像，由邮箱自动生成
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def user_type_ch(self):         # 给出用户类型对应中文
        if self.type == 'student':
            return "学生"
        elif self.type == 'teacher':
            return "教师"
        elif self.type == 'admin':
            return "管理员"

    def get_teacher_type(self):     # 获取教师类型
        teacher = Teacher.query.get(self.user_id)
        # print(teacher.tea_type)
        return teacher.tea_type

    def if_admin(self):             # 判断是否有权限进行审核操作
        if (self.type == 'admin') or (self.type == 'teacher' and self.get_teacher_type() == 1):
            return True
        else:
            return False

    def get_reset_password_token(self, expires_in=600):   # 获取重置密码的令牌，expires_in=600即设置令牌有效时间为10分钟
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod       # 无需创建实例，可以直接使用
    def verify_reset_password_token(token):     # 验证令牌，通过则返回给用户id，否则返回none
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Notice(db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    text = db.Column(db.Text)
    filename1 = db.Column(db.String(100))
    filename2 = db.Column(db.String(100))
    filename3 = db.Column(db.String(100))
    time = db.Column(db.Date)


team_student = db.Table('team_student',
    db.Column('user_id', db.Integer, db.ForeignKey('student.user_id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.team_id'), primary_key=True)
)


class Student(User):
    __tablename__ = 'student'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    major_in = db.Column(db.String(30))
    company_name = db.Column(db.String(30))
    company_type = db.Column(db.String(30))     # 公司级别（类型）
    job = db.Column(db.String(30))   # 在公司中所担任的职务
    salary = db.Column(db.Integer)
    college_name = db.Column(db.String(30))
    after_major = db.Column(db.String(30))     # 考研专业
    college_type = db.Column(db.String(30))
    create_type = db.Column(db.String(30))  # 创业公司类型
    create_job = db.Column(db.String(30))   # 在公司中所担任的职务

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }


class Team(db.Model):
    __tablename__ = 'team'
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    team_name = db.Column(db.String(30))

    parts = db.relationship(
        'Student', secondary=team_student, backref=db.backref('teams', lazy='dynamic'), lazy='dynamic')


class Teacher(User):
    __tablename__ = 'teacher'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    tea_type = db.Column(db.Integer, default=0, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }


# 使得非继承关系的管理员，无需再冗余建表
from flask_sqlalchemy import event
@event.listens_for(User, 'mapper_configured')
def receive_mapper_configured(mapper, class_):
    class FallbackToParentPolymorphicMap(dict):
        def __missing__(self, key):
            # return parent Item's mapper for undefined polymorphic_identity
            return mapper

    new_polymorphic_map = FallbackToParentPolymorphicMap()
    new_polymorphic_map.update(mapper.polymorphic_map)
    mapper.polymorphic_map = new_polymorphic_map

    # for prevent 'incompatible polymorphic identity' warning, not necessarily
    mapper._validate_polymorphic_identity = None


class Contest_type(db.Model):
    __tablename__ = 'contest_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contest_type = db.Column(db.String(20), nullable=True)


class Contest(db.Model):
    __tablename__ = 'contest'
    contest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contest_name = db.Column(db.String(20))
    contest_type = db.Column(db.String(20))
    contest_time = db.Column(db.Date)
    filename = db.Column(db.String(50))
    details = db.Column(db.String(150))
    level = db.Column(db.String(20))


class Request(db.Model):
    __tablename__ = 'request'  # 在数据库中表名称
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 标识为一个属性（列），整型数据，默认长度为11，设置为主键、自动增加
    user_id = db.Column(db.Integer, nullable=False)  # 设置非空
    user_type = db.Column(db.Integer, nullable=False)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'))
    sup_teacher = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    # 设置为外键，对应主键为user表中user_id
    add_time = db.Column(db.DateTime)  # 设置为日期-时间类型
    notes = db.Column(db.String(150))  # 设置为可变字符串类型varchar，长度150
    status = db.Column(db.Integer, default=0)

    teacher_details = db.relationship('User')
    contest_details = db.relationship('Contest')


class Award(db.Model):
    __tablename__ = 'award'
    award_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.Integer, nullable=False)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'))
    sup_teacher = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    grade = db.Column(db.String(20), default='0')

    # part = db.relationship('User', backref=db.backref('awards'))  # 与申请表同理，
    teacher_details = db.relationship('User', backref=db.backref('awards'))
    contest_details = db.relationship('Contest')


@login.user_loader      # 使用Flask-Login的@login.user_loader装饰器来为用户加载功能注册函数。
def load_user(user_id):
    return User.query.get(int(user_id))



