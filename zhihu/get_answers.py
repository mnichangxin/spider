# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 17:04:59 2017

@author: mnichangxin
"""

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

# 进程调用函数
def Process(best_answer):	
	f = open('best_answers.csv', 'a')
	try:
		f.write(','.join((best_answer.author.id, )) + '\n')
	except:
		pass
	f.close()

# 进程创建函数
def main():
	pool = Pool(10) # 创建进程池

	topics = [19550901] # 话题列表
	best_answerss = [] # 最佳回答者迭代器列表

	for i in range(len(topics)):
		best_answerss.append(client.topic(topics[i]).best_answers)

	print(u'正在爬取......')

	# 写入文件
	f = open('best_answers.csv', 'a')    
	f.write(codecs.BOM_UTF8) # 防止csv文件乱码
	f.write(','.join(('UserId',)) + '\n')
	f.close()

	for i in range(len(best_answerss)):
		for j in best_answerss[i]:
			pool.apply_async(Process, (j, ))  

	pool.close()
	pool.join() 

	print(u'爬取完毕！')

if __name__ == '__main__':
	main()