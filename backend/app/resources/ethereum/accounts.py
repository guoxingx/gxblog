
from flask import abort, request, current_app
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


class Transactions(BaseResource):

    def post(self):
        account = request.json.get('address')
        base = w3.eth.accounts[0]
        w3.personal.unlockAccount(w3.eth.accounts[0], current_app.config.get('ETH_COINBASE_PASSWORD'))
        res = w3.eth.sendTransaction({
            'from': base,
            'to': account,
            'value': w3.toWei(1, 'ether')
        })
        return w3.toHex(res)
