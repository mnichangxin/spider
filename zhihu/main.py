# !/usr/bin/python
# -*-coding: utf-8-*-

from __future__ import unicode_literals, print_function
from zhihu_oauth import ZhihuClient, ActType
from multiprocessing import Pool
import os, sys, codecs, time, datetime

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

# 数据集合
topic_id = [] # 父话题及子话题ID
best_answer_id = [] # 精华回答ID
new_best_answer_id = [] # 经过问题筛选后的精华回答ID

# 获取当前时间戳
day_ago = (datetime.datetime.now() - datetime.timedelta(days = 30))
timestamp = int(time.mktime(day_ago.timetuple()))

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
	file = open('breakpoint.txt', 'r') # 断点续爬记录文件
	start = int(file.read())
	file.close()

	f = open('data.csv', 'a') # 追加模式，支持断点续爬
	
	if start == 0:
		f.write(codecs.BOM_UTF8) # 防止csv文件乱码
		f.write(','.join(('ans_id', 'ans_voteup', 'ans_thanks', 'ans_collection', 'ans_comment', 'que_id', 'que_activities', 'author_id', 'author_collected', 'author_follower', 'author_following', 'author_thanked', 'author_voteup')) + '\n') # 写入头部

	for i in range(start, len(new_best_answer_id)):
		try: 
			ans = client.answer(new_best_answer_id[i]) # 答案
			que = ans.question # 问题
			author = ans.author # 答案的作者

			ans_id = new_best_answer_id[i]
			ans_voteup = ans.voteup_count # 赞同数
			ans_thanks = ans.thanks_count # 感谢数
			ans_collection = len(list(ans.collections)) # 收藏数
			ans_comment = ans.comment_count # 评论数

			que_id = que.id # 问题ID 
			que_activities = que.answer_count # 问题活跃度（问题回答数）

			author_id = author.id # 作者ID
			author_collected = author.collected_count # 被收藏数
			author_follower = author.follower_count # 粉丝数]''
			author_following = author.following_count # 关注数
			author_thanked = author.thanked_count # 感谢数
			author_voteup = author.voteup_count # 赞同数

			activities = author.activities 
			author_activities = 0 # 作者活跃度（一个月的动态数目）
			for j in activities:
				if j.created_time > timestamp:
					author_activities += 1
				else:
					break

			f.write(','.join((str(ans_id), str(ans_voteup), str(ans_thanks), str(ans_collection), str(ans_comment), str(que_id), str(que_activities), author_id, str(author_collected), str(author_follower), str(author_following), str(author_thanked), str(author_voteup))) + '\n') # 写入数据
		except:
			pass

		file = open('breakpoint.txt', 'w')
		file.write(str(i + 1))
		file.close()

	f.close()

# 主函数
def main():
	print('爬取中......')
	crawlBestAnswers()
	crawQues()
	classify()

main()