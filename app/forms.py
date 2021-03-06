from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SelectField, BooleanField,\
    SubmitField, DateField, FileField, TextAreaField, IntegerField, MultipleFileField
from flask_admin.form import widgets
from flask_login import current_user
from flask_ckeditor import CKEditorField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from flask_wtf.file import FileRequired, FileAllowed
from app.models import User, Contest_type


class LoginForm(FlaskForm):
    user_id = StringField('学号/工号', validators=[DataRequired('请输入学号')])
    password = PasswordField('密码', validators=[DataRequired('请输入密码')])
    # recaptcha = RecaptchaField('验证码')    # 验证码http://www.pythondoc.com/flask-wtf/form.html?highlight=recaptcha
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')


class AddUserForm(FlaskForm):
    type = SelectField('用户类型', choices=[('admin', '管理员'), ('student', '学生'), ('teacher', '教师')], coerce=str)
    username = StringField('姓名', validators=[DataRequired('请输入姓名'), Length(max=64, message="填写内容过长")])
    user_id = StringField('学号（工号）', validators=[DataRequired('请输入学号'), Length(max=13, message="长度需小于13字符")])
    email = StringField('邮箱（邮箱作为找回密码的唯一凭证，请认真填写）', validators=[DataRequired('请输入邮箱'), Email('请输入正确邮箱格式')])
    tel_num = StringField('联系电话', validators=[DataRequired('请输入联系电话'), Length(min=11, max=11, message="请输入11位手机号")])
    major_in = SelectField('专业', choices=[('机械工程', '机械工程'), ('软件工程', '软件工程'), ('工业工程', '工业工程'),
                                          ('自动化', '自动化'), ('电子信息工程', '电子信息工程'), ('汽车服务工程', '汽车服务工程')], coerce=str)
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
    username = StringField('姓名', validators=[DataRequired('请输入姓名'), Length(max=64, message="填写内容过长")])
    user_id = StringField('学号（工号）', validators=[DataRequired('请输入学号'), Length(max=13, message="长度需小于13字符")])
    email = StringField('邮箱（邮箱作为找回密码的唯一凭证，请认真填写）', validators=[DataRequired('请输入邮箱'), Email('请输入正确邮箱格式')])
    tel_num = StringField('联系电话', validators=[DataRequired('请输入联系电话'), Length(min=11, max=11, message="请输入11位手机号")])
    major_in = SelectField('专业', choices=[('机械工程', '机械工程'), ('软件工程', '软件工程'), ('工业工程', '工业工程'),
                                                ('自动化', '自动化'), ('电子信息工程', '电子信息工程'), ('汽车服务工程', '汽车服务工程')], coerce=str)
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


class ResetPasswordRequestForm(FlaskForm):
    id = IntegerField('学号/工号', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email("请输入正确的邮箱格式")])
    submit = SubmitField('重置密码')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('确定重置密码')


class EditNoticeForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired('请输入标题'), Length(max=50, message="标题长度需小于50字符")])
    text = CKEditorField('正文', validators=[DataRequired('请输入正文')], id='contentcode')
    files = MultipleFileField("相关文件(请上传以下格式的文件'pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg')且再次上传会覆盖之前的文件。",
                              validators=[FileAllowed(['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg'],
                                                      "请上传以下格式的文件'pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg'")])
    submit = SubmitField('发布')


class EditProfileForm(FlaskForm):
    email = StringField('电子邮箱（邮箱作为找回密码的唯一凭证，请认真填写）',
                        validators=[DataRequired('请输入邮箱'), Email('请输入正确邮箱格式'), Length(max=120, message="长度需小于120字符")])
    tel_num = StringField('联系电话', validators=[DataRequired('请输入联系电话'), Length(min=11, max=11, message="请输入11位手机号")])
    # about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交修改')

    def validate_email(self, email):
        email_list = User.query.filter_by(email=email.data).first()
        if current_user.email != email_list.email:
            if email_list is not None:
                raise ValidationError('该邮箱已被使用！')


class EditWorkForm(FlaskForm):
    company_name = StringField('就业单位', validators=[DataRequired('请输入就业单位'), Length(max=30, message="长度需小于30字符")])
    company_type = SelectField('单位类型', choices=[('国有企业', '国有企业'), ('央属企业', '央属企业'), ('公务员', '公务员'),
                                                ('私有企业', '私有企业'), ('事业单位', '事业单位')], coerce=str)
    job = StringField('就职岗位', validators=[DataRequired('请输入岗位'), Length(max=30, message="长度需小于30字符")])
    salary = IntegerField('就职薪水（按月份）', validators=[DataRequired('请输入薪水')])
    submit = SubmitField('提交修改')


class EditStudyForm(FlaskForm):
    college_name = StringField('录取学校', validators=[DataRequired('请输入录取学校'), Length(max=30, message="长度需小于30字符")])
    college_type = SelectField('学校类型', choices=[('985高校', '985高校'), ('211高校', '211高校'),
                                                ('普通高校', '普通高校')], coerce=str)
    after_major = StringField('录取专业（请填写专业全称）', validators=[DataRequired('请输入录取专业'), Length(max=30, message="长度需小于30字符")])
    submit = SubmitField('提交修改')


class EditCreateForm(FlaskForm):
    create_type = StringField('创业公司经营类型', validators=[DataRequired('请输入类型'), Length(max=30, message="长度需小于30字符")])
    create_job = StringField('公司中担任的职务', validators=[DataRequired('请输入职务'), Length(max=30, message="长度需小于30字符")])
    submit = SubmitField('提交修改')


class EditPassword(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired('请输入密码')])
    password = PasswordField('新密码', validators=[DataRequired('请输入密码')])
    password2 = PasswordField(
        '确认密码', validators=[DataRequired(), EqualTo('password', message='请确认两次输入密码是否一致')])
    submit = SubmitField('提交修改')


class AddContestForm(FlaskForm):
    name = StringField('竞赛名', validators=[DataRequired(), Length(max=20, message="长度需小于20字符")])
    type = SelectField('竞赛类型(可以通过上面链接添加更多)', validators=[DataRequired("请选择竞赛类型")], coerce=str)
    # type = StringField('竞赛类型（机器人、无人驾驶、人文、体育、理科、综合）', validators=[DataRequired()])
    time = DateField('竞赛时间', validators=[DataRequired("请按照2010-1-1的格式输入")],
                     format='%Y-%m-%d', widget=widgets.DatePickerWidget())
    details = StringField('竞赛描述（不超过150字节）', validators=[Length(max=150, message="长度需小于150字符")])
    level = SelectField('竞赛等级', choices=[('校级', '校级'), ('市级', '市级'),
                                         ('省级', '省级'), ('国家级', '国家级'), ('国际级', '国际级')], coerce=str)
    file = FileField('添加文件（如果需要添加更多附件，可以利用公告实现）', validators=[FileAllowed(['pdf', 'doc', 'docx'], "请上传pdf或doc文件")])
    submit = SubmitField('添加竞赛')

    def __init__(self, *args, **kwargs):            # 通过加载contest_type表中的数据来完成选项的加载
        super(AddContestForm, self).__init__(*args, **kwargs)
        self.type.choices = [(v.contest_type, v.contest_type) for v in Contest_type.query.all()]


class AddContestTypeForm(FlaskForm):
    type = StringField('竞赛类型', validators=[DataRequired(), Length(max=20, message="长度需小于20字符")])
    submit = SubmitField('添加竞赛类型')


class ApplyContestForm(FlaskForm):
    teacher = StringField('指导教师ID', validators=[DataRequired("请填入教师ID")])
    team_name = StringField('队伍名（以下信息请组队参赛时填写）', validators=[Length(max=30, message="长度需小于30字符")])
    id2 = StringField('成员2学号')
    id3 = StringField('成员3学号')
    id4 = StringField('成员4学号')
    id5 = StringField('成员5学号')
    notes = TextAreaField('备注', validators=[Length(min=0, max=150, message="填写内容过长")])
    submit = SubmitField('确认申请')


class EditAwardForm(FlaskForm):
    grade = SelectField('获奖等级', choices=[('一等奖', '一等奖'), ('二等奖', '二等奖'),
                                         ('三等奖', '三等奖'), ('优秀奖', '优秀奖'), ('无', '无')], coerce=str)
    submit = SubmitField('提交修改')


class EditTimeForm(FlaskForm):
    start = DateField('开始时间', validators=[DataRequired("请按照2010-1-1的格式输入")],
                      format='%Y-%m-%d', widget=widgets.DatePickerWidget())
    end = DateField('结束时间', validators=[DataRequired("请按照2010-1-1的格式输入")],
                    format='%Y-%m-%d', widget=widgets.DatePickerWidget())
    submit = SubmitField('查询')
