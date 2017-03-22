# !/usr/bin/python
# -*-coding: utf-8-*-

import requests

# 构造headers
headers = {
	'Origin': 'http://user.hnjsrcw.com',
	'Referer': 'http://user.hnjsrcw.com/Space/Login.aspx',
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Accept-encoding': 'gzip, deflate',
	'Accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
}

# 建立Session
session = requests.session()

# Get方法
def get(url, data = {}):
	return session.get(url, data = data, headers = headers)

# Post方法
def post(url, data = {}):
	return session.post(url, data = data, headers = headers)
