
from ..base import BaseResource
from ...utils import get_w3, get_node_status


w3 = get_w3()


class EthStatus(BaseResource):

    def get(self):
        return get_node_status()
