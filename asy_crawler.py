import socket 
import asyncio

class Crawler(object):
	def __init__(self):
		self.content = []
		self.text = b''
		self.sock = socket.socket()
	async def get_connect(self):
		self.sock.setblocking(False)
		try:
			self.sock.connect(('www.baidu.com', 80))
		except:
			pass
		await my_send(self)
		self.text = await fetch(self)

	async def my_send(self):
		try:
			ret = self.sock.send('GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n'.encode('ascii'))
			yield ret
		except Exception as e:
			raise e

	async def fetch(self):
		
		chunk = yield get_content(self)
		while chunk:
			self.content.append(chunk)
			chunk = yield get_content(self)
		yield b''.join(self.content)

	def get_content(self):
		try:
			chunk = self.sock.recv(4096)
			yield chunk
		except:
			pass

crawler_list = [Crawler() for x in range(10)]
task = []
for t in crawler_list:
	task.append(t.get_connect())
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(crawler_list))
loop.close()