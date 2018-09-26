from urllib import parse,request
import json
import time,random
import base64,binascii
import hashlib


base_url = 'http://127.0.0.1:8000/api'
tel = '13485842157'
# f = open('er.jpg','rb')
# data = binascii.hexlify(f.read())

post_item = [
    ('/send_sms',{'telephone':tel}),
    # ('/register',{'telephone':'13485842157','code':'469594','vcode':'c7fcf9cd96559d58378fe4d8224cd534','passwd':'abc'})
    # ('/updateinfo',{'telephone':'12345678912','id':1,'name':'abc'}),
    # ('/login',{'telephone':'12345678912','passwd':'abc'}),
    # ('/vlogin',{'telephone':tel,'token':'6a2b9aba35b28603c9acd031dcd6eece2de5bacea62a3a8f1ae8ef0c295e268c2af877d2427389f0f4fdf33195eb86b342509e5ff5652ae57a1c56a52c97b291'}),
    # ('/trusts',{'userId':'1'}),
    # ('/uploadLocation',{'userId':'1','longitude':'23.3E','latitude':'12.5S','address':'myaddr','areaType':'其它区域'}),
    # ('/upload',{'data':data})
    # ('/up_portrait',{'uid':1,'data':data}),
    ]

def link(item):
    textmod=item[1]
    textmod = parse.urlencode(textmod).encode(encoding='utf-8')

    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0)',"Content-Type": "application/x-www-form-urlencoded"}
    url=''.join((base_url,item[0]))
    print(url)
    req = request.Request(url=url,data=textmod,headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    ret = json.loads(res.decode(encoding='utf-8'))
    print(ret)

    if url.endswith('send_sms'):
        print('register start...')
        url = ''.join((base_url,'/register'))
        code = input('Please input code:')
        md5str = ret['smsid'] + item[1]['telephone']
        vcode = hashlib.md5(md5str.encode('utf-8')).hexdigest()

        textmod = {'telephone':tel,'code':code,
            'vcode':vcode,'passwd':'abc'}
        print('url:',url)
        print('data:',textmod)
        textmod = parse.urlencode(textmod).encode(encoding='utf-8')
        req = request.Request(url=url,data=textmod,headers=header_dict)
        res = request.urlopen(req)
        res = res.read()
        ret = json.loads(res.decode(encoding='utf-8'))
        print(ret)

if __name__ == '__main__':
    for p in post_item:
        link(p)
