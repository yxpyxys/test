import requests
import json
import time

headers = {'User-Agent': 'Mozilla/5.1 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.1.3282.119 Safari/537.36'}
url = "https://api.bscscan.com/api?module=contract&action=getsourcecode&address={}"

with open("data/bsc_token.json","r") as f:
    tokens = json.loads(f.readline())

token_lst = []

i = 0
while i < len(tokens):
    t = tokens[i]
    address = t['address']
    res = requests.get(url.format(address), headers=headers)
    if res.status_code == 200:
        try:
            resjson = json.loads(res.text)
            code = 0 if resjson['result'][0]['SourceCode'] == '' else 1
            isproxy = resjson['result'][0]['Proxy']
            token_lst.append([address, code, isproxy])
            print(i, t['symbol'], code, isproxy)
            i += 1
        except:
            print('.', end='')
    time.sleep(0.2)

print(len(token_lst))
with open('token_data.json', 'w') as f:
    json.dump(token_lst, f)

