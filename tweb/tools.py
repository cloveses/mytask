from urllib import parse,request
import ssl
import json
import random
import hashlib
import time
import string
import datetime
import xml.etree.ElementTree as et
# import settings

params = {
    'appid':'wx907069b19af4c709',
    'mch_id':'1516130171',
    'detail':'my detail', #商品描述
    # 'nonce_str':'acc',
    'body':'my body',  #商品详情
    # 'out_trade_no':'abc no',
    # 'total_fee':4,
    'spbill_create_ip':'123.59.194.102',
    'notify_url':'http://123.59.194.102:8000/api/pay_notify',
    'trade_type':'JSAPI',
    # 'sign':'abc'
}

order_txt = """
        <xml>
           <appid>{appid}</appid>
           <mch_id>{mch_id}</mch_id>
           <detail>{detail}</detail>
           <nonce_str>{nonce_str}</nonce_str>
           <sign>{sign}</sign>
           <body>{body}</body>
           <out_trade_no>{out_trade_no}</out_trade_no>
           <total_fee>{total_fee}</total_fee>
           <spbill_create_ip>{spbill_create_ip}</spbill_create_ip>
           <notify_url>{notify_url}</notify_url>
           <trade_type>{trade_type}</trade_type>
        </xml>"""
 
SUCCESS_TXT = '''
<xml>
  <return_code>SUCCESS</return_code>
  <return_msg>OK</return_msg>
</xml>'''

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

def get_nonce_str(length=32):
    str_a = str(time.time()).replace('.','')
    str_b = string.ascii_letters
    mystr = list(''.join((str_a,str_b)))
    random.shuffle(mystr)
    return ''.join(mystr)[:length]

def get_out_trade_no():
    a_str = get_nonce_str(48)
    a_str += str(time.time())
    md5str = hashlib.md5(a_str.encode('utf-8')).hexdigest()
    d = datetime.datetime.isoformat(datetime.datetime.now())
    d = d[:d.index('.')]
    d = d.replace(':','_')
    return d + md5str

def get_sign(params):
    params = {k:str(v) for k,v in params.items() if v}
    ks = list(params.keys())
    ks.sort()
    md5lst = []
    for k in ks:
        md5lst.append('='.join((k,params[k])))
    md5str = '&'.join(md5lst)
    # print(md5str)
    return hashlib.md5(md5str.encode('utf-8')).hexdigest()

def submit_order(total_fee):
    nonce_str = get_nonce_str()
    out_trade_no = get_out_trade_no()
    params['nonce_str'] = nonce_str
    params['out_trade_no'] = out_trade_no
    params['total_fee'] = total_fee

    params['sign'] = get_sign(params)

    textmod = order_txt.format(**params)
    print(textmod)
    textmod = textmod.encode(encoding='utf-8')
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0)',"Content-Type": "text/xml"}
    url='https://api.mch.weixin.qq.com/pay/unifiedorder'
    req = request.Request(url=url,data=textmod,headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    res = res.decode('utf-8')
    print(res)
    return params,get_xml_params(res)
    # ret = json.loads(res.decode(encoding='utf-8'))
    # print(ret)
    # return code,ret

def get_xml_params(xml_txt):
    tree = et.fromstring(xml_txt)
    rets = {}
    for tr in tree.getchildren():
        rets[tr.tag] = tr.text
    return rets


if __name__ == '__main__':
    # send_sms()
    submit_order(5)
