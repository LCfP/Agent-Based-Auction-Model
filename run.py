from entities import *
from environment import Environment
from random import random
from random import randint


environment = Environment()
environment.setup()

auctioneer = Auctioneer(environment)

for _ in range(environment.config.run_length):  # run model!
    if random() < environment.config.random_agent_creation:
        if randint(1, 4) < 3:
            agent = Buyer(environment)
        else:
            agent = Seller(environment)

        agent.registration_id = auctioneer.register(agent)

auctioneer.auction()
