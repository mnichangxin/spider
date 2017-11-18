# !/usr/bin/python
# -*-coding: utf-8-*-

import requests

# 构造headers
headers = {
	'Host': 'www.chips.ltd',
	'Origin': 'https://www.chips.ltd',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
	'Referer': 'https://www.chips.ltd/products/super_book_index',
	'X-Requested-With': 'XMLHttpRequest',
	'X-CSRF-TOKEN': 'd3577802-d3c3-45a1-92db-025757f5ff8f',
	'Cookie': 'aliyungf_tc=AQAAAPh+oBTKZAYAA8qAcX/fE+Ib3e0H; SESSION=6b7c8f45-c84c-4f05-bbbf-f61addcf3803; JSESSIONID=5FC3F15804F1062C5B431583434C4066'
}

# 建立Session
session = requests.session()

# Get方法
def get(url, data = {}):
	return session.get(url, data = data, headers = headers)

# Post方法
def post(url, data = {}):
	return session.post(url, data = data, headers = headers)

