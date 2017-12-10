from entities import *
from config import Config
from random import random
from random import randint




create_regions() 

auctioneer = Auctioneer()

for _ in range(Config.run_length):  # run model!
    if random() < Config.random_agent_creation:
        _ = randint(1, 4)
        if _ < 3:
            agent = Buyer()
        else:
            agent = Seller()
        auctioneer.register(agent)

auctioneer.auction()


