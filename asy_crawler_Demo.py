import socket
from selectors import *
selector = DefaultSelector()
urls = ['www.baidu.com' for x in range(20)]
class Crawler(object):
	def __init__(self):
		self.sock_list = []
		self.resp = []
		self.count = 0

	def get_connected(self,key, mask):
		selector.unregister(key.fileobj)
		get = 'GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n'.encode('ascii')
		key.fileobj.send(get)
		selector.register(key.fileobj, EVENT_READ, self.read_resp)

	def crawl(self):
		self.sock_list = [socket.socket() for x in range(len(urls))]
		self.count = len(urls)
		for sock,url in zip(self.sock_list,urls):
			addr = (url, 80)
			sock.setblocking(False)
			try:
				sock.connect(addr)
			except BlockingIOError:
				pass
			selector.register(sock, EVENT_WRITE, self.get_connected)

	def read_resp(self, key, mask):
		chunk = key.fileobj.recv(4096)
		if chunk:
			self.resp.append(chunk)
		else:
			self.count -= 1
			selector.unregister(key.fileobj)

c = Crawler()
c.crawl()
while c.count:
	events = selector.select()
	for event_key, event_mask in events:
		callback = event_key.data
		callback(event_key, event_mask)