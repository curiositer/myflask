from flask import render_template
import os
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddContestForm, ApplyContestForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Contest, Request, Student, Teacher, Team
from datetime import datetime


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
        print(user)
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='登陆', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_type = form.type.data
        id = int(form.user_id.data)
        if user_type == 'student':
            student = Student(user_id=id, username=form.username.data, email=form.email.data, type=form.type.data,
                              stu_class=form.stu_class.data, tel_num=form.tel_num.data)
            student.set_password(form.password.data)
            db.session.add(student)
        elif user_type == 'teacher':
            teacher = Teacher(user_id=id, username=form.username.data, email=form.email.data, type=form.type.data,
                              stu_class=form.stu_class.data,tea_type=form.tea_type.data)
            teacher.set_password(form.password.data)
            db.session.add(teacher)
        else:
            admin = User(user_id=id, username=form.username.data, email=form.email.data, type=form.type.data)
            admin.set_password(form.password.data)
            db.session.add(admin)
        db.session.commit()
        flash('恭喜您，用户%s已注册成功!' % form.username.data)
        return redirect(url_for('index'))
    return render_template('add_user.html', title='添加用户', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        id = int(form.user_id.data)
        print(id)
        student = Student(user_id=id, username=form.username.data, email=form.email.data, type=form.type.data,
                          stu_class=form.stu_class.data, tel_num=form.tel_num.data)
        student.set_password(form.password.data)
        print(student)
        db.session.add(student)
        db.session.commit()
        flash('恭喜您，学生用户%s已注册成功!' % form.username.data)
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


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
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('信息修改成功.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='编辑资料',
                           form=form)


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
        contest = Contest(contest_name=form.name.data, contest_type=form.type.data, contest_time=form.time.data,
                          details=form.details.data, level=form.level.data)
        # print(form.contest_time.data)
        # 获取上传文件的文件名;
        filename = form.file.data.filename
        print(filename)
        basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'], form.name.data)      # 存在以竞赛名的子文件夹中
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)  # 文件夹不存在就创建
        form.file.data.save(os.path.join(file_dir, filename))     # 将上传的文件保存到服务器;
        db.session.add(contest)
        db.session.commit()
        flash('添加竞赛信息成功!')
        return redirect(url_for('index'))
    return render_template("add_contest.html", title='添加竞赛', form=form)


@app.route('/contest/apply/<contest_id>', methods=['GET', 'POST'])
@login_required
def apply_contest(contest_id):
    # print(type(contest_name))
    form = ApplyContestForm()
    contest = Contest.query.filter(Contest.contest_id == contest_id).first()
    if form.validate_on_submit():
        if not form.name2.data:
            req = Request(user_id=form.id1.data,contest_id=contest_id,status=0,
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
            req = Request(user_id=team.team_id, contest_id=contest_id, status=0,
                          notes=form.notes.data, add_time=datetime.now(), user_type=1)
            db.session.add(req)
        db.session.commit()
        flash('恭喜您，竞赛%s已申请成功!' % contest.contest_name)
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.id1.data = current_user.id
        form.name1.data = current_user.username
    return render_template('apply_contest.html', title='申请竞赛', form=form, contest=contest)


@app.route('/contest/apply_list', methods=['GET', 'POST'])
@login_required
def apply_list():
    page = request.args.get('page', 1, type=int)

    if current_user.type == 'admin':
        lists = Request.query.filter().\
            paginate(page, app.config['POSTS_PER_PAGE'], False)     # 选取所有学生申请信息
    elif current_user.type == 'student':
        lists = Request.query.filter_by(user_id=current_user.user_id).\
            paginate(page, app.config['POSTS_PER_PAGE'], False)     # 选取自己的申请信息
    else:
        lists = Request.query.filter().\
            paginate(page, app.config['POSTS_PER_PAGE'], False)     # 选取自己管理班级的学生申请信息
    next_url = url_for('apply_list', page=lists.next_num) \
        if lists.has_next else None
    prev_url = url_for('apply_list', page=lists.prev_num) \
        if lists.has_prev else None

        # return redirect(url_for('index'))
    return render_template("request_list.html", title='竞赛申请列表',
                           lists=lists.items, next_url=next_url, prev_url=prev_url)


@app.route('/contest/agree', methods=['POST'])
@login_required
def agree_request():
    req_id = request.form['req']
    status = request.form['agree_status']       # 利用ajax的post请求获取表单数据
    req1 = Request.query.filter_by(req_id=req_id).first()

    if status == 'true':
        req1.status = 1
    else:
        req1.status = 2
    db.session.commit()
    return redirect('/contest/apply_list')


# @app.route('/request/<team_id>/popup')
# @login_required
# def user_popup(team_id):
#     team = Team.query.filter_by(team_id=team_id).first_or_404()
#     return render_template('request_popup.html', team=team.parts)
