# !/usr/bin/python
# -*-coding: utf-8-*-

import login, get

# 程序主入口
print u'''
	--------------------------------------
	       爬取知乎数据 By 李昶昕
	--------------------------------------
'''

# 登录
# print u'请输入邮箱或手机号：'
# account = raw_input()
# print u'请输入密码：'
# password = raw_input()

spider_login =  login.SpiderLogin()
spider_login.login('18954109152', 'li1769.')


# 抓取页面
# spider_get = get.GetTop('19776749')
# spider_get.start()

spider_get = get.GetCommit()
spider_get.start()