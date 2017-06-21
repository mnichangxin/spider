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

que_id = [50824266,50050401,55753169,52768740,43304486,38387206,29938038,50643209,54048527,51783509,23299373,29160943,45096702,23418797,51788894,54377817,23945902,48038533,51788678,54217494,54461787,40436801,51879275,34843901,42887126,21802548,28926356,50806552,52740496,52102239,39477444,57052990,38656861,55926939,54680196,53613635,46575222,58778536,36890053,54680317,56169136,50788193,49446556,48038437,51890140,36884389,36692190,57456575,32271883,47741800,54379931,24506695,47045674,54857314,52878619,52531244,26342064,55576523,26851944,54647152,59475884,48034036,54854263,38570005,41835465,46940666,35982249,49272693,22195254,40910893,54425022,20197709,21317756,59464081,37792432,27609802,50742400,31169617,20210846,59319528,29048520,23909308,58056204,42090397,58802415,29073750,59026879,39375325,52712742,53306075,56691747,54857138,54853112,38537425,51817797,23954186,39241682,57676697,56192655,54862155]
answer_id = []

# 获取当前时间戳
day_ago = (datetime.datetime.now() - datetime.timedelta(days = 30))
timestamp = int(time.mktime(day_ago.timetuple()))

def crawAnswers(): 
	if not os.path.exists('answer_id.txt'): # 如果数据存在，直接读取
		f = open('answer_id.txt', 'w')

		for i in range(len(que_id)):
			que = client.question(que_id[i])
			ans = que.answers

			# k = 0

			for j in ans:
				# if k < 20:
				answer_id.append(j.id)
				f.write(str(j.id) + '\n')
				# k += 1

		f.close()
	else:
		f = open('answer_id.txt', 'r')

		for i in f:
			answer_id.append(int(i))

		f.close()

def classify(): 
	file = open('breakpoint.txt', 'r') # 断点续爬记录文件
	start = int(file.read())
	file.close()

	f = open('data.csv', 'a') # 追加模式，支持断点续爬
	
	if start == 0:
		f.write(codecs.BOM_UTF8) # 防止csv文件乱码
		f.write(','.join(('ans_id', 'ans_voteup', 'ans_thanks', 'ans_collection', 'ans_comment', 'que_id', 'que_activities', 'author_id', 'author_collected', 'author_follower', 'author_following', 'author_thanked', 'author_voteup', 'author_activities')) + '\n') # 写入头部

	for i in range(start, len(answer_id)):
		try: 
			ans = client.answer(answer_id[i]) # 答案
			que = ans.question # 问题
			author = ans.author # 答案的作者

			ans_id = answer_id[i]
			ans_voteup = ans.voteup_count # 赞同数
			ans_thanks = ans.thanks_count # 感谢数
			ans_collection = len(list(ans.collections)) # 收藏数
			ans_comment = ans.comment_count # 评论数

			que_id = que.id # 问题ID 
			que_activities = que.answer_count # 问题活跃度（问题回答数）

			author_id = author.id # 作者ID
			author_collected = author.collected_count # 被收藏数
			author_follower = author.follower_count # 粉丝数
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

			f.write(','.join((str(ans_id), str(ans_voteup), str(ans_thanks), str(ans_collection), str(ans_comment), str(que_id), str(que_activities), author_id, str(author_collected), str(author_follower), str(author_following), str(author_thanked), str(author_voteup), str(author_activities))) + '\n') # 写入数据
		except:
			pass

		file = open('breakpoint.txt', 'w')
		file.write(str(i + 1))
		file.close()

	f.close()

# 主函数
def main():
	print('爬取中......')
	crawAnswers()
	classify()

main()