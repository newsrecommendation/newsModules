# -*- coding: utf-8 -*-
# 注意之后在需要运行数据库的文件中导入此文件，配置连接数据库

# 导入SQLAlchemy，可操作数据库以及连接数据库
from flask_sqlalchemy import SQLAlchemy
# 导入app工程文件
from app import app

# 连接数据库（格式：'mysql+pymysql://用户名:密码@端口号/数据库名'）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:19950314@127.0.0.1:3306/users'

# 支持中文操作
app.config['JSON_AS_ASCII'] = False

# 数据库连接(生成一个数据库操作对象)
db = SQLAlchemy(app)

class DBO:
    # 定义函数完成构造对象数据初始化
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self,key,value)

    # 定义一个数据添加操作
    @classmethod
    def add(self, *args, **kwargs):
        if len(args)>0 and isinstance(*args, list):
            for dict in args[0]:
                obj = self(**dict)
                db.session.add(obj)
        else:
            obj = self(**kwargs)
            db.session.add(obj)
        db.session.commit()
        return obj

    # 定义函数完成数据更新
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self,key):
                setattr(self, key, value)
        db.session.commit()

    # 定义函数完成数据删除
    def delete(self):
        db.session.delete(self)
        db.session.commit()
