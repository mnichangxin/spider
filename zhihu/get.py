# !/usr/bin/python
# -*-coding: utf-8-*-

import re, HTMLParser
import req

# HTML解码器
html_parser = HTMLParser.HTMLParser()

# 构造字段容器
user_id = [] # 用户ID
user_name = [] # 昵称

# 爬取信息
class GetPage:
	# 抓取页面内容
	def getContent(self, url):
		r = req.get(url)
		content = html_parser.unescape(r.content)

		return content

	# 获得关注的总人数，每页20人，计算出关注人列表页数
	def getNumber(self):
		content = self.getContent('https://www.zhihu.com/people/mnichangxin/following')

		number = int(re.findall('<div class="NumberBoard-value">(.*?)</div>', content)[0])

		return number / 20 if number / 20 == 0 else number / 20 + 1 

	def getPage(self, page):
		content = self.getContent('https://www.zhihu.com/people/mnichangxin/following?page=' + page)

		# user_id.extend(re.findall('"url":"","urlToken":"(.*?)"', content))
		# user_name.extend(re.findall('"gender":.*?,"name":"(.*?)"', content))
		user_name.extend(re.findall('<span class="UserLink UserItem-name">.*?<a class="UserLink-link" target="_blank" href="(.*?)">(.*?)</a>.*?</span>', content))

	def load(self):
		number = self.getNumber()

		for i in range(0, number):
			self.getPage(str(i + 1))

	def start(self):
		self.load()
		
		f = open('data.txt', 'w')

		# for i in range(0, len(user_name)):
		# 	f.write('用户ID：' + user_name[i] + ', ' + '昵称：' + user_name[i] + '\n')
		for i in range(0, len(user_name)):
			f.write('昵称：' + str(user_name[i]) + '\n')

		f.close()