from collections import namedtuple


class Agent(object):
    Bid = namedtuple('Bid', ['action', 'quantity', 'item_price'])

    def bid(self):
        raise NotImplementedError
