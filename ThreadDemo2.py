import queue, threading, requests
from bs4 import BeautifulSoup

class WorkThread(threading.Thread):
    def __init__(self, func,*args):
        super(WorkThread, self).__init__()
        self.func = func
        self.args = args
    def run(self):
        self.func(self.args)

def GetPage(args):
    (url,headers,my_queue) = args
    resp = requests.get(url,headers = headers)
    my_queue.put(resp)

def Parse_html(my_queue,result):
    while not my_queue.empty():
        html = my_queue.get().text
        soup = BeautifulSoup(html ,'lxml')
        items = soup.find_all('div', attrs={'class':'item'})
        for item in items:
            rank = item.find('div', attrs={'class':'pic'}).em.text
            name = item.find('div', attrs={'class':'hd'}).a.span.text
            result.append((int(rank), name))
    return result

if __name__ == '__main__':
    my_queue =  queue.Queue()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}
    urls = ['https://movie.douban.com/top250?start={}&filter='.format(x*25)
            for x in range(10)]
    GetPageThreads=[]
    for url in urls:
        t = WorkThread(GetPage, url, headers, my_queue)
        GetPageThreads.append(t)
        t.start()
    for t in GetPageThreads:
        t.join()
    result = []
    result = Parse_html(my_queue, result)
    result.sort(key = lambda x:x[0])
    with open('douban.txt','w') as fp:
        for item in result:
            fp.write(str(item[0]) + '\t' +item[1] +'\n')