
from flask import request, abort
from werkzeug.datastructures import MultiDict

from .base import BaseResource, login_required
from .forms import BetOnEtherCreateForm
from .. import db
from ..src.eth import Connector
from ..models import BetOnEther


def form_by_json_request(form_class):
    return get_form(form_class, request.json or request.form)


def get_form(form_class, _dict):
    data = {}
    for k, v in _dict.items():
        if v is not None:
            data[k] = v
    return form_class(MultiDict(data))


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
