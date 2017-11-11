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
	'X-CSRF-TOKEN': '16757a86-ac70-4909-b8c2-cc20143471b0',
	'X-Requested-With': 'XMLHttpRequest',
	'Cookie': 'liyungf_tc=AQAAANbyigUZiwcAHkaAcTv3rqqaeFuq; SESSION=6e69e49e-affd-4c48-89a4-bc8dd04afd7a; JSESSIONID=39FBF4BD7FD3E7911C81007ED6A72AFD'
}

# 建立Session
session = requests.session()

# Get方法
def get(url, data = {}):
	return session.get(url, data = data, headers = headers)

# Post方法
def post(url, data = {}):
	return session.post(url, data = data, headers = headers)

