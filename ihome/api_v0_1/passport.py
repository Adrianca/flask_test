# -*- coding:utf-8 -*-
import re
from flask import session
from ihome import redis_store, db
from ihome.models import User
from . import api
from flask import request, jsonify
from ihome.utils.response_code import RET


#url = users?sms_code=111111&mobile=13111111111&password=123456
@api.route('/users', methods=['POST'])
def register():
    #一、 获取参数
    #request.data
    #request.get_data:更安全
    #request.get_json
    sms_code = request.get_json().get('sms_code')
    mobile = request.get_json().get('mobile')
    passwd = request.get_json().get('password')

    #二、 校验参数
    #校验是否存在
    if not all([sms_code, mobile, passwd]):
        return jsonify(errno=RET.DATAERR, errmsg='参数不全')

    #校验手机号格式
    if not re.match(r"^1[356789]\d{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='就没见过这样的手机号')

    #三、 逻辑处理
    #1. 验证短信验证码是否正确
    #1-1. 从redis中获取数据
    try:
        real_sms_code = redis_store.get('sms_code_%s'%mobile)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='redis获取数据失败')

    #1-2. 验证短信验证码是否为空
    if real_sms_code is None:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码已过期')

    #1-3. 验证验证码是否正确
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码错误')

    #1-4. 删除redis中的短信验证码
    try:
        redis_store.delete('sms_code_%s'%mobile)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='redis删除数据失败')

    #2. 验证手机号
    try:
        user = User.query.filter(User.mobile==mobile).first()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='数据库查询错误')
    else:
        if user is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg='手机号已被注册')

        user = User(name=mobile, mobile=mobile)
        user.password = passwd

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(errno=RET.DBERR, errmsg='redis存储失败')

    #将用户信息存入session中（注册后直接返回主页）
    try:
        session['user_name'] = mobile
        session['user_id'] = user.id
        session['mobile'] = mobile
    except Exception as e:
        return jsonify(errno=RET.SESSIONERR, errmsg='session存储失败')


    #四、 返回数据
    return jsonify(errno=RET.OK, errmsg='成功')


@api.route('/sessions', methods=['POST'])
def login_session():
    #一， 获取数据
    #通过post请求获取mobile以及passwd两个参数
    mobile = request.get_json().get('mobile')
    passwd = request.get_json().get('password')

    #二， 校验
    #校验数据完整性：
    if not all([mobile, passwd]):
        return jsonify(errno=RET.PARAMERR, errmsg='数据不完整')

    #校验手机号码
    if not re.match(r'1[35789]\d{9}', mobile):
        return jsonify(errno=RET.DATAERR, errmsg='手机号码错误')

    #三， 逻辑处理
    #验证错误次数
    user_ip = request.remote_addr
    try:
        user_error_count = redis_store.get('user_error_count_%s'%user_ip)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='redis读取失败')

    if user_error_count is not None and int(user_error_count) > 5:
        return jsonify(errno=RET.REQERR, errmsg='请求次数大于5次，请稍候再试')

    #1 验证手机号
    #1-1, 从mysql中获取数据
    try:
        user = User.query.filter(User.mobile==mobile).first()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='mysql查询失败')
    #1-2, 验证数据是否为空,密码是否正确
    else:
        if user is None or not user.check_passwd(passwd):
            redis_store.incr('user_error_count_%s'%user_ip)
            redis_store.expire('user_error_count_%s'%user_ip, 86400)
            return jsonify(errno=RET.DATAERR, errmsg='用户名或密码错误')

    #1-3, 设置session数据
    try:
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['mobile'] = mobile
    except Exception as e:
        return jsonify(errno=RET.SESSIONERR, errmsg='session存储失败')

    #四， 返回数据
    try:
        redis_store.delete('user_error_count_%s'%user_ip)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg='redis删除数据失败')

    return jsonify(errno=RET.OK, errmsg='成功')


@api.route('/sessions', methods=['GET'])
def check_login():
    #从session中获取user信息
    user_name = session.get('user_name')
    if user_name is None:
        return jsonify(errno=RET.SESSIONERR, errmsg='session未找到user信息')
    else:
        return jsonify(errno=RET.OK, errmsg='获取成功', data={'name':user_name})


@api.route('/sessions', methods=['DELETE'])
def logout():
    #退出登录时要清理缓存
    #session.clear()
    #session.pop()
    csrf_token = session.get('csrf_token')
    session.clear()
    session['csrf_token'] = csrf_token

    return jsonify(errno=RET.OK, errmsg='OK')







