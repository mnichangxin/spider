# !/usr/bin/python
# -*-coding: utf-8-*-

import os, time, re, logging, xlwt
import req
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

queryActionParams = {
	'ssdm': '',
	'dwmc': '',
	'mldm': '03',
	'mlmc': '',
	'yjxkdm': '0301',
	'zymc': '',
	'xxfs': '',
	'pageno': 0
}

def saveToXls(allData):
	if not os.path.exists('./xls'): os.makedirs('./xls')
	f = xlwt.Workbook(encoding = 'utf-8')
	table = f.add_sheet('sheet1', cell_overwrite_ok = True)
	for i in range(len(allData)):
		for j in range(len(allData[i])):
			table.write(i, j, allData[i][j])
	f.save('./xls/硕士专业目录-专业学位-社会工作.xls')
	logging.info('爬取完成并存表...')

def getKskmData(kskmUrl):
	res = req.get(kskmUrl)
	soup = BeautifulSoup(res.content, 'html.parser')
	trDiv = soup.select('tbody.zsml-res-items tr')
	kskmData = []
	for i in range(len(trDiv)):
		tdDiv = trDiv[i].find_all('td')
		for j in range(len(tdDiv)):
			text = tdDiv[j].contents[0].replace(' ', '').replace('\r', '').replace('\n', '')
			if i == 0: kskmData.append(text)
			elif i > 0 and text != kskmData[j]: kskmData[j] = kskmData[j] + ' 或 ' + text
	return kskmData

def getSchData(schUrl):
	res = req.get(schUrl)
	soup = BeautifulSoup(res.content, 'html.parser')
	trDiv = soup.find('table', class_='ch-table').find('tbody').find_all('tr')
	schData = []
	for i in range(len(trDiv)):
			tdDiv = trDiv[i].find_all('td')
			kskmUrl = 'https://yz.chsi.com.cn' + tdDiv[7].find('a').get('href')
			kskmData = getKskmData(kskmUrl)
			trData = []
			for j in range(len(tdDiv)):
				text = tdDiv[j].get_text(separator=' ', strip=True)
				if text == '':
					scriptDiv = tdDiv[j].find('script')
					if scriptDiv:
						pattern = re.compile('cutString\(\'(.*?)\'')
						findText = pattern.findall(scriptDiv.contents[0])
						if findText: text = findText[0]
				trData.append(text)
			trData.extend(kskmData)
			schData.append(trData)
	return schData

def getSchPageNo(schUrl):
	res = req.get(schUrl)
	soup = BeautifulSoup(res.content, 'html.parser')
	return parsePageNoBySoup(soup)

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
			schData = []
			schEndNo = getSchPageNo(schUrl)
			for m in range(1, schEndNo + 1): schData.extend(getSchData(schUrl + '&pageno=' + str(m)))
			newTrData = []
			for o in range(len(schData)):
				newTrDataI = []
				newTrDataI.extend(trData)
				newTrDataI.extend(schData[o])
				newTrData.append(newTrDataI)
			allData.extend(newTrData)
	return allData

def parsePageNoBySoup(soup):
	hasLipBox = soup.find('div', class_='zsml-page-box').find('ul', class_='ch-page').find('li', class_='lip_input-box')
	allPageDiv = soup.find('div', class_='zsml-page-box').find('ul', class_='ch-page').find_all('li', class_='lip')
	endPageDiv = allPageDiv[-3] if hasLipBox else allPageDiv[-2]
	pageNo = int(endPageDiv.find('a').get_text(separator='', strip=True))
	return pageNo

def getPageNo():
	url = 'https://yz.chsi.com.cn/zsml/queryAction.do'
	res = req.post(url, queryActionParams)
	soup = BeautifulSoup(res.content, 'html.parser')
	return parsePageNoBySoup(soup)

if __name__ == '__main__':
	logging.info('开始爬取......')
	pageNo = getPageNo()
	allData = getData(1, pageNo)
	saveToXls(allData)


