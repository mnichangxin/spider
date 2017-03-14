# !/usr/bin/python
# -*-coding: utf-8-*-

import sys, codecs
import jieba
import jieba.analyse

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8')

s = ''

f = open('topic.txt')

for line in f:
	s += line

f.close()

f = open('count.csv', 'a')

f.write(codecs.BOM_UTF8) # 防止csv文件乱码

for x, w in jieba.analyse.extract_tags(s, topK = 100, withWeight = True):
	f.write(','.join((x, str(w))) + '\n')

f.close()