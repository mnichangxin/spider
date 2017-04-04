# !/usr/bin/python
# -*-coding: utf-8-*-

import re, codecs, HTMLParser
import req

# HTML解码器
html_parser = HTMLParser.HTMLParser()

# 构造字段容器
ques_id = [] # 问题ID
answers_name = [] # 回答者用户名
answers_id = [] # 回答者ID
comments_id = [] # 评论者ID 

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
	# def start(self):
	# 	self.load()

	# 	f = open('data.txt', 'a')

	# 	for i in range(0, len(ques_id)):
	# 		f.write(ques_id[i] + '\n')

	# 	f.close()

# 爬取精华问题下的回答者ID
class GetAnswer:
	# Get方式页面内容解析
	def getContent(self, url):
		r = req.get(url)
		return r.content

	# 每页20个回答者，计算出所有可爬回答者的页数
	def getNumber(self):
		ans_content = self.getContent('https://www.zhihu.com/api/v4/questions/28626263/answers?include=data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=3&limit=20&sort_by=default')
		number = int(re.findall('"totals": (.*?), "previous"', ans_content)[0])

		return number / 20 if number / 20 == 0 else number / 20 + 1 

	# 爬取每页下回答者的ID
	def getPage(self, offset):
		content = self.getContent('https://www.zhihu.com/api/v4/questions/28626263/answers?include=data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=' + offset + '&limit=20&sort_by=default')
		answers_name.extend(re.findall('"url_token": "(.*?)"', content))

	# 逐页加载
	def load(self):
		number = self.getNumber()

		for i in range(0, number):
			self.getPage(str(20 * i + 3)) # offset = 20 * (num - 1) + 3 

	# 启动
	def start(self):
		self.load()

		f = open('data.csv', 'a')

		f.write(codecs.BOM_UTF8) # 防止csv文件乱码
		f.write(','.join(('问题ID', '回答者和评论者ID')) + '\n') # 写入首行标题
		f.write(','.join(('28626263',)) + ',')

		for i in range(0, len(answers_name)):
			f.write(','.join((answers_name[i],)) + ',')

		f.close()


# 爬取每个回答下的评论者ID
class GetCommit:
	# Get方式页面内容解析
	def getContent(self, url):
		r = req.get(url)
		return r.content

	# 每页20个评论者，计算出所有可爬回答者的页数
	def getNumber(self):
		ans_content = self.getContent('https://www.zhihu.com/api/v4/answers/42743181/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=20&offset=20&status=open')
		number = int(re.findall('"totals": (.*?), "previous"', ans_content)[0])

		return number / 20 if number / 20 == 0 else number / 20 + 1 

	# 爬取每页下评论者的ID
	def getPage(self, offset):
		content = self.getContent('https://www.zhihu.com/api/v4/answers/42743181/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=20&offset=' + offset + '&status=open')
		answers_name.extend(re.findall('"url_token": "(.*?)"', content))

	# 逐页加载
	def load(self):
		number = self.getNumber()

		for i in range(0, number):
			self.getPage(str(20 * i)) # offset = 20 * (num - 1) 

	# 启动
	def start(self):
		self.load()

		f = open('data.csv', 'a')

		f.write(codecs.BOM_UTF8) # 防止csv文件乱码
		f.write(','.join(('问题ID', '回答者和评论者ID')) + '\n') # 写入首行标题
		f.write(','.join(('28626263',)) + ',')

		for i in range(0, len(answers_name)):
			f.write(','.join((answers_name[i],)) + ',')

		f.close()
