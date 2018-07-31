import os
from pony.orm import *

db = Database()

class User(db.Entity):
    name = Required(str)
    passwd = Required(str)
    gender = Required(int)
    age = Required(str)
    token = Optional(str)
    secure_questions = Set('SecureQuestion')
    qestion_naires = Set('QestionNaire')
    feed_backs = Set('FeedBack')
    trusts = Set('Trust')

    real_name = Optional(str)
    home_addr = Optional(str)
    company_addr = Optional(str)
    height = Optional(int)
    weight = Optional(int)

class Trust(db.Entity):
    nicky_name = Required(str)
    email = Required(str)
    country = Required(str)
    area = Required(str)
    number = Required(str)
    relationship = Required(str)
    user = Required(User,reverse='trusts')

class FeedBack(db.Entity):
    content = Optional(str)
    email = Optional(str)
    score = Optional(int)
    user = Required(User,reverse='feed_backs')

class SecureQuestion(db.Entity):
    question_id = Required(int)
    answer = Required(str)
    user = Required(User,reverse='secure_questions')

class SsQuestion(db.Entity):
    question = Required(str)
    group = Required(int)

class QestionNaire(db.Entity):
    question_id = Required(str)
    answer = Required(str)
    user = Required(User,reverse='qestion_naires')


set_sql_debug(True)
filename = os.path.join(os.path.abspath(os.curdir),'my.db')
db.bind(provider='sqlite', filename=filename, create_db=True)
db.generate_mapping(create_tables=True)