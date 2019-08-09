"""
#coding:utf-8
views.py主要和网页的跳转有关
对于views而言，装饰器下的函数的返回值可以是网页，某个写好的html文件，
甚至是一个字符串或者json字符串，此时会在网页上看到返回的字符串
可以从目录中导入变量

项目名/代码文件名/函数名/传给后端的参数名和参数值
"""
from __future__ import unicode_literals

# # 导入渲染模块，蓝图模块，数据传输模块，路由分配模块
import csv

from flask import render_template, Blueprint, request, url_for
# 导入创建的模型，用来完成下面定义功能时对数据库的操作
from .models import *
# 导入json，来完成前后端的数据交互
import json


# 创建蓝图,蓝图必须有前两个参数，为“蓝图名”，“当前运行文件名”。后两个是设置蓝图文件夹
# （蓝图文件夹即为appnews文件夹）在访问私有网页文件夹templates的位置目录，以及私有静态文件的位置目录
appnews = Blueprint('appnews', __name__, template_folder='templates', static_folder='static')


# 渲染函数
# endpoint用法：当修改某个函数的访问路由名称时，不会影响网页之间的跳转，
# 实现动态获取路由名称。方便提高效率和维护
# url_for路由分配模块
@appnews.route('/login/', endpoint='login')
def show_login():
    return render_template(
        'login.html',
        url_login=url_for('appnews.account_login', _external=True)
    )


@appnews.route('/test123456789/', endpoint='t')
def show_test():
    return render_template('test0.html')


# 功能函数
# 定义登录功能
@appnews.route('/account_login/', methods=['GET', 'POST'])
def account_login():
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        res = User.query.filter(User.username == username).all()
        object = None
        for item in res:
            object = item
        if object is None:
            msg = {'code': 400, 'infor': '用户名不存在,请注册'}
        else:
            if object.password == password:
                msg = {'code': 200, 'infor': '登陆成功'}
            else:
                msg = {'code': 400, 'infor': '密码错误,请重新输入'}
    else:
        msg = {'code': 400, 'infor': '请求方式不正确'}
    return json.dumps(msg)


# 这里的参数是user_id,在后面实际的过程是在DKN模型根据用户信息过滤新闻后返回的新闻的news_id
# .all()得到的结果是装有对象的list(列表)
@appnews.route('/get_news/')
def get_news():
    res = News.query.filter(News.news_id == 1).all()
    object_temp = None
    for item in res:
        object_temp = item
    if object_temp is  None:
        msg = {'no news':123}
    else:
        msg = {'news_id': object_temp.news_id, 'title': object_temp.title,
               'time': object_temp.time, 'author': object_temp.author,
               'content': object_temp.content, 'news_url': object_temp.news_url}
    # if res is None:
    #     msg = {'没有合适新闻': 123}
    # else:
    #     msg = {'get news': 456}
    return json.dumps(msg,ensure_ascii=False)


@appnews.route('/get_news_csv/<int:user_id>/')
def get_news_csv(user_id):
    news_id_list = []
    msg = {}
    msg_list = []
    news_list = []
    with open('recom.csv','rt',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['user_id'] == str(user_id):
                news_id_list.append(row['news_id'])
        #    msg = {user_id:news_id_list}
        # 在csv表中找到user_id对应的news_id
        if news_id_list == []:
            msg = {'Error':'no news/fresh user'}
            return json.dumps(msg,ensure_ascii=False)
        else:
            with open('minidata_raw_train.txt','rt',encoding='utf-8') as newsfile:
                lines = newsfile.readlines()

                index = 0
                num = 0
                for k,line in enumerate(lines):
                    if str(k) in news_id_list:
                        result = line.split("\t")
                        temp={'news title':result[1],'entity_with_id':result[3].split("\n")[0]}
                        news_list.append(temp)
                        num += 1
                    msg = {num:news_list}
                return json.dumps(msg,ensure_ascii=False)


"""
stus = Student.query.filter(Student.s_age==18) 得到的结果是 sqlalchemy.BaseQuery’
stus = Student.query.filter(Student.s_age==18).all() 得到的结果是 装有对象的list(列表)
stus = Student.query.get(1) 得到是一个对象，不是列表， ‘1’默认是s_id
"""

"""
# ~~~~~~~~~~~~~~~~~~~注意：下面的代码很可能出错，还没有跑通
# @appnews.route('/appnews/views/get_news/<int:user_id>/<int:page>/<int:per_page>', methods=['POST', 'GET'])
  def get_news(user_id, page, per_page):
    paginate = News.query.filter_by(news_id=user_id) #.paginate(page=page, per_page=per_page, error_out=False)
    news_per_page = paginate.items
    map_msg = {'has_next': paginate.has_next}
    news_list = []          #返回的新闻列表
    for news in news_per_page:
        msg = {'news_id':news.news_id, 'title':news.title,
               'time':news.time, 'author':news.author,
               'content':news.content, 'news_url':news.news_url}
        news_list.append(msg)
    #map_msg['news'] = news_list
    map_msg = {123:456}
    return json.dumps(map_msg)

@appnews.route('/appnews/views/get_news/<int:user_id>/', methods=['POST', 'GET'])
def get_news(user_id):
    map_msg = {}
    if request.method == 'POST':
        res = User.query.filter(News.news_id == user_id).all()
        for news in res:
            news_list = []          #返回的新闻列表
            msg = {'news_id':news.news_id, 'title':news.title,
                   'time':news.time, 'author':news.author,
                   'content':news.content, 'news_url':news.news_url}
            news_list.append(msg)
    map_msg['news'] = news_list
    #map_msg = {123:456}
    return json.dumps(map_msg)
"""