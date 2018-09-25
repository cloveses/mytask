from .model import *
from tweb import tools
import datetime
import calendar
import base64
import hashlib

@db_session
def send(params):
    if not exists(u for u in User if u.telephone==params['telephone']):
        code,ret = '',{}
        try:
            code,ret = tools.send_sms(params['telephone'])
        except:
            return False
        if code and ret:
            print('code:',code,'ret:',ret)
            delete(s for s in Sms if s.telephone == params['telephone'])
            Sms(code=code, telephone=params['telephone'], smsid=ret['smsid'])
            return ret['smsid']

@db_session
def add_user(params,make_token):
    timeout = 30
    now = datetime.datetime.now()
    delete(s for s in Sms if now - datetime.timedelta(minutes=timeout) >= s.create_date)
    if not exists(u for u in User if u.telephone==params['telephone']):
        sms = select(s for s in Sms if s.telephone==params['telephone'] and 
            s.code==params['code']).first()
        if not sms:
            return 1 #验证码错误
        minutes = (now - sms.create_date).seconds // 60
        if minutes > timeout:
            return 2 #超时
        md5str = sms.smsid + sms.telephone
        print('md5str:',md5str)
        vcode = hashlib.md5(md5str.encode('utf-8')).hexdigest()
        print('local:',vcode,'remote:',params['vcode'])
        if vcode != params['vcode']:
            # sms.delete()
            return 3 #安全验证失败
        sms.delete()
        u = User(telephone=params['telephone'],passwd=params['passwd'])
        token = make_token(','.join((u.telephone,str(u.id))))
        u.token = token
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
def verify_user(params):
    u = select(u for u in User if u.passwd == params['passwd'] and
        u.telephone == params['telephone']).first()
    if u:
        return (u.id,u.is_vip())

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
        rets = set()
        if 'typeid' in params:
            typeid = int(params['typeid'])
            rtype = ResrcType[typeid]
            rets.update(rtype.resources)
        if 'areaid' in params:
            areaid = int(params['areaid'])
            rarea = ResrcArea[areaid]
            rets.update(rarea.resources)
        if 'classid' in params:
            classid = int(params['classid'])
            rclass = ResrcClass[classid]
            rets.update(rclass.resources)
        rets = list(rets)
        rets.sort(key=lambda r:r.viewtimes,reverse=True)
        rets = rets[page*pagesize:(page+1)*pagesize]
    else:
        rets = Resource.select().order_by(desc(Resource.viewtimes))[page*pagesize:(page+1)*pagesize]
    return [r.to_dict(['id','name','description','viewtimes','vipflag']) for r in rets]


@db_session
def search(key):
    rets = (r for r in Resource if key in r.name or key in r.description).order_by(desc(Resource.viewtimes))
    return [r.to_dict(['id','name','description','viewtimes','vipflag']) for r in rets]

@db_session
def get_resrc(rid):
    r = Resource[int(rid)]
    return r.to_dict(['name','description','url','vipflag'])

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