
from .base import BaseModel
from .. import db
from ..src.eth import ManagerConnector, IdentityConnector, Connector
from ..utils import get_static_dir


AbiFile = 'betonether.json'


class BetOnEther(BaseModel):
    home = db.Column(db.String(63))
    visiting = db.Column(db.String(63))
    opening_time = db.Column(db.TIMESTAMP(timezone=True))
    league = db.Column(db.String(63))
    round = db.Column(db.String(63))
    win_odds = db.Column(db.Float())
    draw_odds = db.Column(db.Float())
    lose_odds = db.Column(db.Float())

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

    @property
    def abi_text(self):
        with open(get_static_dir('abis/{}'.format(AbiFile))) as f:
            return f.read()

    @property
    def contract_init_params(self):
        pass

    @property
    def contract(self):
        try:
            return getattr(self, '_contract')
        except AttributeError:
            self.load_contract()
            return self._contract

    def sync_data(self, contract=None):
        if self.has_contract and contract is None:
            contract = self.load_contract()

        self.host = contract.call(contract.functions.host())
        self.pool = contract.call(contract.functions.pool())
        self.earnest_money = contract.call(contract.functions.earnestMoney())
        self.balance = contract.call(contract.functions.balance())
        self.win_bonus = contract.call(contract.functions.bonuss(0))
        self.draw_bonus = contract.call(contract.functions.bonuss(1))
        self.lose_odds = contract.call(contract.functions.bonuss(2))
        self.ended = contract.call(contract.functions.ended())

        db.session.add(self)
        db.session.commit()

        self._contract = contract

    def create_contract(self):
        if self.has_contract:
            return

        self.has_contract = True
        db.session.add(self)
        db.session.commit()

        try:
            coon = ManagerConnector()
            contract = coon.deploy_contract(self.abi_text, **self.contract_init_params)

            self.sync_data(contract)
        except Exception as e:
            self.has_contract = False
            db.session.add(self)
            db.session.commit()

    def load_contract(self):
        if not self.has_contract:
            return

        coon = ManagerConnector()
        contract = coon.load_contract(self.contract_address, self.abi_text)
        return contract

    def bet(self, beton, amount, account, password):
        conn = IdentityConnector(account, password)
        res = conn.transact(self.contract.functions.bet(beton), value=conn.to_wei(amount, 'finney'))
        return res

    def alterOdds(self, win, draw, lose):
        pass

    def confirm(self, result):
        conn = ManagerConnector()
        res = conn.transact(self.contract.functions.bet(result))
        return res

    def withdraw(self, account, password):
        conn = IdentityConnector(account, password)
        res = conn.transact(self.contract.functions.withdraw())
        return res

    def clear(self):
        conn = ManagerConnector()
        res = conn.transact(self.contract.functions.clear())
        return res

    def query_bets(self, account):
        coon = Connector()
        res = []
        bet = coon.call(self.contract.functions.bets(account, 0))
        res.append(bet)
        return res
