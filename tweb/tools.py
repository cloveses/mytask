from urllib import parse,request
import ssl
import json
import random
# import settings

 
ssl._create_default_https_context = ssl._create_unverified_context

def send_sms(mobile):
    code = str(random.randint(100000,999999))
    textmod={'sid':'ed547745364d28602887c8f79b80e3b5',
            'token':'df3e1a8ae3847817c16e7a3cca602ca6',
            'appid':'f53c88ceffb9417db14005794a5bc7d3',
            'templateid':'369959',
            'param':code,
            'mobile':mobile,
            'uid':'1'
            }
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0)',"Content-Type": "application/json"}
    url='https://open.ucpaas.com/ol/sms/sendsms'
    req = request.Request(url=url,data=textmod,headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    ret = json.loads(res.decode(encoding='utf-8'))
    print(ret)
    return code,ret

if __name__ == '__main__':
    send_sms()