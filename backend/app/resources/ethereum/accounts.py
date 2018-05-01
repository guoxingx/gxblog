
from flask import abort, request
from web3.auto import w3

from ..base import BaseResource
from ...utils import to_checked_address


class Accounts(BaseResource):

    def get(self):
        abort(404)

    def post(self):
        password = request.json.get('password')
        return w3.personal.newAccount(password)


class Balance(BaseResource):

    def get(self, address):
        return w3.eth.getBalance(to_checked_address(address))
