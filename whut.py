# -*- coding = utf-8 -*-
# @Time : 2020/5/7 21:32
# @Author : AX
# @File : whut.py
# @Software: PyCharm
import urllib.request
import urllib.error
import urllib.parse
import hashlib


# 1.指定URL
url = "http://sso.jwc.whut.edu.cn/Certification/login.do"
# 2.通过请求头设置为浏览器
# data = {
#     "MsgID": "",
#     "KeyID": "",
#     "UserName": "",
#     "Password": "",
#     "rnd": 64183,
#     "return_EncData": "",
#     "code": 9219201675,

#     "type": "xs",

# }


username =
username1 = hashlib.md5(bytes(username.encode("utf-8")))
username1 = username1.hexdigest()
password =
temp = username + password
password1 = hashlib.sha1(bytes(temp.encode("utf-8")))
password1 = password1.hexdigest()
print(username1, password1)
data = "MsgID=&KeyID=&UserName=&Password=&rnd=64183&return_EncData=&code=9219201675&userName1=" + username1 + "&password1=" + password1 + "&webfinger=b9a7a7901c83c4c0dad90bd2bbf19498&type=xs&userName=" + username + "&password=" + password
data = bytes(data.encode('utf-8'))
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Cookie":
}

# 3.封装req对象
try:
    req = urllib.request.Request(url=url, headers=headers, method="POST", data=data)
except urllib.error.URLError as e:
    if hasattr(e, "code"):
        print(e['code'])
# 4.进行爬取
response = urllib.request.urlopen(req)
# 5.解码阅读
st = str(response.read().decode('utf-8'))
print(st)
