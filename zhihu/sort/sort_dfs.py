# !/usr/bin/python
# -*-coding: utf-8-*-

# DFS排序

import csv

def sort_dfs(csv_data):

	Gs = {} # 存储有向无环图的集合

	csv_reader = csv.reader(open(csv_data))
	csv_writer = csv.writer(open('predict_result_sort_dfs.csv', 'wb'))

	# 构建有向无环图
	for row in csv_reader:
		index_list = list(eval(row[1]))
		
		if index_list[0] not in Gs:
			Gs[index_list[0]] = {}

		if row[4] == '0':
			index = index_list[2]
			to = index_list[1]
		else: 
			index = index_list[1]
			to = index_list[2]
		if index not in Gs[index_list[0]]:
			Gs[index_list[0]].update({index: [to]})
		else:
			value = Gs[index_list[0]][index]
			if to not in value:
				value.append(to)
				Gs[index_list[0]].update({index: value})


	# 深度优先遍历
	def dfs(G):
		vertices = [] # 存储结点信息
		arcs = [] # 邻接矩阵（存储边信息）
		vexnum = len(G) # 图的结点数
		visited = [] # 用于记录结点是否已被遍历

		res = [] # 存储最终数据的集合

		for i in range(vexnum):
			visited.append(False)
			arc = []
			for j in range(vexnum):
				arc.append(0)
			arcs.append(arc)

		for i in G:
			vertices.append(i)

		for i in G:
			for j in G[i]:
				if j in G:
					arcs[vertices.index(i)][vertices.index(j)] = 1

		# 递归
		def traverse(i):
			visited[i] = True

			for j in range(vexnum):
				if (arcs[i][j] == 1 and visited[j] == False):
					traverse(j)

		for i in range(vexnum):
			if visited[i] == False:
				traverse(i)
		return vertices

	# 写入头信息
	csv_writer.writerow(['que_id', 'ans_id'])

	# 遍历每个图
	for i in Gs:
		vertices = []
		vertices.append(i)
		vertices.extend(dfs(Gs[i]))
		csv_writer.writerow(vertices)
