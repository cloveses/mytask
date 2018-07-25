import hashlib
import json
from tweb.web import BaseHandler, route
from models import datamgr

def make_pw(psw,salt):
    psw = ''.join((psw,salt))
    psw = psw.encode()
    return hashlib.sha3_512(psw).hexdigest()

@route('/')
class IndexHdl(BaseHandler):

    def get(self):
        self.write_json({"hint_info":'self.hint_info'})

@route('/app/v1/register')
class RegHdl(BaseHandler):

    def get(self):
        keys = ('userName','psw','gender','age')
        params = self.get_params(keys)
        if all(params.values()):
            params['gender'] = int(gender)
            params['psw'] = make_pw(params['psw'],params['userName'])
            datamgr.add_user(params)
            self.write_json({'status':0})
        else:
            self.write_json({'status':1,'msg':'请完整填写数据！'})

@route('/saveSecrityQuestion')
class SecrityQustHdl(BaseHandler)

    def get(self):
        keys = ('userId','questionId01','answer01',
            'questionId02','answer02','questionId03','answer03')
        params = self.get_params(keys)
        if all(params.values()):
            for key in ('userId','questionId01','questionId02','questionId03'):
                params[key] = int(params[key])
            datamgr.add_secure_qestion(params)
            self.write_json({'status':0})
        else:
            self.write_json({'status':1,'msg':'请完整填写数据！'})

@route('/questionnaire')
class QuestionNaire(BaseHandler):

    def get(self):
        keys = ('userId','questionnaireResult')
        params = self.get_params(keys)
        if all(params.values()):
            params['userId'] = int(params['userId'])
            params['questionnaireResult'] = json.loads(params['questionnaireResult'])
            self.write_json({'status':0})
        else:
            self.write_json({'status':1,'msg':'数据不完整！'})

@route('/login')
class LoginHdl(BaseHandler):

    def get(self):
        keys = ('userName','psw')
        params = self.get_params(keys)
        if all(params.values()):
            psw = make_pw(params['psw'],params['userName'])
            datamgr.user_verify(params['userName'],params['psw'])