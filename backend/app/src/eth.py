#!coding: utf-8

import os
import asyncio
import functools

import requests
from web3 import Web3, HTTPProvider
from hexbytes.main import HexBytes
from eth_utils import to_checksum_address


def draw(account):
    """
    获取免费的testnet ether
    """
    url = 'https://faucet.metamask.io/'
    headers = {'content-type': 'application/rawdata'}
    res = requests.post(url, data=account, headers=headers).text
    return res


def to_checked_address(address):
    """
    非混合大小写的addres会报错，不知道是否是bug
    将address转换成混合大小写
    """
    res = to_checksum_address(address)
    if res.lower() == address or res.upper() == address:
        return res
    return address


def unlock_required(func):
    """
    返回未解锁错误的时候
    执行解锁并重试
    """
    @functools.wraps(func)
    def wrapper(*args, **kw):
        try:
            res = func(*args, **kw)
        except ValueError as e:
            if _locked_exception(e):
                ins = args[0]
                try_unlock(ins, kw)
                res = func(*args, **kw)
        finally:
            return res
    return wrapper


def _locked_exception(error):
    """
    Catch unlocked exception.
    """
    return error.args[0].get('code') == -32000


def try_unlock(instance, kw):
    """
    """
    account = kw.get('from') or kw.get('from_')
    password = kw.get('password')

    if not account:
        try:
            account = getattr(instance, '_account')
            kw['from'] = account
        except Exception:
            raise
    if not password:
        try:
            password = getattr(instance, '_password')
        except Exception:
            raise
    instance.unlock(account, password)


class Connector(object):
    DefaultHTTPRPCAddr = 'http://localhost:8545'

    def __init__(self, url=None):
        """
        @param: url: [optional]: <string> HTTP-RPC server address for ethereum node
        """
        self._w3 = Web3(HTTPProvider(url or Connector.DefaultHTTPRPCAddr))

        self.auto_mine_in_test()

    def create_account(self, password):
        address = self._w3.personal.newAccount('password')
        return address

    def unlock(self, account, password):
        return self._w3.personal.unlockAccount(account, password)

    @unlock_required
    def send_transaction(self, **kw):
        """
        转账
        """
        res = self._w3.eth.sendTransaction(kw)
        return self._w3.toHex(res)

    def to_wei(self, amount, unit):
        return self._w3.toWei(amount, unit)

    def deploy_contract(self, abi):
        """
        Until next time
        """
        Contract = self._w3.eth.contract(abi=abi)
        tx_hash = Contract.deploy()
        tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
        contract_address = tx_receipt['contractAddress']
        return contract_address

    def load_contract(self, address, abi):
        """
        address = to_checked_address('0x2c28144c2ebd7b2e02f9aaa3d7382fb5cb6d52df')
        with open('abi.json') as f:
            abi_json = f.read()
        contract = conn._w3.eth.contract(address=address, abi=abi_json)
        """
        return self._w3.eth.contract(address=address, abi=abi)

    def transact(self, func, **kw):
        """
        执行合约函数
        res = conn.transact(contract.functions.setResult(26, 0, True))
        """
        try:
            res = func.transact(kw)
        except ValueError as e:
            if _locked_exception(e):
                try_unlock(self, kw)
                res = func.transact(kw)
        finally:
            if isinstance(res, HexBytes):
                res = self._w3.toHex(res)
            return res

    def call(self, func, **kw):
        """
        获取合约参数
        res = conn.call(contract.functions.host())
        """
        try:
            res = func.call(kw)
        except ValueError as e:
            if _locked_exception(e):
                try_unlock(self, kw)
                res = func.call(kw)
        finally:
            if isinstance(res, HexBytes):
                res = self._w3.toHex(res)
            return res

    def auto_mine_in_test(self):
        eth_mode = os.environ.get('ETH_MODE') or 'test'
        if eth_mode != 'test':
            return

        async def event_loop(event_filter, poll_interval):
            while True:
                eth = self._w3.eth
                miner = self._w3.miner
                if len(eth.getBlock('pending').transactions) > 0:
                    if not eth.mining:
                        miner.start(1)
                else:
                    if eth.mining:
                        miner.stop()
                await asyncio.sleep(poll_interval)

        tx_filter = self._w3.eth.filter('pending')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.gather(event_loop(tx_filter, 2)))
        finally:
            loop.close()


class IdentityConnector(Connector):

    def __init__(self, account, password, url=None):
        Connector.__init__(self, url)
        self._account = account
        self._password = password
        self._w3.eth.defaultAccount = self.account

    @property
    def password(self):
        return self._password

    @property
    def account(self):
        return self._account


class ManagerConnector(IdentityConnector):

    def __init__(self, password, url=None):
        IdentityConnector.__init__(self, None, password, url)
        self._account = self._w3.eth.coinbase
        self._w3.eth.defaultAccount = self.account


if __name__ == '__main__':
    coon = Connector()
    print(coon._w3.eth.accounts)
    print(coon._w3.eth.filter)

    # account = coon.create_account('3')
    # print('account {} created.'.format(account))

    # res = draw(account)
    # print('draw from faucet ', res)
