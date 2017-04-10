import threading, queue,time
def print_num():
	while True:
		num = q.get()
		if num is None:
			print('Quit')
			break
		else:
			print('get {}'.format(num))
def produce():
	for i in range(5):
		q.put(i)
		time.sleep(1)
	q.put(None)#send message to stop customer thread 
q = queue.Queue()
threads = []
p = threading.Thread(target = produce)#producer thread
threads.append(p)
g = threading.Thread(target = print_num)#customer thread
threads.append(g)
for t in threads:
	t.start()
for t in threads:#block main thread 
	t.join()