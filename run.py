from entities import *
from config import Config
from random import random
from random import randint

buyers = []
sellers = []
auctioneer = Auctioneer(buyers, sellers)

for _ in range(Config.run_length):  # run model!
    if random() < Config.random_agent_creation:
        _ = randint(1,4)
        # We should assume that demand is higher than supply and that there are more sellers than buyers.
        # However, since distribution of Q for both buyers and sellers is equal, this results in a lower
        # demand than supply (needs to be changed in config/buyer/seller?). Therefore, I changed it a
        # bit so that there are more buyers than sellers, but supply < demand.
        if _ < 4:
            agent = Buyer()
            buyers.append(agent)
        else:
            agent = Seller()
            sellers.append(agent)

auctioneer.auction()