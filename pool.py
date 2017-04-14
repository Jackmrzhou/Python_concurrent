from multiprocessing.dummy import Pool
import requests
[print(result) for result in Pool(4).map(requests.get, ['http://www.baidu.com' for _ in range(40)])]