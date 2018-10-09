import os
import datetime
from pony.orm import *

db = Database()

class Resource(db.Entity):
    _table_ = 'video'
    url = Required(str)
    title = Required(str)
    cover = Optional(str)
    category = Optional(str)
    duration = Optional(str)
    releasetime = Optional(str)
    region = Optional(str)
    language = Optional(str)
    type = Optional(str)
    description = Optional(str)
    score = Optional(str)
    featureKeyword = Optional(str)
    orderNum = Optional(str)
    favourites = Set('Favourite')
    historyes = Set('History')

# class Resource(db.Entity):
#     name = Required(str)
#     description =Required(str)
#     url = Required(str)
#     viewtimes = Required(int)
#     vipflag = Required(bool)
#     score = Required(float)
#     myear = Required(int)
#     rtype = Optional('ResrcType', reverse='resources')
#     rarea = Optional('ResrcArea', reverse='resources')
#     rclass = Optional('ResrcClass', reverse='resources')
#     favourites = Set('Favourite')
#     historyes = Set('History')

    
# class ResrcType(db.Entity):
#     name = Required(str)
#     resources = Set(Resource)

# class ResrcArea(db.Entity):
#     area = Required(str)
#     resources = Set(Resource)

# class ResrcClass(db.Entity):
#     mclass = Required(str)
#     resources = Set(Resource)

class User(db.Entity):
    name = Optional(str)
    passwd = Required(str)
    telephone = Required(str)
    portrait = Optional(bytes)
    gender = Optional(int)
    birthday = Optional(datetime.date)
    sign_txt = Optional(str)
    vip_end = Optional(datetime.datetime)
    # token = Optional(str)
    favourites = Set('Favourite')
    historyes = Set('History')
    vorders = Set('Vorder')
    
    def is_vip(self):
        if self.vip_end and self.vip_end <= datetime.datetime.now():
            return True
        else:
            return False

class Vorder(db.Entity):
    total_fee = Required(int)
    order_no = Required(str)
    result = Required(bool,default=False)
    user = Required(User)

class Favourite(db.Entity):
    user = Required(User, reverse='favourites')
    resource = Required(Resource, reverse='favourites')

class History(db.Entity):
    user = Required(User, reverse='historyes')
    resource = Required(Resource, reverse='historyes')

class Sms(db.Entity):
    code = Required(str)
    telephone = Required(str)
    smsid = Optional(str)
    create_date = Required(datetime.datetime)

set_sql_debug(True)
# filename = os.path.join(os.path.abspath(os.curdir),'my.db')
# db.bind(provider='sqlite', filename=filename, create_db=True)
db.bind(provider='mysql',host='localhost',user='webuser',passwd='*Web2user*',db='iqiyi')
db.generate_mapping(create_tables=True)