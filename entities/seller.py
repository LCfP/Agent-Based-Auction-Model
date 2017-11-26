from .agent import Agent
from enums.biddingtypes import BiddingTypes
from random import randint
from random import choice
from config import Config
from typing import NamedTuple
from .regions import Regions


class Seller(Agent):


    def __init__(self):
        self.agent_id = 0
        self.action = 0
        self.quantity = randint(*Config.quantity_range)
        self.item_price = randint(*Config.price_range)
        choose_subregion = choice(Regions().region)
        self.location = [randint(*choose_subregion[0]),  # x axis
                         randint(*choose_subregion[1])]  # y axis

    def bid(self) -> NamedTuple:
        return self.Bid(action=BiddingTypes.SELL,
                        quantity=self.quantity,
                        item_price=self.item_price)
