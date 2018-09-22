from urllib import parse,request
import json
import time,random
import base64

f = open('wa.jpg','rb')
data = base64.b64encode(f.read())
f.close()

base_url = '/api'
post_item = [
    # ('/register',{'telephone':'12345678912','passwd':'abc'}),
    # ('/updateinfo',{'telephone':'12345678912','id':1,'name':'abc'}),
    # ('/login',{'telephone':'12345678912',
    #     'passwd':'abc'}),
    # ('/register',{'telephone':'张三','passwd':'abc'}),
    ('/up_portrait',{'uid':1,'data':data})
    # ('/send_sms',{'telephone':'13485842157'}),
    ('/register',{'telephone':'13495942157','code':'469594','vcode':'c7fcf9cd96559d58378fe4d8224cd534','passwd':'abc'})

    # {'status': 0, 'data': {'telephone': '张三', 'token': 'b13216b2fe8fc7690dd60c611a7f6af5bf1bccf3ba325c7e91584dea17d93d3145959142a76c2b0a7c9ec64db231abb7d7e25ba9c1173b659a3b4285dcc3a26a'}
    # ('/saveSecrityQuestion',{'userId':'1','questionId01':'1','answer01':'a',
    #         'questionId02':'8','answer02':'b','questionId03':'14','answer03':'c'}),
    # ('/questionnaire',{'userId':'1','questionnaireResult':json.dumps({'1':'abc','2':'def'})}),
    # ('/login',{'userName':'abc','psw':'abc'}),
    # ('/obtainSecrityQuestion',{'userName':'abc'}),
    # ('/forgetPswVerify',{'userName':'abc','questionId01':'1','answer01':'a',
    #         'questionId02':'8','answer02':'b','questionId03':'14','answer03':'c'}),
    # ('/forgetPsw',{'userName':'abc','newPsw':'abc'}),
    # ('/obtainProfile',{'userId':'1',}),
    # ('/modifyProfile',{'userId':'1','realName':'abc','gender':'1','age':'11','companyAddr':'fghf11'}),
    # ('/modifyPsw',{'userId':'1','oldPsw':'abc','newPsw':'abc'}),
    # ('/settingTrust',{'userId':'1','nickyName':'abc','email':'ac@kdk.com','country':'China',
    #         'area':'abc','number':'abc','relationship':'abc'}),
    # ('/trusts',{'userId':'1'}),
    # ('/feedback',{'userId':'1','content':'abc','email':'ac@kdk.com','score':'32'}),
    # ('/logout',{'userId':'1'}),
    # ('/modifyTrust',{'userId':'1','trustId':'1','nickyName':'aac','email':'ac@kdk.com','country':'China',
    #         'area':'ddd','number':'abc','relationship':'abc'}),
    # ('/trusts',{'userId':'1'}),
    # ('/queryTrust',{'userId':'1','trustId':'1'}),
    # ('/deleteTrust',{'userId':'1','trustId':'1'}),
    # ('/init',{}),
    # ('/homeStatistics',{'userId':'1','currentMon':'2018-8-12'}),
    # ('/accountActive',{'userId':'1','dateTime':'2018-5-12 3:3:3'}),
    # ('/uploadLocation',{'userId':'1','longitude':'23.3E','latitude':'12.5S','address':'myaddr','areaType':'其它区域'}),

    ]

def link(item):
    textmod=item[1]
    textmod = parse.urlencode(textmod).encode(encoding='utf-8')

    # 测试本地服务器
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0)',"Content-Type": "application/x-www-form-urlencoded"}
    url=''.join(('http://cloveses.pythonanywhere.com',base_url,item[0]))
    print(url)
    # 测试远程服务器
    # header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',"Content-Type": "application/x-www-form-urlencoded",
    # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Language':'en-US,en;q=0.5',
    # 'Accept-Encoding':'gzip, deflate'}
    # url=''.join(('http://cloveses.pythonanywhere.com',base_url,item[0]))

    req = request.Request(url=url,data=textmod,headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    print(json.loads(res.decode(encoding='utf-8')))

# for i in range(5):
#     post_item.append(('/register',
#         {'userName':'absdc'+ str(random.randint(12,39)),
#         'psw':'abc','gender':str(random.randint(1,2)),
#         'age':random.choice(('8-12','13-16','17-25','26-40'))}))
#     post_item.append(('/saveSecrityQuestion',{'userId':str(i+1),'questionId01':'1','answer01':'a',
#             'questionId02':'2','answer02':'b','questionId03':'3','answer03':'c'}))
#     for j in range(random.randint(50,99)):
#         mytime = '{}-{}-{} {}:{}:{}'.format(random.choice(('2017','2018')),
#             random.randint(1,12),random.randint(1,26),
#             random.randint(0,23),random.randint(0,59),random.randint(0,59))
#         post_item.append(('/accountActive',{'userId':str(i+1),
#             'dateTime':mytime}))
#     for k in range(random.randint(20,69)):
#         post_item.append(('/uploadLocation',
#             {'userId':str(i+1),
#             'longitude':str(random.random()*random.randint(1,180))[:5] + 'E',
#             'latitude':str(random.random()*random.randint(1,90))[:4] + 'N',
#             'address':'myaddr'+str(random.randint(1,10)),
#             'areaType':random.choice(('工作区域','医疗区域','生活区域','其它区域'))}))

if __name__ == '__main__':
    for p in post_item:
        link(p)
