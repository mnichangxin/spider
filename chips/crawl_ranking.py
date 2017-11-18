# !/usr/bin/python
# -*-coding: utf-8-*-

import json, xlwt
import req

# 爬取方法
def crawl():
	# POST参数
	post_data = {
		'bookNum': 'ROW_2_COL_1',
		'curPage': 1,
		'pageSize': 10000
	}
	# 爬取链接
	res = req.post('https://www.chips.ltd/products/super_book_query', post_data)
	data_json = json.loads(res.text)

	return data_json['results']

# 数据导入文件
def save(data):
	f = xlwt.Workbook(encoding = 'utf-8')
	# 写入表头
	table = f.add_sheet('sheet1', cell_overwrite_ok = True)
	table.write(0, 0, '排行')
	table.write(0, 1, '用户昵称')
	table.write(0, 2, 'CPS余额')
	table.write(0, 3, 'BTC余额')
	table.write(0, 4, 'LTC余额')
	table.write(0, 5, 'ETH余额')
	# 逐个写入
	for i in range(0, len(data)):
		table.write(i + 1, 0, i + 1)
		table.write(i + 1, 1, data[i]['userName'])
		table.write(i + 1, 2, data[i]['cps'])
		table.write(i + 1, 3, data[i]['btc'])
		table.write(i + 1, 4, data[i]['ltc'])
		table.write(i + 1, 5, data[i]['eth'])
	f.save('ranking.xls')

# 主方法
def main():
	save(crawl())

# 执行
main()