#!/usr/bin/python
#-*-coding:utf-8-*-

# 爬取天猫商品评论数据

import urllib2, re, codecs, sys

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8')

#爬虫类
class Spider:

	# 请求网页，获得数据
	def getPage(self, page):
		url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=537734028319&spuId=696624585&sellerId=197232874&order=3&currentPage=' + page
		user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36' # 模拟浏览器 
		headers = {'User-Agent': user_agent}

		req = urllib2.Request(url, headers = headers)
		res = urllib2.urlopen(req)
		pageContent = res.read()

		# 构建字段容器
		nickname = [] # 昵称
		ratedate = [] # 评论日期
		ratecate = [] # 商品类型
		ratecontent = [] # 评论内容

		# 正则匹配
		nickname.extend(re.findall('"displayUserNick":"(.*?)"', pageContent))
		ratedate.extend(re.findall('"rateDate":"(.*?)"', pageContent))
		ratecate.extend(re.findall('"auctionSku":"(.*?)"', pageContent))
		ratecontent.extend(re.findall('"rateContent":"(.*?)"', pageContent.replace('<b></b>', '')))


		# 存储为csv文件
		f = open('rate_tmall.csv', 'a')

		for i in range(0, len(nickname)):
			f.write(','.join((nickname[i], ratedate[i], ratecate[i], ratecontent[i])) + '\n')

		f.close()

	# 当前页爬完，加载下一页
	def load(self, page):
		for i in range(1, page + 1):
			print u'爬取第' + str(i) + '页......'
			self.getPage(str(i))


# 程序主入口
print u'''
	----------------------------------
	  爬取天猫商品评论数据 By 李昶昕
	----------------------------------
'''

print u'输入要爬取的评论页数：'

mySpider = Spider()
mySpider.load(int(raw_input()))