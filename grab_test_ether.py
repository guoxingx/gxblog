#!/usr/bin/env python

import os
import enum
import time
import asyncio
import hashlib
import argparse

import requests
from web3 import Web3, HTTPProvider
from apscheduler.schedulers.blocking import BlockingScheduler


class RequestStrategies(enum.Enum):
    Null = 0  # request every time.
    Minimum = 1  # request with minimum time interval in records.
    Maximum = 2  # request with maximum time interval in records.
    MinimumHalf = 3  # request with half of the maximum time interval in records.


URL = 'http://faucet.ropsten.be:3001/donate/{}'
PORT = 3001
STRATEGY = RequestStrategies.Null
DATADIR = 'data_grab_test_ether'
ETH_RPC_URL = None


def get_w3():
    if ETH_RPC_URL:
        return Web3(HTTPProvider(ETH_RPC_URL, request_kwargs={'timeout': 10}))
    from web3.auto import w3
    return w3


async def request_test_ether(account, loop):
    url = URL.format(account)
    future = loop.run_in_executor(None, requests.get, url)
    response = await future
    print(response.text)


def test_ether_request_pool(counts):
    """
    Use syncio event loop to call request_test_ether()
    """
    accounts = load_accounts(counts)
    loop = asyncio.get_event_loop()
    tasks = [request_test_ether(account, loop) for account in accounts]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


async def create_account(data):
    password = _generate_password()
    w3 = get_w3()
    account = w3.personal.newAccount(password)
    data[account] = password
    await asyncio.sleep(1)


def create_accounts_pool(counts):
    """
    """
    data = {}
    loop = asyncio.get_event_loop()
    tasks = [create_account(data) for i in range(counts)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    _save_account_password(data)


def load_accounts(counts):
    """
    """
    data = {}
    accounts = get_w3().eth.accounts
    with open("{}/accounts".format(DATADIR)) as f:
        current = 1
        for line in f:
            if current > counts:
                break
            account, password = line.split(" ")
            if account in accounts:
                data[account] = password.strip("\n")
            current += 1
    return data


def transact_to_coinbase(counts, value, remote=None):
    from backend.app.src.memcheck import get_used_memory

    accounts = load_accounts(counts)
    for account, password in accounts.items():
        try:
            meminfo = get_used_memory(remote_addr=remote)
            while meminfo.get("used") > 90:
                print("memory busy: {}".format(meminfo))
                time.sleep(10)
                meminfo = get_used_memory(remote_addr=remote)
            w3 = get_w3()
            w3.personal.unlockAccount(account, password)
            resp = w3.eth.sendTransaction({'from': account, "to": w3.eth.accounts[0], "value": value * 10 ** 15})
            print(w3.toHex(resp))
            del w3
        except Exception as e:
            print(e)


def _save_request_interval(data):
    """
    data: dict {account: last_success_ts}
    """
    if not os.path.isdir(DATADIR):
        os.system("mkdir -p {}".format(DATADIR))
    with open("{}/intervals".format(DATADIR), "a") as f:
        for account, last_ts in data.items():
            f.write("{} {}\n".format(account, last_ts))


def _save_account_password(data):
    """
    data: dict {account: password}
    """
    if not os.path.isdir(DATADIR):
        os.system("mkdir -p {}".format(DATADIR))
    with open("{}/accounts".format(DATADIR), "a") as f:
        for account, password in data.items():
            f.write("{} {}\n".format(account, password))


def _generate_password():
    return hashlib.md5(str(time.time()).encode()).hexdigest()


def run_cli():
    """
    Start cmd client.
    """
    global STRATEGY, DATADIR, ETH_RPC_URL

    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str,
                        help='Mode, create - Create accounts; run - Start request test ether;\
                             load - Print accounts and password; transact - Send to coinbase;\
                             schedule - "run" and "transact" in schedule;')
    parser.add_argument('-n', type=int, default=1,
                        help='Account number to operate, between 1 ~ 50, default as 1. Except coinbase.')
    parser.add_argument('-stg', type=int, default=0,
                        help='Request strategy. Null = 0, Minimum = 1, Maximum = 2, MinimumHalf = 3. Default as 0')
    parser.add_argument('-data', type=str, default=DATADIR,
                        help='Data storage file path, default "{}"'.format(DATADIR))
    parser.add_argument('-v', type=int, default=900,
                        help='How much finney to send.')
    parser.add_argument('--rpcurl', type=str,
                        help='Eth rpc connect url. default as http://localhost:8545')
    parser.add_argument('--remote', type=str,
                        help='If eth node run in remote server.')

    args = parser.parse_args()

    # Set counts
    if args.n > 50:
        args.n = 50
    if args.n < 1:
        args.n = 1

    # Set global params
    if args.stg != STRATEGY:
        STRATEGY = args.stg
    if args.data != DATADIR:
        DATADIR = args.data
    if args.rpcurl:
        ETH_RPC_URL = args.rpcurl

    # Run action
    if args.mode == 'create':
        create_accounts_pool(args.n)
    elif args.mode == 'run':
        test_ether_request_pool(args.n)
    elif args.mode == 'load':
        for account, password in load_accounts(args.n).items():
            print(account, password)
    elif args.mode == 'transact':
        print("trasact could be unbearable slow cause only one account will be unlocked at one time till the memory released.")
        transact_to_coinbase(args.n, args.v)
    elif args.mode == 'schedule':
        def request_test_ether_schedule():
            test_ether_request_pool(args.n)

        def transact_to_coinbase_schedule():
            if args.remote:
                transact_to_coinbase(args.n, args.v, args.remote)
            else:
                transact_to_coinbase(args.n, args.v)

        sched = BlockingScheduler(daemon=True)
        sched.add_job(request_test_ether_schedule, 'interval', hours=13)
        sched.add_job(transact_to_coinbase_schedule, 'interval', hours=14)
        sched.start()
    else:
        parser.print_help()


if __name__ == '__main__':
    run_cli()
