# !/usr/bin/python
# -*-coding: utf-8-*-

from Tkinter import *

import threading, os

# 窗体模块
class Window:
	def __init__(self, spider, account, holds, score):
		self.spider = spider
		self.account = account
		self.holds = holds
		self.score = score
		self.target_type = 0
		self.createWindow()

	def createWindow(self):
		# button事件处理
		def btnClick(event):
			if entry.get() == '':
				label3['text'] = '表单为空！'
				return

			try: 
				if (int(entry.get()) < 10):
					label3['text'] = '不能小于10！'
					return
			except:
				label3['text'] = '不合法字符！'
				return

			if event.widget == button1:
				self.spider.create('call', entry.get(), self.target_type)
			else:
				self.spider.create('put', entry.get(), self.target_type)

			btnState()

		# 按钮恢复可用状态
		def btnShow():
			button1['state'] = NORMAL
			button1['bg'] = '#F0F0F0'
			button2['state'] = NORMAL
			button2['bg'] = '#F0F0F0'
			label3['text'] = '可以投注'

		# 结束进程
		def stop():
			btnShow()
			dur_timer.cancel()
			state_timer.cancel()

		# 按钮的状态判断
		def btnState():
			dur_time = self.spider.getTime();
			
			if (dur_time):
				button1['state'] = DISABLED
				button1['bg'] = '#ccc'
				button2['state'] = DISABLED
				button2['bg'] = '#ccc'
				
				state_timer = threading.Timer(0, getTimeState)
				state_timer.start()

				global dur_timer
				dur_timer = threading.Timer(dur_time * 60, stop)
				dur_timer.start()

		# 定时获取按钮的可用时间
		def getTimeState():
			dur_time = self.spider.getTime()

			label3['text'] = '投注进行中，约' + str(dur_time) + '分钟后可继续投注'

			global state_timer
			state_timer = threading.Timer(30, getTimeState)
			state_timer.start()
			
		# radio事件处理
		def radioClick(event):
			if event.widget == radio1:
				self.target_type = 0 
			else:
				self.target_type = 1

		# 定时刷新数据
		def shuffle():
			try:
				label1['text'] = self.spider.getPage()[0]
				label2['text'] = self.spider.getPage()[1]
			except:
				pass

			global timer
			timer = threading.Timer(60, shuffle)
			timer.start()

		# 获取进程PID
		def getProcess(process_name):
			pids = psutil.pids()

			for pid in pids:
				p = psutil.Process(pid)

				if p.name() == process_name:
					print pid
					return pid

		# 外围窗体
		root = Tk()

		root.title(self.account)
		root.geometry('280x300')
		root.resizable(width = False, height = False)

		# 顶部Label
		frame1 = Frame(root, padx = 10, pady = 10)

		color = 'green'

		if int(self.score) < 0:
			color = 'red'
		
		label1 = Label(frame1, relief = 'sunken', text = self.holds, font = 'Helvetica 12 bold', width = 15, height = 3)
		label2 = Label(frame1, relief = 'sunken', fg = color, text = self.score, font = 'Helvetica 12 bold', width = 15, height = 3)

		label1.pack(side = LEFT)
		label2.pack(side = RIGHT)
		frame1.pack()

		# 中间Label
		frame2 = Frame(root, padx = 10, pady = 10)

		label3 = Label(frame2, relief = 'sunken', text = '登录成功！', font = 'Helvetica 10 bold', width = 40, height = 5)

		label3.pack()
		frame2.pack()

		# 表单
		frame3 = Frame(root, padx = 10, pady = 10)

		var = IntVar()

		radio1 = Radiobutton(frame3, variable = var, text = 'XAU', font = 'Helvetica 10 bold', value = 1, state = 'active')
		radio2 = Radiobutton(frame3, variable = var, text = 'EUR', font = 'Helvetica 10 bold', value = 2)
		entry = Entry(frame3)

		radio1.bind('<Button-1>', radioClick)
		radio2.bind('<Button-1>', radioClick)

		radio1.select()

		radio1.pack(side = LEFT)
		radio2.pack(side = LEFT)
		entry.pack()
		frame3.pack()

		# 按钮
		frame4 = Frame(root, width = 40, padx = 10, pady = 10)

		button1 = Button(frame4, text = '涨', font = 'Helvetica 10 bold', bg = '#F0F0F0', width = 10, height = 2)
		button2 = Button(frame4, text = '跌', font = 'Helvetica 10 bold', bg = '#F0F0F0', width = 10, height = 2)

		button1.bind('<Button-1>', btnClick)
		button2.bind('<Button-1>', btnClick)

		button1.pack(side = LEFT)
		button2.pack(side = RIGHT)
		frame4.pack()

		timer = threading.Timer(5, shuffle)
		timer.start()

		btnState()

		root.mainloop()

		try:
			dur_timer.cancel()
			state_timer.cancel()
		except:
			pass
			
		# 杀死进程
		os.popen('taskkill -f -t -im python.exe')