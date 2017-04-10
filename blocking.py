import socket
socket_list=[socket.socket() for x in range(10)]
for s in socket_list:
	s.connect(('www.baidu.com', 80))
for s in socket_list:
	s.close()