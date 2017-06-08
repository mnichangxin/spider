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


# 爬AI包括子话题下所有的精华答案，把这些答案按对应的问题进行分类，
# 只要一个问题下有十个以上的答案的问题，然后再爬答案的特征： 
# 答案赞同数 答案对应问题的火热度（这个问题下一共有多少个答案） 
# 收藏数 感谢数 评论数 作者的pagerank值（这个有了） 
# 作者的活跃度（爬他最近一个月的动态数目） 作者的粉丝数 作者的赞同数 感谢数 收藏数 （关于答案的属性越多越好）

# 数据集合
topic_id = [] # 父话题及子话题ID
best_answer_id = [] # 精华回答ID
new_best_answer_id = [] # 经过问题筛选后的精华回答ID

# 1. 爬取AI包括子话题下所有的精华答案ID并做去重
def crawlBestAnswers():
	parent_topic = client.topic(19551275) # 父话题ID

	for i in parent_topic.children:
		topic_id.append(int(i.id)) # 子话题ID入队列

	if not os.path.exists('best_answer_id.txt'): # 如果数据存在，直接读取
		f = open('best_answer_id.txt', 'w')

		for i in range(len(topic_id)):
			best_answers = client.topic(topic_id[i]).best_answers # 每个话题下的精华回答
			for j in best_answers:
				j_id = j.id
				if j_id not in best_answer_id:
					best_answer_id.append(j_id) # 精华回答ID入队列
					f.write(str(j_id) + '\n') # 写入文件

		f.close()
	else:
		f = open('best_answer_id.txt', 'r')

		for i in f:
			best_answer_id.append(int(i))

		f.close()


# 2. 爬取答案ID对应的问题（筛选一个问题下有十个以上答案的问题）
def crawQues():
	if not os.path.exists('new_best_answer_id.txt'):
		f = open('new_best_answer_id.txt', 'w')	

		for i in range(len(best_answer_id)):
			que = client.answer(best_answer_id[i]).question
			que_count = que.answer_count # 问题下的回答数
			if que_count >= 10:
				new_best_answer_id.append(best_answer_id[i]) # 筛选后后的精华问题ID
				f.write(str(best_answer_id[i]) + '\n') # 写入文件

		f.close()
	else:
		f = open('new_best_answer_id.txt', 'r')

		for i in f:
			new_best_answer_id.append(int(i))

# 3. 再次爬取并归类存入数据文件
def classify():
	for i in range(len(new_best_answer_id)):
		ans = client.answer(new_best_answer_id[i]) # 答案
		que = ans.question # 问题
		author = ans.author # 答案的作者

		ans_voteup = ans.voteup_count # 赞同数
		ans_thanks = ans.thanks_count # 感谢数
		ans_collection = len(list(ans.collections)) # 收藏数
		ans_comment = ans.comment_count # 评论数

		que_id = que.id # 问题ID 
		que_count = que.answer_count # 问题活跃度，即问题回答数


crawlBestAnswers()
crawQues()