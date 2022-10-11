import requests
import json
import time

headers = {'User-Agent': 'Mozilla/5.1 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.1.3282.119 Safari/537.36'}
url = "https://api.bscscan.com/api?module=logs&action=getLogs&fromBlock=21216080&toBlock=22071440&address={}&topic0=0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"

with open("data/bsc_pair.json","r") as f:
    tokens = json.loads(f.readline())

pair_lst = []

i = 0
while i < len(tokens):
    p = tokens[i]
    address = p['address']
    res = requests.get(url.format(address), headers=headers)
    if res.status_code == 200:
        try:
            resjson = json.loads(res.text)
            result = resjson['result']
            l = len(result)
            if 0 < l < 100:
                addr_set = set()
                for r in result:
                    addr_set.add(r['topics'][1])
                    addr_set.add(r['topics'][2])
                pair_lst.append([address, l, len(addr_set)])
                print(i, l, len(addr_set))
            else:
                pair_lst.append([address, l, 0])
                print(i, l)
            i += 1
        except:
            print('.', end='')
    time.sleep(0.6)

print(len(pair_lst))
with open('pair_log.json', 'w') as f:
    json.dump(pair_lst, f)

