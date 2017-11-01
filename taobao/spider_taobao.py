#!/usr/bin/python
#-*-coding:utf-8-*-

# 爬取 taobao 商品数据

import re
import requests
from pandas import *
from collections import OrderedDict

def getDetails(startpage, endpage):
	#如果需要爬取具体的商品详情，页数过多可能会出现异常，此函数可以用来控制一次爬取的页数
	url_head = 'https://s.taobao.com/search?q=母婴&s='  
	#这是淘宝搜索列表的url前面的相同部分，q=''代表搜索的关键词，s=''代表第几页，s=0为第1页s=44为第二页，以此类推
 
	url_list = [url_head + str(i * 44) for i in range(startpage - 1, endpage)]  #生成需要爬取的商品列表url
 
	#定义存储商品列表数据数据的列表
	nid_list = []
	raw_title_list = []
	view_price_list = []
	view_sales_list = []
	item_loc_list = []
	img_src_list = []
	shop_name_list = []

	for url in url_list:
		resp = requests.get(url)

		print(resp.url)
		
		nid = re.findall(pattern = '"nid":"(.*?)"', string = resp.text)  #商品id,唯一，可以此跳转到其商品详情页面，然后进行其他信息的抓取
		raw_title = re.findall(pattern = '"raw_title":"(.*?)"', string = resp.text)  #商品名称
		view_price = re.findall(pattern = '"view_price":"(.*?)"', string = resp.text)  #商品价格
		view_sales = re.findall(pattern = '"view_sales":"(.*?)"', string = resp.text)  #商品销量
		item_loc = re.findall(pattern = '"item_loc":"(.*?)"', string = resp.text)  #发货地址
 		img_src = re.findall(pattern = '"pic_url":"(//.*?)"', string = resp.text) # 图片链接
 		# shop_name = re.findall(pattern = '"nick":"(.*?)"', string = resp.text) # 店铺名称

		#逐个存储
		nid_list.extend(nid)
		raw_title_list.extend(raw_title)
		view_price_list.extend(view_price)
		view_sales_list.extend(view_sales)
		item_loc_list.extend(item_loc)
 		img_src_list.extend(img_src)
 		# shop_name_list.extend(shop_name)

	#生成数据框
	dt = {'商品id': nid_list, '商品名称': raw_title_list, '商品价格': view_price_list, '商品销量': view_sales_list, '地址': item_loc_list, '展示图': img_src_list}

	df = DataFrame(dt)  #根据字典生成数据框

	#写入Excel
	writer1 = ExcelWriter("taobao_details.xlsx")  #新建一个空白Excel工作簿
	df.to_excel(writer1, "Sheet1")  #将df写入Sheet1工作表
	writer1.save()

getDetails(1, 2)
