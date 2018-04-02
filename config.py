# -*- coding:utf-8 -*-
import redis

class ProcessSettings(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/ihome'
    DEBUG = True

    #创建SECRETY_KEY
    '''
    base64.b64encode(os.urandom(24))
    'ge93CyMABWNHSSwRBWrh/3SItqn1is1l'
    '''
    SECRET_KEY = 'ge93CyMABWNHSSwRBWrh/3SItqn1is1l'

    #redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    #session配置
    SESSION_TYPE = 'redis'
    PERMANENT_SESSION_LIFETIME = 86400
    SESSION_USE_SINGER = True







class DevelopSettings(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/ihome'


