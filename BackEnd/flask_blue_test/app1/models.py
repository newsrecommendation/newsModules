# 用来创建模型数据

# 导入db_operate文件中的db数据库，DBO（封装的数据库操作函数，觉得不需要也可不导DBO）
from db_operate import db,DBO
# 创建简单的用户账号，密码模型。（flask一对一，一对多，多对多关系的创建在第Y18博客中有介绍）
class User(db.Model,DBO):
    userid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(77),nullable=False,unique=True)
    password = db.Column(db.String(77),nullable=False)
    # 表格更名
    __tablename__ = 'user'

    # 初始化每个实例。（若在第6步导入DBO文件，可不用写以下初始化语句，DBO类方法中已封装。）
    # def __init__(self, username, password):
    # self.username = username
    # self.password = password


