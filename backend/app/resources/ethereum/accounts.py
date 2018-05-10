
from flask import abort, request, current_app
from redis import Redis
# from web3.auto import w3

from ..base import BaseResource
from ...utils import to_checked_address, get_w3


w3 = get_w3()


class Accounts(BaseResource):

    def get(self):
        abort(404)

    def post(self):
        password = request.json.get('password')
        return w3.personal.newAccount(password)


class Balance(BaseResource):

    def get(self, address):
        return w3.eth.getBalance(to_checked_address(address))


class TestEtherCoin(BaseResource):

    def post(self):
        if current_app.config.get('ETH_MODE') != 'test':
            abort(404)
        account = to_checked_address(request.json.get('address'))

        redis = Redis.from_url(current_app.config['REDIS_URL'])
        key = 'TestEtherCoin:{}'.format(account)
        last = redis.get(key)
        if last:
            return 20001, 'you are greedy.'
        redis.set(key, 1, 300)

        base = w3.eth.accounts[0]
        w3.personal.unlockAccount(base, current_app.config.get('ETH_COINBASE_PASSWORD'))
        res = w3.eth.sendTransaction({
            'from': base,
            'to': account,
            'value': w3.toWei(1, 'ether')
        })
        return {'transaction': w3.toHex(res)}
