# !/usr/bin/python
# -*-coding: utf-8-*-

import login, get

# 程序主入口
print u'''
	--------------------------------------
	       模拟登录知乎 By 李昶昕
	--------------------------------------
'''

print u'请输入知乎账号（手机号或邮箱）：'
account = str(raw_input())
print u'请输入密码：'
password = str(raw_input())

# 登录
spider_login =  login.SpiderLogin() # 实例化登录模块
spider_login.login(account, password) # 给登录模块的方法传参

# 抓取页面
spider_get = get.Get()
spider_get.start()