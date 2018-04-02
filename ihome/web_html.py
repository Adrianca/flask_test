# -*- coding:utf-8 -*-
from flask_wtf.csrf import generate_csrf
from flask import Blueprint, current_app, make_response

html = Blueprint('html',__name__)

@html.route('/<re(r".*"):filename>')
def html_static(filename):
    #判断filename是否为空
    if not filename:
        filename = 'index.html'

    #判断filename是否为静态页面
    if filename != 'favicon.ico':
        filename = 'html/' + filename

    resp = make_response(current_app.send_static_file(filename))
    csrf_token = generate_csrf()
    resp.set_cookie('csrf_token', csrf_token)
    return resp
