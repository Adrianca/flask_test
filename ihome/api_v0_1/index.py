# -*- coding:utf-8 -*-
from . import api

@api.route('/index')
def index_text():
    return 'hello modo'