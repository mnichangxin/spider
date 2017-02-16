# !/usr/bin/python
# -*-coding: utf-8-*-

import req

class GetPage:
	def getContent(self):
		r = req.get('https://www.zhihu.com/people/mnichangxin')
		print r.content.decode('utf-8', 'ignore').encode('gbk', 'ignore')