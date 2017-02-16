#!/usr/bin/python
#-*-coding:utf-8-*-

# 模拟登录济大教管系统，爬取个人成绩

import urllib, urllib2, cookielib, re, codecs, sys

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8')

# 爬虫类
class Spider:
	cookie = cookielib.MozillaCookieJar('cookie.txt') # 对象实例
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie)) # 装载实例
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'} # 模拟浏览器
		
	# 登录
	def login(self, username, password):
		postdata = urllib.urlencode({"yhm": username, "mm": password, "yzm": ""}) # 构造POST对象
		url = 'http://jwgl6.ujn.edu.cn/jwglxt/xtgl/login_login.html' # 请求登录的地址

		req = urllib2.Request(url, postdata, Spider.headers)
		res = Spider.opener.open(req)

		Spider.cookie.save(ignore_discard = True, ignore_expires = True) # 存储cookie到本地

	# 登录后获取成绩信息
	def getInfo(self, xnm, xqm):
		tuples = {'1': '3', '2': '12', '3': '16'}

		syear = xnm[0:4]
		term = tuples[xqm]

		postdata = urllib.urlencode({"xnm": syear, "xqm": term, "_search": "false", "nd": "1486564855577", "queryModel.showCount": "30", "queryModel.currentPage": "1", "queryModel.sortName": "", "queryModel.sortOrder": "asc", "time": "0"})

		url = 'http://jwgl6.ujn.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query' # 查询成绩的URL
		req = urllib2.Request(url, postdata, Spider.headers)
		res = Spider.opener.open(req)
		content = res.read()

		# 构造字段容器
		xn = [] # 学年
		xq = [] # 学期
		xh = [] # 学号
		xm = [] # 姓名
		xb = [] # 性别
		xy = [] # 学院
		zy = [] # 专业
		nj = [] # 年级
		bj = [] # 班级
		kkbm = [] # 开课部门
		kch = [] # 课程代码
		kcm = [] # 课程名称
		xf = [] # 学分
		cj = [] # 成绩
		jd = [] # 绩点
		kclb = [] # 课程类别

		# 正则匹配
		xn.extend(re.findall('"xnmmc":"(.*?)"', content))
		xq.extend(re.findall('"xqmmc":"(.*?)"', content))
		xh.extend(re.findall('"xh":"(.*?)"', content))
		xm.extend(re.findall('"xm":"(.*?)"', content))
		xb.extend(re.findall('"xb":"(.*?)"', content))
		xy.extend(re.findall('"jgmc":"(.*?)"', content))
		zy.extend(re.findall('"zymc":"(.*?)"', content))
		nj.extend(re.findall('"njmc":"(.*?)"', content))
		bj.extend(re.findall('"bj":"(.*?)"', content))
		kkbm.extend(re.findall('"kkbmmc":"(.*?)"', content))
		kch.extend(re.findall('"kch":"(.*?)"', content))
		kcm.extend(re.findall('"kcmc":"(.*?)"', content))
		xf.extend(re.findall('"xf":"(.*?)"', content))
		cj.extend(re.findall('"cj":"(.*?)"', content))
		jd.extend(re.findall('"jd":"(.*?)"', content))
		kclb.extend(re.findall('"kclbmc":"(.*?)"', content))

		# 存储为表格文件
		f = open(xnm + '-' + xqm + '.csv', 'w')
		
		f.write(codecs.BOM_UTF8) # 防止csv文件乱码

		f.write(','.join(('学年', '学期', '学号', '姓名', '性别', '学院', '专业', '年级', '班级', '开课部门', '课程代码', '课程名称', '学分', '成绩', '绩点', '课程类别')) + '\n') # 写入首行标题

		for i in range(0, len(xm)):
			f.write(','.join((xn[i], xq[i], xh[i], xm[i], xb[i], xy[i], zy[i], nj[i], bj[i], kkbm[i], kch[i], kcm[i], xf[i], cj[i], jd[i], kclb[i])) + '\n')
			print u'正在进行......'
		
		f.close()
		print u'完毕！'

# 程序主入口
print u'''
	--------------------------------------
	  模拟登录济大教管查询成绩 By 李昶昕
	--------------------------------------
'''

print u'输入学号：'
username = str(raw_input())
print u'输入密码：'
password = str(raw_input()) 
print u'输入查询的学年（格式如2016-2017）：'
xn = str(raw_input())
print u'输入查询的学期（格式如1）：'
xq = str(raw_input())

mySpider = Spider()
mySpider.login(username, password)
mySpider.getInfo(xn, xq)