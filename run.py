from entities import *
from config import Config
from random import random

auctioneer = Auctioneer()

for _ in range(Config.run_length):  # run model!
    if random() < Config.random_agent_creation:
        pass  # TODO: create and register an agent, either a Seller or a Buyer

    auctioneer.auction()  # runs the auction!
