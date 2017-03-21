# !/usr/bin/python
# -*-coding: utf-8-*-

import re, HTMLParser
import req

# HTML解码器
html_parser = HTMLParser.HTMLParser()

# 构造字段容器
user_id = ['mnichangxin'] # 用户ID
user_name = ['mnichangxin'] # 昵称
topic_name = [] # 话题
ques = [] # 问题

# 爬取关注的人
class GetFollow:
	def __init__(self, user_id):
		self.user_id = user_id # 默认是自己的user_id

	# 抓取页面内容
	def getContent(self, url):
		r = req.get(url)
		content = html_parser.unescape(r.content.decode('unicode-escape').encode('utf-8'))

		return content

	# 获得关注的总人数，每页20人，计算出关注人列表页数
	def getNumber(self):
		content = self.getContent('https://www.zhihu.com/people/' + self.user_id + '/following')

		number = int(re.findall('<div class="NumberBoard-value">(.*?)</div>', content)[0])

		return number / 20 if number / 20 == 0 else number / 20 + 1 

	def getPage(self, offset):
		content = self.getContent('https://www.zhihu.com/api/v4/members/' + self.user_id + '/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=' + offset + '&limit=20')

		# user_id_t = re.findall('"url_token": "(.*?)"', content)
		# user_name_t = re.findall(', "name": "(.*?)"', content)

		# ID去重
		# for i in range(0, len(user_id)):
		# 	for j in range(0, len(user_id_t)):
		# 		if user_id[i] != user_id_t[j]:
		# 			user_id.append(user_id_t[j])
		# 			user_name.append(user_name_t[j])

		user_id.extend(re.findall('"url_token": "(.*?)"', content))
		user_name.extend(re.findall(', "name": "(.*?)"', content))

	def load(self):
		number = self.getNumber()

		for i in range(0, number):
			self.getPage(str(i * 20)) # offset = (page - 1) * 20

	def start(self):
		self.load()

		f = open('user.txt', 'w')

		for i in range(0, len(user_id)):
			f.write('用户ID：' + user_id[i] + ', ' + '昵称：' + user_name[i] + '\n')

		f.close()


# 爬取关注的话题
class GetTopic:
	def __init__(self, user_id):
		self.user_id = user_id

	# 抓取页面内容
	def getContent(self, url):
		r = req.get(url)
		content = html_parser.unescape(r.content.decode('unicode-escape').encode('utf-8'))

		return content

	# 获得关注话题，每页20个，计算出关注话题列表页数
	def getNumber(self):
		content = self.getContent('https://www.zhihu.com/people/' + self.user_id + '/following')

		number = int(re.findall('<span class="Profile-lightItemName">关注的话题</span>.*?<span class="Profile-lightItemValue">(.*?)</span>', content)[0])

		return number / 20 if number / 20 == 0 else number / 20 + 1 

	def getPage(self, offset):
		content = self.getContent('https://www.zhihu.com/api/v4/members/' + self.user_id + '/following-topic-contributions?include=data%5B*%5D.topic.introduction&offset=' + offset + '&limit=20')

		topic_name.extend(re.findall('"topic": {"name": "(.*?)"', content))

	def load(self):
		number = self.getNumber()

		for i in range(0, number):
			self.getPage(str(i * 20)) # offset = (page - 1) * 20

	def start(self):
		self.load()
		
		f = open('topic.txt', 'a')

		for i in range(0, len(topic_name)):
			f.write(topic_name[i] + '\n')

		f.close()


# 爬取关注的问题
class GetQue:
	def __init__(self, user_id):
		self.user_id = user_id

	# 抓取页面内容
	def getContent(self, url):
		r = req.get(url)
		content = html_parser.unescape(r.content.decode('unicode-escape').encode('utf-8'))

		return content

	# 获得关注的问题，每页20个，计算出关注的问题列表页数
	def getNumber(self):
		content = self.getContent('https://www.zhihu.com/people/' + self.user_id + '/following')

		number = int(re.findall('<span class="Profile-lightItemName">关注的问题</span>.*?<span class="Profile-lightItemValue">(.*?)</span>', content)[0])

		return number / 20 if number / 20 == 0 else number / 20 + 1 

	def getPage(self, offset):
		content = self.getContent('https://www.zhihu.com/api/v4/members/' + self.user_id + '/following-questions?include=data%5B*%5D.created%2Canswer_count%2Cfollower_count%2Cauthor&offset=' + offset + '&limit=20')

		ques.extend(re.findall('"title": "(.*?)"', content))

	def load(self):
		number = self.getNumber()

		for i in range(0, number):
			self.getPage(str(i * 20)) # offset = (page - 1) * 20

	def start(self):
		self.load()
		
		f = open('ques.txt', 'a')

		for i in range(0, len(ques)):
			f.write(ques[i] + '\n')

		f.close()

# 深度循环遍历关注人，获取关注话题和关注问题
class Get:
	def start(self):
		follows = GetFollow('mnichangxin') # 初始为user_id为自己的
		follows.start()

	    # 遍历两层关注用户
		for i in range(0, len(user_id)):
			follows = GetFollow(user_id[i])
			follows.start()

		# 获得关注用户话题和问题数据
		for i in range(0, len(user_id)):
			topics = GetTopic(user_id[i])
			ques = GetQue(user_id[i])

			topics.start()
			ques.start()