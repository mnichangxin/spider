#!/usr/bin/python
#-*-coding:utf-8-*-

# 糗事百科爬虫

import urllib, urllib2, re, sys

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8') 

# 爬虫类
class Spider:
	def __init__(self):
		self.url = 'http://www.qiushibaike.com/hot/page/' # 爬取的URL前缀

	# 请求网页，正则匹配相应段子
	def getPage(self, page):
		curUrl = self.url + page # 当前URL
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' # 模拟浏览器 
		headers = {'User-Agent': user_agent}
		
		req = urllib2.Request(curUrl, headers = headers) # 请求对象
		res = urllib2.urlopen(req) # 响应对象
		pageContent = res.read().decode('utf-8') # 读取结果，其他编码转换为utf-8格式  
 		
 		author =  re.findall('<div class="author clearfix">.*?<a href=".*?" target="_blank" title=".*?">.*?<h2>(.*?)</h2>.*?</a>.*?</div>', pageContent, re.S) # 段子作者
		content = re.findall('<div class="content">.*?<span>(.*?).</span>.*?</div>', pageContent, re.S) # 段子内容

		f = open('data.txt', 'a')

		items = []
		
		for i, j in zip(author, content):
			items.append(i + '：' + '\n' + j.replace('<br/>', '\n') + '\n\n')

		for item in items:
			f.write(item)

		f.close()

	# 当前页爬完，加载下一页
	def load(self, page):
		for i in range(1, page + 1):
			print u'爬取第' + str(i) + '页......'
			self.getPage(str(i))

# 程序主入口
print u'''
	----------------------------------
	    糗事百科简单爬虫 By 李昶昕
	----------------------------------
'''

print u'输入要爬取的页数：'

mySpider = Spider()
mySpider.load(int(raw_input()))