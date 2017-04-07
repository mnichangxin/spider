# !/usr/bin/python
# -*-coding: utf-8-*-

import codecs

answers_name = ['1', '2', '3', '4', '5', '6']

f = open('data.csv', 'a')

f.write(codecs.BOM_UTF8) # 防止csv文件乱码
f.write(','.join(('问题ID', '回答者和评论者ID')) + '\n') # 写入首行标题

for n in range(0, len(answers_name)):
	f.write(','.join((answers_name[n],)) + ',')

f.write(','.join(('')) + '\n')

f.write(','.join(('7')))

f.close()