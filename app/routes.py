from flask import render_template
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddContestForm, ApplyContestForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Contest, Request
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
        user = User.query.filter_by(id=form.id.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
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
        user = User(username=form.username.data, id=int(form.id.data), email=form.email.data, type=form.type.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜您，用户%s已注册成功!' % form.username.data)
        return redirect(url_for('index'))
    return render_template('add_user.html', title='添加用户', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    form.type.data = 1
    if form.validate_on_submit():
        user = User(username=form.username.data, id=int(form.id.data), email=form.email.data, type=1)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print(user)
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


@app.route('/edit_profile', methods=['GET', 'POST'])
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
        contest = Contest(contest_name=form.name.data, contest_type=form.type.data,
                          details=form.details.data, level=form.level.data)
        db.session.add(contest)
        db.session.commit()
        flash('添加竞赛信息成功!')
        return redirect(url_for('index'))
    return render_template("add_contest.html", title='添加竞赛', form=form)


@app.route('/user/apply/<contest_name>', methods=['GET', 'POST'])
@login_required
def apply_contest(contest_name):
    # print(type(contest_name))
    form = ApplyContestForm()
    if form.validate_on_submit():
        req = Request(id=current_user.id,username=current_user.username,contest_name=contest_name,
                      notes=form.notes.data, add_time=datetime.now())
        db.session.add(req)
        db.session.commit()
        flash('恭喜您，竞赛%s已申请成功!' % contest_name)
        return redirect(url_for('index'))
    return render_template('apply_contest.html', title='申请竞赛', form=form, contest_name=contest_name)
