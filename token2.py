import requests
from bs4 import BeautifulSoup
import json

headers = {'User-Agent': 'Mozilla/5.1 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.1.3282.119 Safari/537.36'}
url = "https://bscscan.com/address/{}"
token_lst = []

with open("bsc_token.json","r") as f:
    tokens = json.loads(f.readline())

for t in tokens:
    html = requests.get(url.format(t['address']), headers=headers)
    val = BeautifulSoup(html.text, 'html.parser')
    code = val.find('pre', attrs={'class': 'js-sourcecopyarea editor', 'id': 'editor'})
    if code is not None:
        token_lst.append({t['address']: 1})

print(len(token_lst))
with open('token_data.json', 'w') as f:
    json.dump(token_lst, f)

