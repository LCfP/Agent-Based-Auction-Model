from .agent import Agent
from typing import NamedTuple


class Seller(Agent):

    def __init__(self):
        self.quantity = 10  # TODO
        self.item_price = .95  # TODO

    def bid(self) -> NamedTuple:
        return self.Bid(action="sell",
                        quantity=self.quantity,
                        item_price=self.item_price)
