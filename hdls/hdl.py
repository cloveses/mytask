import hashlib
import time
import json
import calendar
import datetime
import tornado.web
from tweb.web import BaseHandler, route
from models import datamgr
from tweb import tools

def make_pw(psw,salt):
    psw = ''.join((psw,salt))
    psw = psw.encode('utf-8')
    ret = hashlib.sha512(psw).hexdigest()
    return ret

# def make_token(s):
#     curr_time = ''.join((str(time.time()),time.ctime(),
#         time.asctime(),str(time.clock())))
#     md5_str = make_pw(s,curr_time)
#     sha1_str = hashlib.sha1(','.join((s,curr_time)).encode()).hexdigest()
#     return make_pw(md5_str,sha1_str)

def make_token(s):
    return make_pw(s,salt='')

# def get_days(y,m,d,months=6):
#     days = 0
#     for i in range(months):
#         if m - 1 > 0:
#             m -= 1
#         else:
#             y -= 1
#             m = 12
#         days += calendar.monthrange(y,m)[1]
#     return days

# def get_date(y,m,d,months=6):
#     end_date = datetime.date(y,m,d)
#     days = get_days(y,m,d,months)
#     start_date = end_date - datetime.timedelta(days=days)
#     return start_date,end_date

@route('/')
class IndexHdl(BaseHandler):

    def get(self):
        self.write_json({"hint_info":'self.hint_info'})

# @route('/api/upload')
# class UploHdl(BaseHandler):
#     def post(self):
#         # import binascii
#         # data = self.get_argument('data')
#         # print(type(data))
#         # with open('a.jpg','wb') as f:
#         #     f.write(binascii.unhexlify(data.encode('ascii')))
#         import base64
#         data = self.get_argument('data')
#         print(type(data))
#         with open('a.jpg','wb') as f:
#             f.write(base64.b64decode(data.encode('ascii')))
#         self.write_json({'status':0})

@route('/api/send_sms')
class SendHdl(BaseHandler):
    def post(self):
        keys = ('telephone',)
        params = self.get_params(keys)
        if params and params['telephone'].isdigit():
            res = datamgr.send(params)
            if res is not None:
                if res:
                    self.write_json({'status':0,'smsid':res})
                else:
                    self.write_json({'status':1,'msg':'验证短信发送失败！'})
            else:
                self.write_json({'status':1,'msg':'手机号已注册！'})
        else:
            self.write_json({'status':1,'msg':'无正确手机号！'})


@route('/api/register')
class RegHdl(BaseHandler):
    def post(self):
        keys = ('telephone','passwd','code','vcode')
        params = self.get_params(keys)
        if params and len(params) == 4:
            params['passwd'] = make_pw(params['passwd'],params['telephone'])
            res = datamgr.add_user(params,make_token)
            if isinstance(res,tuple):
                self.write_json({'status':0,'data':{'telephone':res[0],'token':res[1]}})
            else:
                msgs = ('号码已注册','验证码错误','超时','安全验证失败')
                self.write_json({'status':1,'msg':msgs[res]})
        else:
            self.write_json({'status':1,'msg':'请完整填写数据！'})

@route('/api/updateinfo')
class UdtHdl(BaseHandler):
    def post(self):
        keys = ('name','gender','birthday','sign_txt','id','telephone')
        params = self.get_params(keys)
        if params and len(params) > 2 and 'id' in params and 'telephone' in params and params['id'].isdigit():
            res = datamgr.update_info(params)
            if res:
                self.write_json({'status':0})
        else:
            self.write_json({'status':1,'msg':'数据不完整！'})

@route('/api/login')
class LoginHdl(BaseHandler):
    def post(self):
        keys = ('telephone','passwd')
        params = self.get_params(keys)
        if params and len(params) == 2:
            params['passwd'] = make_pw(params['passwd'],params['telephone'])
            res = datamgr.verify_user(params,make_token)
            if res:
                self.write_json({'status':0,'data':{'id':res[0],'is_vip':res[1],'token':res[2]}})
            else:
                self.write_json({'status':1})
        else:
            self.write_json({'status':1,'msg':'数据不完整！'})

@route('/api/vlogin')
class VloginHdl(BaseHandler):
    def post(self):
        keys = ('telephone','token')
        params = self.get_params(keys)
        if params and len(params) == 2 and datamgr.vlogin(params,make_token):
            self.write_json({'status':0})
        else:
            self.write_json({'status':1})

@route('/api/setpw')
class SetPwHdl(BaseHandler):
    def post(self):
        keys = ('telephone','passwd','opasswd')
        params = self.get_params(keys)
        if params and len(params) == 3:
            params['opasswd'] = make_pw(params['opasswd'],params['telephone'])
            params['passwd'] = make_pw(params['passwd'],params['telephone'])
            if datamgr.set_passwd(params):
                self.write_json({'status':0})
                return
        self.write_json({'status':1})


@route('/api/resources')
class ResrcHdl(BaseHandler):
    def post(self):
        keys = ('category','page','region','type','releasetime','language')
        params = self.get_params(keys)
        # params = {k:v for k,v in params.items() if v.isdigit()}
        res = datamgr.get_resrcs(params)
        if res:
            self.write_json({'status':0,'data':res})
        else:
            self.write_json({'status':1})

@route('/api/search')
class SearchHdl(BaseHandler):
    def post(self):
        keys = ('key',)
        params = self.get_params(keys)
        if params:
            res = datamgr.search(params['key'])
            if res:
                self.write_json({'status':0,'data':res})
        else:
            self.write_json({'status':1})

@route('/api/show')
class ShowHdl(BaseHandler):
    def post(self):
        keys = ('rid',)
        params = self.get_params(keys)
        if params and params['rid'].isdigit():
            res = datamgr.get_resrc(params['rid'])
            if res:
                self.write_json({'status':0,'data':res})
        else:
            self.write_json({'status':1})

@route('/api/up_portrait')
class UpPortraitHdl(BaseHandler):
    def post(self):
        keys = ('uid','data')
        params = self.get_params(keys)
        if params and params['uid'].isdigit():
            if datamgr.save_portrait(params):
                self.write_json({'status':0})
        else:
            self.write_json({'status':1})

@route('/api/get_portrait')
class GetPortraitHdl(BaseHandler):
    def post(self):
        keys = ('uid',)
        params = self.get_params(keys)
        if params and params['uid'].isdigit():
            res = datamgr.get_portrait(params['uid'])
            if res:
                self.set_header("Content-Type", "image/jpeg")
                self.write(res)
        else:
            self.write_json({'status':1})

@route('/api/pay')
class PayHdl(BaseHandler):
    def post(self):
        keys = ('total_fee','uid')
        params = self.get_params(keys)
        if 'total_fee' in params:
            total_fee = int(float(params['total_fee']) * 100)
            order_params, result = tools.submit_order(total_fee)
            if result['return_code'] == 'SUCCESS':
                datamgr.save_vorder(order_params['out_trade_no'],total_fee,params['uid'])
                self.write_json({'status':0})
            else:
                self.write_json({'status':1,'msg':result['return_msg']})
        else:
            self.write_json({'status':1,'msg':'params not enough!'})


@route('/api/pay_notify')
class PayNotifyHdl(BaseHandler):
    def post(self):
        rets = self.request.body.decode('utf-8')
        params = tools.get_xml_params(rets)
        if 'sign' in params:
            sign = params['sign']
            del params['sign']
            sign_b = tools.get_sign(params)
            if sign == sign_b:
                print('SUCCESS')
                self.write(tools.SUCCESS_TXT)
    def get(self):
        self.post()
