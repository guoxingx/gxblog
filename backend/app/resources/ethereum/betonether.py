
from flask import abort, request

from ..base import BaseResource, login_required, form_by_json_request
from ..forms import BetOnEtherCreateForm
from ... import db
from ...models import BetOnEther


class BetOnEtherList(BaseResource):

    # decorators = [login_required]

    def get(self):
        res = BetOnEther.query.filter_by(has_contract=True).all()
        return [b.to_json() for b in res]

    def post(self):
        form = form_by_json_request(BetOnEtherCreateForm)
        if form.validate_on_submit():
            boe = BetOnEther(**form.data)
            db.session.add(boe)
            db.session.commit()
            return boe.to_json()
        abort(400, form.errors)


class BetOnEtherBetList(BaseResource):

    def get(self, id):
        address = request.args.get('address')
        boe = BetOnEther.query.get(id)
        res = boe.query_bets(address)
        return res

    def post(self, id):
        address = request.json.get('address')
        beton = request.json.get('beton')
        amount = request.json.get('amount')
        password = request.json.get('password')
        boe = BetOnEther.query.get(id)
        code, res = boe.bet(beton, amount, address, password)
        return {
            'code': code,
            'data': res,
            'error': ''
        }


class BetOnEtherWithdraw(BaseResource):

    def post(self, id):
        address = request.json.get('address')
        password = request.json.get('password')
        boe = BetOnEther.query.get(id)
        res = boe.withdraw(address, password)
        return res
