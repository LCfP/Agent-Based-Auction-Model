from entities import *
from config import Config

buyers = []
for _ in range(0, Config.buyers):
    pass  # TODO init buyers here

sellers = []
for _ in range(0, Config.sellers):
    pass  # TODO init sellers here

# use seller and buyers lists for the auctioneer
auctioneer = Auctioneer(buyers, sellers)

auctioneer.auction()  # runs the auction!
