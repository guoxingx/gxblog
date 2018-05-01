
import time

from flask import current_app

from .base import BaseModel
from .. import db
# from ..src.eth import ManagerConnector, IdentityConnector, Connector
from web3.auto import w3
from web3.exceptions import BadFunctionCallOutput
from ..utils import get_static_dir, to_checked_address


AbiFile = 'betonether_abi.json'
ByteCodeFile = 'betonether_bytecode.json'


class BetOnEther(BaseModel):
    home = db.Column(db.String(63))
    home_image = db.Column(db.String(255))
    visiting = db.Column(db.String(63))
    visiting_image = db.Column(db.String(255))
    opening_time = db.Column(db.TIMESTAMP(timezone=True))
    league = db.Column(db.String(63))
    round = db.Column(db.String(63))
    win_odds = db.Column(db.Integer())
    draw_odds = db.Column(db.Integer())
    lose_odds = db.Column(db.Integer())

    has_contract = db.Column(db.Boolean())
    contract_address = db.Column(db.String(63))

    host = db.Column(db.String(63))
    pool = db.Column(db.Integer())
    earnest_money = db.Column(db.Integer())
    balance = db.Column(db.Integer())
    win_bonus = db.Column(db.Integer())
    draw_bonus = db.Column(db.Integer())
    lose_bonus = db.Column(db.Integer())
    ended = db.Column(db.Boolean())
    result = db.Column(db.Integer())

    @property
    def bytecode_text(self):
        with open(get_static_dir('contracts/{}'.format(ByteCodeFile))) as f:
            return f.read().encode()

    @property
    def abi_text(self):
        with open(get_static_dir('contracts/{}'.format(AbiFile))) as f:
            return f.read()

    @property
    def contract_init_params(self):
        return {}

    @property
    def contract(self):
        try:
            return getattr(self, '_contract')
        except AttributeError:
            self.load_contract()
            return self._contract

    def sync_data(self, contract=None):
        if self.has_contract and contract is None:
            contract = self.load_contract(sync_data=False)

        # self.host = contract.functions.host().call()
        # self.pool = int(contract.functions.pool().call() / (10 ** 15))
        # self.earnest_money = int(contract.functions.earnestMoney().call() / (10 ** 15))
        # self.balance = int(contract.functions.balance().call() / (10 ** 15))
        # self.win_odds = contract.functions.oddss(0).call()
        # self.draw_odds = contract.functions.oddss(1).call()
        # self.lose_odds = contract.functions.oddss(2).call()
        # self.win_bonus = int(contract.functions.bonuss(0).call() / (10 ** 15))
        # self.draw_bonus = int(contract.functions.bonuss(1).call() / (10 ** 15))
        # self.lose_bonus = int(contract.functions.bonuss(2).call() / (10 ** 15))
        self.ended = contract.functions.ended().call()
        if self.ended:
            self.result = contract.functions.game().call()[3]

        db.session.add(self)
        db.session.commit()

        self._contract = contract

    def deploy(self, earnest_money, win_odds, draw_odds, lose_odds):
        """
        not yet
        """
        if self.has_contract:
            return 0

        self.has_contract = True
        db.session.add(self)
        db.session.commit()

        # remarks = '{}-{}'.format(self.league, self.round)
        oddss = [int(win_odds), int(draw_odds), int(lose_odds)]
        bet_time = int(self.opening_time.timestamp() - time.time() - 3600)
        if bet_time < 3600:
            return 1
        game_time = 3600 * 2

        try:
            w3.personal.unlockAccount(w3.eth.coinbase, current_app.config.get('ETH_COINBASE_PASSWORD'))
            contract = w3.eth.contract(abi=self.abi_text, bytecode=self.bytecode_text)
            tx_hash = contract.constructor(
                self.home, self.visiting_image,
                self.league, oddss,
                bet_time, game_time,
                str(self.id)).transact({'value': earnest_money * (10 ** 18)})
            tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
            contract_address = tx_receipt['contractAddress']
            return contract_address

            self.sync_data(contract)
        except Exception as e:
            print(e)
            self.has_contract = False
            db.session.add(self)
            db.session.commit()

    def load_contract(self, address=None, sync_data=True):
        if self.has_contract:
            pass

        address = to_checked_address(address or self.contract_address)
        contract = w3.eth.contract(address=address, abi=self.abi_text)

        if contract:
            self.has_contract = True
            self.contract_address = contract.address
            db.session.add(self)
            db.session.commit()
            if sync_data:
                self.sync_data(contract)
            return contract

    def bet(self, beton, amount, account, password):
        account = to_checked_address(account)
        params = {'from': account, 'value': w3.toWei(amount, 'finney')}
        w3.personal.unlockAccount(account, password)
        try:
            gas = self.contract.functions.bet(beton).estimateGas(params)
        except ValueError:
            return 1, None
        res = self.contract.functions.bet(beton).transact({
            'from': to_checked_address(account),
            'value': w3.toWei(amount, 'finney'),
            'gas': gas
        })
        res = w3.toHex(res)
        return 0, res

    def alterOdds(self, win, draw, lose):
        pass

    def confirm(self, result):
        w3.personal.unlockAccount(w3.eth.coinbase, current_app.config.get('ETH_COINBASE_PASSWORD'))
        gas = self.contract.functions.confirm(result).estimateGas({'from': w3.eth.coinbase})
        res = self.contract.functions.confirm(result).transact({'from': w3.eth.coinbase, 'gas': gas})
        return w3.toHex(res)

    def withdraw(self, account, password):
        account = to_checked_address(account)
        w3.personal.unlockAccount(account, password)
        res = self.contract.functions.withdraw().transact({'from': account})
        return w3.toHex(res)

    def clear(self):
        w3.personal.unlockAccount(w3.eth.coinbase, current_app.config.get('ETH_COINBASE_PASSWORD'))
        res = self.contract.functions.clear().transact({'from': w3.eth.coinbase})
        return w3.toHex(res)

    def query_bets(self, account):
        res = []
        account = to_checked_address(account)
        for i in range(10):
            try:
                bet = self.contract.functions.bets(account, i).call()
                res.append(bet)
            except BadFunctionCallOutput:
                break
        return res

    def to_json(self):
        return dict(
            id=self.id,
            home=self.home,
            home_image=self.home_image,
            visiting=self.visiting,
            visiting_image=self.visiting_image,
            opening_time=self.opening_time.strftime('%Y-%m-%d %H:%M:%S'),
            league=self.league,
            round=self.round,
            win_odds=self.win_odds,
            draw_odds=self.draw_odds,
            lose_odds=self.lose_odds,
            has_contract=self.has_contract,
            contract_address=self.contract_address,
            host=self.host,
            pool=self.pool,
            earnest_money=self.earnest_money,
            balance=self.balance,
            win_bonus=self.win_bonus,
            draw_bonus=self.draw_odds,
            lose_bonus=self.lose_bonus,
            ended=self.ended,
            result=self.result
        )
