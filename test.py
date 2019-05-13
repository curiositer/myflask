# coding=gbk
from app import app, db
from app.models import User, Contest, Request, Student, Teacher, Team, Award, team_student, Notice
import random

# 添加数据专用

name_list = ['赵泽晨', '赵子桐', '赵建川', '赵琦锐', '赵家妍', '赵宇琪', '赵佳鑫', '赵语彤', '赵紫睿', '赵天琪', '赵懿轩', '赵子鑫', '赵谨瑶', '赵玉涵', '赵俊辰', '赵泊君', '赵无名', '赵书瑶', '赵若涵', '赵涵睿', '赵栾涵', '赵宇涵', '赵涵恩', '赵韶涵', '赵语涵', '赵杰', '赵浩航', '赵绎涵', '赵靖巍', '赵楷', '赵鹏奕', '赵煦', '赵煦恺', '赵子瑜', '赵凯瑞', '赵逸霏', '赵振', '赵振楦', '赵振暄', '赵振煊', '赵振璇', '赵振萱', '赵乐珊', '赵晶婧', '赵婧晶', '赵婧婧', '赵旭玉', '赵婧玉', '赵瑾瑜', '赵静怡', '赵婧怡', '赵婧瑜', '赵闯', '赵美玲', '赵晨怡', '赵建宇', '赵铁皖', '赵麓丞', '赵骧鑫', '赵誉惘', '赵略竖', '赵太逖', '赵内驱', '赵内藩', '赵斓夷', '赵若彤', '赵亦俊', '赵奕俊', '赵建伟', '赵暖暖', '赵仡浚', '赵屹浚', '赵奕浚', '赵奕骏', '赵屹骏', '赵仡骏',
             '王满', '王琳', '王锐', '王艺博', '王伟', '王辰硕', '王鸿轩', '王涵润', '王涵涵', '王兴', '王淳曦', '王雨微', '王钧涵', '王浩晏', '王芊语', '王乐怡', '王皓月', '王文田', '王文田', '王文田', '王禹勋', '王思卓', '王国珍', '王建', '王天佑', '王昕', '王玥婷', '王浩南', '王玥雯', '王天睿', '王雨辰', '王靖雯', '王镜雯', '王翠楠', '王镜文', '王静文', '王静雯', '王楠', '王之骏', '王子骏', '王九雏', '王韬茫', '王麒鄄', '王丹', '王椒勃', '王泊君', '王诗议', '王思馨', '王誉涵', '王思思', '王梦菲', '王贤博', '王博琨', '王复贤', '王博贤', '王博毅', '王博逸', '王肇博', '王博儒', '王傲野', '王韬韧', '王傲瑜', '王傲璇', '王傲煦', '王傲昭', '王韬博', '王傲琬', '王傲玥', '王傲熙', '王傲漾',
             '刘佳乐', '刘慧娴', '刘嘉源', '刘盈锐', '刘德华', '刘娜', '刘欣玥', '刘晗玥', '刘益嘉', '刘如玥', '刘兆祥', '刘永昌', '刘泽林', '刘国佩', '刘佳绮', '刘哲宇', '刘佳晰', '刘佳琦', '刘长鑫', '刘佳萱', '刘思哲', '刘长洪', '刘长润', '刘宸旭', '刘毅', '刘森柱', '刘永胜', '刘昊天', '刘新奇', '刘文军', '刘鑫源', '刘永旭', '刘希岭', '刘希玲', '刘国荣', '刘永震', '刘新琦', '刘一越', '刘一玑', '刘越', '刘慕瑶', '刘雨林', '刘尚直', '刘尚猛', '刘竞朗', '刘轩铭', '刘辕铭', '刘约礼', '刘金霞', '刘菡卿', '刘红', '刘梓恒', '刘智赟', '刘应琴', '刘帥希', '刘宇希',
             '张观博', '张欣竹', '张欣阳', '张刚军', '张扬阳', '张靖阳', '张熙阳', '张嘉萱', '张铭阳', '张飞', '张雨荨', '张文博', '张诗含', '张诗若', '张辰海', '张晓雨', '张展鸣', '张晓春', '张洪文', '张默', '张轩杰', '张金海', '张俊杰', '张展旭', '张建烁', '张婧琪', '张婧涵', '张诗晴', '张传浩', '张怡萍', '张诗涵', '张雅婷', '张雅涵', '张萍', '张晓萍', '张兴飞', '张小平', '张建龙', '张宇谟', '张子辰', '张辰', '张湍灵', '张骅株', '张春莲', '张娟敏', '张智涵', '张欣妍', '张慧妍', '张雅静', '张月婷', '张雨婷', '张芸馨', '张韵涵', '张涵韵', '张雨欣', '张馨蕾', '张静媛', '张子涵', '张雨泽', '张静蕾', '张茛淯', '张珑沧', '张芮娟', '张梓萱', '张轶诚', '张嘉文', '张晓朋', '张一凡', '张昊楠', '张浩楠', '张瑞君', '张佳宁', '张雨杨', '张昊然', '张浩然', '张滕浩', '张雨菡', '张海一', '张晨宸', '张之政', '张晨菲', '张修闻', '张宁夫', '张轩',
             '杨文锦', '杨泽晨', '杨博瀚', '杨伊珂', '杨子桐', '杨雨桐', '杨雅涵', '杨建川', '杨琦锐', '杨琦炜', '杨子瑾', '杨子辰', '杨炳', '杨鸣鹤', '杨景宜', '杨乐乐', '杨雨潼', '杨涛了', '杨淼', '杨铭', '杨宇欣', '杨丽华', '杨旭', '杨旭芳', '杨亚悫', '杨亚兰', '杨子一', '杨海辰', '杨君浩', '杨焙元', '杨文博', '杨金鹏', '杨荣', '杨坤', '杨绍文', '杨换', '杨曦', '杨浩然', '杨铭羽', '杨浩宇', '杨思辰', '杨悦熙', '杨海英', '杨艾潼', '杨惟岚', '杨蓓', '杨馨媛', '杨佩林', '杨佩云', '杨子琦', '杨泽硕', '杨泽涛', '杨涛', '杨国涛', '杨雅洁', '杨静涵', '杨帆', '杨若雪', '杨淑颖', '杨倩雪', '杨漫妮', '杨锋', '杨睿渊']


def add_student(start, end):
    ids = range(start, end)
    password = 1
    types = ['机械工程', '软件工程', '工业工程', '自动化', '电子信息工程', '汽车服务工程']
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
    types = ['优秀奖', '一等奖', '二等奖', '三等奖', '无']
    for id in ids:
        type = random.choice(types)
        awd = Award.query.get(id)
        awd.grade = type
    db.session.commit()



import xlrd

def get_data(filename, sheetnum):       # 获取企业列表，及对应的类型
    dir_case = 'app/file/' + filename + '.xlsx'
    data = xlrd.open_workbook(dir_case)
    table = data.sheets()[sheetnum]         # 读取第一个工作簿
    nor = table.nrows       # 获取总行数
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
def get_university():           # 利用爬虫从研招网上获取学校信息，保存到表格中
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
        output.write(str(lists[i]))  # write函数不能写int类型的参数，所以使用str()转化
            # output.write('\t')  # 相当于Tab一下，换一个单元格
        output.write('\n')  # 写完一行立马换行
    output.close()

    return lists


def study_data():           # 获得所有有研究生招生的学校信息
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

    for item in list_none[::-1]:         # 需要倒序删除，要不连续元素无法正确删除;获得普通学校列表
        if item in list_211:
            list_none.remove(item)

    for item in list_211[::-1]:         # 需要倒序删除，要不连续元素无法正确删除；获得211高校列表
        if item in list_985:
            list_211.remove(item)

    dict1 = {}
    for item in list_none:
        dict1[item] = '普通高校'
    for item in list_211:
        dict1[item] = '211高校'
    for item in list_985:
        dict1[item] = '985高校'
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
# scatter = Scatter("散点图示例")
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
#     tooltip_formatter='个数{c}',
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
# # y = ['211','958','211','普通','211','211']
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
# # count1 = Award.query.join(  # 选出每一类的参赛人数
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
