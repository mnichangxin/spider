# !/usr/bin/python
# -*-coding: utf-8-*-

from Tkinter import *

import threading, os

# 窗体模块
class Window:
	def __init__(self, spider_login, spider_get):
		self.spider_login = spider_login
		self.spider_get = spider_get
		self.createWindow()

	def createWindow(self):
		# 按钮1事件处理
		def btn1Click(event):
			if entry3['state'] == NORMAL and entry3.get() != '':
				try:
					self.spider_login.login(entry1.get(), entry2.get(), entry3.get())
				except:
					label4['text'] = '登录失败！'
					return
				
				label4['text'] = '登录成功！'
				button1['state'] = DISABLED
				button2['state'] = NORMAL
 				return

			if entry1.get() == '' or entry2.get() == '':
				label4['text'] = '表单为空！'
				return 
			
			if entry3['state'] != NORMAL:
				try:
					self.spider_login.getCaptcha()

					label4['text'] = '请找到 captcha.jpg 并输入验证码'
					entry3['state'] = NORMAL
				except:
					label4['text'] = '登录失败！'
					return
		
		# 按钮2事件处理
		def btn2Click(event):	
			pass

		# 外围窗体
		root = Tk()

		root.title('爬取知乎')
		root.geometry('280x280')
		root.resizable(width = False, height = False)

		# 表单1
		frame1 = Frame(root, padx = 10, pady = 10)

		label1 = Label(frame1, text = '账户：')
		entry1 = Entry(frame1)

		label1.pack(side = LEFT)
		entry1.pack(side = RIGHT)
		frame1.pack()

		# 表单2
		frame2 = Frame(root, padx = 10, pady = 10)

		label2 = Label(frame2, text = '密码：')
		entry2 = Entry(frame2)

		label2.pack(side = LEFT)
		entry2.pack(side = RIGHT)
		frame2.pack()

		# 表单3
		frame3 = Frame(root, padx = 10, pady = 10)

		label3 = Label(frame3, text = '验证码：')
		entry3 = Entry(frame3, state = DISABLED)

		label3.pack(side = LEFT)
		entry3.pack(side = RIGHT)
		frame3.pack()

		# 消息Label
		frame4 = Frame(root, padx = 10, pady = 10)

		label4 = Label(frame4, relief = 'sunken', width = 30, height = 3)

		label4.pack()
		frame4.pack()

		# 按钮
		frame5 = Frame(root, padx = 10, pady = 10)

		button1 = Button(frame5, text = '登录', width = 10, height = 2)
		button2 = Button(frame5, text = '抓取', width = 10, height = 2, state = DISABLED)

		button1.bind('<Button-1>', btn1Click)
		button2.bind('<Button-2>', btn2Click)

		button1.pack(side = LEFT)
		button2.pack(side = RIGHT)
		frame5.pack()

		# 启动
		root.mainloop()