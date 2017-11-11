# !/usr/bin/python
# -*-coding: utf-8-*-

import json, xlwt
import req

# 爬取方法
def crawl():
	# POST参数
	post_data = {
		'bookNum': 'ROW_1_COL_1',
		'curPage': 1,
		'pageSize': 10000,
		'serverID': '',
		'userName': ''
	}
	# 爬取链接
	res = req.post('https://www.chips.ltd/products/super_book_query', post_data)
	data_json= json.loads(res.text)

	return data_json['results']

# 数据导入文件
def save(data):
	f = xlwt.Workbook(encoding = 'utf-8')
	# 写入表头
	table = f.add_sheet('sheet1', cell_overwrite_ok = True)
	table.write(0, 0, 'UID')
	table.write(0, 1, '所属银行镜像')
	table.write(0, 2, '用户昵称')
	table.write(0, 3, '用户手机号')
	table.write(0, 4, '信用积分')
	table.write(0, 5, 'VIP')
	table.write(0, 6, '实名认证')
	# 逐个写入
	for i in range(0, len(data)):
		table.write(i + 1, 0, data[i]['userID'])
		table.write(i + 1, 1, 'www.chips.ltd' if data[i]['serverID'] == 0 else 'www.cpschain.org')
		table.write(i + 1, 2, data[i]['userName'])
		table.write(i + 1, 3, data[i]['userPhone'])
		table.write(i + 1, 4, data[i]['creditPoint'])
		table.write(i + 1, 5, data[i]['vip'])
		table.write(i + 1, 6, '未申请认证' if data[i]['realStatus'] == 0 else '已完成审核')
	f.save('users.xls')

# 主方法
def main():
	save(crawl())

# 执行
main()