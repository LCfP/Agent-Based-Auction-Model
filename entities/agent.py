from collections import namedtuple
from .entity import Entity


class Agent(Entity):
    Bid = namedtuple('Bid', ['action', 'quantity', 'item_price'])

    def bid(self):
        raise NotImplementedError
