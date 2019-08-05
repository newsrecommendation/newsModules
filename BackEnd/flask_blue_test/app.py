# 导入flask模块
from flask import Flask

# 创建Flask的实例app，并设置共享网页文件夹templates的访问位置
app = Flask(__name__, template_folder='static/templates')

# 设置代码发生改变时，自动启动服务器
app.debug = True

# 以下两句先不写，蓝图创建后执行
# 导入app1/views.py中创建的蓝图

from app1.views import app1

app.register_blueprint(app1, url_prefix='/app1')
