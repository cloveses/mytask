from .model import *

@db_session
def add_user(params,make_token):
    if not exists(u for u in User if u.name==params['name']):
        u = User(**params)
        token = make_token(','.join((u.name,str(u.id))))
        u.token = token
        commit()
        return (u.id,token,u.name)
    else:
        return False

@db_session
def add_secure_qestion(params):
    u = User[params['userId']]
    qsts =( 
        SecureQuestion(question_id=params['questionId01'],answer=params['answer01'],user=u),
        SecureQuestion(question_id=params['questionId02'],answer=params['answer02'],user=u),
        SecureQuestion(question_id=params['questionId03'],answer=params['answer03'],user=u))
    for qst in qsts:
        u.secure_questions.add(qst)

@db_session
def add_question_naire(params):
    u = User[params['userId']]
    qresults = params['questionnaireResult']
    qns = []
    for k,v in qresults.items():
        qns.add(QestionNaire(question_id=k,answer=v,user=u))
    for qn in qns:
        u.question_naires.add(qn)

@db_session
def user_verify(username,psw,make_token):
    u = select(u for u in User if u.name == username and u.passwd == psw).first()
    if u:
        token = make_token(','.join((u.name,str(u.id))))
        u.token = token
        return {'userName':u.name,'userId':u.id,'token':token}

@db_session
def get_secure_qstn(userName):
    u = select(u for u in User if u.name == userName).first()
    if u:
        # return {'userName':u.name,'id':u.id}
        qstns = list(u.secure_questions)
        qstns.sort(key=lambda q:q.id)
        return qstns

@db_session
def verify_secure_question(name,qstn_data):
    u = select(u for u in User if u.name == name).first()
    if u:
        for qstn in u.secure_questions:
            if qstn_data[qstn.question_id] != qstn.answer:
                return False
        return True
    else:
        return False

@db_session
def new_psw(name,psw):
    u = select(u for u in User if u.name == name).first()
    if u:
        u.passwd = psw
        return True

@db_session
def get_user_info(uid):
    u = select(u for u in User if u.id == uid).first()
    if u:
        return {'userName':u.name,'age':u.age}

@db_session
def modify_user(uid,params):
    u = select(u for u in User if u.id == uid).first()
    if u:
        keys = {'realName':'real_name','gender':'gender',
            'age':'age','homeAddr':'home_addr','companyAddr':'company_addr',
            'height':'height','weight':'weight'}
        for k,v in params.items():
            setattr(u,keys[k],v)
        commit()
        ret = u.to_dict()
        kvs = {'name':'userName','real_name':'realName','home_addr':'homeAddr','company_addr':'companyAdd'}
        for k,v in kvs.items():
            ret[v] = ret[k]
            del ret[k]
        return ret

@db_session
def modify_psw(uid,params,make_pw):
    u = select(u for u in User if u.id == uid).first()
    if u:
        opsw = make_pw(params['oldPsw'],u.name)
        if u.passwd == opsw:
            u.passwd = make_pw(params['newPsw'],u.name)
            return True

@db_session
def setting_trust(uid,params):
    u = select(u for u in User if u.id == uid).first()
    if u:
        params['nicky_name'] = params['nickyName']
        del params['nickyName']
        t = Trust(user=u,**params)
        u.trusts.add(t)

        return True

@db_session
def add_feed_back(uid,params):
    u = User[uid]
    if u:
        fb = FeedBack(content=params['content'],email=params['email'],
                score=int(params['score']),user=u)
        u.feed_backs.add(fb)
        return True

@db_session
def logout(uid):
    u = User[uid]
    if u:
        u.token = ''
        return True

@db_session
def get_trusts(uid):
    u = User[int(uid)]
    if u:
        return [t.to_dict() for t in u.trusts]

@db_session
def modify_trust(tid,params):
    t = select(t for t in Trust if t.id==tid).first()
    if t:
        for k,v in params.items():
            setattr(t,k,v)
        return True

@db_session
def delete_trust(uid,tid):
    t = select(t for t in Trust if t.id==tid).first()
    if t:
        u = User[uid]
        u.trusts.remove(t)
        t.delete()
        return True

@db_session
def query_trust(uid,tid):
    t = select(t for t in Trust if t.id==tid).first()
    if t:
        return t.to_dict()