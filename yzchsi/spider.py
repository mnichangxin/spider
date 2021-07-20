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
	'yjxkdm': '0352',
	'zymc': '',
	'xxfs': '',
	'pageno': 0
}

def getPageNo():
	url = 'https://yz.chsi.com.cn/zsml/queryAction.do'
	res = req.post(url, queryActionParams)
	soup = BeautifulSoup(res.content, 'html.parser')
	hasLipBox = soup.find('div', class_='zsml-page-box').find('ul', class_='ch-page').find('li', class_='lip_input-box')
	allPageDiv = soup.find('div', class_='zsml-page-box').find('ul', class_='ch-page').find_all('li', class_='lip')
	endPageDiv = allPageDiv[-3] if hasLipBox else allPageDiv[-2]
	pageNo = int(endPageDiv.find('a').get_text(separator='', strip=True))
	return pageNo

def getSchData(schActionUrl):
	res = req.get(schActionUrl)
	soup = BeautifulSoup(res.content, 'html.parser')
	trDiv = soup.find('table', class_='ch-table').find('tbody').find_all('tr')
	schData = []
	for i in range(len(trDiv)):
			trData = []
			tdDiv = trDiv[i].find_all('td')
			for j in range(0, len(tdDiv)):
				text = tdDiv[j].get_text(separator=' ', strip=True)
				if text == '':
					scriptDiv = tdDiv[j].find('script')
					if scriptDiv:
						pattern = re.compile('cutString\(\'(.*?)\'')
						findText = pattern.findall(scriptDiv.contents[0])
						if findText: text = findText[0]
				trData.append(text)
			schData.append(trData)
	return schData

def getData(startNo, endNo):
	allData = []
	for i in range(startNo, endNo + 1):
		logging.info('开始爬取第 {} 页...'.format(i))
		queryActionParams['pageno'] = i
		url = 'https://yz.chsi.com.cn/zsml/queryAction.do'
		res = req.post(url, queryActionParams)
		soup = BeautifulSoup(res.content, 'html.parser')
		trDiv = soup.find('table', class_='ch-table').find('tbody').find_all('tr')
		for j in range(len(trDiv)):
			trData = []
			tdDiv = trDiv[j].find_all('td')
			schUrl = 'https://yz.chsi.com.cn' + tdDiv[0].find('a').get('href')
			for k in range(0, len(tdDiv)):
				text = tdDiv[k].get_text(separator=' ', strip=True)
				text = text.replace('\ue664', '是')
				trData.append(text)
			schData = getSchData(schUrl)
			newTrData = []
			for o in range(len(schData)):
				newTrDataI = []
				newTrDataI.extend(trData)
				newTrDataI.extend(schData[o])
				newTrData.append(newTrDataI)
			allData.extend(newTrData)
	return allData

def saveToXls(allData):
	if not os.path.exists('./xls'): os.makedirs('./xls')
	f = xlwt.Workbook(encoding = 'utf-8')
	table = f.add_sheet('sheet1', cell_overwrite_ok = True)
	for i in range(len(allData)):
		for j in range(len(allData[i])):
			table.write(i, j, allData[i][j])
	f.save('./xls/硕士专业目录-专业学位-社会工作.xls')
	logging.info('爬取完成并存表...')

if __name__ == '__main__':
	logging.info('开始爬取......')
	pageNo = getPageNo()
	allData = getData(1, pageNo)
	saveToXls(allData)


