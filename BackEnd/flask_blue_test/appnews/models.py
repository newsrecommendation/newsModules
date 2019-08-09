# 用来创建模型数据

# 导入db_operate文件中的db数据库，DBO（封装的数据库操作函数，觉得不需要也可不导DBO）
from db_operate import db,DBO
# 创建简单的用户账号，密码模型
from datetime import datetime


class User(db.Model,DBO):
    userid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(77),nullable=False,unique=True)
    password = db.Column(db.String(77),nullable=False)

#   feature = ...   作为用户的订阅频道

    # 表格更名
    __tablename__ = 'user'

    # 初始化每个实例。（若在第6步导入DBO文件，可不用写以下初始化语句，DBO类方法中已封装。）
    # def __init__(self, username, password):
    # self.username = username
    # self.password = password


class News(db.Model, DBO):
    news_id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    title = db.Column(db.String(255))
    time = db.Column(db.String(64))
    content = db.Column(db.String(255))
    author = db.Column(db.String(255))
    news_url = db.Column(db.String(255))

#    pageSize = db.C

    # 外键先设置在这里 不一定需要用.连外键时出错
    # user_id = db.Column(db.Integer, db.ForeignKey('user.userid'))

    __tablename__ = 'news'


#给网站中的图片设置一个类
class Image(db.Model):
    id = db.Column(db.Integer,primary_key = True , autoincrement = True)
    url = db.Column(db.String(512))
    # 数据库中的外键，表示ID来源于User.id

    # URL为什么不用粘贴网址？db.Datetime是自定义数据类型？

    # id是图片id,user_id是图片所属的人的id，外键链接到user.id这一列上

    # news_id可能有问题
    #news_id =db.Column(db.Integer, db.ForeignKey('news.news_id'))
    create_date = db.Column(db.DateTime)
    # comments = db.relationship('Comment')
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'image'

# 初始化函数
    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id
        self.create_date = datetime.now() #当前时间

    def __repr__(self):
        return '<Image %d %s>'%(self.id,self.url)

# #详flask_login官网
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)  #查询数据库加载用户

