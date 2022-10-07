from web3 import Web3, HTTPProvider, IPCProvider
import json
import pandas as pd
from multiprocessing.pool import ThreadPool

# w3 = Web3(HTTPProvider("https://damp-bitter-emerald.bsc.discover.quiknode.pro/dea7bf580630027687c7af772e1aa3b1183e72f3/"))
w3 = Web3(IPCProvider("../node/geth.ipc"))

with open("uni_factory.abi","r") as f:
    factory_abi = json.loads(f.readline())
with open("uni_pair.abi","r") as f:
    pair_abi = json.loads(f.readline())

# pancakeswap_factory = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'
# smallswap_factory = '0xD04A80baeeF12fD7b1D1ee6b1f8ad354f81bc4d7'

exchange = {
    # 'pancakeswap': '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73',
    'sushiswap': '0xc35DADB65012eC5796536bD9864eD8773aBc74C4',
    'pandaswap': '0x9Ad32bf5DaFe152Cbe027398219611DB4E8753B3',
    'digiswap': '0x98813bD470A3BA8Da3D16488c58374e8dBc2FF22',
    'nomiswap': '0xd6715A8be3944ec72738F0BFDC739d48C3c29349',
    'broccoli': '0x5B9f88Ee10413e764BEFACa083fB290c4f25F720',
    'biswap': '0x858E3312ed3A876947EA49d572A7C42DE08af7EE',
    'bakeryswap': '0x01bF7C66c6BD861915CdaaE475042d3c4BaE16A7',
    'apeswap': '0x0841BD0B734E4F5853f0dD8d7Ea041c241fb0Da6',
    'safeswap': '0x4d05D0045df5562D6D52937e93De6Ec1FECDAd21',
    'coswap': '0xf1B735685416253A8F7c8a6686970cA2B0cceCce',
    'sphynx': '0x8BA1a4C24DE655136DEd68410e222cCA80d43444',
    'dooarswap': '0x1e895bFe59E3A5103e8B7dA3897d1F2391476f3c',
    'elk': '0x31aFfd875e9f68cd6Cd12Cee8943566c9A4bBA13',
    'orbital': '0x1A04Afe9778f95829017741bF46C9524B91433fB',
    'fstswap': '0x9A272d734c5a0d7d84E0a892e891a553e8066dce',
    'w3swap': '0xD04A80baeeF12fD7b1D1ee6b1f8ad354f81bc4d7',
    'bscswap': '0xCe8fd65646F2a2a897755A1188C04aCe94D2B8D0',
    'bscsswap': '0x8b6Ca4B3E08c9f80209e66436187088C99C9C2AC',
    'cheeseswap': '0xdd538E4Fd1b69B7863E1F741213276A6Cf1EfB3B',
}

token_df = pd.read_csv("bsc_token.csv")
token_set = set(token_df['address'].to_list())
print(len(token_set))

result_df = pd.DataFrame()

for e in exchange:
    c = w3.eth.contract(address=exchange[e], abi=factory_abi)
    pair_len = c.functions.allPairsLength().call()
    print(e, pair_len)

    pair_dict = {}

    for i in range(0, pair_len):
        pair_address = c.functions.allPairs(i).call()
        p = w3.eth.contract(address=pair_address, abi=pair_abi)
        t0 = p.functions.token0().call().lower()
        t1 = p.functions.token1().call().lower()
        if t0 in token_set and t1 in token_set:
            pair_dict[pair_address.lower()] = {"token0": t0, "token1": t1}

    # def get_one_pair(i: int):
    #     pair_address = c.functions.allPairs(i).call()
    #     p = w3.eth.contract(address=pair_address, abi=pair_abi)
    #     t0 = p.functions.token0().call().lower()
    #     t1 = p.functions.token1().call().lower()
    #     if t0 in token_set and t1 in token_set:
    #         pair_dict[pair_address.lower()] = {"token0": t0, "token1": t1}

    # mypool = ThreadPool(5)
    # mypool.map(get_one_pair, range(pair_len))
    # mypool.close()
    # mypool.join()

    df = pd.DataFrame.from_dict(pair_dict, orient='index')
    # df = df.reset_index()
    # df = df.rename(columns={'index': 'address'},)
    df['exchange'] = [e]*len(df)
    print(e, len(df))
    result_df = pd.concat([result_df, df])

result_df.to_csv("pair.csv", index=True, index_label='address')