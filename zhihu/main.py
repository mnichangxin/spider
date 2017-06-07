# !/usr/bin/python
# -*-coding: utf-8-*-

from __future__ import unicode_literals, print_function
from zhihu_oauth import ZhihuClient
from multiprocessing import Pool
import os, sys, codecs

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8') 

# 登录
TOKEN_FILE = 'token.pkl'

client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
	client.load_token(TOKEN_FILE)
else:
	client.login_in_terminal()
	client.save_token(TOKEN_FILE)