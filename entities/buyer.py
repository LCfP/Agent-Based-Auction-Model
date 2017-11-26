from .agent import Agent
from enums.biddingtypes import BiddingTypes
from config import Config
from random import randint
from random import choice
from typing import NamedTuple
from .regions import *



class Buyer(Agent):
    def __init__(self):
        self.agent_id = 0
        self.action = 1
        self.quantity = randint(*Config.quantity_range)
        self.item_price = randint(*Config.price_range)
        choose_subregion_id = randint(0,Config.number_of_regions*Config.number_of_subregions -1)
        self.location = [randint(*regions[choose_subregion_id].region()[0]),  # x axis #TODO Confirm if 'regions' inherit in run
                         randint(*regions[choose_subregion_id].region()[1])]  # y axis

    def bid(self) -> NamedTuple:
        return self.Bid(action=BiddingTypes.BUY,
                        quantity=self.quantity,
                        item_price=self.item_price)