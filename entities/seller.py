from .agent import Agent
from enums import BiddingTypes, EntityTypes
from random import randint
from typing import NamedTuple


class Seller(Agent):

    def __init__(self, env):
        self.env = env

        self.type = EntityTypes.SELLER

        self.quantity = randint(*env.config.quantity_range)
        self.item_price = randint(*env.config.price_range)

        self.location = [randint(*env.config.region[0]),  # x axis
                         randint(*env.config.region[1])]  # y axis

    def bid(self) -> NamedTuple:
        return self.Bid(action=BiddingTypes.SELL,
                        quantity=self.quantity,
                        item_price=self.item_price)
