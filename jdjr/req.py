# !/usr/bin/python
# -*-coding: utf-8-*-

import requests

# 构造headers
headers = {
	'Origin': 'https://z.jd.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
	'Referer': 'https://z.jd.com/bigger/search.html',
	'Cookie': 'user-key=f846b5d6-e5b8-45d2-8f26-9124ab2eb3bb; cn=0; ipLocation=%u5317%u4EAC; areaId=13; ipLoc-djd=13-1000-40492-4277.137629911; mt_xid=V2_52007VwMWUlxdW10dSRBVBW4LFlVdX1JSHUgpDAMyARYAWV1OWR4cG0AAZgoQTg4PBl4DGU0LVTIERQdcXFMPL0oYXAN7AxJOXVpDWhhCHVgOZAQiUG1YYlocTh1bBmYAFWJdXlZe; unpl=V2_ZzNtbREFSh12DUVXchgMUWJWEVUSXkYWcl8SUi9NXVYzBRoJclRCFXMURlRnGVgUZwYZX0NcRhFFCHZUehhdBGYBFV5GZxpFKwhFVidSbDVkAyJVcldHFXQNT1N5GVUMZwoaWUVXRBV9CkdkSx5sNVcCIlxyVnNeGwkLVH8ZXQBuBBBdS15DHH0MQVR8GVQHZjMTbUE%3d; TrackID=19zPGamV6-Y074EilWWp5TSNwx2bvJnwlSc4w9g_bbyNs6rk81EXNAruBRqvDpiQPHHxYxTtb8iR9IDWBG16fBy8wb1aGder6KvomchwVUX4; pinId=khm7VKivzyMkqZ8j8dPfCg; pin=hao19960218; unick=mnichangxin; _tp=OjxHtB7gBWG066vjVFz7tg%3D%3D; _pst=hao19960218; __jdv=122270672|www.hao123.com|t_1000003625_hao123mz|tuiguang|bc89242280ae4d29a8426fe7ee0be79e|1510727461638; 3AB9D23F7A4B3C9B=5TO4NNP35UP435GFJSEYDO33G6DKLIN2JPNFJNJAIP7JYD2EFNEXQ3KZPZFLZDVTSIPBMLKBXX2YDRJEOSIX7LIYYI; sec_flag=2d284fcb7f8091395bfb6ad1c2e6a716; sec_addr=7180cac3; recentbrowse=b0638d6b953d47dcafb75743af99068e; _ga=GA1.3.1501191359.1510812848; _gid=GA1.3.830776757.1510812848; _jrda=2; __jda=238784459.1510486318818956161930.-.1510812802.1510823341.6; __jdc=238784459; __jdu=1510486318818956161930',
	'Upgrade-Insecure-Requests': '1'
}
# 建立Session
session = requests.session()

# Get方法
def get(url, data = {}):
	return session.get(url, data = data, headers = headers)

# Post方法
def post(url, data = {}):
	return session.post(url, data = data, headers = headers)

