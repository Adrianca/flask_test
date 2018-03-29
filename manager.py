# -*- coding:utf-8 -*-
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from config import DevelopSettings,ProcessSettings
from ihome import create_obj

app,db = create_obj(ProcessSettings)

#创建迁移命令
Migrate(db,app)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

@app.route('/')
def index():
    return 'Hello flask!'

if __name__ == '__main__':
    #运行 --> 相当于Django runserver. 都是框架自带的简易服务器
    manager.run()