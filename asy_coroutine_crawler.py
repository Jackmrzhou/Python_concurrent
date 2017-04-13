import socket
from selectors import *
class Future(object):
	def __init__(self):
		self.result = None
		self._callback = []

	def add_callback(self, func):
		self._callback.append(func)

	def set_result(self, result):
		self.result = result
		for func in self._callback:
			func(self)
	def __iter__(self):
		yield self
		return self.result

class Crawler(object):
	def __init__(self):
		self.url = 'www.baidu.com'
		self.sock = socket.socket()
		self.sock.setblocking(False)
		self.resp = b''

	def fetch(self):
		f = Future()
		try:
			self.sock.connect((self.url, 80))
		except:
			pass

		def connected():
			f.set_result(None)

		selector.register(self.sock, EVENT_WRITE, connected)
		yield from f
		print('connected.')
		
		self.send_data()
		selector.unregister(self.sock)
		chunk = yield from self.recv_data()
		self.resp += chunk
		print(self.resp)
		global stop, count
		count -= 1
		if count <= 0:
			stop = True

	def send_data(self):
		get = 'GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n'.encode('ascii')
		self.sock.send(get)

	def recv_data(self):
		f = Future()
		
		def read_ready():
			f.set_result(self.sock.recv(4096))
		selector.register(self.sock, EVENT_READ, read_ready)
		chunk = yield from f
		selector.unregister(self.sock)
		return chunk

class Task(object):
	def __init__(self,coro):
		self.coro = coro
		f = Future()
		f.set_result(None)
		self.next_step(f)

	def next_step(self,future):
		try:
			next_future = self.coro.send(future.result)
		except StopIteration:
			return
		next_future.add_callback(self.next_step)

stop = False
selector = DefaultSelector()
count = 10

for i in range(10):
	task = Task(Crawler().fetch())
while not stop:
	events = selector.select()
	for event_key , event_mask in events:
		call = event_key.data
		call()
