import os
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EditPassword, EditWorkForm, EditStudyForm,\
    AddContestForm, ApplyContestForm, AddUserForm, EditAwardForm, EditCreateForm, EditTimeForm, EditNoticeForm, \
    ResetPasswordRequestForm, ResetPasswordForm, AddContestTypeForm
from flask import render_template, flash, redirect, url_for, request, send_from_directory, make_response, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, Contest, Request, Student, Teacher, Team, Award, team_student, Notice, Contest_type
import datetime

from pyecharts import Bar, Pie, Grid, Page, Scatter, Line, configure        # 用于画图表

import numpy as np      # 用于计算相关性
from scipy.stats import pearsonr
from sqlalchemy import func     # 为在query中使用func.count()
from app.email import send_password_reset_email     # 用于重置密码
# import shutil   # 用于删除文件及文件夹
configure(global_theme='dark')         # 规定pycharts的主题roma chalk halloween essos


@app.route('/')
@app.route('/index')
@login_required
def index():
    notice = Notice.query.order_by(Notice.time.desc()).limit(10).all()
    contest = Contest.query.order_by(Contest.contest_time.desc()).limit(4).all()
    return render_template('index.html', title='主页', lists=notice, lists2=contest)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':  # 如果不是相对地址，为防止恶意攻击，跳转到主页
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('normal_form.html', title='登陆', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.id.data).first()
        if not user:
            flash("该用户不存在！请重新输入")
            return redirect(url_for('reset_password_request'))
        if user.email == form.email.data:
            send_password_reset_email(user)
            flash('请查收邮件以重置密码！')
            return redirect(url_for('login'))
        else:
            flash("您输入的邮箱有误！请重新输入")
            return redirect(url_for('reset_password_request'))
    return render_template('normal_form.html',
                           title='重置密码', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('恭喜您，重置密码成功！')
        return redirect(url_for('login'))
    return render_template('normal_form.html', title='重置密码', form=form)


@app.route('/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.type != 'admin':
        abort(404)
    form = AddUserForm()
    if form.validate_on_submit():
        user_type = form.type.data
        id = int(form.user_id.data)
        if user_type == 'student':
            student = Student(user_id=id, username=form.username.data, email=form.email.data, type=form.type.data,
                              major_in=form.major_in.data, tel_num=form.tel_num.data)
            student.set_password(form.password.data)
            db.session.add(student)
        elif user_type == 'teacher':
            teacher = Teacher(user_id=id, username=form.username.data, email=form.email.data, tel_num=form.tel_num.data,
                              type=form.type.data, tea_type=form.tea_type.data)
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
        student = Student(user_id=id, username=form.username.data, email=form.email.data, type='student',
                          major_in=form.major_in.data, tel_num=form.tel_num.data)
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('恭喜您，学生用户%s已注册成功!' % form.username.data)
        return redirect(url_for('login'))
    return render_template('normal_form.html', title='注册', form=form)


@app.route('/notice/add', methods=['GET', 'POST'])
@login_required
def add_notice():
    if current_user.type != 'admin':
        abort(404)
    form = EditNoticeForm()
    if form.validate_on_submit():
        notice = Notice(title=form.title.data, text=form.text.data, time=datetime.datetime.today().date())
        db.session.add(notice)
        db.session.flush()

        basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
        file_dir = os.path.join(basedir, app.config['NOTICE_FOLDER'], str(notice.id))  # 存在以竞赛名的子文件夹中
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)  # 文件夹不存在就创建
        if form.files.data:     # 从上传的多个文件中获取文件列表
            for file in form.files.data:
                file.save(os.path.join(file_dir, file.filename))        # 将上传的文件保存到服务器;

        db.session.commit()
        flash('公告添加成功.')
        return redirect(url_for('index'))

    return render_template('normal_form.html', title='添加公告', form=form)


@app.route('/notice/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_notice(id):
    if current_user.type != 'admin':
        abort(404)
    form = EditNoticeForm()
    notice = Notice.query.get(id)
    if form.validate_on_submit():
        notice.title = form.title.data
        notice.text = form.text.data

        basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
        file_dir = os.path.join(basedir, app.config['NOTICE_FOLDER'], str(notice.id))  # 存在以竞赛名的子文件夹中
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)  # 文件夹不存在就创建
        if form.files.data:  # 从上传的多个文件中获取文件列表
            file_list = os.listdir(file_dir)  # 给出文件列表
            for old_file in file_list:         # 删除原文件
                os.remove(file_dir + old_file)
            for file in form.files.data:        # 添加新文件
                file.save(os.path.join(file_dir, file.filename))  # 将上传的文件保存到服务器;

        db.session.commit()
        flash("公告修改成功！")
        return notice_details(id)
    elif request.method == 'GET':
        form.title.data = notice.title
        form.text.data = notice.text
    return render_template('normal_form.html', title='编辑公告', form=form)


@app.route('/notice/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_notice(id):
    if current_user.type != 'admin':
        abort(404)
    notice = Notice.query.get(id)
    db.session.delete(notice)
    # dirpath = os.path.join(app.root_path, app.config['NOTICE_FOLDER'], id)  # 获得文件路径
    # if os.path.exists(dirpath):
    #     shutil.rmtree('要清空的文件夹名')      # 删除相关文件及文件夹
    db.session.commit()
    flash('删除成功！')
    return redirect(url_for('notice_list'))


@app.route('/notice')
@login_required
def notice_list():
    page = request.args.get('page', 1, type=int)
    lists = Notice.query.filter().order_by(Notice.time.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    return render_template("notice_list.html", title='公告列表',
                           lists=lists.items, pagination=lists)


@app.route('/notice/<id>', methods=['GET', 'POST'])
@login_required
def notice_details(id):
    notice = Notice.query.get(id)
    dirpath = os.path.join(app.root_path, app.config['NOTICE_FOLDER'], id)  # 获得文件路径
    file_list = os.listdir(dirpath)     # 给出文件列表
    return render_template("notice_details.html", list=notice, file_list=file_list)


@app.route("/notice/download/<id>/<filename>")
@login_required
def notice_downloader(id, filename):
    dirpath = os.path.join(app.root_path, app.config['NOTICE_FOLDER'], id)  # 获得文件路径
    response = make_response(send_from_directory(dirpath, filename, as_attachment=True) )  # as_attachment=True 一定要写，不然会变成打开，而不是下载
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response


@app.route('/user/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
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
    if current_user.type != 'student':
        abort(404)
    stu = Student.query.get(current_user.user_id)
    if stu.company_name:
        exist = 'work'
        form = EditWorkForm()
    elif stu.create_type:
        exist = 'create'
        return redirect(url_for('edit_create'))
    elif stu.college_name:
        exist = 'study'
        return redirect(url_for('edit_study'))
    else:
        exist = 'no'
        form = EditWorkForm()
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

    return render_template('edit_work.html', title='添加就业信息', form=form, exist=exist, student=stu)


@app.route('/user/edit/study', methods=['GET', 'POST'])
@login_required
def edit_study():
    if current_user.type != 'student':
        abort(404)
    stu = Student.query.get(current_user.user_id)
    if stu.company_name:
        exist = 'work'
    elif stu.create_type:
        exist = 'create'
    elif stu.college_name:
        exist = 'study'
        form = EditStudyForm()
    else:
        exist = 'no'
        form = EditStudyForm()
        if form.validate_on_submit():
            stu.college_name = form.college_name.data
            stu.college_type = form.college_type.data
            stu.after_major = form.after_major.data
            db.session.commit()
            flash('信息修改成功.')
            return redirect(url_for('edit_study'))
        elif request.method == 'GET':
            form.college_name.data = stu.college_name
            form.college_type.data = stu.college_type
            form.after_major.data = stu.after_major

    return render_template('edit_work.html', title='添加考研信息', form=form, exist=exist, student=stu)


@app.route('/user/edit/create', methods=['GET', 'POST'])
@login_required
def edit_create():
    if current_user.type != 'student':
        abort(404)
    stu = Student.query.get(current_user.user_id)
    if stu.company_name:
        exist = 'work'
    elif stu.college_name:
        exist = 'study'
    elif stu.create_type:
        exist = 'create'
        form = EditCreateForm()
    else:
        exist = 'no'
        form = EditCreateForm()
        if form.validate_on_submit():
            stu.create_type = form.create_type.data
            stu.create_job = form.create_job.data
            db.session.commit()
            flash('信息修改成功.')
            return redirect(url_for('edit_create'))
        elif request.method == 'GET':
            form.create_type.data = stu.create_type
            form.create_job.data = stu.create_job

    return render_template('edit_work.html', title='添加创业信息', form=form, exist=exist, student=stu)


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
@login_required
def contest_list():
    page = request.args.get('page', 1, type=int)
    lists = Contest.query.filter().order_by(Contest.contest_time.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    return render_template("contest_list.html", title='竞赛列表',
                           lists=lists.items, pagination=lists)


@app.route('/contest/type/edit', methods=['GET', 'POST'])
@login_required
def edit_contest_type():
    if current_user.type != 'admin':
        abort(404)
    contest_type = Contest_type.query.filter_by().all()
    form = AddContestTypeForm()
    new_type = form.type.data
    if form.validate_on_submit():
        old_type = Contest_type.query.filter_by(contest_type=new_type).first()
        if old_type:
            flash("该竞赛类型已存在！")
            return redirect(url_for('add_contest_type'))
        new = Contest_type(contest_type=new_type)
        db.session.add(new)
        db.session.commit()
        flash("竞赛类型添加成功！")
        return redirect(url_for('add_contest'))
    return render_template('edit_type.html', lists=contest_type, form=form)


@app.route('/contest/type/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_contest_type(id):
    if current_user.type != 'admin':
        abort(404)
    type = Contest_type.query.get(id)
    db.session.delete(type)
    db.session.commit()
    flash('删除成功！')
    return redirect(url_for('edit_contest_type'))


@app.route('/contest/add', methods=['GET', 'POST'])
@login_required
def add_contest():
    if current_user.type != 'admin':
        abort(404)
    form = AddContestForm()
    if form.validate_on_submit():
        date = form.time.data.strftime('%Y-%m-%d')
        contest = Contest(contest_name=form.name.data, contest_type=form.type.data, contest_time=date,
                          details=form.details.data, level=form.level.data, filename=form.file.data.filename)
        # 获取上传文件的文件名;记录到数据库中，方便标识该竞赛是否有文件
        filename = form.file.data.filename
        db.session.add(contest)
        db.session.flush()
        # print(filename)
        basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'], str(contest.contest_id))  # 存在以竞赛id的子文件夹中
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)  # 文件夹不存在就创建
        form.file.data.save(os.path.join(file_dir, filename))     # 将上传的文件保存到服务器;
        db.session.commit()
        flash('添加竞赛信息成功!')
        return redirect(url_for('index'))
    return render_template("normal_form.html", title='添加竞赛', form=form)


@app.route("/download/<contest_id>")
@login_required
def downloader(contest_id):
    dirpath = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], contest_id)  #
    file_name = os.listdir(dirpath)[0]  # 因为只有一个文件，直接取即可
    response = make_response(send_from_directory(dirpath, file_name, as_attachment=True) )  # as_attachment=True 一定要写，不然会变成打开，而不是下载
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name.encode().decode('latin-1'))
    return response


@app.route('/contest/<contest_id>', methods=['GET', 'POST'])
@login_required
def contest_details(contest_id):
    form = ApplyContestForm()
    contest = Contest.query.filter(Contest.contest_id == contest_id).first()
    if form.validate_on_submit():
        try:  # 查看指导教师是否存在
            tea1 = int(form.teacher.data)
            teacher = User.query.get(tea1)
        except ValueError:
            flash("指导教师的ID不存在！")
            return redirect(url_for('contest_details', contest_id=contest_id))
        if not teacher:
            flash("指导教师的ID不存在！")
            return redirect(url_for('contest_details', contest_id=contest_id))

        id1 = current_user.user_id      # 第一个人即自己，直接获取当前用户信息即可
        if not form.id2.data:
            req = Request(user_id=id1,contest_id=contest_id,status=0,sup_teacher=tea1,
                          notes=form.notes.data, add_time=datetime.datetime.now(), user_type=0)
            db.session.add(req)

        else:
            team = Team(team_name=form.team_name.data)
            id = id1
            team.parts.append(Student.query.get(id))
            id2 = form.id2.data
            if id2:
                try:                 # 查看该ID是否存在
                    id2 = int(form.id2.data)
                    stu2 = Student.query.get(id2)
                except ValueError:
                    flash("学生2的ID不存在！")
                    return redirect(url_for('contest_details', contest_id=contest_id))
                if id2 == current_user.user_id:
                    flash("填写的ID有重复！")
                    return redirect(url_for('contest_details', contest_id=contest_id))
                elif not stu2:
                    flash("学生2的ID不存在！")
                    return redirect(url_for('contest_details', contest_id=contest_id))
                else:
                    team.parts.append(stu2)

            id3 = form.id3.data
            if id3:
                try:  # 查看该ID是否存在
                    id3 = int(form.id3.data)
                    stu3 = Student.query.get(id3)
                except ValueError:
                    flash("学生3的ID不存在！")
                    return redirect(url_for('contest_details', contest_id=contest_id))
                if id3 == current_user.user_id or id3 == id2:
                    flash("填写的ID有重复！")
                    return redirect(url_for('contest_details', contest_id=contest_id))
                elif not stu3:
                    flash("学生3的ID不存在！")
                    return redirect(url_for('contest_details', contest_id=contest_id))
                else:
                    team.parts.append(stu3)

            id4 = form.id4.data
            if id4:
                try:  # 查看该ID是否存在
                    id4 = int(form.id4.data)
                    stu4 = Student.query.get(id4)
                except ValueError:
                    flash("学生4的ID不存在！")
                    return redirect(url_for('contest_details', contest_id=contest_id))
                if id4 == current_user.user_id or id4 == id3 or id4 == id2:
                    flash("填写的ID有重复！")
                    return redirect(url_for('contest_details', contest_id=contest_id))
                elif not stu4:
                    flash("学生4的ID不存在！")
                    return redirect(url_for('contest_details', contest_id=contest_id))
                else:
                    team.parts.append(stu4)

            id5 = form.id5.data
            if id5:
                try:  # 查看该ID是否存在
                    id5 = int(form.id5.data)
                    stu5 = Student.query.get(id5)
                except ValueError:
                    flash("学生5的ID不存在！")
                    return redirect(url_for('contest_details', contest_id=contest_id))
                if id5 == current_user.user_id or id5 == id2 or id5 == id3 or id5 == id4:
                    flash("填写的ID有重复！")
                    return redirect(url_for('contest_details', contest_id=contest_id))
                elif not stu5:
                    flash("学生5的ID不存在！")
                    return redirect(url_for('contest_details', contest_id=contest_id))
                else:
                    team.parts.append(stu5)

            req = Request(user_id=team.team_id, contest_id=contest_id, status=0, sup_teacher=form.teacher.data,
                          notes=form.notes.data, add_time=datetime.datetime.now(), user_type=1)
            db.session.add(req)
        db.session.commit()
        flash('恭喜您，竞赛%s已申请成功!' % contest.contest_name)
        if stu2:
            return redirect(url_for('request_list_team'))
        else:
            return redirect(url_for('request_list'))

    return render_template('contest_details.html', title='申请竞赛', form=form, contest=contest)


@app.route('/request', methods=['GET', 'POST'])
@login_required
def request_list():
    page = request.args.get('page', 1, type=int)

    if current_user.type == 'student':          # 如果为学生，将个人参赛和组队参赛分开查看e
        lists = Request.query.filter_by(user_id=current_user.user_id, user_type=0).order_by(Request.add_time.desc())\
            .paginate(page, app.config['POSTS_PER_PAGE'], False)     # 选取自己个人的申请信息

    elif current_user.type == 'admin':
        lists = Request.query.filter().order_by(Request.add_time.desc()).\
            paginate(page, app.config['POSTS_PER_PAGE'], False)     # 选取所有学生申请信息
    else:
        tea_type = current_user.get_teacher_type()
        if tea_type == 0:       # 普通教师
            lists = Request.query.filter_by(sup_teacher=current_user.user_id).order_by(Request.add_time.desc()). \
                paginate(page, app.config['POSTS_PER_PAGE'], False)  # 选取自己带队学生申请信息
        else:                   # 管理层教师
            lists = Request.query.filter().order_by(Request.add_time.desc()). \
                paginate(page, app.config['POSTS_PER_PAGE'], False)  # 选取所有学生申请信息

    return render_template("request_list.html", title='竞赛申请列表',
                           lists=lists.items, pagination=lists)


@app.route('/request/team', methods=['GET', 'POST'])
@login_required
def request_list_team():        # 如果为学生，将个人参赛和组队参赛分开查看
    if current_user.type != 'student':
        abort(404)
    page = request.args.get('page', 1, type=int)
    lists = Request.query.join(  # 选出组队参加中所有与自己相关的记录
        team_student, (team_student.c.team_id == Request.user_id)).filter(
        Request.user_type == 1, team_student.c.user_id == current_user.user_id).order_by(Request.add_time.desc()). \
        paginate(page, app.config['POSTS_PER_PAGE'], False)

    return render_template("request_list.html", title='竞赛申请列表',
                           lists=lists.items, pagination=lists)


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


def if_request_admin():             # 判断是否是有权限对学生申请信息进行更改的用户
    if current_user.type == 'admin':
        return True
    elif current_user.type == 'teacher':
        if current_user.get_teacher_type() == 1:
            return True
    return False


@app.route('/request/agree/<request_id>', methods=['GET', 'POST'])
@login_required
def agree_request(request_id):
    if not if_request_admin():
        abort(404)
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
    if not if_request_admin():
        abort(404)
    req1 = Request.query.filter_by(request_id=request_id).first()
    req1.status = 2
    db.session.commit()
    flash('申请已审核成功!')
    return redirect(url_for('request_list'))


@app.route('/award', methods=['GET', 'POST'])
@login_required
def award_list():
    page = request.args.get('page', 1, type=int)
    lists = Award.query.join(Contest, (Contest.contest_id==Award.contest_id)).\
        order_by(Contest.contest_time.desc()).filter(). \
        paginate(page, app.config['POSTS_PER_PAGE'], False)

    return render_template("award_list.html", title='参赛/获奖列表',
                           lists=lists.items, pagination=lists)


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


def cut_piece(num):
    """
    将数据分段记录，返回的是所属数据段
    :param num:
    :return:
    """
    piece = 0
    if num in range(0, 3999):
        piece = 0
    elif num in range(4000, 5999):
        piece = 4000
    elif num in range(6000, 7999):
        piece = 6000
    elif num in range(8000, 10000):
        piece = 8000
    elif num > 10000:
        piece = 10000
    return piece


def dict_to_numpy(dict1):       # 将字典类型转换为数组，并计算相应的皮尔逊系数
    """
    将字典类型转换为两个数组，并计算相应的皮尔逊系数
    data为分段后的数据，data2为未分段的原始数据
    :param dict1: 原字典
    :return: pear,data,data2
    """
    x,y = [],[]     # 每个学生对应的参赛情况和就业情况
    for record in dict1:
        x.append(record[0])
        y.append(record[1])
    xnp = np.array(x)
    ynp = np.array(y)
    pear,p2 = pearsonr(xnp,ynp)

    lists = []
    data = []
    for record in dict1:
        piece1 = cut_piece(record[1])
        each = record[0],piece1
        each = list(each)
        data1 = record[0],piece1,1
        data1 = list(data1)
        # print('data;',data)
        if each in lists:
            for item in data:
                if item[0] == record[0] and item[1] == record[1]:
                    item[2] = item[2]+1
        else:
            lists.append(each)
            data.append(data1)

    lists = []
    data2 = []
    for record in dict1:
        piece1 = record[1]
        each = record[0], piece1
        each = list(each)
        data1 = record[0], piece1, 1
        data1 = list(data1)

        if each in lists:
            for item in data2:
                if item[0] == record[0] and item[1] == record[1]:
                    item[2] = item[2] + 1
        else:
            lists.append(each)
            data2.append(data1)

    return format(pear, '.3f'), data, data2  # 保留三位小数


def user_describe(pear):
    flag1 = None
    if pear != 'nan':
        pear = float(pear)
        if pear > 0:
            flag1 = '正相关，且'
        else:
            flag1 = '负相关，且'
            pear = -pear
        if pear<0.3:
            flag1 = flag1 + '相关性非常弱'
        elif pear<0.7:
            flag1 = flag1 + '相关性较强'
        else:
            flag1 = flag1 + '相关性极强'
        return flag1
    return None


def custom_formatter(params):
    return '此点人数'+params.value[2]


@app.route("/relate/<type>")
@login_required
def relate(type):
    page = Page()
    if type == 'contest':
        title = '参加比赛次数'
        c_w,c_s = relate_work('contest')
        scatter = Scatter("参赛-就业")
        pear1, piece, data = dict_to_numpy(c_w)     # piece为分段后的数据，data为未分段的原始数据
        flag1 = user_describe(pear1)

        x_lst = [v[0] for v in data]
        y_lst = [v[1] for v in data]
        extra_data = [v[2] for v in data]
        scatter.add(
            "参赛-就业", x_lst, y_lst,
            xaxis_name='参赛次数',
            yaxis_name='就职薪水',
            xaxis_name_pos='end',
            yaxis_name_pos='middle',
            yaxis_name_gap=40,
            extra_data=extra_data,
            tooltip_formatter=custom_formatter,
            is_visualmap=True,
            visual_dimension=2,
            visual_orient="horizontal",
            visual_range_size=[6, 200],
            visual_type="size",
            visual_range=[0, 100],
            visual_text_color="#000",
        )
        page.add_chart(scatter, name='参赛-就业')

        pear2, piece2, data2 = dict_to_numpy(c_s)
        flag2 = user_describe(pear2)

        x_2st = [v[0] for v in data2]
        y_2st = [v[1] for v in data2]
        extra_data2 = [v[2] for v in data2]
        scatter2 = Scatter("参赛-考研\n(类型1,2,3分别对应为985,211,普通高校)")

        scatter2.add(
            "参赛-考研", x_2st, y_2st,
            xaxis_name='参赛次数',
            yaxis_name='学校类型',
            xaxis_name_pos='end',
            yaxis_name_pos='middle',
            yaxis_max=3,
            yaxis_force_interval=1,
            extra_data=extra_data2,
            tooltip_formatter=custom_formatter,
            is_visualmap=True,
            visual_dimension=2,
            visual_orient="horizontal",
            visual_range_size=[6, 200],
            visual_type="size",
            visual_range=[0, 100],
            visual_text_color="#000",
        )
        page.add_chart(scatter2, name='参赛-考研')

    elif type == 'award':
        title = '获奖次数'
        a_w, a_s = relate_work('award')
        pear1, piece, data = dict_to_numpy(a_w)     # piece为分段后的数据，data为未分段的原始数据
        flag1 = user_describe(pear1)

        title = '获得奖项次数'
        c_w,c_s = relate_work('award')
        scatter = Scatter("获奖-就业")

        x_lst = [v[0] for v in data]
        y_lst = [v[1] for v in data]
        extra_data = [v[2] for v in data]
        scatter.add(
            "获奖-就业", x_lst, y_lst,
            xaxis_name='获奖次数',
            yaxis_name='就职薪水',
            xaxis_name_pos='end',
            yaxis_name_pos='middle',
            yaxis_name_gap=40,
            extra_data=extra_data,
            tooltip_formatter=custom_formatter,
            is_visualmap=True,
            visual_dimension=2,
            visual_orient="horizontal",
            visual_range_size=[6, 200],
            visual_type="size",
            visual_range=[0, 100],
            visual_text_color="#000",
        )
        page.add_chart(scatter, name='获奖-就业')

        pear2, piece2, data2 = dict_to_numpy(c_s)
        flag2 = user_describe(pear2)

        x_2st = [v[0] for v in data2]
        y_2st = [v[1] for v in data2]
        extra_data2 = [v[2] for v in data2]
        scatter2 = Scatter("获奖-考研\n(类型[1,2,3]分别对应为[985,211,普通高校])")

        scatter2.add(
            "获奖-考研", x_2st, y_2st,
            xaxis_name='获奖次数',
            yaxis_name='学校类型',
            xaxis_name_pos='end',
            yaxis_name_pos='middle',
            yaxis_max=3,
            yaxis_force_interval=1,
            extra_data=extra_data2,
            tooltip_formatter=custom_formatter,
            is_visualmap=True,
            visual_dimension=2,
            visual_orient="horizontal",
            visual_range_size=[6, 200],
            visual_type="size",
            visual_range=[0, 100],
            visual_text_color="#000",
        )
        page.add_chart(scatter2, name='获奖-考研')
    return render_template("relate.html", title=title, pear1=pear1, flag1=flag1, configure=configure,
                           myechart=page.render_embed(), host=app.config['REMOTE_HOST'],
                           script_list=page.get_js_dependencies(),
                           data=piece, x_list=range(0,10), y_list=[0,4000,6000,8000,10000],
                           pear2=pear2, flag2=flag2, data2=data2, x_list2=range(0,10), y_list2=[1,2,3])


def relate_work(type):
    if type == 'contest':
        ss = db.session.query(Award.user_id, func.count(Award.user_id)).filter(Award.user_type == 0).group_by(
            Award.user_id).all()        # 获取个人的参赛记录
    elif type == 'award':
        ss = db.session.query(Award.user_id, func.count(Award.user_id)).\
            filter(Award.user_type == 0, Award.grade != '0', Award.grade != '无').group_by(
            Award.user_id).all()  # 获取个人的获奖记录
    dict1 = {}
    for s in ss:
        dict1[s[0]] = s[1]
    if type == 'contest':
        ss1 = db.session.query(Award.user_id, team_student.c.user_id, func.count(team_student.c.user_id)). \
            join(team_student, (team_student.c.team_id == Award.user_id)). \
            filter(Award.user_type == 1).group_by(team_student.c.user_id).all()     # 获取组队的参赛记录
    elif type == 'award':
        ss1 = db.session.query(Award.user_id, team_student.c.user_id, func.count(team_student.c.user_id)). \
            join(team_student, (team_student.c.team_id == Award.user_id)). \
            filter(Award.user_type == 1, Award.grade != '0', Award.grade != '无').\
            group_by(team_student.c.user_id).all()  # 获取组队的获奖记录
    dict2 = {}
    for s in ss1:
        dict2[s[1]] = s[2]
    for key, value in dict2.items():    # 将同一学生的个人、组队情况统一起来，放入dict1中，格式为{id:count}
        if key in dict1:
            dict1[key] += value
        else:
            dict1[key] = value

    c_w, c_s ,c_c = [],[],[]
    for key, value in dict1.items():       # key为id，value为参赛次数
        stu = Student.query.get(key)
        if stu.company_name:    # 如果该学生为就业，则添加其薪水为一条记录
            c_w.append((value, stu.salary))
        elif stu.college_name:
            types = stu.college_type
            if types == '985高校':
                c_s.append((value, 3))
            elif types == '211高校':
                c_s.append((value, 2))
            elif types == '普通高校':
                c_s.append((value, 1))

    return c_w,c_s


@app.route("/echarts/<chart_type>", methods=['GET', 'POST'])
@login_required
def echarts(chart_type):
    end = datetime.date.today()
    start = datetime.datetime(end.year, 1, 1)  # 默认时间为今年第一天到今天为止
    form = EditTimeForm()
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']

    if chart_type == 'contest_bar':     # 竞赛种类-柱状图
        _bar = contest_bar(start, end)
        title = '参赛（获奖）情况-按竞赛种类'
    elif chart_type == 'award_bar':     # 获奖级别-柱状图
        _bar = award_bar(start, end)
        title = '获奖情况-按获奖级别'
    elif chart_type == 'contest_pie':   # 竞赛种类-饼图
        _bar = contest_pie(start, end)
        title = '参赛（获奖）情况-按竞赛种类'
    elif chart_type == 'award_pie':     # 获奖级别-饼图
        _bar = award_pie(start, end)
        title = '获奖情况-按获奖级别'

    return render_template(
        "echarts.html",
        title=title,
        form=form,
        myechart=_bar.render_embed(),
        host=app.config['REMOTE_HOST'],
        script_list=_bar.get_js_dependencies(),
    )


def contest_bar(start, end):
    bar = Bar("参赛种类统计", height=500, width="100%", title_text_size=30)
    contest_types = Contest.query.with_entities(Contest.contest_type).distinct().all()
    join_count = []
    award_count = []
    type = []
    for types in contest_types:     # types[0]即竞赛种类
        type.append(types[0])
        count1 = Award.query.join(  # 选出每一类的参赛人数
            Contest, (Award.contest_id == Contest.contest_id)).filter(
            Contest.contest_type == types[0], Contest.contest_time >= start, Contest.contest_time <= end).count()
        join_count.append(count1)
        count2 = Award.query.join(  # 选出每一类的获奖人数
            Contest, (Award.contest_id == Contest.contest_id)).filter(
            Contest.contest_type == types[0], Contest.contest_time >= start, Contest.contest_time <= end,
            Award.grade != '0', Award.grade != '无').count()
        award_count.append(count2)
    bar.add("参赛人数", contest_types, join_count, legend_text_size=20, xaxis_label_textsize=20, yaxis_force_interval=1)
    bar.add("获奖人数", contest_types, award_count, legend_text_size=20, xaxis_label_textsize=20, yaxis_force_interval=1)
    return bar


def award_bar(start, end):
    bar = Bar("获奖级别统计", height=500, width="100%", title_text_size=30)
    award_types = ['一等奖', '二等奖', '三等奖', '优秀奖']
    award_count = []
    for types in award_types:  # types[0]即竞赛种类
        count1 = Award.query.join(Contest, (Contest.contest_id == Award.contest_id)).filter(
            Contest.contest_time >= start, Contest.contest_time <= end,
            Award.grade == types[0], Award.grade != '无').count()    # 选出每一获奖级别的人数
        award_count.append(count1)

    bar.add("获奖人数", award_types, award_count,
            legend_text_size=20, label_text_size=20, xaxis_label_textsize=20, yaxis_force_interval=1)
    return bar


def contest_pie(start, end):
    pie1 = Pie("获奖比例", title_pos='center', title_text_size=30)
    pie2 = Pie("参赛比例", title_text_size=30)
    contest_types = Contest.query.with_entities(Contest.contest_type).distinct().all()
    join_count = []
    award_count = []
    for types in contest_types:  # types[0]即竞赛种类
        count1 = Award.query.join(  # 选出每一类的参赛人数
            Contest, (Award.contest_id == Contest.contest_id)).filter(
            Contest.contest_type == types[0], Contest.contest_time >= start, Contest.contest_time <= end).count()
        join_count.append(count1)
        count2 = Award.query.join(  # 选出每一类的获奖人数
            Contest, (Award.contest_id == Contest.contest_id)).filter(
            Contest.contest_type == types[0], Contest.contest_time >= start, Contest.contest_time <= end,
            Award.grade != '0', Award.grade != '无').count()
        award_count.append(count2)
    pie1.add("参赛情况", contest_types, join_count, is_label_show=True, center=[25,60] ,legend_pos="20%", label_text_size=20)
    pie2.add("获奖情况", contest_types, award_count, is_label_show=True, center=[75,60], legend_pos="80%", label_text_size=20)
    gird = Grid(width=1200)
    gird.add(pie1, grid_right="55%")
    gird.add(pie2, grid_left="60%")
    return gird


def award_pie(start, end):
    pie = Pie("各奖项获奖比例", height=500, width="100%", title_text_size=30)
    award_types = Award.query.with_entities(Award.grade).\
        filter(Award.grade != '0', Award.grade != '无').distinct().all()
    award_count = []
    for types in award_types:  # types[0]即竞赛种类
        count1 = Award.query.join(Contest, (Contest.contest_id == Award.contest_id)).filter(
            Contest.contest_time >= start, Contest.contest_time <= end,
            Award.grade == types[0], Award.grade != '无').count()     # 选出每一获奖级别的人数
        award_count.append(count1)
    pie.add("", award_types, award_count, is_label_show=True, label_text_size=20)

    return pie
