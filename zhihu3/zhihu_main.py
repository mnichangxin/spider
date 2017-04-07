# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 17:04:59 2017

@author: mnichangxin
"""

from __future__ import unicode_literals, print_function
from zhihu_oauth import ZhihuClient
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
    
# 爬取话题下关注的人
f = open('followers.csv', 'a')    
f.write(codecs.BOM_UTF8) # 防止csv文件乱码
f.write(','.join(('用户ID',)) + '\n')    
f.close()
  
followers = client.topic(19551275).followers

f = open('followers.csv', 'a')

print(u'正在爬取......')

for follower in followers:
    try:
        if follower.follower_count >= 5000:
            f.write(','.join((follower.id,)) + '\n')    
    except:
        pass
        
f.close()

print(u'爬取完毕！')
    