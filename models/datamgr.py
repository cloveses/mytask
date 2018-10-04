from .model import *
from tweb import tools
import datetime
import calendar
import base64
import hashlib
import math


@db_session
def send(params):
    if not exists(u for u in User if u.telephone==params['telephone']):
        code,ret = '',{}
        try:
            code,ret = tools.send_sms(params['telephone'])
        except:
            return False
        if code and ret:
            sms = select(s for s in Sms if s.telephone == params['telephone']).first()
            now = datetime.datetime.now()
            if sms:
                sms.code,sms.telephone = code,params['telephone']
                sms.smsid,sms.create_date = smsid=ret['smsid'],now
            else:
                Sms(code=code, telephone=params['telephone'], smsid=ret['smsid'], create_date=now)
            commit()
            return ret['smsid']

@db_session
def add_user(params,make_token):
    now = datetime.datetime.now()
    delete(s for s in Sms if s.create_date < now - datetime.timedelta(minutes=30))
    if not exists(u for u in User if u.telephone==params['telephone']):
        sms = select(s for s in Sms if s.telephone==params['telephone'] and 
            s.code==params['code']).first()
        if not sms:
            return 1 #验证码错误
        seconds = (now - sms.create_date).seconds
        if seconds > 3 * 60:
            return 2 #超时
        md5str = sms.smsid + sms.telephone
        vcode = hashlib.md5(md5str.encode('utf-8')).hexdigest()
        if vcode != params['vcode']:
            return 3 #安全验证失败
        sms.delete()
        u = User(telephone=params['telephone'],passwd=params['passwd'])
        commit()
        token_str = ','.join((u.telephone,str(u.id)))
        token = make_token(token_str)
        commit()
        return (u.telephone,token)
    else:
        return 0 # 号码已注册

@db_session
def update_info(params):
    u = select(u for u in User if u.id == int(params['id']) and
        u.telephone == params['telephone']).first()
    if u:
        del params['id']
        del params['telephone']
        if 'gender' in params:
            if params['gender'].isdigit():
                params['gender'] = int(params['gender'])
            else:
                del params['gender']
        if params:
            for k,v in params.items():
                setattr(u,k,v)
            return True

@db_session
def verify_user(params,make_token):
    u = select(u for u in User if u.passwd == params['passwd'] and
        u.telephone == params['telephone']).first()
    if u:
        token_str = ','.join((u.telephone,str(u.id)))
        token = make_token(token_str)
        return (u.id,u.is_vip(),token)

@db_session
def vlogin(params,make_token):
    u = select(u for u in User if u.telephone==params['telephone']).first()
    if u:
        token_str = ','.join((u.telephone,str(u.id)))
        token = make_token(token_str)
        if token == params['token']:
            return True

@db_session
def set_passwd(params):
    u = select(u for u in User if u.telephone==params['telephone'] and 
        u.passwd ==params['opasswd']).first()
    if u:
        u.passwd = params['passwd']
        return True

@db_session
def get_resrcs(params, pagesize=6):
    page = int(params['page']) if 'page' in params else 0
    del params['page']
    if params:
        rets = Resource.select()
        if 'category' in params:
            rets.where(category==params[category])
        if 'region' in params:
            rets.where(region==params['region'])

        rets = list(rets)
        rets.sort(key=lambda r:r.score,reverse=True)
        rets = rets.page(page,pagesize)
    else:
        rets = Resource.select().order_by(desc(Resource.score)).page(page,pagesize)
    return [r.to_dict(['id','title','description','score']) for r in rets]


@db_session
def search(key):
    rets = select(r for r in Resource if key in r.title or key in r.description).order_by(desc(Resource.score))
    return [r.to_dict(['id','title','description','','cover','url']) for r in rets]

@db_session
def get_resrc(rid):
    r = Resource[int(rid)]
    return r.to_dict(['title','description','url','cover'])

@db_session
def save_portrait(params):
    u = User[int(params['uid'])]
    if u:
        u.portrait = base64.b64decode(params['data'].encode('ascii'))
        return True

@db_session
def get_portrait(uid):
    u = User[int(uid)]
    if u:
        return u.portrait