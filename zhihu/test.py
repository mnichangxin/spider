# !/usr/bin/python
# -*-coding: utf-8-*-

from multiprocessing import Pool
import os, sys, codecs, csv, time
import client

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8') 

FILE1 = 'best_answers.csv' # 用户ID文件
FILE2 = 'voteup.csv' # 用户赞感谢文件
FILE3 = 'followings.csv' # 用户关注文件

# 登录
client.Login('13256120647', '12345678910.')

# 进程调用函数
def process(user_id):	
	try:
		people = client.People(user_id)

		name = people.getName() # 用户昵称
		voteup = people.getVote() # 赞同数
		thanked = people.getThank() # 感谢数
		# followings = people.getFollowing() # 关注人

		print name
	except:
		pass

	return (name, voteup, thanked)

# 进程回调函数
def callback(user):
	f2 = open(FILE2, 'a')

	try: 
		f2.write(','.join((user[0], user[1], user[2])) + '\n')
	except:
		pass
	
	f2.close() 

	# f3 = open(FILE3, 'a')
	
	# try: 
	# 	name = user[0]
	# 	following_name = user[1]

	# 	for i in range(len(following_name)):
	# 		f3.write(','.join((name, following_name[i])) + '\n')
	# except:
	# 	pass

	# f3.close()


# 进程创建函数
def main():
	pool = Pool(2) # 创建进程池 

	# 读取文件
	f1 = open(FILE1, 'r')
	content = f1.readlines() # 逐行读为列表
	f1.close()

	# 创建赞同感谢表和关注表
	f2 = open(FILE2, 'a')
	f2.write(codecs.BOM_UTF8) # 防止csv 文件乱码
	f2.write(','.join(('UserName', 'VoteUp', 'Thanked')) + '\n')
	f2.close()

	# 创建关注表
	# f3 = open(FILE3, 'a')
	# f3.write(codecs.BOM_UTF8) # 防止csv文件乱码
	# f3.write(','.join(('UserName', 'FollowingName')) + '\n')
	# f3.close() 

	print(u'获取中......')

	# 创建多进程
	for i in range(1, len(content)):
		pool.apply_async(process, (content[i].strip('\n'), ), callback = callback) 

	pool.close()
	pool.join()

	print(u'完毕！')

if __name__ == '__main__':
	main()