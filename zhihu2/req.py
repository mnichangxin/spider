# !/usr/bin/python
# -*-coding: utf-8-*-

import requests

# 构造headers
headers = {
	'Host': 'www.zhihu.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Accept-Encoding': 'gzip, deflate, sdch, br',
	'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
	'Connection': 'keep-alive',
	'authorization': 'Bearer Mi4wQUJBQVlpaUxJQWdBY0lLQTZDMWNDeGNBQUFCaEFsVk5fVDhEV1FCSWFHYjRzSUIzT2Jnczk4c29vdkZ4ZUFLR3JR|1491279444|27963ce8e50914850523c7033ef6ef9c4cddad36'
}

# 建立Session会话
session = requests.session()

# Get方法
def get(url, data = {}):
	return session.get(url, data = data, headers = headers)

# Post方法
def post(url, data = {}):
	return session.post(url, data = data, headers = headers)
