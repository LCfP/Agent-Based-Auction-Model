from entities import *
from config import Config

buyers = []
for _ in range(Config.buyers):
    buyers.append(Buyer())

sellers = []
for _ in range(0, Config.sellers):
    sellers.append(Seller())

# use seller and buyers lists for the auctioneer
auctioneer = Auctioneer(buyers, sellers)

auctioneer.auction()  # runs the auction!
