# 导入flask模块
from flask import Flask
from flask_cors import CORS

# 创建Flask的实例app，并设置共享网页文件夹templates的访问位置
app = Flask(__name__, template_folder='static/templates')
CORS(app, supports_credentials = True)


# 设置代码发生改变时，自动启动服务器
app.debug = True

# 以下两句先不写，蓝图创建后执行
# 导入appnews/views.py中创建的蓝图

from appnews.views import appnews

app.register_blueprint(appnews, url_prefix='/appnews')
