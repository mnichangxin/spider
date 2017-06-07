# !/usr/bin/python
# -*-coding: utf-8-*-

from __future__ import unicode_literals, print_function
from zhihu_oauth import ZhihuClient
from multiprocessing import Pool
import os, sys, codecs

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8') 

# 登录
TOKEN_FILE = 'token.pkl'

client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
	client.load_token(TOKEN_FILE)
else:
	client.login_in_terminal()
	client.save_token(TOKEN_FILE)


# 爬AI包括子话题下所有的精华答案，把这些答案按对应的问题进行分类，只要一个问题下有十个以上的答案的问题，然后再爬答案的特征： 答案赞同数 答案对应问题的火热度（这个问题下一共有多少个答案） 收藏数 感谢数 评论数 作者的pagerank值（这个有了） 作者的活跃度（爬他最近一个月的动态数目） 作者的粉丝数 作者的赞同数 感谢数 收藏数 （关于答案的苏醒越多越好）

# 1. 爬AI包括子话题下所有的精华答案ID并做去重
def crawlBestAnswers():
	topic_id = [] # 父话题及子话题ID
	best_answer_id = [] # 精华回答ID

	parent_topic = client.topic(19551275) # 父话题ID

	for i in parent_topic.children:
		topic_id.append(int(i.id)) # 子话题ID入队列

	f = open('best_answer_id.txt', 'w');

	for i in range(len(topic_id)):
		best_answers = client.topic(topic_id[i]).best_answers # 每个话题下的精华回答
		for j in best_answers:
			j_id = j.id
			if j_id not in best_answer_id:
				best_answer_id.append(j_id) # 精华回答ID入队列
				f.write(str(j_id) + '\n') # 写入文件

	f.close()

crawlBestAnswers()