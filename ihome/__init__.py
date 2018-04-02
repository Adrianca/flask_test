# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from utils.common import RegerConverter
from config import ProcessSettings



#ihome程序初始化文件


#惰性加载app，方便其他文件调用
db = SQLAlchemy()

#外部创建redis对象，以方便外部调用
redis_store = None


#通过函数调用
def create_obj(configFiles):
    #创建app
    app = Flask(__name__)
    #加载配置文件
    app.config.from_object(configFiles)

    #注册路由
    app.url_map.converters['re'] = RegerConverter


    #惰性加载app
    db.init_app(app)

    #CSRF保护
    CSRFProtect(app)

    #连接redis服务器,默认host为127.0.0.1,默认port为6379
    global redis_store
    redis_store = redis.StrictRedis(port = ProcessSettings.REDIS_PORT, host=ProcessSettings.REDIS_HOST)

    #注册蓝图
    from ihome.api_v0_1 import api
    app.register_blueprint(api)

    import web_html
    app.register_blueprint(web_html.html)


    #创建flask-session，将cookie中的session存到你想要的地方
    Session(app)


    return app,db
