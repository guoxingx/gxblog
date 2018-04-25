
from flask import request

from .base import BaseResource
from ..src.eth import Connector


class EthAccounts(BaseResource):

    def post(self):
        pass
