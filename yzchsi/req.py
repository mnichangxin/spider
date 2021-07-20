# !/usr/bin/python
# -*-coding: utf-8-*-

import requests
from requests.adapters import HTTPAdapter

# 构造headers
headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
	'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"'
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

