from .agent import Agent
from enums.biddingtypes import BiddingTypes
from random import randint
from random import choice
from config import Config
from typing import NamedTuple
from .regions import *


class Seller(Agent):


    def __init__(self):
        self.agent_id = 0
        self.action = 0
        self.quantity = randint(*Config.quantity_range)
        self.item_price = randint(*Config.price_range)
        choose_subregion = choice(Regions().region)
        self.location = [randint(*regions[choose_subregion_id].region()[0]), #TODO Confirm if 'regions' inherit in run
                         randint(*regions[choose_subregion_id].region()[1])]

    def bid(self) -> NamedTuple:
        return self.Bid(action=BiddingTypes.SELL,
                        quantity=self.quantity,
                        item_price=self.item_price)
