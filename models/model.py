import os
from pony.orm import *

db = Database()

class User(db.Entity):
    name = Required(str)
    passwd = Required(str)
    gender = Required(int)
    age = Required(str)
    secure_questions = Set('SecureQuestion')
    qestion_naires = Set('QestionNaire')
    feed_backs = Set('FeedBack')

    real_name = Optional(str)
    home_addr = Optional(str)
    company_addr = Optional(str)
    height = Optional(int)
    weight = Optional(int)

    nicky_name = Optional(str)
    email = Optional(str)
    country = Optional(str)
    area = Optional(str)
    number = Optional(str)
    relationship = Optional(str)

class FeedBack(db.Entity):
    content = Optional(str)
    email = Optional(str)
    score = Optional(int)
    user = Required(User,reverse='feed_backs')

class SecureQuestion(db.Entity):
    question_id = Required(int)
    answer = Required(str)
    user = Required(User,reverse='secure_questions')

class QestionNaire(db.Entity):
    question_id = Required(str)
    answer = Required(str)
    user = Required(User,reverse='qestion_naires')


set_sql_debug(True)
filename = os.path.join(os.path.abspath(os.curdir),'my.db')
db.bind(provider='sqlite', filename=filename, create_db=True)
db.generate_mapping(create_tables=True)