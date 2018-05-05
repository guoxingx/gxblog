
from flask import current_app

from .accounts import Accounts, Balance, TestEtherCoin
from .betonether import BetOnEtherList, BetOnEtherWithdraw, BetOnEtherBetList

from ..base import BaseResource
from ...utils import get_w3


w3 = get_w3()


class EthStatus(BaseResource):

    def get(self):
        if current_app.config.get('ETH_MODE') == 'test':
            return {
                'code': 0,
                'data': {
                    'status': 0,
                    'peer_count': 0,
                    'message': 'private chain'
                }
            }
        status = 0
        message = 'working'
        peer_count = w3.net.peerCount
        try:
            w3.eth.getBalance(w3.eth.accounts[0])
        except ValueError as e:
            if e.args[0].get('code') == -32000:
                if peer_count > 0:
                    status = 1
                    message = 'syncing'
                else:
                    status = 2
                    message = 'warting for peers'
            else:
                raise e

        return {
            'code': 0,
            'data': {
                'status': status,
                'peer_count': peer_count,
                'message': message
            },
            'error': ''
        }
