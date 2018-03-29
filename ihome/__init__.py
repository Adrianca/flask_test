# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect



#ihome程序初始化文件


#惰性加载app，方便其他文件调用
db = SQLAlchemy()

#外部创建redis对象，以方便外部调用
redis_stone = None


#通过函数调用
def create_obj(configFiles):
    #创建app
    app = Flask(__name__)
    #加载配置文件
    app.config.from_object(configFiles)
    #惰性加载app
    db.init_app(app)

    #CSRF保护
    CSRFProtect(app)

    #注册蓝图
    from ihome.api_v0_1 import api
    app.register_blueprint(api)

    #连接redis服务器,默认host为127.0.0.1,默认port为6379
    global redis_stone
    redis_stone = redis.StrictRedis(host = configFiles.REDIS_HOST, port = configFiles.REDIS_PORT)

    #创建flask-session，将cookie中的session存到你想要的地方
    Session(app)


    return app,db
