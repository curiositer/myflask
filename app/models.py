from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

# class User(UserMixin, db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     password_hash = db.Column(db.String(128))
#     username = db.Column(db.String(30))
#     type = db.Column(db.Integer, nullable=False)
#     ice = db.Column(db.Integer, nullable=False)
#     # users = db.relationship('User', backref='role')
#
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def verify_password(self, password):
#         """verify the password whether matched
#         :return True:if matched
#                 False:if not matched or hash isn't exist"""
#         return check_password_hash(self.password_hash, password)
#
#     # def __init__(self, username, email):
#     #     self.username = username
#     #     self.email = email
#     #
#     def __repr__(self):
#         return '<User %r>' % self.username
#
# #

# #
# #




#
# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))


from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    type = db.Column(db.Integer, default=1)
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):     # 载入头像
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    stu_class = db.Column(db.String(30))
    tel_num = db.Column(db.String(30))
    work_name = db.Column(db.String(30))
    work_type = db.Column(db.String(30))


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tea_class = db.Column(db.String(30))
    tea_type = db.Column(db.String(30))


class Contest(db.Model):
    __tablename__ = 'contest'
    contest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contest_name = db.Column(db.String(20))
    contest_type = db.Column(db.String(20))
    details = db.Column(db.String(150))
    level = db.Column(db.String(20))

    # def contest_list(self):



@login.user_loader
def load_user(id):
    return User.query.get(int(id))



