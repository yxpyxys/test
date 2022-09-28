package main

import (
    "fmt"
    "log"
    "uniswap"

    "github.com/ethereum/go-ethereum/ethclient"
    "github.com/ethereum/go-ethereum/common"
)

func main() {
    fmt.Println("start")
    client, err := ethclient.Dial("/node/geth.ipc")
    // client, err := ethclient.Dial("https://damp-bitter-emerald.bsc.discover.quiknode.pro/dea7bf580630027687c7af772e1aa3b1183e72f3/")
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println("we have a connection")

    // pancake swap factory v2 contract address
    string factory_address := "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"

    u := NewUniswap(common.HexToAddress(factory_address), client)
    n := u.UniswapCaller.AllPairsLength()
    fmt.Println(n)


    pair_address := u.GetPair(token0Address, token1Address)
    p := NewPair(common.HexToAddress(pair_address), client)
    reserve0, reserve1 := p.GetReserve()

}