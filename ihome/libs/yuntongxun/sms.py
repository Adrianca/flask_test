# -*- coding: UTF-8 -*-

from CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8a216da862467c3a01627155bc651314'

# 主帐号Token
accountToken = 'c7762a3a16564c3daae23e0b6de5000b'

# 应用Id
appId = '8a216da862467c3a01627155bcc7131a'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'

# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id


'''
1. 将鉴权操作封装成单例
2. 网络请求增加异常处理
3. 增加返回值,便于判断发送情况
'''


class CCP(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            # 没有就创建
            obj = super(CCP, cls).__new__(cls)
            # 将鉴权操作封装到了初始化中, 鉴权只需要1次
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.instance = obj
        return cls.instance

    def send_template_sms(self, to, datas, temp_id):
        try:
            result = self.rest.sendTemplateSMS(to, datas, temp_id)
        except Exception as e:
            raise e

        # status_code如果是'000000'就表示发送成功
        status_code = result.get('statusCode')
        return status_code



# def sendTemplateSMS(to,datas,tempId):
#
#
#
#     # 初始化REST SDK
#     # 鉴权, 服务器运行期间, 只需要鉴权一次即可
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)

# sendTemplateSMS(手机号码,内容数据,模板Id)


if __name__ == '__main__':
    # sendTemplateSMS('17610811111', ['9527','5'], 1)
    # ccp1 = CCP()
    # ccp2 = CCP()
    # ccp3 = CCP()
    ccp = CCP()
    ccp.send_template_sms('17610811111', ['9527','5'], 1)