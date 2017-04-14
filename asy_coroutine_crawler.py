import socket
from selectors import *
class Future(object):
    def __init__(self):
        self._callback = None
        self.result = None

    def _call(self):
        self._callback(self)

    def set_callback(self, future):
        self._callback = future

    def __iter__(self):
        yield self
        return self.result

def connect(sock, addr):
    f = Future()
    try:
        sock.connect(addr)
    except BlockingIOError:
        pass
    def connected():
        f._call()
    selector.register(sock, EVENT_WRITE, connected)
    yield from f
    selector.unregister(sock)

def send(sock,get):
    sock.send(get)

def recv_data_all(sock, Buffer):
    data = b''
    chunk = yield from read(sock, Buffer)
    while chunk:
        data += chunk
        chunk = yield from read(sock, Buffer)
    return data

def read(sock, Buffer):
    f = Future()
    def read_ready():
        f.result = sock.recv(Buffer)
        f._call()
    selector.register(sock, EVENT_READ, read_ready)
    chunk = yield from f
    selector.unregister(sock)
    return chunk

class Crawler(object):
    def __init__(self):
        self.url = 'www.baidu.com'
        self.sock = socket.socket()
        self.sock.setblocking(False)
        self.resp = b''

    def fetch(self):
        yield from connect(self.sock, (self.url, 80))
        get = 'GET / HTTP/1.0\r\nHost:www.baidu.com\r\n\r\n'.encode('ascii')
        send(self.sock, get)
        data = yield from recv_data_all(self.sock, 4096)
        self.resp = data
        print(self.resp.decode('utf8'))
        self.sock.close()

class Task(object):
    def __init__(self, coro):
        self.coro = coro
        f =Future()
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            global count_tasks
            count_tasks -= 1
            return
        next_future.set_callback(self.step)

class Loop(object):
    def __init__(self, tasks):
        self.tasks = tasks
        self.count_tasks = len(tasks)

    def main(self):
        for task in self.tasks:
            Task(task)

    def run_until_complete(self):
        for task in self.tasks:
            Task(task)
        global count_tasks
        while count_tasks > 0:
            events = selector.select()
            for event_key, event_mask in events:
                _callback = event_key.data
                _callback()

selector = DefaultSelector()
tasks = [Crawler().fetch() for i in range(2)]
count_tasks = len(tasks)
loop = Loop(tasks)
loop.run_until_complete()