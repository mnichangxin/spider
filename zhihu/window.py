# !/usr/bin/python
# -*-coding: utf-8-*-

from Tkinter import *

import threading, os

# 窗体模块
class Window:
	def createWindow(self):
		# 按钮事件处理
		def btnClick(event):
			if entry1.get() == '' or entry2.get() == '' or entry3.get() == '':
				label4['text'] = '表单为空！'
				return 
			else:
				label4['text'] = ''

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
		entry3 = Entry(frame3)

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

		button = Button(frame5, text = '登录', width = 10, height = 2)

		button.bind('<Button-1>', btnClick)

		button.pack()
		frame5.pack()

		# 启动
		root.mainloop()


window = Window()
window.createWindow()