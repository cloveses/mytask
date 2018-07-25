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
    return u
