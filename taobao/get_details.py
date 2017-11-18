#!/usr/bin/python
#-*-coding:utf-8-*-

import sys
import re
import requests
from pandas import *
from collections import OrderedDict
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

def getTaoBaoDetails(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text,"html.parser")
	 
	dd = soup.select(".tb-shop-rate dd") #获取描述、服务、物流的数字信息，该信息存放在一个列表，需要使用正则表达式提取
	dd_value = []
	
	if len(dd) > 0:
		try:
		    for d in range(0, 3):
		        dd_value.append(re.search(pattern = r'[\s]*([0-9]\.[0-9])[\s]*',string = dd[d].text).group(1))
		except IndexError as err:
		    print(res.url)

	#下面的语句获取属性列表
	attrs = soup.select(".attributes-list li")
	attrs_name = []
	attrs_value = []
	for attr in attrs:
		attrs_name.append(re.search(r'(.*?):[\s]*(.*)', attr.text).group(1))
		attrs_value.append(re.search(r'(.*?):[\s]*(.*)', attr.text).group(2))
	allattrs = OrderedDict() #存放该产品详情页面所具有的属性
	for k in range(0, len(attrs_name)):
		allattrs[attrs_name[k]] = attrs_value[k]

	info = OrderedDict()  #存放该商品所具有的全部信息

	#下面三条语句获取描述、服务、物流的评分信息
	if len(dd_value) > 0:
		info['描述'] = dd_value[0]
		info['服务'] = dd_value[1]
		info['物流'] = dd_value[2]
	else:
		info['描述'] = 'NA'
		info['服务'] = 'NA'
		info['物流'] = 'NA'

	#下面的语句用来判断该商品具有哪些属性，如果具有该属性，将属性值插入有序字典，否则，该属性值为空
	#款式
	if '款式' in attrs_name:
		info['款式'] = allattrs['款式'.decode('utf-8')]
	else:
		info['款式'] = 'NA'
	#品牌
	if '品牌' in attrs_name:
		info['品牌'] = allattrs['品牌'.decode('utf-8')]
	else:
		info['品牌'] = 'NA'
	#颜色分类
	if '颜色分类' in attrs_name:
		info['颜色分类'] = allattrs['颜色分类'.decode('utf-8')]
	else:
		info['颜色分类'] = 'NA'
	#大小
	if '大小' in attrs_name:
		info['大小'] = allattrs['大小'.decode('utf-8')]
	else:
		info['大小'] = 'NA'
	#产地
	if '产地' in attrs_name:
		info['产地'] = allattrs['产地'.decode('utf-8')]
	else:
		info['产地'] = 'NA'
	#妈咪包分类
	if '妈咪包分类' in attrs_name:
		info['妈咪包分类'] = allattrs['妈咪包分类'.decode('utf-8')]
	else:
		info['妈咪包分类'] = 'NA'

	return info

def getTmallDetails(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "html.parser")
 
	dd = soup.select(".shop-rate ul li") #获取描述、服务、物流的数字信息，该信息存放在一个列表，需要使用正则表达式提取
	dd_value = []
	
	if len(dd) > 0:
		for d in dd:
			dd_value.append(re.search(r'([0-9][.][0-9])', d.text).group())

	#下面的语句获取属性列表
	attrs = soup.select(".#J_AttrUL li")
	attrs_name = []
	attrs_value = []
	for attr in attrs:
		attrs_name.append(re.search(r'(.*?):[\s]*(.*)', attr.text).group(1))
		attrs_value.append(re.search(r'(.*?):[\s]*(.*)', attr.text).group(2))
	allattrs = OrderedDict() #存放该产品详情页面所具有的属性
	for k in range(0, len(attrs_name)):
		allattrs[attrs_name[k]] = attrs_value[k]

	info = OrderedDict()  #存放该商品所具有的全部信息

	#下面三条语句获取描述、服务、物流的评分信息
	if len(dd_value) > 0:
		info['描述'] = dd_value[0]
		info['服务'] = dd_value[1]
		info['物流'] = dd_value[2]
	else:
		info['描述'] = 'NA'
		info['服务'] = 'NA'
		info['物流'] = 'NA'

	#下面的语句用来判断该商品具有哪些属性，如果具有该属性，将属性值插入有序字典，否则，该属性值为空
	#款式
	if '款式' in attrs_name:
		info['款式'] = allattrs['款式'.decode('utf-8')]
	else:
		info['款式'] = 'NA'
	#品牌
	if '品牌' in attrs_name:
		info['品牌'] = allattrs['品牌'.decode('utf-8')]
	else:
		info['品牌'] = 'NA'
	#颜色分类
	if '颜色分类' in attrs_name:
		info['颜色分类'] = allattrs['颜色分类'.decode('utf-8')]
	else:
		info['颜色分类'] = 'NA'
	#大小
	if '大小' in attrs_name:
		info['大小'] = allattrs['大小'.decode('utf-8')]
	else:
		info['大小'] = 'NA'
	#产地
	if '产地' in attrs_name:
		info['产地'] = allattrs['产地'.decode('utf-8')]
	else:
		info['产地'] = 'NA'
	#妈咪包分类
	if '妈咪包分类' in attrs_name:
		info['妈咪包分类'] = allattrs['妈咪包分类'.decode('utf-8')]
	else:
		info['妈咪包分类'] = 'NA'

	return info


f = open('ids.txt', 'r')
ids = []
for line in f:
	ids.append(line.strip('\n'))
f.close()

df = DataFrame()
for id in ids:
	url = 'https://item.taobao.com/item.htm?id=' + id
	print(url + '...')
	res = requests.get(url)
	if not isnull(re.search('tmall', res.url)):
		details = getTmallDetails(url)
	else:
		details = getTaoBaoDetails(url)
	details['商品id'] = id
	df = df.append(details, ignore_index = True)
writer = ExcelWriter('shop_details.xlsx')
df.to_excel(writer, 'Sheet1')
writer.save()