import socket
socket_list = [socket.socket() for s in range(10)]
for s in socket_list:
	s.setblocking(False)
	try:
		s.connect(('www.baidu.com', 80))
	except:
		pass
while socket_list:
	for s in socket_list:
		try:
			s.send('GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n'.encode('ascii'))
			socket_list.remove(s)
		except:
			pass