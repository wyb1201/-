# 所有路由的定义

from flask import Blueprint, render_template
from app.routes.upload_file import upload_file, set_key
from app.routes.ask_ai import ask


main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def init():
    return render_template('webSite.html')

# 接收用户视频，生成
@main.route('/upload', methods=['POST'])
def upload():
    return upload_file()

# ai助手回答问题
@main.route('/ask', methods=['POST'])
def ask_route():
    return ask()

# 设置用户密钥
@main.route('/key',methods=['POST'])
def user_key():
    return set_key()