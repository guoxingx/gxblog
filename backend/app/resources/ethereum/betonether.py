
from flask import abort, request, current_app
from redis import Redis

from ..base import BaseResource, login_required, form_by_json_request
from ..forms import BetOnEtherCreateForm
from ... import db
from ...models import BetOnEther


class BetOnEtherList(BaseResource):

    # decorators = [login_required]

    def get(self):
        res = BetOnEther.query.filter_by(has_contract=True).filter_by(deleted=False).order_by(BetOnEther.created_at.desc()).all()
        return [b.to_json() for b in res]

    # def post(self):
    #     form = form_by_json_request(BetOnEtherCreateForm)
    #     if form.validate_on_submit():
    #         boe = BetOnEther(**form.data)
    #         db.session.add(boe)
    #         db.session.commit()
    #         return boe.to_json()
    #     abort(400, form.errors)


class BetOnEtherBetList(BaseResource):

    def get(self, id):
        address = request.args.get('address')
        boe = BetOnEther.query.get(id)
        if boe and boe.deleted:
            boe = None
        res = boe.query_bets(address)
        if not res:
            abort(404)
        return res

    def post(self, id):
        address = request.json.get('address')
        redis = Redis.from_url(current_app.config['REDIS_URL'])
        key = 'BetOnEtherAction:{}'.format(address)
        if redis.get(key):
            return 30001, 'Operation too frequent'
        redis.set(key, 1, 20)

        beton = request.json.get('beton')
        amount = request.json.get('amount')
        password = request.json.get('password')
        boe = BetOnEther.query.get(id)
        if boe and boe.deleted:
            boe = None
        code, res = boe.bet(beton, amount, address, password)
        return code, res


class BetOnEtherWithdraw(BaseResource):

    def post(self, id):
        address = request.json.get('address')
        redis = Redis.from_url(current_app.config['REDIS_URL'])
        key = 'BetOnEtherAction:{}'.format(address)
        if redis.get(key):
            return 30001, 'Operation too frequent'
        redis.set(key, 1, 20)

        password = request.json.get('password')
        boe = BetOnEther.query.get(id)
        if boe and boe.deleted:
            boe = None
        res = boe.withdraw(address, password)
        return res
