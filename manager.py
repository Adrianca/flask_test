# -*- coding:utf-8 -*-

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello flask!'

if __name__ == '__main__':
    #运行 --> 相当于Django runserver. 都是框架自带的简易服务器
    app.run()