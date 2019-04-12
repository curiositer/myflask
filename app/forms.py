from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField,\
    SubmitField, DateField, FileField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileRequired, FileAllowed
from app.models import User


class LoginForm(FlaskForm):
    user_id = StringField('学号/工号', validators=[DataRequired('请输入学号')])
    password = PasswordField('密码', validators=[DataRequired('请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')


class AddUserForm(FlaskForm):
    type = SelectField('用户类型', choices=[('admin', '管理员'), ('student', '学生'), ('teacher', '教师')], coerce=str)
    username = StringField('姓名', validators=[DataRequired('请输入姓名')])
    user_id = StringField('学号', validators=[DataRequired('请输入学号')])
    email = StringField('邮箱', validators=[DataRequired('请输入邮箱'), Email('请输入正确邮箱格式')])
    tel_num = StringField('联系电话', validators=[DataRequired('请输入联系电话')])
    stu_class = StringField('班级(学生、教师填写)')
    tea_type = SelectField('教师类型（仅教师填写）',
                           choices=[(-1, '请选择...'), (0, '普通教师'), (1, '管理教师')], coerce=int)
    password = PasswordField('密码', validators=[DataRequired('请输入密码')])
    password2 = PasswordField(
        '确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_user_id(self, user_id):
        id_num = User.query.filter_by(user_id=user_id.data).first()
        if id_num is not None:
            raise ValidationError('该ID已被使用！')

    def validate_email(self, email):
        email_list = User.query.filter_by(email=email.data).first()
        if email_list is not None:
            raise ValidationError('该邮箱已被使用！')

    def validate_tea_type(self, tea_type):
        if self.type.data == 'teacher':
            if tea_type.data == -1:
                raise ValidationError('请选择教师类型！')


class RegistrationForm(FlaskForm):
    username = StringField('姓名', validators=[DataRequired('请输入姓名')])
    user_id = StringField('学号', validators=[DataRequired('请输入学号')])
    email = StringField('邮箱', validators=[DataRequired('请输入邮箱'), Email('请输入正确邮箱格式')])
    tel_num = StringField('联系电话', validators=[DataRequired('请输入联系电话')])
    stu_class = StringField('班级')
    password = PasswordField('密码', validators=[DataRequired('请输入密码')])
    password2 = PasswordField(
        '确认密码', validators=[DataRequired(), EqualTo('password', message='请确认两次输入密码是否一致')])
    submit = SubmitField('注册')

    def validate_user_id(self, user_id):
        id_num = User.query.filter_by(user_id=user_id.data).first()
        if id_num is not None:
            raise ValidationError('该ID已被使用！')

    def validate_email(self, email):
        email_list = User.query.filter_by(email=email.data).first()
        if email_list is not None:
            raise ValidationError('该邮箱已被使用！')


class EditProfileForm(FlaskForm):
    email = StringField('电子邮箱', validators=[DataRequired('请输入邮箱'), Email('请输入正确邮箱格式')])
    tel_num = StringField('联系电话', validators=[DataRequired('请输入联系电话')])
    # about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交修改')

    def __init__(self, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('该邮箱已存在，请更换一个！')


class EditWorkForm(FlaskForm):
    work_name = StringField('就业单位', validators=[DataRequired('请输入就业单位')])
    work_type = StringField('就业类型', validators=[DataRequired('请输入就业类型')])
    submit = SubmitField('提交修改')


class EditPassword(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired('请输入密码')])
    password = PasswordField('新密码', validators=[DataRequired('请输入密码')])
    password2 = PasswordField(
        '确认密码', validators=[DataRequired(), EqualTo('password', message='请确认两次输入密码是否一致')])
    submit = SubmitField('提交修改')


class AddContestForm(FlaskForm):
    name = StringField('竞赛名', validators=[DataRequired()])
    type = StringField('竞赛类型', validators=[DataRequired()])
    time = DateField('竞赛时间', validators=[DataRequired("请按照2010-1-1的格式输入")], format='%Y-%m-%d')
    details = StringField('竞赛描述', validators=[Length(min=0, max=150)])
    level = SelectField('竞赛等级', choices=[('校级', '校级'), ('市级', '市级'),
                                         ('省级', '省级'), ('国家级', '国家级'), ('国际级', '国际级')], coerce=str)
    file = FileField('添加文件', validators=[FileRequired("请上传pdf文件"), FileAllowed(['pdf'], "请上传pdf文件")])
    submit = SubmitField('添加竞赛')


class ApplyContestForm(FlaskForm):
    teacher = StringField('指导教师', validators=[DataRequired()])
    id1 = StringField('成员1（队长）学号', validators=[DataRequired()])
    name1 = StringField('成员1（队长）姓名', validators=[DataRequired()])
    team_name = StringField('队伍名（组队参加）')
    id2 = StringField('成员2学号')
    name2 = StringField('成员2姓名')
    id3 = StringField('成员3学号')
    name3 = StringField('成员3姓名')
    id4 = StringField('成员4学号')
    name4 = StringField('成员4姓名')
    id5 = StringField('成员5学号')
    name5 = StringField('成员5姓名')
    notes = TextAreaField('备注', validators=[Length(min=0, max=150)])
    submit = SubmitField('确认申请')


