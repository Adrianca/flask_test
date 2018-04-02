# -*- coding:utf-8 -*-
import random

from flask import jsonify
from flask import make_response,request

from . import api
from ihome.utils.captcha.captcha import captcha
from ihome.utils.response_code import RET
from ihome import redis_store
from ihome.models import User
from ihome.libs.yuntongxun import sms

@api.route('/image_codes/<image_code_id>')
def get_image_code(image_code_id):
    print type(redis_store)
    #通过第三方获取验证码：
    name, text, image_data = captcha.generate_captcha()
    #将验证码存储到redis中
    try:
        redis_store.setex('image_code_%s'%image_code_id, 300, text)
    except Exception as e:
        print e
        #返回给前端页面
        resp = {
            'errno': RET.DBERR,
            'errmsg': 'redis存储错误'
        }
        return jsonify(resp)
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'
    return response

#url = /sms_codes/17777777777?image_code_id=uuid&image_code=abcd
@api.route('/sms_codes/<re(r"1[3456789][0-9]{9}"):mobile>')
def get_sms_codes(mobile):
    #1 获取验证码，获取手机号
    mobile = mobile
    image_code = request.args.get('image_code')
    image_code_id = request.args.get('image_code_id')

    #2 验证完整性
    if not all([mobile,image_code,image_code_id]):
        resp = {
            'errno':RET.PARAMERR,
            'errmsg':'请求参数不全',
        }
        return jsonify(resp)

    #3 逻辑处理
    #(1).  验证图片验证码是否正确
    #1-1. 从redis中获取数据
    try:
        data = redis_store.get('image_code_%s'%image_code_id)
    except Exception as e:
        resp = {
            'errno':RET.DBERR,
            'errmsg':'redis数据库查询失败',
        }
        return jsonify(resp)

    #1-2. 判断数据是否过期
    if data is None:
        resp = {
            'errno':RET.NODATA,
            'errmsg':'验证码已过期',
        }
        return jsonify(resp)

    #1-3, 删除验证码
    try:
        redis_store.delete('image_code_%s'%image_code_id)
    except Exception as e:
        resp = {
            'errno':RET.DBERR,
            'errmsg':'数据库操作失效',
        }
        return jsonify(resp)

    #1-4, 校验验证码是否正确
    if data.lower() != image_code.lower():
        resp = {
            'errno': RET.DATAERR,
            'errmsg': '验证码错误'
        }

    #(2).  验证手机号是否存在
    #2-1. 从数据库中查询
    try:
        user = User.query.filter(User.mobile==mobile).first()
    except Exception as e:
        resp = {
            'error' : RET.DBERR,
            'errmsg' : '数据库查询不存在',
        }
        return jsonify(resp)

    #2-2. 该手机号是否注册
    if user is not None:
        resp = {
            'error' : RET.DATAEXIST,
            'errmsg' : '手机已注册',
        }
        return jsonify(resp)

    #(3).  调用第三方发送短信验证码
    #3-1. 创建6位验证码
    #通过random函数来创建六位验证码
    virification_code = '%06d'%random.randint(0,999999)

    #3-2. 保存到redis中
    try:
        redis_store.setex('sms_code_%s'%mobile, 300, virification_code)
    except Exception as e:
        resp = {
            'errno' : RET.DBERR,
            'errmsg' : 'redis保存失败',
        }
        return jsonify(resp)

    #3-3. 调用第三方发送验证短信
    cpp = sms.CCP()
    result_code = cpp.send_template_sms(mobile, [virification_code,'5'], 1)

    #(4).  验证短信验证码
    if result_code == '000000':
        resp = {
            'errno' : RET.OK,
            'errmsg' : '发送成功'
        }
        return jsonify(resp)

    else:
        resp = {
            'errno' : RET.THIRDERR,
            'errmsg' : '发送验证码失败',
        }
        return jsonify(resp)
