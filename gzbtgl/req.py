# !/usr/bin/python
# -*-coding: utf-8-*-

import requests
from requests.adapters import HTTPAdapter

# 构造headers
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
}

# 建立Session
session = requests.session()
session.mount('http://', HTTPAdapter(max_retries=5))
session.mount('https://', HTTPAdapter(max_retries=5))

# Get方法
def get(url, data = {}):
	return session.get(url, data = data, headers = headers, timeout=30)

# Post方法
def post(url, data = {}):
	return session.post(url, data = data, headers = headers, timeout=30)

