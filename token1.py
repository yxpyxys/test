import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

headers = {'User-Agent': 'Mozilla/5.1 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.1.3282.119 Safari/537.36'}
url = "https://bscscan.com/address/{}"
token_lst = []
thread_pool = ThreadPoolExecutor(1)

def func(address: str):
    html = requests.get(url.format(address), headers=headers)
    val = BeautifulSoup(html.text, 'html.parser')
    code = val.find('pre', attrs={'class': 'js-sourcecopyarea editor', 'id': 'editor'})
    if code is not None:
        return address, 1
    else:
        print(html)
        return address, 0

with open("bsc_token.json","r") as f:
    tokens = json.loads(f.readline())

all_task = [thread_pool.submit(func, t['address']) for t in tokens]

for future in as_completed(all_task):
    res = future.result()
    token_lst.append(res)

thread_pool.shutdown(wait=True)

print(len(token_lst))
with open('token_data.json', 'w') as f:
    json.dump(token_lst, f)

