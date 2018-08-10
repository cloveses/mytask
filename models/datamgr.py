from .model import *
import datetime
import calendar

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
def get_ss_questions():
    groups = select(s.group for s in SsQuestion)[:]
    groups.sort()
    datas = []
    for group in groups:
        qstns = select(s for s in SsQuestion if s.group == group)
        for qstn in qstns:
            datas.append(qstn.to_dict())
    return {'secrityQuestions':datas}


@db_session
def add_secure_qestion(params):
    u = User[params['userId']]
    if u:
        u.secure_questions.clear()
        qsts =( 
            SecureQuestion(question_id=params['questionId01'],answer=params['answer01'],user=u),
            SecureQuestion(question_id=params['questionId02'],answer=params['answer02'],user=u),
            SecureQuestion(question_id=params['questionId03'],answer=params['answer03'],user=u))
        for qst in qsts:
            u.secure_questions.add(qst)
        commit()
        return qsts

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
        datas = []
        for qstn in qstns:
            datas.append({'questionId':qstn.question_id,
                'question':SsQuestion[qstn.question_id].question})
        return datas

# @db_session
# def get_ss_qstn(userName):
#     u = select(u for u in User if u.name == userName).first()
#     if u:
#         qs = select(q for q in SsQuestion)[:]
#         if not qs:
#             SsQuestion(question='aaa')
#             SsQuestion(question='bbb')
#             SsQuestion(question='ccc')
#         commit()
#         qs = select(q for q in SsQuestion)[:]
#         return qs

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
        ret = u.to_dict()
        kvs = {'name':'userName','real_name':'realName','home_addr':'homeAddr','company_addr':'companyAddr'}
        for k,v in kvs.items():
            ret[v] = ret[k]
            del ret[k]
        ret = {k:v if v else '' for k,v in ret.items()}
        for k in ('gender','height','weight'):
            if not ret[k]:
                ret[k] = 0
        return ret

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
        kvs = {'name':'userName','real_name':'realName','home_addr':'homeAddr','company_addr':'companyAddr'}
        for k,v in kvs.items():
            ret[v] = ret[k]
            del ret[k]
        ret = {k:v if v else '' for k,v in ret.items()}
        for k in ('gender','height','weight'):
            if not ret[k]:
                ret[k] = 0
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
        commit()
        data = t.to_dict()
        data['nickyName'] = data['nicky_name']
        del data['nicky_name']
        data['user'] = t.user.id
        return data

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
        trusts = [t for t in u.trusts]
        data = []
        for t in trusts:
            data.append({'area':t.area,'email':t.email,'relationship':t.relationship,
                'nickyName':t.nicky_name,'country':t.country,'number':t.number,
                'id':t.id,'user':t.user.id})
        return data


@db_session
def modify_trust(tid,params):
    if 'nickyName' in params:
        params['nicky_name'] = params['nickyName']
        del params['nickyName']
    t = select(t for t in Trust if t.id==tid).first()
    if t:
        for k,v in params.items():
            setattr(t,k,v)
        commit()
        data = t.to_dict()
        data['nickyName'] = data['nicky_name']
        del data['nicky_name']
        data['user'] = t.user.id
        return data

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

@db_session
def save_loginlog(uid,dt):
    u = User[uid]
    if u:
        log = LoginLog(date_time=dt,user=u)
        u.loginlogs.add(log)
        return True

@db_session
def save_used_location(uid,params):
    u = User[uid]
    if u:
        loc = UsedLocation(user=u,**params)
        u.usedlocations.add(loc)
        return True

def get_datetimes(c_date,months=6):
    y,m,d = c_date.year,c_date.month,c_date.day
    rets = [(datetime.datetime(y,1,1),datetime.datetime.now()),]
    for i in range(months-1):
        if m - 1 > 0:
            m -= 1
        else:
            y -= 1
            m = 12
        rets.append((datetime.datetime(y,m,1),
            datetime.datetime(y,m,calendar.monthrange(y,m)[1],23,59,59,999999)))
    return rets[::-1]


@db_session
def count_loginlog_count(uid,c_date):
    u = User[uid]
    if u:
        totals = len(u.loginlogs)
        periods = get_datetimes(c_date)
        start,end = periods[0]
        curMonthCount = count(g for g in LoginLog 
            if g.user == u and start <= g.date_time <= end)
        othMonthCount = []
        for start,end in periods[1:]:
            counts = count(g for g in LoginLog 
            if g.user == u and between(g.date_time, start, end))
            othMonthCount.append({'mon':start.month,'data':counts})
        return {"screenActive":
                    {"currentMonCount":curMonthCount,"totalCount":totals,"statisticsData":othMonthCount}}

@db_session
def count_local_info(uid):
    u = User[uid]
    if u:
        local_infos = select((loc.area_type,count(loc.id)) for loc in UsedLocation if loc.user==u)
        if local_infos:
            rets = [{'label':v[0],'data':v[1]} for v in local_infos]
            return {"localInfo":rets}