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
	text = soup.select('.f_red')[1].text
	target_num = text if u'￥' in text else u'∞' # 筹款目标金额
	support_num = soup.select('.p-progress .fr')[0].text.split(u'名')[0] # 支持者数量

	date = soup.select('.f_red')[0].text.strip() # 筹款日期
	progress_num = soup.select('.tab-bubble')[0].text # 项目进展

	system_id = re.search(r'\d+', url).group(0)
	
	get_topic = 'https://sq.jr.jd.com/topic/count?key=1000&systemId=' + system_id + '&callback=jQuery18305593621608794495_1511077188596&_=1511077190427'
	topic_content = req.get(get_topic).content
	topic_num = re.findall('"count":(.*?),', topic_content)[0] #话题

	get_fp = 'https://sq.jr.jd.com/cm/getCount?key=1000&systemId=' + system_id + '&pin=&callback=jQuery18305593621608794495_1511077188596&temp=0.4715818729939495&_=1511077190951'
	fp_content = req.get(get_fp).content
	focus_num = re.findall('"focus":(.*?),', fp_content)[0] # 关注
	prais_num = re.findall('"praise":(.*?),', fp_content)[0] # 赞
	
	return [shop_name, url, get_num, target_num, support_num, date, focus_num, prais_num, progress_num, topic_num]

def save(data):
	f = xlwt.Workbook(encoding = 'utf-8')
	# 写入表头
	table = f.add_sheet('sheet1', cell_overwrite_ok = True)
	table.write(0, 0, '商品名称')
	table.write(0, 1, '商品链接')
	table.write(0, 2, '已筹到金额')
	table.write(0, 3, '筹款目标金额')
	table.write(0, 4, '支持者数量')

	table.write(0, 5, '筹款日期')
	table.write(0, 6, '关注')
	table.write(0, 7, '赞')
	table.write(0, 8, '项目进展')
	table.write(0, 9, '话题')
	
	# 逐个写入
	for i in range(0, len(data)):
		table.write(i + 1, 0, data[i][0])
		table.write(i + 1, 1, data[i][1])
		table.write(i + 1, 2, data[i][2])
		table.write(i + 1, 3, data[i][3])
		table.write(i + 1, 4, data[i][4])

		table.write(i + 1, 5, data[i][5])
		table.write(i + 1, 6, data[i][6])
		table.write(i + 1, 7, data[i][7])
		table.write(i + 1, 8, data[i][8])
		table.write(i + 1, 9, data[i][9])
	f.save('data.xls')

def main():
	urls = getUrls(getPage())
	datas = []

	for i in range(len(urls)):
		data = getShop(urls[i])
		datas.append(data)

	save(datas)

main()
