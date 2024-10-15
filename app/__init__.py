from flask import Flask
from app.routes.main_routes import main

def create_app():
    app = Flask(__name__)

    #初始化 注册蓝图
    app.register_blueprint(main)

    return app
