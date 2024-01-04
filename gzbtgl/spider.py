# !/usr/bin/python
# -*-coding: utf-8-*-

import os, time, re, logging, xlwt
import req
from bs4 import BeautifulSoup

reqPublicPath = 'http://nyt.hubei.gov.cn/gzbtgl/Bt21To23/pub'
savePath = './xls/2023湖北农机轮式拖拉机类目.xls'
queryParams = {
	'__RequestVerificationToken': '',
	'YearNum': 2023,
	'JiJuLeiXing': '轮式拖拉机',
	'JiJuLeiXingCode': 200101,
	'FactoryName': '',
	'BusinessName': '',
	'ChuCBH': '',
	'StartGJRiQi': '',
	'EndGJRiQi': '',
	'StateValue': '',
	'StateName': '',
	'areaName': '',
	'AreaCode': '',
	'qy': '',
	'n': '',
	't': ''
}

logging.basicConfig(level=logging.INFO)

# 获取 __RequestVerificationToken
def getReqVerToken(soup):
	return soup.find('input', type='hidden')['value']

# 获取 t
def getReqT(soup):
	findScript = soup.find('script', text=re.compile('var t ='))
	tTextSearch = re.search(r'var t = \'(.*)\'', findScript.string)
	t = tTextSearch.groups()[0]
	return t

# 更新 queryParams
def updateQueryParams(reqVerToken, reqT):
	queryParams['__RequestVerificationToken'] = reqVerToken
	queryParams['t'] = reqT

# 预爬取，获得表头和页码数
def preGet():
	# 获取初始的 __RequestVerificationToke
	initialUrl = '{}/gongshi'.format(reqPublicPath)
	initialRes = req.get(initialUrl)

	initialSoup = BeautifulSoup(initialRes.content, 'html.parser')

	hiddenInput = initialSoup.find('input', type='hidden')

	updateQueryParams(getReqVerToken(initialSoup), getReqT(initialSoup))

	# 获取表头和页码数
	url = '{}/GongShiSearch'.format(reqPublicPath)
	res = req.post(url, queryParams)

	soup = BeautifulSoup(res.content, 'html.parser')

	updateQueryParams(getReqVerToken(soup), getReqT(initialSoup))

	tdList = soup.find('table').find('thead').find('tr').find_all('td')

	thData = [tdList[i].find('span').string for i in range(len(tdList))]

	pageCount = int(re.findall(r'pageIndex=(\d+)', soup.find('div', class_='divPage').find_all('a')[-1]['href'])[0])

	return (thData, pageCount)

# 爬取每一页的数据
def getPage(pageNum):
	url = '{}/GongShiSearch?pageIndex='.format(reqPublicPath) + str(pageNum)
	res = req.post(url, queryParams)

	soup = BeautifulSoup(res.content, 'html.parser')

	updateQueryParams(getReqVerToken(soup), getReqT(soup))

	trList = soup.find('table').find('tbody').find_all('tr')

	pageData = []

	for i in range(len(trList)):
		tdList = trList[i].find_all('td')
		temp = []
		for j in range(len(tdList)):
			temp.append(tdList[j].string.replace('\r', '').replace('\n', '').strip())
		pageData.append(temp)

	return pageData

# 开始爬取
def startGet(startPageNum, endPageNum, preData):
	thData = preData[0]

	f = xlwt.Workbook(encoding = 'utf-8')
	table = f.add_sheet('sheet1', cell_overwrite_ok = True)

	for i in range(len(thData)): table.write(0, i, thData[i])

	dataPool = [[thData]]

	for i in range(startPageNum, endPageNum + 1):
		if i % 15 == 0:
			logging.info('限流，40s 之后继续')
			time.sleep(40)

		logging.info('开始爬取第 {} 页'.format(i))
		data = getPage(i)

		dataLength = len(data)
		dPLength = len(dataPool)

		for j in range(dataLength):
			rowLength = len(data[j])
			for k in range(rowLength):
				table.write(dPLength + j, k, data[j][k])

		if i == endPageNum:
			if not os.path.exists('./xls'): os.makedirs('./xls')
			f.save('{}'.format(savePath))
			logging.info('爬取完成并存表！')

		dataPool.extend(data)

	return dataPool

if __name__ == '__main__':
	preData = preGet()
	pageCount = preData[1]
	startGet(1, pageCount, preData)
