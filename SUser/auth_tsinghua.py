import urllib
import requests
import json

def get_ip(request):
    try:
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
            ip =  request.META['HTTP_X_FORWARDED_FOR']
            return str(ip).replace('.', '_')
        else:  
            ip = request.META['REMOTE_ADDR'] 
            return str(ip).replace('.', '_')
    except:
        return '127_0_0_1'

def auth_tsinghua(request, username, password):
    url = 'https://id.tsinghua.edu.cn/thuser/authapi/login/XSGZPT/' + get_ip(request)
    data = {'username':username, 'password':password}
    headers = {'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'Connection':'keep-alive',
            'Content-Length':'76',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'net.tsinghua.edu.cn',
            'Origin':'http://net.tsinghua.edu.cn',
            'Referer':'http://net.tsinghua.edu.cn/wired/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_90_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(encoding='UTF8'))
    response = urllib.request.urlopen(req)
    res = response.read()
    ret = json.loads(res.decode())
    if ret['status'] == 'RESTLOGIN_OK':
        return True
    else:
        return False

if __name__ == "__main__":
    auth('request', 'username', 'password')