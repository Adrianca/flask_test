# -*- coding:utf-8 -*-
from werkzeug.routing import BaseConverter

#创建自定义路由类
class RegerConverter(BaseConverter):
    def __init__(self, url_map, regex):
        BaseConverter.__init__(self, url_map)
        self.regex = regex