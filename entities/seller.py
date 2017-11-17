from .agent import Agent
from enums.biddingtypes import BiddingTypes
from random import randint
from config import Config
from typing import NamedTuple


class Seller(Agent):


    def __init__(self):
        self.agent_id = 0
        self.action = 0
        self.quantity = randint(*Config.quantity_range)
        self.item_price = randint(*Config.price_range)
        region_generate = randint(0, 8)
        self.location = [randint(*Config.region[region_generate][0]),  # x axis
                         randint(*Config.region[region_generate][1])]  # y axis

    def bid(self) -> NamedTuple:
        return self.Bid(action=BiddingTypes.SELL,
                        quantity=self.quantity,
                        item_price=self.item_price)
