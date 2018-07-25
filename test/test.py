from urllib import parse,request
import json

base_url = '/app/v1'
post_item = [
    ('/register',{'userName':'abc','psw':'abc','gender':'2','age':'23-8'}),
    ]

def link(item):
    textmod=items[1]
    #json串数据使用
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    #普通数据使用
    textmod = parse.urlencode(textmod).encode(encoding='utf-8')
    # print(textmod)
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0)',"Content-Type": "application/json"}
    url=''.join(('http://127.0.0.1',base_url,post_item[0]))
    req = request.Request(url=url,data=textmod,headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    # print(res)
    #输出内容:b'{"jsonrpc":"2.0","result":"37d991fd583e91a0cfae6142d8d59d7e","id":1}'
    print(res.decode(encoding='utf-8'))

if __name__ == '__main__':
    for p in post_item:
        link(p)
