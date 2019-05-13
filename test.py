# coding=gbk
from app import app, db
from app.models import User, Contest, Request, Student, Teacher, Team, Award, team_student, Notice
import random

# �������ר��

name_list = ['����', '����ͩ', '�Խ���', '������', '�Լ���', '������', '�Լ���', '����ͮ', '�����', '������', '��ܲ��', '������', '�Խ���', '����', '�Կ���', '�Բ���', '������', '������', '������', '�Ժ��', '���ﺭ', '���', '�Ժ���', '���غ�', '���ﺭ', '�Խ�', '�Ժƺ�', '���ﺭ', '�Ծ�Ρ', '�Կ�', '������', '����', '������', '�����', '�Կ���', '������', '����', '�����', '������', '������', '�����', '������', '����ɺ', '�Ծ��', '��溾�', '����', '������', '�����', '����', '�Ծ���', '�����', '����', '�Դ�', '������', '�Գ���', '�Խ���', '������', '��´ة', '������', '�����', '������', '��̫��', '������', '���ڷ�', '�����', '����ͮ', '���࿡', '���ȿ�', '�Խ�ΰ', '��ůů', '���', '���ٿ�', '���ȿ�', '���ȿ�', '���ٿ�', '���',
             '����', '����', '����', '���ղ�', '��ΰ', '����˶', '������', '������', '������', '����', '������', '����΢', '������', '������', '��ܷ��', '������', '�����', '������', '������', '������', '����ѫ', '��˼׿', '������', '����', '������', '���', '���h��', '������', '���h��', '�����', '���곽', '������', '������', '�����', '������', '������', '������', '���', '��֮��', '���ӿ�', '���ų�', '���ã', '����۲', '����', '������', '������', '��ʫ��', '��˼ܰ', '������', '��˼˼', '���η�', '���Ͳ�', '������', '������', '������', '������', '������', '���ز�', '������', '����Ұ', '�����', '�����', '�����', '������', '������', '��躲�', '������', '�����h', '������', '������',
             '������', '�����', '����Դ', '��ӯ��', '���»�', '����', '�����h', '���ϫh', '�����', '����h', '������', '������', '������', '������', '�����', '������', '������', '������', '������', '������', '��˼��', '������', '������', '�����', '����', '��ɭ��', '����ʤ', '�����', '������', '���ľ�', '����Դ', '������', '��ϣ��', '��ϣ��', '������', '������', '������', '��һԽ', '��һ��', '��Խ', '��Ľ��', '������', '����ֱ', '������', '������', '������', '��ԯ��', '��Լ��', '����ϼ', '������', '����', '������', '�����S', '��Ӧ��', '����ϣ', '����ϣ',
             '�Ź۲�', '������', '������', '�Ÿվ�', '������', '�ž���', '������', '�ż���', '������', '�ŷ�', '����ݡ', '���Ĳ�', '��ʫ��', '��ʫ��', '�ų���', '������', '��չ��', '������', '�ź���', '��Ĭ', '������', '�Ž�', '�ſ���', '��չ��', '�Ž�˸', '�����', '��溺�', '��ʫ��', '�Ŵ���', '����Ƽ', '��ʫ��', '������', '���ź�', '��Ƽ', '����Ƽ', '���˷�', '��Сƽ', '�Ž���', '������', '���ӳ�', '�ų�', '������', '������', '�Ŵ���', '�ž���', '���Ǻ�', '������', '�Ż���', '���ž�', '������', '������', '��ܿܰ', '���Ϻ�', '�ź���', '������', '��ܰ��', '�ž���', '���Ӻ�', '������', '�ž���', '��ݢ�U', '�����', '���Ǿ�', '������', '�����', '�ż���', '������', '��һ��', '����', '�ź��', '�����', '�ż���', '������', '���Ȼ', '�ź�Ȼ', '������', '������', '�ź�һ', '�ų��', '��֮��', '�ų���', '������', '������', '����',
             '���Ľ�', '����', '��', '������', '����ͩ', '����ͩ', '���ź�', '���', '������', '�����', '�����', '���ӳ�', '���', '������', '���', '������', '������', '������', '���', '����', '������', '������', '����', '����', '�����', '������', '����һ', '���', '�����', '�Ԫ', '���Ĳ�', '�����', '����', '����', '������', '�', '����', '���Ȼ', '������', '�����', '��˼��', '������', '�Ӣ', '���', '��Ω�', '����', '��ܰ��', '������', '������', '������', '����˶', '������', '����', '�����', '���Ž�', '���', '�', '����ѩ', '����ӱ', '��ٻѩ', '������', '���', '���Ԩ']


def add_student(start, end):
    ids = range(start, end)
    password = 1
    types = ['��е����', '�������', '��ҵ����', '�Զ���', '������Ϣ����', '�������񹤳�']
    for id in ids:
        major_types = random.choice(types)
        tel = random.randint(13000000000,19000000000)
        # print(major_types, tel)
        # name = ''.join(random.sample(
        #     ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
        #      'e', 'd', 'c', 'b', 'a'], 5))
        username = random.choice(name_list)
        stu = Student(user_id=id,major_in=major_types,tel_num=tel, username=username)
        stu.set_password(str(password))
        db.session.add(stu)
        # stu = Student.query.get(id)
        # print(stu.username)
    db.session.commit()


def edit_user(start, end):
    for i in range(start, end):
        user = User.query.get(i)
        if user:
            user.username = random.choice(name_list)
    db.session.commit()


def add_teacher(start, end):
    ids = range(start, end)
    password = 1
    # types = ['��е����', '�������', '��ҵ����', '�Զ���', '������Ϣ����', '�������񹤳�']
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
    types = ['�Ƽ�', '����', '����', '���', '�ۺ�']
    levels = ['У��', '�м�', 'ʡ��', '���Ҽ�', '���ʼ�']

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
        name = '����' + str(id)
        detail = '��' + str(id) + '������'
        # email = str(id) + '@test.com'
        stu = Contest(contest_name=name, contest_type=type, contest_time=time, details=detail, level=level)
        # stu.set_password(str(password))
        db.session.add(stu)
        # stu = Student.query.get(id)
        # print(stu.username)
    db.session.commit()


def add_request(type,count):
    '''
    ������Ӿ�������
    :param type: �����ж�����
    :param count: Ҫ��Ӷ�����������Ϣ
    :return:
    '''

    for i in range(count):
        contest_id = random.randint(1, 29)
        teacher = random.randint(200, 220)
        times = randomtimes('2017-01-01', '2019-05-01')
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


def agree_request(start, end):
    for i in range(start, end):
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


def award_in(start, end):
    ids = range(start, end)
    types = ['���㽱', 'һ�Ƚ�', '���Ƚ�', '���Ƚ�', '��']
    for id in ids:
        type = random.choice(types)
        awd = Award.query.get(id)
        awd.grade = type
    db.session.commit()



import xlrd

def get_data(filename, sheetnum):       # ��ȡ��ҵ�б�����Ӧ������
    dir_case = 'app/file/' + filename + '.xlsx'
    data = xlrd.open_workbook(dir_case)
    table = data.sheets()[sheetnum]         # ��ȡ��һ��������
    nor = table.nrows       # ��ȡ������
    # nol = table.ncols
    # print(nor)
    dict = {}
    for i in range(nor):
        title = table.cell_value(i, 0)
        value = table.cell_value(i, 1)
        dict[title] = value
    return dict


def work_in(start, end):
    ids = range(start, end)
    company = get_data('list', 0)
    for id in ids:
        # print(list(company))
        name = random.choice(list(company.keys()))
        type = company[name]
        awd = Student.query.get(id)
        awd.company_name = name
        awd.company_type = type
        awd.salary = random.randrange(4000,12000,1000)
    db.session.commit()


import requests
from lxml import etree
def get_university():           # ����������������ϻ�ȡѧУ��Ϣ�����浽�����
    url = "https://yz.chsi.com.cn/sch/?start={}"

    lists = []
    for i in range(44):
        cur_url = url.format(i * 20)
        html = requests.get(cur_url).text
        xpath_parser = etree.HTML(html)
        univer = xpath_parser.xpath("//table[@class='ch-table']//tr/td[1]/a/text()")
        for i in range(len(univer)):
            univer[i] = univer[i].strip()
            lists.append(univer[i])
    # print(lists)

    output = open('C:\\Users\\MRZhao\\Desktop\\data.xls', 'w', encoding='gbk')
    for i in range(len(lists)):
        # for j in range(len(list1[i])):
        output.write(str(lists[i]))  # write��������дint���͵Ĳ���������ʹ��str()ת��
            # output.write('\t')  # �൱��Tabһ�£���һ����Ԫ��
        output.write('\n')  # д��һ��������
    output.close()

    return lists


def study_data():           # ����������о���������ѧУ��Ϣ
    dir_case = 'app/file/' + 'study.xlsx'
    data = xlrd.open_workbook(dir_case)
    table = data.sheets()[0]
    nor = table.nrows
    # list_none = get_university()
    list_none, list_211, list_985 = [], [], []
    for i in range(nor):
        type_none = table.cell_value(i, 0)
        type_211 = table.cell_value(i, 1)
        type_985 = table.cell_value(i, 2)
        list_none.append(type_none)
        if type_211:
            list_211.append(type_211)
        if type_985:
            list_985.append(type_985)

    for item in list_none[::-1]:         # ��Ҫ����ɾ����Ҫ������Ԫ���޷���ȷɾ��;�����ͨѧУ�б�
        if item in list_211:
            list_none.remove(item)

    for item in list_211[::-1]:         # ��Ҫ����ɾ����Ҫ������Ԫ���޷���ȷɾ�������211��У�б�
        if item in list_985:
            list_211.remove(item)

    dict1 = {}
    for item in list_none:
        dict1[item] = '��ͨ��У'
    for item in list_211:
        dict1[item] = '211��У'
    for item in list_985:
        dict1[item] = '985��У'
    # print(dict1)
    return dict1


def study_in(start, end):
    ids = range(start, end)
    univer = study_data()
    for id in ids:
        name = random.choice(list(univer.keys()))
        type = univer[name]
        stu = Student.query.get(id)
        stu.college_name = name
        stu.college_type = type
    db.session.commit()


def add_notice(count):
    notice1 = Notice.query.order_by(Notice.id.desc()).first()
    start = int(notice1.id)

    for i in range(start, start+count):
        title = 'notice' + str(i)
        text = ''.join(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
             'f', 'e', 'd', 'c', 'b', 'a', ' ', ','], 20))
        print(text)
        times = randomtimes('2017-01-01', '2019-05-01')
        notice = Notice(title=title,text=text,time=times)
        db.session.add(notice)
    db.session.commit()

# study_in(140, 149)
# add_notice(10)
# add_contest(10,30)
# add_teacher(200, 230)
# edit_user(1, 230)
# add_request(1, 50)
# agree_request(75, 130)
# award_in(52,106)
# get_data('list', 0)

from pyecharts import Scatter

# v1 = [10, 10, 20, 30, 40, 50, 60]
# v2 = [10, 10, 20, 30, 40, 50, 60]
# extra = [1,2,1,1,1,1,5]
# scatter = Scatter("ɢ��ͼʾ��")
# scatter.add("scatter",
#     v1,
#     v2,
#     extra_data=extra,
#     is_visualmap=True,
#     visual_dimension=2,
#     visual_orient="horizontal",
#     visual_type="size",
#     visual_range=[0, 10],
#     visual_text_color="#000",)
# scatter.render()
# work_in(104,110)


# data = [
#         [28604, 77, 17096869],
#         [31163, 77.4, 27662440],
#         [1516, 68, 1154605773],
#         [13670, 74.7, 10582082],
#         [28599, 75, 4986705],
#         [29476, 77.1, 56943299],
#         [31476, 75.4, 78958237],
#         [28666, 78.1, 254830],
#         [1777, 57.7, 870601776],
#         [29550, 79.1, 122249285],
#         [2076, 67.9, 20194354],
#         [12087, 72, 42972254],
#         [24021, 75.4, 3397534],
#         [43296, 76.8, 4240375],
#         [10088, 70.8, 38195258],
#         [19349, 69.6, 147568552],
#         [10670, 67.3, 53994605],
#         [26424, 75.7, 57110117],
#         [37062, 75.4, 252847810]
#     ]
#
# x_lst = [v[0] for v in data]
# y_lst = [v[1] for v in data]
# extra_data = [v[2] for v in data]
# sc = Scatter()
# sc.add(
#     "scatter",
#     x_lst,
#     y_lst,
#     extra_data=extra_data,
#     tooltip_formatter='����{c}',
#     is_visualmap=True,
#     visual_dimension=2,
#     visual_orient="horizontal",
#     visual_type="size",
#     visual_range=[254830, 1154605773],
#     visual_text_color="#000",
# )
# sc.render()


# import numpy as np
# from scipy.stats import pearsonr
# # import random
# #
# x = [1, 5,2,0,4,2]
# y = [4000,8000,3000,8000,6000,5000]
# # y = ['211','958','211','��ͨ','211','211']
# xnp = np.array(x)
# ynp = np.array(y)
# print(pearsonr(x,y)[0])
#
# result = {0: 1.1181753789488595, 1: 0.5566080288678394, 2: 0.4718269778030734, 3: 0.48716683119447185, 4: 1.0, 5: 0.1395076201641266, 6: 0.20941558441558442}
#
# x,y = [],[]
# for key,value in result.items():
#     x.append(key)
#     y.append(value)
# xnp = np.array(x)
# ynp = np.array(y)
# print(pearsonr(x,y))
# names = ['id','data']
# formats = ['f8','f8']
# dtype = dict(names = names, formats=formats)
# array = np.array(result.items(), dtype=dtype)
# print(repr(array))
# np.random.seed(0)
# size=300
# x=np.random.normal(0,1,size)
# print("Lower noise",pearsonr(x,x+np.random.normal(0,1,size)))
# print("Higher noise",pearsonr(x,x+np.random.normal(0,10,size)))
# from sqlalchemy import func
# # students = Award.query().filter(Award.user_type==0).group_by(Award.user_id).all()
# # students1 = Award.query().filter(Award.user_type==0).group_by(Award.user_id).count()
# ss = db.session.query(Award.user_id, func.count(Award.user_id)).filter(Award.user_type==0).group_by(Award.user_id).all()
# dict1 = {}
# for s in ss:
#     print(s[0],s[1])
#     dict1[s[0]] = s[1]
# # count1 = Award.query.join(  # ѡ��ÿһ��Ĳ�������
# #             Contest, (Award.contest_id == Contest.contest_id)).filter(
# #             Contest.contest_type == types[0], Contest.contest_time >= start, Contest.contest_time <= end).count()
# ss1 = db.session.query(Award.user_id, team_student.c.user_id, func.count(team_student.c.user_id)).\
#     join(team_student, (team_student.c.team_id == Award.user_id)).\
#     filter(Award.user_type==1).group_by(team_student.c.user_id).all()
#
# print(ss1)
# dict2 = {}
# for s in ss1:
#     # print(s[1],':',s[2])
#     dict2[s[1]] = s[2]
# for key, value in dict2.items():
#     if key in dict1:
#         dict1[key] += value
#     else:
#         dict1[key] = value
# print(dict1)
# print(str(ss))
# for s1,s2 in zip(ss1,ss2):
#     print(':',s2)
    # dict1[s[0]] = s[1]
# print(dict1)
