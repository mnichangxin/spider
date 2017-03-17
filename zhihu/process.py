import multiprocessing

def process(num):
	print 'Process:', num

if __name__ == '__main__':
	for i in range(5):
		p = multiprocessing.Process(target = process, args = (i,))
		p.start()

