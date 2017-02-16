# !/usr/bin/python
# -*-coding: utf-8-*-

import req, HTMLParser

class GetPage:
	def getContent(self):
		html_parser = HTMLParser.HTMLParser()

		r = req.get('https://www.zhihu.com/people/mnichangxin/following')
		
		f = open('data.txt', 'w')
		f.write(html_parser.unescape(r.content))
		f.close()