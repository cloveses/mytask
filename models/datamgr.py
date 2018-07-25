from .model import *

@db_session
def add_user(params):
    User(**params)

@db_session
def add_secure_qestion(params):
    u = User[params['userId']]
    qsts =( 
        SecureQuestion(qestion_id=params['questionId01'],answer=params['answer01'],user=u)
        SecureQuestion(qestion_id=params['questionId02'],answer=params['answer02'],user=u)
        SecureQuestion(qestion_id=params['questionId03'],answer=params['answer03'],user=u))
    for qst in qsts:
        user.secure_questions.add(qst)

@db_session
def add_question_naire(params):
    u = User[params['userId']]
    qresults = params['questionnaireResult']
    qns = []
    for k,v in qresults.items():
        qns.add(QestionNaire(qestion_id=k,answer=v,user=u))
    for qn in qns:
        u.question_naires.add(qn)

@db_session
def user_verify(username,psw):
    u = select(u for u in User if u.name == username and u.passwd == psw).first()
    if u:
        return {'userName':u.name,'id':u.id}

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
        for k,v in params:
            setattr(u,keys[k],v)
            return True

@db_session
def modify_psw(uid,params,make_pw):
    u = select(u for u in User if u.id == uid).first()
    if u:
        opsw = make_pw(params['oldPsw'],u.name)
        if u.passwd == opsw:
            u.passwd = make_pw(params['newPsw'],u.name)

@db_session
def setting_trust(uid,params):
    u = select(u for u in User if u.id == uid).first()
    if u:
        for k,v in params.items():
            if k == 'nickyName':
                u.nicky_name = v
            else:
                setattr(u,k,v)
        return True
@db_session
def add_feed_back(uid,params):
    u = User[uid]
    if u:
        fb = FeedBack(content=params['content'],email=params['email'],
                score=int(params['score']),user=u)
        u.feed_backs.add(fb)
        return True
