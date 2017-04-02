# !/usr/bin/python
# -*-coding: utf-8-*-

import login, get, window

# 程序主入口
print u'''
	--------------------------------------
	       爬取知乎数据 By 李昶昕
	--------------------------------------
'''

# 登录
spider_login =  login.SpiderLogin() # 实例化登录模块
spider_get = get.Get()

# window = window.Window(spider_login, spider_get)


# 抓取页面
# spider_get = get.Get()
# spider_get.start()