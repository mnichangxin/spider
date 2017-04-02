# !/usr/bin/python
# -*-coding: utf-8-*-

import re, time, os.path, sys
import req

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8')

# 爬虫登录模块
class SpiderLogin:
	# 登录
	def login(self, account, password, captcha):
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
			res = req.post(post_url, data = post_data)
		except:
			del post_data['captcha_type']
	    	# post_data['captcha'] = self.getCaptcha()
	    	post_data['captcha'] = captcha
       		res = req.post(post_url, data = post_data)

    # 获取验证码
	def getCaptcha(self):
		t = str(int(time.time() * 1000))
		captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
		r = req.get(captcha_url)
    	
		with open('captcha.jpg', 'wb') as f:
			f.write(r.content)
			f.close()
			
    # 获取_xsrf动态参数
	def getXsrf(self):       
		page = req.get('https://www.zhihu.com')   
		_xsrf = re.findall(r'name="_xsrf" value="(.*?)"', page.text)

		return _xsrf[0]