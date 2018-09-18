import os

port = 8000

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
CURRENT_PATH = os.path.dirname(CURRENT_PATH)
HDL_DIR = ["hdls",]
web_server = {
    # 'xsrf_cookies': True,
    'cookie_secret': "jjhfu845646dfds%^&(*(ghgy6$@%^@#!*()^GTG",
    # 'cookie_expires': 86400,
    # 'autoescape': None,
    'debug': True,
}

# SECRITY_QUESTION = (
#     ('你少年时代最好的朋友叫什么名字？',
#         '你的第一个宠物叫什么名字？',
#         '你学会做的第一道菜是什么？',
#         '你第一次去电影院看的是哪一部电影？',
#         '你第一次坐飞机是去哪里？',
#         '你上小学时最喜欢的老师姓什么？'),

#     ('你的理想工作是什么？',
#         '你小时候最喜欢哪一本书？',
#         '你拥有的第一辆车是什么型号？',
#         '你童年时代的绰号是什么？',
#         '你在学生时代最喜欢哪个电影明星或角色？',
#         '你在学生时代最喜欢哪个歌手或乐队？'),

#     ('你的父母是在哪里认识的？',
#         '你的第一个上司叫什么名字？',
#         '您从小长大的那条街叫什么？',
#         '你去过的第一个海滨浴场是哪一个？',
#         '你购买的第一张专辑是什么？',
#         '您最喜欢哪个球队？')
#     )