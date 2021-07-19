# !/usr/bin/python
# -*-coding: utf-8-*-

import os, time, re, logging, xlwt
import req
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

queryActionParams = {
	'ssdm': '',
	'dwmc': '',
	'mldm': 'zyxw',
	'mlmc': '',
	'yjxkdm': '0351',
	'zymc': '',
	'xxfs': '',
	'pageno': 0
}

# # 获取 __RequestVerificationToken
# def getReqVerToken(soup):
# 	return soup.find('input', type='hidden')['value']

# # 更新 queryParams
# def updateQueryParams(reqVerToken):
# 	queryParams['__RequestVerificationToken'] = reqVerToken

# # 预爬取，获得表头和页码数
# def preGet():
# 	# 获取初始的 __RequestVerificationToke
# 	initialUrl = 'http://222.143.21.233:2018/pub/gongshi'
# 	initialRes = req.get(initialUrl)

# 	initialSoup = BeautifulSoup(initialRes.content, 'html.parser')

# 	hiddenInput = initialSoup.find('input', type='hidden')

# 	updateQueryParams(getReqVerToken(initialSoup))

# 	# 获取表头和页码数
# 	url = 'http://222.143.21.233:2018/pub/GongShiSearch'
# 	res = req.post(url, queryParams)

# 	soup = BeautifulSoup(res.content, 'html.parser')

# 	updateQueryParams(getReqVerToken(soup))

# 	tdList = soup.find('table').find('thead').find('tr').find_all('td')

# 	thData = [tdList[i].find('span').string for i in range(len(tdList))]

# 	pageCount = int(re.findall(r'\d+', soup.find('div', class_='divPage').find_all('a')[-1]['href'])[0])

# 	return (thData, pageCount)

# # 爬取每一页的数据
# def getPage(pageNum):
# 	url = 'http://222.143.21.233:2018/pub/GongShiSearch?pageIndex=' + str(pageNum)
# 	res = req.post(url, queryParams)

# 	soup = BeautifulSoup(res.content, 'html.parser')

# 	updateQueryParams(getReqVerToken(soup))

# 	trList = soup.find('table').find('tbody').find_all('tr')

# 	pageData = []

# 	for i in range(len(trList)):
# 		tdList = trList[i].find_all('td')
# 		temp = []
# 		for j in range(len(tdList)):
# 			temp.append(tdList[j].string.replace('\r', '').replace('\n', '').strip())
# 		pageData.append(temp)

# 	return pageData

# # 开始爬取
# def startGet(startPageNum, endPageNum, preData):
# 	thData = preData[0]

# 	f = xlwt.Workbook(encoding = 'utf-8')
# 	table = f.add_sheet('sheet1', cell_overwrite_ok = True)

# 	for i in range(len(thData)): table.write(0, i, thData[i])

# 	dataPool = [[thData]]

# 	for i in range(startPageNum, endPageNum + 1):
# 		if i % 15 == 0:
# 			logging.info('限流，20s 之后继续')
# 			time.sleep(20)

# 		logging.info('开始爬取第 {} 页'.format(i))
# 		data = getPage(i)

# 		dataLength = len(data)
# 		dPLength = len(dataPool)

# 		for j in range(dataLength):
# 			rowLength = len(data[j])
# 			for k in range(rowLength):
# 				table.write(dPLength + j, k, data[j][k])

# 		if i == endPageNum:
# 			if not os.path.exists('./xls'): os.makedirs('./xls')
# 			f.save('./xls/2020河南农机拖拉机类目.xls')
# 			logging.info('爬取完成并存表！')

# 		dataPool.extend(data)

# 	return dataPool

def getPageNo():
	url = 'https://yz.chsi.com.cn/zsml/queryAction.do'
	res = req.post(url, queryActionParams)
	soup = BeautifulSoup(res.content, 'html.parser')
	pageDiv = soup.find('div', class_='zsml-page-box').find('ul', class_='ch-page').find_all('li', class_='lip')[-3]
	pageNo = int(pageDiv.find('a').get_text(separator='', strip=True))
	return pageNo

def getData(startNo, endNo):
	f = xlwt.Workbook(encoding = 'utf-8')
	table = f.add_sheet('sheet1', cell_overwrite_ok = True)
	for i in range(startNo, endNo + 1):
		queryActionParams[pageNo] = i
		url = 'https://yz.chsi.com.cn/zsml/queryAction.do'
		res = req.post(url, queryActionParams)
		soup = BeautifulSoup(res.content, 'html.parser')
		trDiv = soup.find('table', class_='ch-table').find('tbody').find_all('tr')
		for j in range(len(trDiv)):
			tdDiv = trDiv[j].find_all('td')
			schActionUrl = tdDiv[0].find('a').get('href')


if __name__ == '__main__':
	pageNo = getPageNo()
	getData(1, pageNo)
	logging.info('开始爬取......')


