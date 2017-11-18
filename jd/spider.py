# !/usr/bin/python
# -*-coding: utf-8-*-

import re, xlwt
import req
from bs4 import BeautifulSoup

# 爬取页码数
def getPage():
	post_data = {
		'status': 2,
		'sort': 'zhtj',
		'categoryId': '',
		'parentCategoryId': '',
		'sceneEnd': '',
		'productEnd': '',
		'keyword': '',
		'page': 1
	}
	res = req.post('https://z.jd.com/bigger/search.html', post_data)
	soup = BeautifulSoup(res.content, 'html.parser')
	page_num = int(re.findall(r'pagination\((.*),', soup.select('html')[0].text)[0])

	return page_num

# 爬取商品详情链接
def getUrls(page_num):
	post_data = {
		'status': 2,
		'sort': 'zhtj',
		'categoryId': '',
		'parentCategoryId': '',
		'sceneEnd': '',
		'productEnd': '',
		'keyword': '',
		'page': 1
	}

	urls = []

	for i in range(page_num):
		post_data['page'] = i + 1

		res = req.post('https://z.jd.com/bigger/search.html', post_data)
		soup = BeautifulSoup(res.content, 'html.parser')
		links = soup.select('.link-pic')
		
		for i in range(len(links)):
			urls.append(links[i]['href'])

	return urls

def getShop(url):
	url = 'https://z.jd.com' + url

	print(url + '...')

	res = req.get(url)
	soup = BeautifulSoup(res.content, 'html.parser')
	
	shop_name = soup.select('.project-introduce .p-title')[0].text # 商品名称
	get_num = soup.select('.p-num')[0].text # 已筹到金额
	target_num = soup.select('.f_red')[1].text # 筹款目标金额
	support_num = soup.select('.p-progress .fr')[0].text.split(u'名')[0] # 支持者数量

	return [shop_name, url, get_num, target_num, support_num]

def save(data):
	f = xlwt.Workbook(encoding = 'utf-8')
	# 写入表头
	table = f.add_sheet('sheet1', cell_overwrite_ok = True)
	table.write(0, 0, '商品名称')
	table.write(0, 1, '商品链接')
	table.write(0, 2, '已筹到金额')
	table.write(0, 3, '筹款目标金额')
	table.write(0, 4, '支持者数量')

	# 逐个写入
	for i in range(0, len(data)):
		table.write(i + 1, 0, data[i][0])
		table.write(i + 1, 1, data[i][1])
		table.write(i + 1, 2, data[i][2])
		table.write(i + 1, 3, data[i][3])
		table.write(i + 1, 4, data[i][4])
	f.save('data.xls')

def main():
	urls = getUrls(getPage())
	datas = []

	for i in range(len(urls)):
		data = getShop(urls[i])
		datas.append(data)

	save(datas)

main()
