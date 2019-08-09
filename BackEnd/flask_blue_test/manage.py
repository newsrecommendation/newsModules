# -*- coding: utf-8 -*-

# 此文件命名不可自拟！在其中配置数据库的迁移操作

# 导入app工程
from app import app
# 导入数据库
from db_operate import db
# 导入Manager用来设置应用程序可通过指令操作
from flask_script import Manager
# 导入数据库迁移类和数据库迁移指令类
from flask_migrate import Migrate,MigrateCommand

# 构建指令，设置当前app受指令控制（即将指令绑定给指定app对象）
manage = Manager(app)
# 构建数据库迁移操作，将数据库迁移指令绑定给指定的app和数据库
migrate = Migrate(app, db)
# 添加数据库迁移指令，该操作保证数据库的迁移可以使用指令操作
manage.add_command('db', MigrateCommand)

# 以下为当指令操作runserver时，开启服务。
if __name__ == '__main__':
    manage.run()