from urllib import parse,request
import json

base_url = '/app/v1'
post_item = [
    ('/register',{'userName':'abc','psw':'abc','gender':'2','age':'23-8'}),
    ('/saveSecrityQuestion',{'userId':'1','questionId01':'1','answer01':'a',
            'questionId02':'2','answer02':'b','questionId03':'3','answer03':'c'}),
    # ('/questionnaire',{'userId':'1','questionnaireResult':json.dumps({'1':'abc','2':'def'})}),
    # ('/login',{'userName':'abc','psw':'abc'}),
    # ('/obtainSecrityQuestion',{'userName':'abc'}),
    # ('/forgetPswVerify',{'userName':'abc','questionId01':'1','answer01':'a',
    #         'questionId02':'2','answer02':'b','questionId03':'3','answer03':'c'}),
    # ('/forgetPsw',{'userName':'abc','newPsw':'abc'}),
    # ('/obtainProfile',{'userId':'1',}),
    # ('/modifyProfile',{'userId':'1','realName':'abc','gender':'1','age':'11','companyAddr':'fghf11'}),
    # ('/modifyPsw',{'userId':'1','oldPsw':'abc','newPsw':'abc'}),
    # ('/settingTrust',{'userId':'1','nickyName':'abc','email':'ac@kdk.com','country':'China',
    #         'area':'abc','number':'abc','relationship':'abc'}),
    # ('/feedback',{'userId':'1','content':'abc','email':'ac@kdk.com','score':'32'}),
    # ('/logout',{'userId':'1'}),
    # ('/trusts',{'userId':'1'}),
    # ('/modifyTrust',{'userId':'1','trustId':'1','nickyName':'aac','email':'ac@kdk.com','country':'China',
    #         'area':'abc','number':'abc','relationship':'abc'}),
    # ('/queryTrust',{'userId':'1','trustId':'1'}),
    # ('/deleteTrust',{'userId':'1','trustId':'1'}),
    # ('/init',{}),


    ]

def link(item):
    textmod=item[1]
    textmod = parse.urlencode(textmod).encode(encoding='utf-8')

    # 测试本地服务器
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0)',"Content-Type": "application/x-www-form-urlencoded"}
    url=''.join(('http://127.0.0.1:8000',base_url,item[0]))
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

if __name__ == '__main__':
    for p in post_item:
        link(p)
