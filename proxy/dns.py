# !/usr/bin/python
# -*-coding: utf-8-*-

import os, sys, re, json, socket, shutil, winshell
from ftplib import FTP

# DNS修改模块
class Dns:
	# 读取配置文件
	def getConf(self):
		f = open(r'config.json')

		s = json.load(f)

		f.close()
		
		return s

	# 重写hosts文件
	def rewriteHosts(self, hosts):
		f = open(r'C:\Windows\System32\drivers\etc\hosts', 'w')

		f.write(hosts)

		f.close()

	# 映射
	def mapping(self):
		s = self.getConf()

		hosts = ''

		# 遍历构造映射
		for key in s:
			ip_info = socket.getaddrinfo(key, None)[0][4][0]

			for i in range(0, len(s[key])):
				hosts += ip_info + ' ' + s[key][i] + '\n'

		self.rewriteHosts(hosts)

	# 创建到开机启动项
	def startup(self):    
		title = 'dns.exe' 
		fname = os.path.splitext('dns.exe')[0]  
		winshell.CreateShortcut(Path = os.path.join(winshell.startup(), fname + '.lnk'), Target = './dns.exe', Description = title)

class FtpDown:
	def ftpDown(self):
		# FTP地址
		FTP_SERVER = '221.229.162.155'
		PORT = '511'
		USER = 'a88088325'
		PWD = '789942F2AF351b'

		ftp = FTP()

		# 设置调试级别
		ftp.set_debuglevel(2) 

		# 连接登录
		ftp.connect(FTP_SERVER, PORT)
		ftp.login(USER, PWD)

		# 选择操作目录
		bufsize = 1024
		remote_path = 'web/config.json'
		local_path = './config.json'
		fp = open(local_path, 'wb')

		# 以写模式在本地打开文件
		ftp.retrbinary('RETR %s' % remote_path, fp.write, bufsize)

		# 接收服务器上的文件并写入本地文件
		ftp.set_debuglevel(0)
		fp.close()
		ftp.quit()

# 主入口
dns = Dns()
ftp = FtpDown()

ftp.ftpDown()

dns.mapping()
dns.startup()

 