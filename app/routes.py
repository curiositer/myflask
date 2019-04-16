from flask import render_template
import os
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EditPassword, EditWorkForm, EditStudyForm,\
    AddContestForm, ApplyContestForm, AddUserForm, EditAwardForm
from flask import render_template, flash, redirect, url_for, request, send_from_directory, make_response
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Contest, Request, Student, Teacher, Team, Award, team_student
from datetime import datetime

from pyecharts import Bar, Pie
from pyecharts_javascripthon.api import TRANSLATOR


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data).first()
        # print(user)
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('normal_form.html', title='登陆', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user_type = form.type.data
        id = int(form.user_id.data)
        if user_type == 'student':
            student = Student(user_id=id, username=form.username.data, email=form.email.data, type=form.type.data,
                              stu_class=form.stu_class.data, tel_num=form.tel_num.data)
            student.set_password(form.password.data)
            db.session.add(student)
        elif user_type == 'teacher':
            teacher = Teacher(user_id=id, username=form.username.data, email=form.email.data, tel_num=form.tel_num.data,
                              type=form.type.data,stu_class=form.stu_class.data,tea_type=form.tea_type.data)
            teacher.set_password(form.password.data)
            db.session.add(teacher)
        else:
            admin = User(user_id=id, username=form.username.data, email=form.email.data, tel_num=form.tel_num.data,
                         type=form.type.data)
            admin.set_password(form.password.data)
            db.session.add(admin)
        db.session.commit()
        flash('恭喜您，用户%s已注册成功!' % form.username.data)
        return redirect(url_for('index'))
    return render_template('normal_form.html', title='添加用户', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        id = int(form.user_id.data)
        print(id)
        student = Student(user_id=id, username=form.username.data, email=form.email.data, type='student',
                          stu_class=form.stu_class.data, tel_num=form.tel_num.data)
        student.set_password(form.password.data)
        print(student)
        db.session.add(student)
        db.session.commit()
        flash('恭喜您，学生用户%s已注册成功!' % form.username.data)
        return redirect(url_for('login'))
    return render_template('normal_form.html', title='注册', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/user/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.email)
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.tel_num = form.tel_num.data
        db.session.commit()
        flash('信息修改成功.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.tel_num.data = current_user.tel_num
    return render_template('normal_form.html', title='编辑资料',
                           form=form)


@app.route('/user/edit/work', methods=['GET', 'POST'])
@login_required
def edit_work():
    form = EditWorkForm()
    stu = Student.query.get(current_user.user_id)
    if (not stu.company_name) and (not stu.college_name):
        exist = 'no'
        if form.validate_on_submit():
            stu.company_name = form.company_name.data
            stu.company_type = form.company_type.data
            stu.job = form.job.data
            stu.salary = form.salary.data
            db.session.commit()
            flash('信息修改成功.')
            return redirect(url_for('edit_work'))
        elif request.method == 'GET':
            form.company_name.data = stu.company_name
            form.company_type.data = stu.company_type
            form.job.data = stu.job
            form.salary.data = stu.salary
    else:
        if stu.company_name:
            exist = 'work'
        elif stu.college_name:
            exist = 'study'
    return render_template('normal_form.html', title='添加就业信息', form=form, exist=exist, student=stu)


@app.route('/user/edit/study', methods=['GET', 'POST'])
@login_required
def edit_study():
    form = EditStudyForm()
    stu = Student.query.get(current_user.user_id)
    if (not stu.company_name) and (not stu.college_name):
        exist = 'no'
        if form.validate_on_submit():
            stu.college_name = form.college_name.data
            stu.college_type = form.college_type.data
            db.session.commit()
            flash('信息修改成功.')
            return redirect(url_for('edit_study'))
        elif request.method == 'GET':
            form.college_name.data = stu.college_name
            form.college_type.data = stu.college_type
    else:
        if stu.company_name:
            exist = 'work'
        elif stu.college_name:
            exist = 'study'
    return render_template('normal_form.html', title='添加考研信息', form=form, exist=exist, student=stu)


@app.route('/user/edit/password', methods=['GET', 'POST'])
@login_required
def edit_password():
    form = EditPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=current_user.user_id).first()
        # print(user)
        if not user.check_password(form.old_password.data):
            flash('密码错误')
            return redirect(url_for('edit_password'))
        else:
            user.set_password(form.password.data)
            db.session.commit()
            flash('密码修改成功')
            return redirect(url_for('index'))
    return render_template('normal_form.html', title='修改密码', form=form)


@app.route('/contest')
def contest_list():
    page = request.args.get('page', 1, type=int)
    lists = Contest.query.filter().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('contest_list', page=lists.next_num) \
        if lists.has_next else None
    prev_url = url_for('contest_list', page=lists.prev_num) \
        if lists.has_prev else None
    return render_template("contest.html", title='竞赛列表',
                           lists=lists.items, next_url=next_url, prev_url=prev_url)


@app.route('/contest/add', methods=['GET', 'POST'])
@login_required
def add_contest():
    form = AddContestForm()
    if form.validate_on_submit():
        date = form.time.data.strftime('%Y-%m-%d')
        contest = Contest(contest_name=form.name.data, contest_type=form.type.data, contest_time=date,
                          details=form.details.data, level=form.level.data)
        # print(form.contest_time.data)
        # 获取上传文件的文件名;
        filename = form.file.data.filename
        # print(filename)
        basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'], form.name.data)      # 存在以竞赛名的子文件夹中
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)  # 文件夹不存在就创建
        form.file.data.save(os.path.join(file_dir, filename))     # 将上传的文件保存到服务器;
        db.session.add(contest)
        db.session.commit()
        flash('添加竞赛信息成功!')
        return redirect(url_for('index'))
    return render_template("normal_form.html", title='添加竞赛', form=form)


@app.route("/download/<contest_name>")
def downloader(contest_name):
    dirpath = os.path.join(app.root_path, 'upload', contest_name)  #
    # print(contest_name)
    file_name = os.listdir(dirpath)[0]
    # print(file_name)
    # return redirect(url_for('index'))
    response = make_response(send_from_directory(dirpath, file_name, as_attachment=True) )  # as_attachment=True 一定要写，不然会变成打开，而不是下载
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name.encode().decode('latin-1'))
    return response


@app.route('/contest/apply/<contest_id>', methods=['GET', 'POST'])
@login_required
def apply_contest(contest_id):
    # print(type(contest_name))
    form = ApplyContestForm()
    contest = Contest.query.filter(Contest.contest_id == contest_id).first()
    if form.validate_on_submit():
        if not form.name2.data:
            req = Request(user_id=form.id1.data,contest_id=contest_id,status=0,sup_teacher=form.teacher.data,
                          notes=form.notes.data, add_time=datetime.now(), user_type=0)
            db.session.add(req)
        else:
            team = Team(team_name=form.team_name.data)

            # student = Student.query.filter_by(user_id=)
            id = form.id1.data
            if id:
                team.parts.append(Student.query.get(id))
            id = form.id2.data
            if id:
                team.parts.append(Student.query.get(id))
            id = form.id3.data
            if id:
                team.parts.append(Student.query.get(id))
            id = form.id4.data
            if id:
                team.parts.append(Student.query.get(id))
            id = form.id5.data
            if id:
                team.parts.append(Student.query.get(id))
            db.session.add(team)
            # print(team.team_id)
            req = Request(user_id=team.team_id, contest_id=contest_id, status=0, sup_teacher=form.teacher.data,
                          notes=form.notes.data, add_time=datetime.now(), user_type=1)
            db.session.add(req)
        db.session.commit()
        flash('恭喜您，竞赛%s已申请成功!' % contest.contest_name)
        return redirect(url_for('request_list'))
    elif request.method == 'GET':
        form.id1.data = current_user.id
        form.name1.data = current_user.username
    return render_template('apply_contest.html', title='申请竞赛', form=form, contest=contest)


@app.route('/request', methods=['GET', 'POST'])
@login_required
def request_list():
    page = request.args.get('page', 1, type=int)

    # if current_user.type == 'admin':
    #     lists = Request.query.filter().\
    #         paginate(page, app.config['POSTS_PER_PAGE'], False)     # 选取所有学生申请信息
    if current_user.type == 'student':          # 如果为学生，将个人参赛和组队参赛分开查看e
        lists = Request.query.filter_by(user_id=current_user.user_id, user_type=0)\
            .paginate(page, app.config['POSTS_PER_PAGE'], False)     # 选取自己个人的申请信息
        #

    elif current_user.type == 'admin':
        lists = Request.query.filter().\
            paginate(page, app.config['POSTS_PER_PAGE'], False)     # 选取所有学生申请信息
    else:
        tea_type = current_user.get_teacher_type()
        if tea_type == 0:       # 普通教师
            lists = Request.query.filter_by(sup_teacher=current_user.user_id). \
                paginate(page, app.config['POSTS_PER_PAGE'], False)  # 选取自己带队学生申请信息
        else:                   # 管理层教师
            lists = Request.query.filter(). \
                paginate(page, app.config['POSTS_PER_PAGE'], False)  # 选取所有学生申请信息
    next_url = url_for('request_list', page=lists.next_num) \
        if lists.has_next else None
    prev_url = url_for('request_list', page=lists.prev_num) \
        if lists.has_prev else None
    # current_user.
        # return redirect(url_for('index'))
    return render_template("request_list.html", title='竞赛申请列表',
                           lists=lists.items, next_url=next_url, prev_url=prev_url)


@app.route('/request/team', methods=['GET', 'POST'])
@login_required
def request_list_team():        # 如果为学生，将个人参赛和组队参赛分开查看
    page = request.args.get('page', 1, type=int)
    lists = Request.query.join(  # 选出组队参加中所有与自己相关的记录
        team_student, (team_student.c.team_id == Request.user_id)).filter(
        Request.user_type == 1, team_student.c.user_id == current_user.user_id). \
        paginate(page, app.config['POSTS_PER_PAGE'], False)
    # print(lists.items)
    next_url = url_for('request_list_team', page=lists.next_num) \
        if lists.has_next else None
    prev_url = url_for('request_list_team', page=lists.prev_num) \
        if lists.has_prev else None
    return render_template("request_list.html", title='竞赛申请列表',
                           lists=lists.items, next_url=next_url, prev_url=prev_url)


@app.route('/request/<request_id>', methods=['GET', 'POST'])
@login_required
def request_details(request_id):
    req = Request.query.get(request_id)
    if req.user_type == 0:      # 如果为个人申请
        stu = Student.query.get(req.user_id)
        team = None
    else:                       # 如果为组队申请
        team = Team.query.get(req.user_id)
        stu = None
    return render_template("request_details.html", title='申请详情', request=req, user_details=stu, team=team)


# 最开始的ajax，采用JavaScript实现在当前界面做申请，后认为不合适改为跳转为另一界面显示其详细信息
@app.route('/contest/if_agree', methods=['POST'])
@login_required
def if_agree_request():
    req_id = request.form['req']
    status = request.form['agree_status']       # 利用ajax的post请求获取表单数据
    req1 = Request.query.filter_by(request_id=req_id).first()

    if status == 'true':
        req1.status = 1
    else:
        req1.status = 2
    db.session.commit()
    return redirect('/contest/request_list')


@app.route('/request/agree/<request_id>', methods=['GET', 'POST'])
@login_required
def agree_request(request_id):
    req1 = Request.query.filter_by(request_id=request_id).first()
    req1.status = 1
    award = Award(user_id=req1.user_id, user_type=req1.user_type, contest_id=req1.contest_id,
                  sup_teacher=req1.sup_teacher)
    db.session.add(award)
    db.session.commit()
    flash('申请已审核成功!')
    return redirect(url_for('request_list'))


@app.route('/request/disagree/<request_id>', methods=['GET', 'POST'])
@login_required
def disagree_request(request_id):
    req1 = Request.query.filter_by(request_id=request_id).first()
    req1.status = 2
    db.session.commit()
    flash('申请已审核成功!')
    return redirect(url_for('request_list'))


@app.route('/award', methods=['GET', 'POST'])
@login_required
def award_list():
    page = request.args.get('page', 1, type=int)
    lists = Award.query.filter(). \
        paginate(page, app.config['POSTS_PER_PAGE'], False)
    # print(lists.items)
    next_url = url_for('award_list', page=lists.next_num) \
        if lists.has_next else None
    prev_url = url_for('award_list', page=lists.prev_num) \
        if lists.has_prev else None
    return render_template("award_list.html", title='获奖列表',
                           lists=lists.items, next_url=next_url, prev_url=prev_url)


@app.route('/award/<award_id>', methods=['GET', 'POST'])
@login_required
def award_details(award_id):
    award = Award.query.get(award_id)
    if award.user_type == 0:      # 如果为个人申请
        stu = Student.query.get(award.user_id)
        team = None
    else:                       # 如果为组队申请
        team = Team.query.get(award.user_id)
        stu = None
    form = EditAwardForm()
    if form.validate_on_submit():
        award1 = Award.query.filter_by(award_id=award_id).first()
        award1.grade = form.grade.data
        db.session.commit()
        flash('获奖录入成功!')
    return render_template("award_details.html", form=form, title='申请详情',
                           award=award, user_details=stu, team=team)


@app.route("/echarts/<chart_type>")
def echarts(chart_type):
    if chart_type == 'contest':
        _bar = contest_chart()
    elif chart_type == 'award':
        _bar = award_chart()
    # javascript_snippet = TRANSLATOR.translate(_bar.options)     # TRANSLATOR即EChartsTranslator类
    return render_template(
        "echarts.html",
        myechart=_bar.render_embed(),
        host=app.config['REMOTE_HOST'],
        script_list=_bar.get_js_dependencies(),
        # chart_id=_bar.chart_id,
        # renderer=_bar.renderer,
        # my_width="100%",
        # my_height=600,
        # custom_function=javascript_snippet.function_snippet,
        # options=javascript_snippet.option_snippet,

    )


def contest_chart():
    bar = Bar("按参赛种类统计", "这里是副标题", height=600, width="100%")
    contest_types = Contest.query.with_entities(Contest.contest_type).distinct().all()
    print(contest_types)
    join_count = []
    award_count = []
    for types in contest_types:     # types[0]即竞赛种类
        # print(types[0])
        count1 = Award.query.join(  # 选出每一类的参赛人数
            Contest, (Award.contest_id == Contest.contest_id)).filter(
            Contest.contest_type == types[0]).count()
        join_count.append(count1)
        count2 = Award.query.join(  # 选出每一类的获奖人数
            Contest, (Award.contest_id == Contest.contest_id)).filter(
            Contest.contest_type == types[0], Award.grade != '0', Award.grade != '无').count()
        award_count.append(count2)
    bar.add("参赛人数", contest_types, join_count)
    bar.add("获奖人数", contest_types, award_count)
    # bar.use_theme('dark')   # 更换主题
    return bar


def award_chart():
    bar = Bar("按获奖级别统计", "这里是副标题", height=600, width="100%")
    award_types = Award.query.with_entities(Award.grade).\
        filter(Award.grade != '0', Award.grade != '无').distinct().all()
    award_count = []
    for types in award_types:  # types[0]即竞赛种类
        # print(types[0])
        count1 = Award.query.\
            filter(Award.grade == types[0], Award.grade != '无').count()     # 选出每一获奖级别的人数
        award_count.append(count1)
    bar.add("获奖人数", award_types, award_count)
    # bar.use_theme('dark')   # 更换主题
    return bar

# @app.route('/echarts')
# def my_echarts():
#     s3d = scatter3d()
#     return render_template(
#         "echarts.html",
#         myechart=s3d.render_embed(),
#         host=app.config['REMOTE_HOST'],
#         script_list=s3d.get_js_dependencies(),
#     )
#
#
# def scatter3d():
#     data = [generate_3d_random_point() for _ in range(80)]
#     range_color = [
#         "#313695",
#         "#4575b4",
#         "#74add1",
#         "#abd9e9",
#         "#e0f3f8",
#         "#fee090",
#         "#fdae61",
#         "#f46d43",
#         "#d73027",
#         "#a50026",
#     ]
#     scatter3D = Scatter3D("3D scattering plot demo", width=1200, height=600)
#     scatter3D.add("", data, is_visualmap=True, visual_range_color=range_color)
#     return scatter3D
#
#
# def generate_3d_random_point():
#     return [
#         random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)
#     ]



# @app.route('/request/<team_id>/popup')
# @login_required
# def user_popup(team_id):
#     team = Team.query.filter_by(team_id=team_id).first_or_404()
#     return render_template('request_popup.html', team=team.parts)
