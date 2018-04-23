
from .base import BaseResource


class Informations(BaseResource):

    def get(self, _id):
        if _id.lower() == 'latest':
            return 'I am latest info.'
        return 'fuck RuntimeError.'
