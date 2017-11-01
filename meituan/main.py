# !/usr/bin/python
# -*-coding: utf-8-*-

import sys, re, csv, codecs
import req

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8')

# 获取城市
def getCity():
	city = [] # 城市列表

	res = req.get('http://www.meituan.com/index/changecity/initiative').content
	city.extend(re.findall('<a gaevent="changecity/build" class="isonline" href="(.*?)">.*?</a>', res))

	return city

# 获取页码
def getPage(city):
	page = {} # 页码数

	for i in city:
		num = 0

		res = req.get(i + '/category/jiankangliren/all/page1').content
		page_num = re.findall('<li  data-page=(.*?)>', res)

		if (len(page_num) != 0):
			num = int(page_num[-1:][0])

		print i
		page[i] = num

	return page

# 获取店铺ID
def getId(page):
	id = [] # 所有店铺ID

	for i in page:
		for j in range(page[i]):
			res = req.get(i + '/category/jiankangliren/all/page' + str(j)).content
			try:
				id.extend(re.findall(r'\\"poiidList\\":\[(.*?)\]', res)[0].split(','))
			except:
				pass
		print id 	
	return id

id = getId(getPage(getCity()))

f = open('id.txt', 'w')
for i in id:
	f.write(i + '\n')
f.close()