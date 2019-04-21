from app import app, db
from app.models import User, Contest, Request, Student, Teacher, Team, Award, team_student
import random

# 添加数据专用

def add_student(start, end):
    ids = range(start, end)
    password = 1
    types = ['机械工程', '软件工程', '工业工程', '自动化', '电子信息工程', '汽车服务工程']
    for id in ids:
        major_types = random.choice(types)
        tel = random.randint(13000000000,19000000000)
        # print(major_types, tel)
        name = ''.join(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
             'e', 'd', 'c', 'b', 'a'], 5))
        username = 'stu_' + name
        stu = Student(user_id=id,major_in=major_types,tel_num=tel, username=username)
        stu.set_password(str(password))
        db.session.add(stu)
        # stu = Student.query.get(id)
        # print(stu.username)
    db.session.commit()


def add_teacher(start, end):
    ids = range(start, end)
    password = 1
    # types = ['机械工程', '软件工程', '工业工程', '自动化', '电子信息工程', '汽车服务工程']
    for id in ids:
        # major_types = random.choice(types)
        tel = random.randint(13000000000,19000000000)
        types = random.randint(0,1)
        # print(major_types, tel)
        name = ''.join(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
             'e', 'd', 'c', 'b', 'a'], 5))
        username = 'tea_' + name
        email = str(id) + '@test.com'
        stu = Teacher(user_id=id, tea_type=types,tel_num=tel, username=username, email=email)
        stu.set_password(str(password))
        db.session.add(stu)
        # stu = Student.query.get(id)
        # print(stu.username)
    db.session.commit()


import time, datetime
def randomtimes(start, end, frmt="%Y-%m-%d"):
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))

    ptime = stime + random.random() * (etime - stime)
    return time.strftime(frmt, time.localtime(ptime))


def add_contest(start, end):
    ids = range(start, end)
    password = 1
    types = ['科技', '人文', '体育', '理科', '综合']
    levels = ['校级', '市级', '省级', '国家级', '国际级']

    for id in ids:
        # major_types = random.choice(types)
        # tel = random.randint(13000000000,19000000000)
        # types = random.randint(0,1)
        # print(major_types, tel)
        # name = ''.join(random.sample(
        #     ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
        #      'e', 'd', 'c', 'b', 'a'], 5))
        time = randomtimes('2017-01-01', '2020-01-01')
        print(time)
        type = random.choice(types)
        level = random.choice(levels)
        name = '竞赛' + str(id)
        detail = '第' + str(id) + '个竞赛'
        # email = str(id) + '@test.com'
        stu = Contest(contest_name=name, contest_type=type, contest_time=time, details=detail, level=level)
        # stu.set_password(str(password))
        db.session.add(stu)
        # stu = Student.query.get(id)
        # print(stu.username)
    db.session.commit()


def add_request(type,count):
    '''
    批量添加竞赛申请
    :param type: 队伍有多少人
    :param count: 要添加多少条申请信息
    :return:
    '''
    for i in range(count):
        contest_id = random.randint(1, 29)

        teacher = random.randint(200, 220)
        id1 = random.randint(101, 110)
        id2 = random.randint(111, 120)
        id3 = random.randint(121, 130)
        id4 = random.randint(131, 140)
        if type == 1:
            id2 = None
            id3 = None
            id4 = None
        elif type == 2:
            id3 = None
            id4 = None
        elif type == 3:
            id4 = None

        print(id1, id2, id3)
        if not id2:
            req = Request(user_id=id1, contest_id=contest_id, status=0, sup_teacher=teacher,
                          add_time=datetime.datetime.now(), user_type=0)
            db.session.add(req)
        else:
            team_name = ''.join(random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                 'f',
                 'e', 'd', 'c', 'b', 'a'], 5))
            team = Team(team_name=team_name)

            # student = Student.query.filter_by(user_id=)
            id = id1
            if id:
                team.parts.append(Student.query.get(id))
            id = id2
            if id:
                team.parts.append(Student.query.get(id))
            id = id3
            if id:
                team.parts.append(Student.query.get(id))
            id = id4
            if id:
                team.parts.append(Student.query.get(id))
            # id = id5
            # if id:
            #     team.parts.append(Student.query.get(id))
            db.session.add(team)
            # print(team.team_id)
            req = Request(user_id=team.team_id, contest_id=contest_id, status=0, sup_teacher=teacher,
                          add_time=datetime.datetime.now(), user_type=1)
            db.session.add(req)
    db.session.commit()


def agree_request():
    for i in range(40, 49):
        print(i)
        request_id = i
        req1 = Request.query.get(request_id)
        req1.status = 1
        award = Award(user_id=req1.user_id, user_type=req1.user_type, contest_id=req1.contest_id,
                      sup_teacher=req1.sup_teacher)
        print(req1.user_id)
        db.session.add(award)
        # print(award.award_id)
    db.session.commit()


def award_in():
    ids = range(28 , 34)
    types = ['优秀奖', '一等奖', '二等奖', '三等奖', '无']
    for id in ids:
        type = random.choice(types)
        awd = Award.query.get(id)
        awd.grade = type
    db.session.commit()


# add_contest(10,30)
# add_teacher(200, 230)
# add_request(2, 5)
# agree_request()
# award_in()


