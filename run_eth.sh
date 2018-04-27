#!/bin/bash

if [ $MODE ];then
	echo 'dev'
	geth --testnet --rpc --rpcaddr 0.0.0.0 --syncmode light
else
	echo 'test'
	geth --datadir /root/test/data --preload mineWhenNeeded.js,teams.js --rpc --rpccorsdomain 0.0.0.0 --rpcapi eth,net,web3,personal
fi
