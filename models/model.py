import os
from pony.orm import *

db = Database()

class User(db.Entity):
    name = Required(str)
    passwd = Required(str)
    gender = Required(int)
    age = Required(str)
    secure_questions = Set('SecureQuestion')
    qestion_naires = set('QestionNaire')

class SecureQuestion(db.Entity):
    qestion_id = Required(int)
    answer = Required(str)
    user = Required(User)

class QestionNaire(db.Entity):
    qestion_id = Required(str)
    answer = Required(str)
    user = Required(User)


set_sql_debug(True)
filename = os.path.join(os.path.abspath(os.curdir),'my.db')
db.bind(provider='sqlite', filename=filename, create_db=True)
db.generate_mapping(create_tables=True)