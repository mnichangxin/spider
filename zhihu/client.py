# !/usr/bin/python
# -*-coding: utf-8-*-

import re, time, os, sys, HTMLParser
import req

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8')

# 登录模块
class Login:
	def __init__(self, account, password):
		self.login(account, password)

	# 登录
	def login(self, account, password):
		# POST参数
		post_data = {
	        '_xsrf': self.getXsrf(),
	        'password': password
	    }

		# 手机号登录
		if re.match(r'^1\d{10}$', account):
			post_data['phone_num'] = account
			post_url = 'https://www.zhihu.com/login/phone_num'    
		# 邮箱登录
		else:
			post_data['email'] = account
			post_url = 'https://www.zhihu.com/login/email'

		if not os.path.exists('cookies'):
			try:
				req.post(post_url, data = post_data)
			except:
				del post_data['captcha_type']
				post_data['captcha'] = self.getCaptcha()
				req.post(post_url, data = post_data)
			req.session.cookies.save()
		else:
			req.session.cookies.load()
    
    # 获取验证码
	def getCaptcha(self):
		t = str(int(time.time() * 1000))
		captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
		r = req.get(captcha_url)
    	
		with open('captcha.jpg', 'wb') as f:
			f.write(r.content)
			f.close()

		print u'请在当前目录下找到验证码并输入：'
		captcha = raw_input()

		return captcha 
			
    # 获取_xsrf动态参数
	def getXsrf(self):       
		page = req.get('https://www.zhihu.com')   
		_xsrf = re.findall(r'name="_xsrf" value="(.*?)"', page.text)

		return _xsrf[0]


# People类
class People:
	def __init__(self, id):
		self.url = 'https://www.zhihu.com/people/' + id
		self.content = self._getContent()
		self.url_token = self._getToken()
		self.following_count = self._getFollowing_count()
	
	def _getContent(self):
		content = req.get(self.url).content.replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>')
		return re.findall('data-state="{(.*?)}"', content)[0]

	def _getToken(self):
		return re.findall('"urlToken":"(.*?)",', self.content)[0]
	
	def _getFollowing_count(self):
		return int(re.findall('"followingCount":(.*?),', self.content)[0])

	def getName(self):
		return self.url_token

	def getVote(self):
		return re.findall('"voteupCount":(.*?),', self.content)[0]

	def getThank(self):
		return re.findall('"thankedCount":(.*?),', self.content)[0]

	def getFollowing(self):
		number = self.following_count
		num = number / 20 if number / 20 == 0 else number / 20 + 1
		queue = []
			
		for i in range(num):
			url = 'https://www.zhihu.com/api/v4/members/' + self.url_token + '/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=' + str(i * 20) + '&limit=20'
			content = req.get(url).content
			queue.extend(re.findall('"url_token": "(.*?)"', content))
			time.sleep(2)

		return queue