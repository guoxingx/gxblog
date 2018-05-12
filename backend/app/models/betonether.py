#!coding: utf-8

import time
import json

from flask import current_app

from .base import BaseModel
from .. import db
# from ..src.eth import ManagerConnector, IdentityConnector, Connector
# from web3.auto import w3
from web3.exceptions import BadFunctionCallOutput
from ..utils import get_static_dir, to_checked_address, get_w3


w3 = get_w3()
AbiFile = 'betonether_abi'
ByteCodeFile = 'betonether_bytecode'


class BetOnEther(BaseModel):
    """
    @param: contract_status: <int>
        0: 未绑定合约
        1: 合约写入区块中 tx_hash load_contract_by_tx_hash()
        2: 合约正常
        3: 合约未找到
    """
    home = db.Column(db.String(63))
    home_image = db.Column(db.String(255))
    visiting = db.Column(db.String(63))
    visiting_image = db.Column(db.String(255))
    opening_time = db.Column(db.TIMESTAMP(timezone=True))
    league = db.Column(db.String(63))
    round = db.Column(db.String(63))
    abifile = db.Column(db.String(63), default='betonether_abi.0.20.json')
    bytecodefile = db.Column(db.String(63), default='betonether_bytecode.0.20.json')

    # 合约状态
    has_contract = db.Column(db.Boolean())
    contract_address = db.Column(db.String(63))
    tx_hash = db.Column(db.String(127))
    contract_status = db.Column(db.Integer())

    # 合约信息
    win_odds = db.Column(db.Integer())
    draw_odds = db.Column(db.Integer())
    lose_odds = db.Column(db.Integer())
    host = db.Column(db.String(63))
    pool = db.Column(db.Integer())
    earnest_money = db.Column(db.Integer())
    balance = db.Column(db.Integer())
    win_bonus = db.Column(db.Integer())
    draw_bonus = db.Column(db.Integer())
    lose_bonus = db.Column(db.Integer())
    ended = db.Column(db.Boolean())
    result = db.Column(db.Integer())
    bet_count = db.Column(db.Integer())

    deleted = db.Column(db.Boolean(), default=False)

    @property
    def bytecode_text(self):
        if not self.bytecodefile:
            self.bytecodefile = 'betonether_bytecode.0.10.json'
            db.session.add(self)
            db.session.commit()
        with open(get_static_dir('contracts/{}'.format(self.bytecodefile))) as f:
            res = f.read()
            res = json.loads(res)
            res = res.get('object')
            return res

    @property
    def abi_text(self):
        if not self.abifile:
            self.abifile = 'betonether_abi.0.10.json'
            db.session.add(self)
            db.session.commit()
        with open(get_static_dir('contracts/{}'.format(self.abifile))) as f:
            return f.read()

    @property
    def contract(self):
        try:
            return getattr(self, '_contract')
        except AttributeError:
            contract = self.load_contract()
            if contract:
                self.has_contract = True
                self.contract_address = contract.address
                db.session.add(self)
                db.session.commit()
                self._contract = contract
                return self._contract

    def sync_data(self):
        """
        从合同加载参数并保存到数据库
        """
        pass

    def sync_data_base(self):
        """
        从合同加载部分参数并保存到数据库
        """
        try:
            contract = self.contract

            self.host = contract.functions.host().call()
            self.earnest_money = int(contract.functions.earnestMoney().call() / (10 ** 15))
            self.win_odds = contract.functions.oddss(0).call()
            self.draw_odds = contract.functions.oddss(1).call()
            self.lose_odds = contract.functions.oddss(2).call()

            # 向下兼容
            try:
                self.bet_count = contract.functions.betCount().call()
            except AttributeError as e:
                pass

            self.ended = contract.functions.ended().call()
            if self.ended:
                self.result = contract.functions.game().call()[3]
            self.contract_status = 2
        except BadFunctionCallOutput as e:
            self.contract_status = 3
        finally:
            db.session.add(self)
            db.session.commit()

    def sync_data_all(self):
        """
        从合同加载全部参数并保存到数据库
        """
        try:
            contract = self.contract

            self.host = contract.functions.host().call()
            self.earnest_money = int(contract.functions.earnestMoney().call() / (10 ** 15))
            self.win_odds = contract.functions.oddss(0).call()
            self.draw_odds = contract.functions.oddss(1).call()
            self.lose_odds = contract.functions.oddss(2).call()
            self.pool = int(contract.functions.pool().call() / (10 ** 15))
            self.balance = int(contract.functions.balance().call() / (10 ** 15))
            self.win_bonus = int(contract.functions.bonuss(0).call() / (10 ** 15))
            self.draw_bonus = int(contract.functions.bonuss(1).call() / (10 ** 15))
            self.lose_bonus = int(contract.functions.bonuss(2).call() / (10 ** 15))

            # 向下兼容
            try:
                self.bet_count = contract.functions.betCount().call()
            except AttributeError as e:
                pass

            self.ended = contract.functions.ended().call()
            if self.ended:
                self.result = contract.functions.game().call()[3]
            self.contract_status = 2
        except BadFunctionCallOutput as e:
            self.contract_status = 3
        finally:
            db.session.add(self)
            db.session.commit()

    def deploy(self, earnest_money, win_odds, draw_odds, lose_odds, host=None, password=None):
        """
        部署合约
        @param: earnest_money: <int> 庄家保证金 单位finney
        @param: win_odds: <int> 主胜利率x1000
        @param: draw_odds: <int> 平局利率x1000
        @param: lose_odds: <int> 客胜利率x1000
        @param: host: optional: <string> 庄家账号，默认使用eth.accounts[0]
        @param: password: optional: <string> 庄家密码，默认app.config.get('ETH_COINBASE_PASSWORD') 环境变量
        """
        if self.has_contract or self.contract_status:
            return 1

        remarks = '{}-{}'.format(self.league, self.round)
        oddss = [int(win_odds), int(draw_odds), int(lose_odds)]
        bet_time = int(self.opening_time.timestamp() - time.time() - 3600)
        if bet_time < 3600:
            return 2
        game_time = 3600 * 2

        host = host or w3.eth.accounts[0]
        host = to_checked_address(host)
        password = password or current_app.config.get('ETH_COINBASE_PASSWORD')
        w3.personal.unlockAccount(host, password)
        contract = w3.eth.contract(abi=self.abi_text, bytecode=self.bytecode_text)
        tx_hash = contract.constructor(
            w3.toHex(text=self.home), w3.toHex(text=self.visiting),
            w3.toHex(text=remarks), oddss,
            bet_time, game_time,
            w3.toHex(text=str(self.id))).transact({'from': host, 'value': w3.toWei(earnest_money, 'finney')})
        self.tx_hash = w3.toHex(tx_hash)
        self.contract_status = 1
        db.session.add(self)
        db.session.commit()
        return 0

    def load_contract_by_tx_hash(self):
        """
        用tx_hash来加载合约
        """
        if self.contract_status != 1:
            return 1
        tx_receipt = w3.eth.getTransactionReceipt(self.tx_hash)
        if tx_receipt:
            self.contract_address = tx_receipt['contractAddress']
            self.contract_status = 2
            self.has_contract = True
            db.session.add(self)
            db.session.commit()
            return 0
        return 2

    def load_contract(self, address=None, sync_data=True):
        """
        从合约地址加载合约
        @param: address: <string> 合约地址
        @param: sync_data: optional <bool> 是否同步合约数据
        """
        if self.has_contract:
            pass

        address = to_checked_address(address or self.contract_address)
        contract = w3.eth.contract(address=address, abi=self.abi_text)

        return contract

    def bet(self, beton, amount, account, password):
        """
        下注
        """
        account = to_checked_address(account)
        params = {'from': account, 'value': w3.toWei(amount, 'finney')}
        res = w3.personal.unlockAccount(account, password)
        if not res:
            return 1, None
        try:
            gas = self.contract.functions.bet(beton).estimateGas(params)
        except ValueError as e:
            return 2, None
        res = self.contract.functions.bet(beton).transact({
            'from': to_checked_address(account),
            'value': w3.toWei(amount, 'finney'),
            'gas': gas
        })
        res = w3.toHex(res)
        return 0, res

    def alterOdds(self, win, draw, lose, password=None):
        """
        修改赔率
        """
        password = password or current_app.config.get('ETH_COINBASE_PASSWORD')
        w3.personal.unlockAccount(self.host, password)
        gas = self.contract.functions.alterOdds(win, draw, lose).estimateGas({'from': self.host})
        res = self.contract.functions.alterOdds(win, draw, lose).transact({'from': self.host, 'gas': gas})
        return w3.toHex(res)

    def inputEarnestMoney(self, amount, password=None):
        """
        增加保证金
        """
        params = {'from': self.host, 'value': w3.toWei(amount, 'finney')}
        password = password or current_app.config.get('ETH_COINBASE_PASSWORD')
        w3.personal.unlockAccount(self.host, password)
        gas = self.contract.functions.inputEarnestMoney().estimateGas(params)
        params['gas'] = gas
        res = self.contract.functions.inputEarnestMoney().transact(params)
        return w3.toHex(res)

    def confirm(self, result, password=None):
        """
        输入结果
        """
        password = password or current_app.config.get('ETH_COINBASE_PASSWORD')
        w3.personal.unlockAccount(self.host, password)
        gas = self.contract.functions.confirm(result).estimateGas({'from': self.host})
        res = self.contract.functions.confirm(result).transact({'from': self.host, 'gas': gas})
        return w3.toHex(res)

    def withdraw(self, account, password):
        """
        提现
        """
        account = to_checked_address(account)
        w3.personal.unlockAccount(account, password)
        res = self.contract.functions.withdraw().transact({'from': account})
        return w3.toHex(res)

    def clear(self, password=None):
        """
        庄家提款
        """
        password = password or current_app.config.get('ETH_COINBASE_PASSWORD')
        w3.personal.unlockAccount(self.host, password)
        res = self.contract.functions.clear().transact({'from': self.host})
        return w3.toHex(res)

    def query_bets(self, account, index=0, count=10):
        """
        获取某个玩家的下注信息
        """
        res = []
        account = to_checked_address(account)
        for i in range(index, index + count):
            try:
                bet = self.contract.functions.bets(account, i).call()
                res.append(bet)
            except BadFunctionCallOutput:
                break
        return res

    def query_players(self, index=0, count=10):
        """
        获取参与的玩家地址
        """
        res = []
        for i in range(index, index + count):
            try:
                player = self.contract.functions.players(i).call()
                res.append(player)
            except AttributeError as e:
                return None
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
            result=self.result,
            contract_status=self.contract_status
        )
