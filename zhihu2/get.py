# !/usr/bin/python
# -*-coding: utf-8-*-

import re, HTMLParser
import req

# HTML解码器
html_parser = HTMLParser.HTMLParser()

# 构造字段容器
ques_id = []

# 爬取话题下的精华问题
class GetTop:
	def __init__(self, topic_id):
		self.topic_id = topic_id

	# Get方式页面内容解析
	def getContent(self, url):
		r = req.get(url)
		# content = html_parser.unescape(r.content.decode('unicode-escape').encode('utf-8'))
		return r.content

	# 每页20个问题，计算出所有可爬问题的页数
	def getNumber(self):
		topic_content = self.getContent('https://www.zhihu.com/topic/' + self.topic_id + '/top-answers')
		q = re.findall('<h1 class="zm-editable-content" data-disabled="1">(.*?)</h1>', topic_content)[0]

		search_content = self.getContent('https://www.zhihu.com/search?type=content&q=' + q)
		top_answers = int(re.findall('<a href="/topic/.*?/top-answers" class="col"><strong>(.*?)</strong><span>精华</span></a>', search_content)[0])

		return top_answers / 20 if top_answers / 20 == 0 else top_answers / 20 + 1 

	# 爬取每页下问题的ID
	def getPage(self, page):
		content = self.getContent('https://www.zhihu.com/topic/' + self.topic_id + '/top-answers?page=' + page)
		ques_id.extend(re.findall('<a class="question_link" href="/question/(.*?)".*>', content))

	# 逐页加载
	def load(self):
		number = self.getNumber()

		for i in range(0, number):
			self.getPage(str(i + 1)) 

	# 启动
	def start(self):
		self.load()

		f = open('data.txt', 'a')

		for i in range(0, len(ques_id)):
			f.write(ques_id[i] + '\n')

		f.close()

