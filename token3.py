from web3 import Web3, HTTPProvider, IPCProvider
import json

w3 = Web3(IPCProvider("../node/geth.ipc"))

with open("data/uni_pair.abi","r") as f:
    pair_abi = json.loads(f.readline())

with open("data/bsc_token.json","r") as f:
    tokens = json.loads(f.readline())

fromBlock = 22048683 - int(86400*0.33)*10

for t in tokens:
    address = t['address']
    c = w3.eth.contract(address=Web3.toChecksumAddress(address), abi=pair_abi)
    event_filter = c.events.Swap.createFilter(fromBlock=fromBlock)
    el = event_filter.get_all_entries()
    print(el)
    # print(el[1])