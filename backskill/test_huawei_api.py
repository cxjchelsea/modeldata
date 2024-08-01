# _*_ coding: utf-8 _*_
# @File:    test_huawei_api
# @Time:    2024/5/8 9:02
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1

import requests
import json

url = "https://8c4190eb6a4d45debccb8b52869672de.apic.cn-north-4.huaweicloudapis.com/4a39c8a24abb47c7a144ad6f1e03d723"
data = {"req_data":{"H":25,"K1":2,"K2":3,"E":1,"phi":2,"K":0.1}}
headers = {"Content-Type": "application/json;charset=UTF-8"}
result = requests.post(url=url, json=data, headers=headers, verify=False)

# resp_data = json.loads(result.text)["resp_data"]
print(result.text)
