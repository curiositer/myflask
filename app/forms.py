from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    id = StringField('学号', validators=[DataRequired('请输入学号')])
    password = PasswordField('密码', validators=[DataRequired('请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')


class RegistrationForm(FlaskForm):
    username = StringField('姓名', validators=[DataRequired()])
    id = StringField('学号', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '确认密码', validators=[DataRequired(), EqualTo('password')])
    type = SelectField('用户类型', choices=[(0, '管理员'), (1, '学生'), (2, '教师')], coerce=int)
    submit = SubmitField('注册')

    def validate_id(self, id):
        id_num = User.query.filter_by(id=id.data).first()
        # print(id.data)
        # print(id_num)
        if id_num is not None:
            raise ValidationError('该ID已被使用！')

    def validate_email(self, email):
        email_list = User.query.filter_by(email=email.data).first()
        if email_list is not None:
            raise ValidationError('该邮箱已被使用！')


class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('电子邮箱', validators=[DataRequired()])
    # about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交修改')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('该用户名已存在，请更换一个！')


class AddContestForm(FlaskForm):
    name = StringField('竞赛名', validators=[DataRequired()])
    type = StringField('竞赛类型', validators=[DataRequired()])
    details = StringField('竞赛描述', validators=[Length(min=0, max=150)])
    level = StringField('竞赛等级', validators=[DataRequired()])
    submit = SubmitField('添加竞赛')


class ApplyContestForm(FlaskForm):
    notes = StringField('备注', validators=[Length(min=0, max=150)])
    submit = SubmitField('确认申请')

