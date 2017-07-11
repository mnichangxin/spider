# !/usr/bin/python
# -*-coding: utf-8-*-

import requests

# 构造headers
headers = {
	'User-Agent': 'Apache-HttpClient/UNAVAILABLE (java 1.4)',
	'Connection': 'keep-alive',
	'Host': '219.143.202.141'
}

# 建立Session
session = requests.session()

# Get方法
def get(url, data = {}):
	return session.get(url, data = data, headers = headers)

# Post方法
def post(url, data = {}):
	return session.post(url, data = data, headers = headers)
