# !/usr/bin/python
# -*-coding: utf-8-*-

import spider, window

spider = spider.Spider()

# 登录
spider.login()

# 抓取页面信息
account = spider.getConf()[0]
holds = spider.getPage()[0]
score = spider.getPage()[1]

window = window.Window(spider, account, holds, score)
