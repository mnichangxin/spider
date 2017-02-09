# !/usr/bin/python
# -*-coding: utf-8-*-

import requests, cookielib, re, time, os.path, sys

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8')

# 爬虫类
class Spider:
	# 构造headers
	headers = {
		'Host': 'www.zhihu.com',
		'Referer': 'https://www.zhihu.com/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
	}

	# 建立持久连接
	session = requests.session()
	# session.cookies = cookielib.LWPCookieJar(filename = 'cookies')
	# session.cookies.load(ignore_discard = True)

	# 登录
	def login(self, account, password):
		# POST参数
		post_data = {
	        '_xsrf': self.getXsrf(),
	        'password': password,
	        'captcha_type': 'cn'
	    }

		# 手机号登录
		if re.match(r'^1\d{10}$', account):
			post_data['phone_num'] = account
			post_url = 'https://www.zhihu.com/login/phone_num'    
		# 邮箱登录
		else:
			post_data['email'] = account
			post_url = 'https://www.zhihu.com/login/email'

	    # 尝试登录，如果出现验证码，则输入验证码登录
		try: 
			res = Spider.session.post(post_url, data = post_data, headers = Spider.headers)
		except:
			del post_data['captcha_type']
	    	post_data['captcha'] = self.getCaptcha()
       		res = Spider.session.post(post_url, data = post_data, headers = Spider.headers)

		# r = Spider.session.get('https://www.zhihu.com/people/mnichangxin', headers = Spider.headers)

    # 获取验证码
	def getCaptcha(self):
		t = str(int(time.time() * 1000))
		captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
		r = Spider.session.get(captcha_url, headers = Spider.headers)
    	
		with open('captcha.jpg', 'wb') as f:
			f.write(r.content)
			f.close()
    	
		print u'请到 %s 目录找到 captcha.jpg 输入验证码：' % os.path.abspath('captcha.jpg')
   
		captcha = str(raw_input())
    	
		return captcha

    # 获取_xsrf动态参数
	def getXsrf(self):       
		page = Spider.session.get('https://www.zhihu.com', headers = Spider.headers)   
		_xsrf = re.findall(r'name="_xsrf" value="(.*?)"', page.text)

		return _xsrf[0]

# 程序主入口
print u'''
	--------------------------------------
	       模拟登录知乎 By 李昶昕
	--------------------------------------
'''

print u'请输入知乎账号（手机号或邮箱）：'
account = str(raw_input())
print u'请输入密码：'
password = str(raw_input())

spider = Spider()
spider.login(account, password)
