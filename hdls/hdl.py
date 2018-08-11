import hashlib
import time
import json
import calendar
import datetime
import tornado.web
from tweb.web import BaseHandler, route
from models import datamgr

def make_pw(psw,salt):
    psw = ''.join((psw,salt))
    psw = psw.encode()
    try:
        ret = hashlib.sha3_512(psw).hexdigest()
    except:
        ret = hashlib.sha512(psw).hexdigest()
        
    return ret

def make_token(s):
    curr_time = ''.join((str(time.time()),time.ctime(),
        time.asctime(),str(time.clock())))
    md5_str = make_pw(s,curr_time)
    sha1_str = hashlib.sha1(','.join((s,curr_time)).encode()).hexdigest()
    return make_pw(md5_str,sha1_str)

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

@route('/app/v1/register')
class RegHdl(BaseHandler):

    def post(self):
        keys = ('userName','psw','gender','age')
        params = self.get_params(keys)
        if all(params.values()):
            params['gender'] = int(params['gender'])
            params['psw'] = make_pw(params['psw'],params['userName'])
            keys_dict = {'userName':'name','psw':'passwd','gender':'gender','age':'age'}
            params = {v:params[k] for k,v in keys_dict.items()}
            res = datamgr.add_user(params,make_token)
            if res:
                self.write_json({'status':0,'data':{'userId':res[0],'token':res[1],'userName':res[2]}})
            else:
                if res is not None:
                    self.write_json({'status':1,'msg':'用户名已被注册！'})
        else:
            self.write_json({'status':1,'msg':'请完整填写数据！'})

@route('/app/v1/init')
class InitHdl(BaseHandler):

    def post(self):
        from .tmp_data import data
        datas = datamgr.get_ss_questions()
        data.update(datas)
        self.write_json({"data":data,"msg":"", "status":0})

@route('/app/v1/saveSecrityQuestion')
class SecrityQustHdl(BaseHandler):

    # @tornado.web.authenticated
    def post(self):
        keys = ('userId','questionId01','answer01',
            'questionId02','answer02','questionId03','answer03')
        params = self.get_params(keys)
        if all(params.values()):
            for key in ('userId','questionId01','questionId02','questionId03'):
                params[key] = int(params[key])
            data = datamgr.add_secure_qestion(params)
            ret = []
            for d in data:
                ret.append({'questionId':d.question_id,'answer':d.answer})
            self.write_json({'status':0,'msg':'安全问题保存成功！','data':{'secrityQuestions':ret}})
        else:
            self.write_json({'status':1,'msg':'请完整填写数据！'})

@route('/app/v1/questionnaire')
class QuestionNaire(BaseHandler):

    def post(self):
        keys = ('userId','questionnaireResult')
        params = self.get_params(keys)
        if all(params.values()):
            params['userId'] = int(params['userId'])
            params['questionnaireResult'] = json.loads(params['questionnaireResult'])
            self.write_json({'status':0})
        else:
            self.write_json({'status':1,'msg':'数据不完整！'})

@route('/app/v1/login')
class LoginHdl(BaseHandler):

    def post(self):
        keys = ('userName','psw')
        params = self.get_params(keys)
        if all(params.values()):
            psw = make_pw(params['psw'],params['userName'])
            u = datamgr.user_verify(params['userName'],psw,make_token)
            if u:
                self.write_json({'status':0,'msg':'登录成功！','data':u})
            else:
                self.write_json({'status':1,'msg':'用户名或密码错误！'})
        else:
            self.write_json({'status':1,'msg':'请输入用户名和密码！'})

@route('/app/v1/obtainSecrityQuestion')
class ObtainSecrityHdl(BaseHandler):

    def post(self):
        keys = ('userName',)
        params = self.get_params(keys)
        if all(params.values()):
            data = datamgr.get_secure_qstn(params['userName'])
            if data:
                res = {'status':0}
                res['data'] = {'secrityQuestions':data}
                self.write_json(res)
                return
        self.write_json({'status':1,'msg':'未设置安全问题或用户名错误！'})

@route('/app/v1/forgetPswVerify')
class PswVerifyHdl(BaseHandler):

    def post(self):
        keys = ('userName','questionId01','answer01',
            'questionId02','answer02','questionId03','answer03')
        params = self.get_params(keys)
        for key in ('questionId01','questionId02','questionId03'):
            params[key] = int(params[key])
        if all(params.values()):
            qstn_data = {}
            qstn_data[params['questionId01']] = params['answer01']
            qstn_data[params['questionId02']] = params['answer02']
            qstn_data[params['questionId03']] = params['answer03']
            print(qstn_data)
            if datamgr.verify_secure_question(params['userName'],qstn_data):
                self.write_json({'status':0})
                return
        self.write_json({'status':1,'msg':'安全问题验证未通过！'})

@route('/app/v1/forgetPsw')
class ForgetPsw(BaseHandler):

    def post(self):
        keys = ('userName','newPsw')
        params = self.get_params(keys)
        if all(params.values()):
            psw = make_pw(params['newPsw'],params['userName'])
            if datamgr.new_psw(params['userName'],psw):
                self.write_json({'status':0})
                return
        self.write_json({'status':1,'msg':'密码修改失败！'})

@route('/app/v1/obtainProfile')
class ObtainProfileHdl(BaseHandler):

    def post(self):
        keys = ('userId',)
        params = self.get_params(keys)
        if all(params.values()):
            data = datamgr.get_user_info(params['userId'])
            if data:
                self.write_json({'status':0,'data':data})
                return
        self.write_json({'status':1,'msg':'信息获取失败！'})

@route('/app/v1/modifyProfile')
class ModifyProfileHdl(BaseHandler):

    def post(self):
        keyas = ('userId','realName','gender','age')
        keybs = ('homeAddr','companyAddr','height','weight')
        paramas = self.get_params(keyas)
        parambs = self.get_params(keybs)
        if all(paramas.values()):
            paramas['gender'] = int(paramas['gender'])
            parambs = {k:v for k,v in parambs.items() if v}
            for k,v in parambs.items():
                paramas[k] = v
            if 'height' in paramas:
                paramas['height'] = int(paramas['height'])
            if 'weight' in paramas:
                paramas['weight'] = int(paramas['weight'])
            uid = int(paramas['userId'])
            del paramas['userId']
            data = datamgr.modify_user(uid,paramas)
            if data:
                self.write_json({'status':0,'data':data})
                return
        self.write_json({'status':1,'msg':'信息修改失败！'})

@route('/app/v1/modifyPsw')
class ModifyPswHdl(BaseHandler):

    def post(self):
        keys = ('userId','oldPsw','newPsw')
        params = self.get_params(keys)
        if all(params.values()):
            uid = int(params['userId'])
            if datamgr.modify_psw(uid,params,make_pw):
                self.write_json({'status':0})
                return
        self.write_json({'status':1,'msg':'密码修改失败！'})


@route('/app/v1/settingTrust')
class SettingTrustHdl(BaseHandler):

    def post(self):
        keys = ('userId','nickyName','email','country',
            'area','number','relationship')
        params = self.get_params(keys)
        if all(params.values()):
            uid = int(params['userId'])
            del params['userId']
            data = datamgr.setting_trust(uid,params)
            if data:
                self.write_json({'status':0,'data':data})
                return
        self.write_json({'status':1,'msg':'设置失败！'})

@route('/app/v1/feedback')
class FeedBackHdl(BaseHandler):

    def post(self):
        keys = ('userId','content','email','score')
        params = self.get_params(keys)
        if all(params.values()):
            uid = int(params['userId'])
            if datamgr.add_feed_back(uid,params):
                self.write_json({'status':0})
                return
        self.write_json({'status':1,'msg':'设置失败！'})

@route('/app/v1/logout')
class LogoutHdl(BaseHandler):

    def post(self):
        keys = ('userId',)
        params = self.get_params(keys)
        if params['userId']:
            uid = int(params['userId'])
            if datamgr.logout(uid):
                self.write_json({'status':0})
                return
        self.write_json({'status':1,'msg':'失败！'})

@route('/app/v1/trusts')
class TrustsHdl(BaseHandler):

    def post(self):
        keys = ('userId',)
        params = self.get_params(keys)
        if params['userId']:
            uid = int(params['userId'])
            data = datamgr.get_trusts(uid)
            if data is not None:
                self.write_json({'status':0,'data':{'trusts':data}})
                # from .tmp_data import data_trust
                # self.write_json(data_trust)
                return
        self.write_json({'status':1,'msg':'失败！'})

@route('/app/v1/modifyTrust')
class ModifyTrustHdl(BaseHandler):

    def post(self):
        keys = ('userId','trustId','nickyName','email','country',
            'area','number','relationship')
        params = self.get_params(keys)
        if all(params.values()):
            uid = int(params['userId'])
            del params['userId']
            tid = int(params['trustId'])
            del params['trustId']
            data = datamgr.modify_trust(tid,params)
            if data:
                self.write_json({'status':0,'data':data})
                return
        self.write_json({'status':1,'msg':'修改信任组失败！'})

@route('/app/v1/deleteTrust')
class DeleteTrustHdl(BaseHandler):
    def post(self):
        keys = ('userId','trustId',)
        params = self.get_params(keys)
        if all(params.values()):
            uid = int(params['userId'])
            tid = int(params['trustId'])
            if datamgr.delete_trust(uid,tid):
                self.write_json({'status':0})
                return
        self.write_json({'status':1,'msg':'删除信任组失败！'})

@route('/app/v1/queryTrust')
class QueryTrust(BaseHandler):
    def post(self):
        keys = ('userId','trustId',)
        params = self.get_params(keys)
        if all(params.values()):
            uid = int(params['userId'])
            tid = int(params['trustId'])
            data = datamgr.query_trust(uid,tid)
            if data:
                self.write_json({'status':0,'data':data})
                return
        self.write_json({'status':1,'msg':'查询信任组失败！'})

@route('/app/v1/homeStatistics')
class HomeStatisticsHdl(BaseHandler):
    def post(self):
        keys = ('userId','currentMon',)
        params = self.get_params(keys)
        if all(params.values()):
            uid = int(params['userId'])
            ymd = params['currentMon'].split('-')
            ymd = [int(n) for n in ymd]
            # start_date,end_date = get_date(*ymd)
            c_date = datetime.date(*ymd)
            from .tmp_data import home_static
            rets = {}
            rets.update(home_static)
            screen_active = datamgr.count_loginlog_count(uid,c_date)
            local_info = datamgr.count_local_info(uid)
            if screen_active:
                rets['data'].update(screen_active)
            if local_info:
                rets['data'].update(local_info)
            self.write_json(rets)
            return
        self.write_json({'status':1,'msg':'失败！'})


@route('/app/v1/accountActive')
class AccountActiveHdl(BaseHandler):
    def post(self):
        keys = ('userId','dateTime')
        params = self.get_params(keys)
        if all(params.values()):
            uid = int(params['userId'])
            dt = datetime.datetime.strptime(params['dateTime'],
                '%Y-%m-%d %H:%M:%S')
            if datamgr.save_loginlog(uid,dt):
                self.write_json({'status':0})
                return
        self.write_json({'status':1,'msg':'失败！'})

@route('/app/v1/uploadLocation')
class UploadLocationHdl(BaseHandler):
    def post(self):
        keys = ('userId','longitude','latitude','address','areaType')
        params = self.get_params(keys)
        if all(params.values()):
            uid = int(params['userId'])
            params['area_type'] = params['areaType']
            del params['areaType']
            del params['userId']
            if datamgr.save_used_location(uid,params):
                self.write_json({'status':0})
                return
        self.write_json({'status':1,'msg':'失败！'})
