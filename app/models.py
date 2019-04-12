from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))


from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    type = db.Column(db.String(10), default='student')
    # posts = db.relationship('Post', backref='author', lazy='dynamic')
    __mapper_args__ = {         # 表示继承
        # 'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    @property       # 为适应login_user中字段id，进行转换
    def id(self):
        return self.user_id

    def __repr__(self):     # 格式化此模块输出
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """verify the password whether matched
        #         :return True:if matched
        #                 False:if not matched or hash isn't exist"""
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):     # 载入头像，由邮箱自动生成
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_teacher_type(self):     # 获取教师类型
        teacher = Teacher.query.get(self.user_id)
        # print(teacher.tea_type)
        return teacher.tea_type


team_student = db.Table('team_student',
    db.Column('user_id', db.Integer, db.ForeignKey('student.user_id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.team_id'), primary_key=True)
)


class Student(User):
    __tablename__ = 'student'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    stu_class = db.Column(db.String(30))
    tel_num = db.Column(db.String(30))
    work_name = db.Column(db.String(30))
    work_type = db.Column(db.String(30))

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
    stu_class = db.Column(db.String(30))
    tea_type = db.Column(db.Integer, default=0)

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
# class Admin(User):
#     __tablename__ = 'admin'
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
#     admin_type = db.Column(db.Integer, default=0)
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'admin',
#     }


class Contest(db.Model):
    __tablename__ = 'contest'
    contest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contest_name = db.Column(db.String(20))
    contest_type = db.Column(db.String(20))
    contest_time = db.Column(db.Date)
    details = db.Column(db.String(150))
    level = db.Column(db.String(20))

    # def contest_list(self):


class Request(db.Model):
    __tablename__ = 'request'
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    user_type = db.Column(db.Integer, nullable=False)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'))
    sup_teacher = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    add_time = db.Column(db.DateTime)
    notes = db.Column(db.String(150))
    status = db.Column(db.Integer, default=0)

    # applicant = db.relationship('User', backref=db.backref('requests'))   # 对于user_id申请人可能为用户或者队伍，故不能用外键
    # # Request添加一个applicant属性，可直接访问申请人详细信息
    # backref使得反向通过User.requests访问该表
    teacher_details = db.relationship('User')
    contest_details = db.relationship('Contest')


class Award(db.Model):
    __tablename__ = 'award'
    award_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    user_type = db.Column(db.Integer, nullable=False)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'))
    sup_teacher = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    grade = db.Column(db.String(20), default='0')

    # part = db.relationship('User', backref=db.backref('awards'))  # 与申请表同理，
    teacher_details = db.relationship('User', backref=db.backref('awards'))
    contest_details = db.relationship('Contest')


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



