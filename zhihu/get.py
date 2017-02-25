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
		content = html_parser.unescape(r.content.decode('unicode-escape').encode('utf-8'))

		return content

	# 获得关注的总人数，每页20人，计算出关注人列表页数
	def getNumber(self):
		content = self.getContent('https://www.zhihu.com/people/mnichangxin/following')

		number = int(re.findall('<div class="NumberBoard-value">(.*?)</div>', content)[0])

		return number / 20 if number / 20 == 0 else number / 20 + 1 

	def getPage(self, offset):
		content = self.getContent('https://www.zhihu.com/api/v4/members/mnichangxin/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=' + offset + '&limit=20')

		user_id.extend(re.findall('"url_token": "(.*?)"', content))
		user_name.extend(re.findall('"avatar_url_template": ".*?", "name": "(.*?)"', content))

	def load(self):
		number = self.getNumber()

		for i in range(0, number):
			self.getPage(str(i * 20)) # offset = (page - 1) * 20

	def start(self):
		self.load()
		
		f = open('data.txt', 'w')

		for i in range(0, len(user_id)):
			f.write('用户ID：' + user_id[i] + ', ' + '昵称：' + user_name[i] + '\n')

		f.close()