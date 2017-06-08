# !/usr/bin/python
# -*-coding: utf-8-*-

from __future__ import unicode_literals, print_function
from zhihu_oauth import ZhihuClient, ActType
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


# que = client.question(27731353)

ans = client.answer(38027489)

ans_voteup = ans.voteup_count # 赞同数
ans_thanks = ans.thanks_count # 感谢数
ans_collection = len(list(ans.collections)) # 收藏数
ans_comment = ans.comment_count # 评论数

author = ans.author

# print(author.id) # 作者ID
# print(author.collected_count) # 被收藏数
# print(author.follower_count) # 粉丝数
# # print(author.following_count) # 关注数
# print(author.thanked_count) # 感谢数
# print(author.voteup_count) # 赞同数

activities = author.activities

for i in activities:
	print(i.created_time)

# print(str(ans_voteup) + '\n')
# print(str(ans_thanks) + '\n')
# print(str(ans_collection) + '\n')
# print(str(ans_comment) + '\n')