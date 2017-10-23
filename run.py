from entities import *
from config import Config

buyers = {}
buyer_code = 0
for b in range(0, Config.buyers):
    buyer_code += 1

    buyers[buyer_code] = Bid

sellers = []
for _ in range(0, Config.sellers):
    pass  # TODO init sellers here

# use seller and buyers lists for the auctioneer
auctioneer = Auctioneer(buyers, sellers)

auctioneer.auction  # runs the auction!
