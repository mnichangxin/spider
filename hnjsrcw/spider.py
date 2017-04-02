# !/usr/bin/python
# -*-coding: utf-8-*-

import re, sys, time
import req

# 防止Unicode报错
reload(sys)
sys.setdefaultencoding('utf-8')

# 登录模块
class Spider:
	def __init__(self): 
		self.login_url = 'http://user.hnjsrcw.com/Space/Login.aspx'
	
	# 登录
	def login(self):
		# 参数
		data = {
			'__EVENTTARGET': '',
			'__EVENTARGUMENT': '',
			'__VIEWSTATE': '/wEPDwUKLTg3NjE5MTg5MmQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFCWJ0bl9Mb2dpbpvlbV/vb8pesvh7/XTIOzq6RI/U',
			'__EVENTVALIDATION': '/wEWBQKS9MK8BgLQro20BQLm3aHbCgKPnaPRBQKDkOvcBCWgcNYJTfTHObIDOuARFuLsZXxa',
			'tbx_UserID': '430725199402107270',
			'tbx_UserName': '文贤',
			'tbx_Password': '111111',
			'btn_Login.x': 78,
			'btn_Login.y': 18
		} 

		req.post(self.login_url, data = data)
	
		req.get('http://train.hnjsrcw.com/Space/Default.aspx?id=430725199402107270&type=CE2017&sign=2BB6CDCC6548E33078BE45D50995B798')	
		# req.get('http://train.hnjsrcw.com/space/sta_edu/EduFrame.aspx')
		# req.get('http://train.hnjsrcw.com/space/sta_edu/GoToEduClass.aspx')

		req.get('http://train.hnjsrcw.com/space/mytrain/WarePlay.aspx?wareId=189')

		post_data = {
			'studyInfoId': '1827479',
			'pos': 90566,
			'totaltime': 144,
			'medialength': 0,
			'actionType': 'f'
		}

		f = open('data.html', 'w')

		# f.write(req.get('http://train.hnjsrcw.com/space/mytrain/ClassCourseList.aspx').content)
		f.write(req.post('http://train.hnjsrcw.com/space/mytrain/RecordStudyInfo.ashx', data = post_data).content)
		
		f.close()


	# 获得用户信息
	def getAccount(self):
		return (user_id, user_name, password)

spider = Spider()

# print u'user_id: '
# user_id = raw_input()

# # print u'user_name: '
# user_name = u'黄树平'

# print u'password: '
# password = raw_input()

spider.login()