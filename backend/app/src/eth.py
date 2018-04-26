#!coding: utf-8

import requests
import functools

from web3 import Web3, HTTPProvider
from hexbytes.main import HexBytes
from eth_utils import to_checksum_address


def draw(account):
    url = 'https://faucet.metamask.io/'
    headers = {'content-type': 'application/rawdata'}
    res = requests.post(url, data=account, headers=headers).text
    return res


def to_checked_address(address):
    res = to_checksum_address(address)
    if res.lower() == address:
        return res


def unlock_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        try:
            res = func(*args, **kw)
        except ValueError as e:
            if locked_exception(e):
                ins = args[0]
                try_unlock(ins, kw)
                res = func(*args, **kw)
        finally:
            return res
    return wrapper


def locked_exception(error):
    return error.args[0].get('code') == -32000


def try_unlock(instance, kw):
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

    def deploy_contract(self, **kw):
        """
        Until next time
        """
        NotImplementedError

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
            if locked_exception(e):
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
            if locked_exception(e):
                try_unlock(self, kw)
                res = func.call(kw)
        finally:
            if isinstance(res, HexBytes):
                res = self._w3.toHex(res)
            return res


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
    import time
    account = '0x39bbc3788130827bbaba742fd3c41fb5b5ce82b8'
    for i in range(10):
        res = draw(account)
        print(res)
        time.sleep(10)

    # coon = Connector()

    # account = coon.create_account('3')
    # print('account {} created.'.format(account))

    # res = draw(account)
    # print('draw from faucet ', res)
