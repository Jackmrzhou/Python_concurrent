import socket
import asyncio
loop = asyncio.get_event_loop()
data = []
get = 'GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n'.encode('ascii')
async def Crawl(addr):
	sock = socket.socket()
	sock.setblocking(False)
	await loop.sock_connect(sock, addr)
	await loop.sock_sendall(sock, get)
	chunk = await loop.sock_recv(sock, 4096)
	data.append(chunk)
	sock.close()
	print('done')

tasks = [Crawl(('www.baidu.com', 80)) for x in range(40)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()