# -*- coding = utf-8 -*-
# @Time : 2020/5/13 16:25
# @Author : AX
# @File : whutreq.py
# @Software: PyCharm
import requests
import re
from bs4 import BeautifulSoup
import hashlib

'''
@:param:username password
@:return data:[{
    class:
    start:
    end:
    place:
    time:
    where:
}]
'''


def req(username, password):
    # 预处理武汉理工大学登陆数据
    username1 = hashlib.md5(bytes(username.encode("utf-8")))
    username1 = username1.hexdigest()
    temp = username + password
    password1 = hashlib.sha1(bytes(temp.encode("utf-8")))
    password1 = password1.hexdigest()
    print(username1, password1)
    # 设置params
    data = {
        "MsgID": "",
        "KeyID": "",
        "UserName": "",
        "Password": "",
        "rnd": 64183,
        "return_EncData": "",
        "code": 9219201675,
        "userName1": username1,
        "password1": password1,
        "webfinger": "8e9444ad687caac8ab5be6731715c549",
        "type": "xs",
        "userName": username,
        "password": password,
    }
    # url切换
    url = "http://sso.jwc.whut.edu.cn/Certification/login.do"
    # 伪装为浏览器
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }

    # 发起请求
    html = requests.post(url=url, headers=headers, params=data)
    html = html.text

    # 解析数据
    bs = BeautifulSoup(html, "html.parser")
    class_table = bs.select(".table-class-even")[0]
    # 拿到表格数组
    oneLine = class_table.select("tr")
    data = []
    count = 1
    for i in range(len(oneLine)):
        # j用于定位
        j = 0
        current = oneLine[i].select("td")
        newCurrent = []
        # 处理掉碍事的日期td
        for item in current:
            if not re.search(re.compile("style"), str(item)) is None:
                newCurrent.append(item)

        for item in newCurrent:
            flag = item.select("div")
            if len(flag) != 0:
                # 不为空课程，则判断颜色,则通过遍历div判断颜色
                for current in flag:
                    # 如果是红色的
                    if not re.search(re.compile("red"), str(current)) is None:
                        # print(current)
                        class_name = current.select("a")
                        chinese_word = re.search(re.compile(
                            r"[\u4e00-\u9fa5]+"), str(class_name)).group()
                        # print(chinese_word)
                        class_place = current.select("p")
                        # print(chinese_word, class_place)
                    # 如果是蓝色的
                    if not re.search(re.compile("blue"), str(current)) is None:
                        # print(current)
                        class_name = current.select("a")
                        chinese_word = re.search(re.compile(
                            r"[\u4e00-\u9fa5]+"), str(class_name)).group()

                        class_place = current.select("p")
                        if len(class_place) == 3:
                            class_where = class_place[0].string[1:]
                            class_time = class_place[1].string
                            class_qq_group = class_place[2].string
                        if len(class_place) == 2:
                            class_where = class_place[0].string[1:]
                            class_time = class_place[1].string
                            class_qq_group = "无qq群信息"
                        class_sometime = re.findall(
                            re.compile(r"\d+"), str(class_time))
                        for i in range(len(class_sometime)):
                            class_sometime[i] = int(class_sometime[i])
                        class_start = class_sometime[0]
                        class_end = class_sometime[1]
                        data.append({
                            "class_name": chinese_word,
                            "class_where": class_where,
                            "class_qq_group": class_qq_group,
                            "class_time": class_time,
                            "class_start": class_start,
                            "class_end": class_end,
                            "count": count
                        })
                        count += 1
            j += 1
    for item in data:
        print(item)
    return data
