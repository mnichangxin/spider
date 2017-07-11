# !/usr/bin/python
# -*-coding: utf-8-*-

import xml.etree.ElementTree as ET
import hashlib
import sys, csv, codecs

import req

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8')

# md5加密
def md5(str):
	m = hashlib.md5()
	m.update(str)
	return m.hexdigest()

# 爬取函数
def crawl(USERNAME, PASSWORD):
	username = USERNAME
	password = md5(md5(PASSWORD)) # 密码
	
	bhd = ['8', 'Z'] # 搜索类型（'8' 或 'Z'）

	contno = [] # 用于存储保单号的列表

	# 存储每个保单号
	for i in bhd:
		search_tpl = '''
			<?xml version="1.0" encoding="UTF-8"?>
			<TransData>
				<BaseInfo>
					<TransType></TransType>
					<TransCode>M0403</TransCode>
					<TransClient>MOBILE</TransClient>
					<SubTransCode>07072343361517</SubTransCode>
					<UserName>''' + username + '''</UserName>
					<UserNameMd5></UserNameMd5>
					<Password>''' + password + '''§</Password>
					<TransDate></TransDate>
					<TransTime></TransTime>
					<TransSeq></TransSeq>
					<Operator>4</Operator>
					<PageFlag></PageFlag>
					<TotalRowNum></TotalRowNum>
					<RowNumStart></RowNumStart>
					<PageRowNum></PageRowNum>
					<ResultCode></ResultCode>
					<ResultMsg></ResultMsg>
					<OrderFlag></OrderFlag>
					<OrderField></OrderField>
					<Key>7d192353725b8c2e3f67e83f2f6b2e3b</Key></BaseInfo>
					<InputData><PARAMLIST><BDH>''' + i + '''</BDH><FLAG>0</FLAG></PARAMLIST></InputData>
			</TransData>
		'''

		res = req.post('http://219.143.202.141/SyncDataService/NCISAMService.aspx', search_tpl).content
		tree = ET.fromstring(res)

		for elem in tree.iter(tag = 'ITEM'):
			contno.append(elem[0].text)
			print elem[0].text

	file = open(username + '.csv', 'wb')
	file.write(codecs.BOM_UTF8) # 防止csv文件乱码
	csv_writer = csv.writer(file) # 打开文件
	csv_writer.writerow(['投保人', '保单号', '主险险种', '主险保额', '保全保费', '交费期限', '已交次数', '交费对应日', '性别', '手机', '住址', '证件号码', '出生日期', '账户', '开户行'])

	# 遍历每个保单号的信息
	for i in contno:
		contno_tpl = '''
			<?xml version="1.0" encoding="UTF-8"?>
			<TransData>
				<BaseInfo>
					<TransType></TransType>
					<TransCode>0422</TransCode>
					<TransClient>MOBILE</TransClient>
					<SubTransCode>07072343361517</SubTransCode>
					<UserName>''' + username + '''</UserName>
					<UserNameMd5></UserNameMd5>
					<Password>''' + password + '''§</Password>
					<TransDate></TransDate>
					<TransTime></TransTime>
					<TransSeq></TransSeq>
					<Operator>4</Operator>
					<PageFlag></PageFlag>
					<TotalRowNum></TotalRowNum>
					<RowNumStart></RowNumStart>
					<PageRowNum></PageRowNum>
					<ResultCode></ResultCode>
					<ResultMsg></ResultMsg>
					<OrderFlag></OrderFlag>
					<OrderField></OrderField>
					<Key>d07f882ed3f46f88b5ff60e42cdd7b21</Key></BaseInfo>
					<InputData><PARAMLIST><CONTNO>''' + i + '''</CONTNO></PARAMLIST></InputData>
			</TransData>
		'''

		res = req.post('http://219.143.202.141/SyncDataService/NCISAMService.aspx', contno_tpl).content
		tree = ET.fromstring(res)

		def reader():	
			row = []

			for elem in tree.iter(tag = 'BQ'):
				if elem.text == '-1':
					return
				bq = elem[0]
				row.extend([bq[2].text, bq[0].text, bq[4].text, bq[6].text, bq[7].text, bq[9].text, bq[10].text, bq[8].text])
			for elem in tree.iter(tag = 'TBR'):
				if elem.text == '-1':
					row = []
					return
				tbr = elem[0]
				row.extend([tbr[4].text, tbr[5].text, tbr[9].text, "'" + (tbr[14].text), tbr[15].text])
			for elem in tree.iter(tag = 'ZH'):
				if elem.text == '-1':
					row = []
					return
				zh = elem[0]
				row.extend([zh[4].text, zh[3].text])

			print row

			if (len(row) != 0):
				csv_writer.writerow(row)

		reader()


# 开始爬取		
USERNAME = '37526062' # 用户名
PASSWORD = '37526062' # 密码

crawl(USERNAME, PASSWORD)