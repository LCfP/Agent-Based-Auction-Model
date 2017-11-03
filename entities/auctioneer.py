from .buyer import Buyer
from .seller import Seller
from .agent import Agent
from random import random

class Auctioneer(object):

    def __init__(self):
        self.buyers = []
        self.sellers = []
        self.shipments = []
        self.auction_results = []

    def auction(self):
        """
        Auctions with the buyers and sellers provided to this Auctioneer.
        """

        # List of all buyers and sellers:
        print('+++ REGISTER +++')
        print('Buyers:')
        print(' ID     P')
        print('---- -----')
        fmt = '{:4} {:4}'
        for buyer in self.buyers:
            print(fmt.format(buyer.agent_id, buyer.item_price))

        print('\nSellers:')
        print(' ID     P')
        print('---- -----')
        for seller in self.sellers:
            print(fmt.format(seller.agent_id, seller.item_price))

        # AUCTION ALGORITHM:
        # For for every container an auction is run
        while len(self.buyers) != 0:
            for buyer in self.buyers:
                for _ in range(100):
                    if random() < 0.05:
                        # Shipments (temporary: are refined later)
                        shipment = Seller()
                        shipment_id = id(shipment)
                        self.shipments.append(shipment)

                winning_bid = max([shipment.item_price for shipment in self.shipments])
                # TODO Adjust prices in buyers/sellers (buyer wants higher price than seller)
                # TODO Also implement location + destination + size + transport costs + pick-up deadline
                auction = [buyer.agent_id, shipment_id, (winning_bid + buyer.item_price) / 2, winning_bid, buyer.item_price]
                self.auction_results.append(auction)
                self.unregister(buyer.agent_id)

        # (2) Print auction results:
        print('+++ AUCTION RESULTS +++')
        print('B    Shipment         P   Winning bid Buyer bid')
        print('--- --------------- ----- ----------- --------')
        fmt = '{:3} {:5} {:4} {:7} {:10}'
        for _ in self.auction_results:
            print(fmt.format(_[0], _[1], _[2], _[3], _[4]))
            # TODO save results somewhere

    def register(self, agent: Agent):
        # Container: "Hi, I'm here!"
        if agent.action == 1:
            agent.agent_id = 'B%s' % (len(self.buyers) + 1)
            self.buyers.append(agent)
        # Seller: "I have a shipment!"
        if agent.action == 0:
            agent.agent_id = 'S%s' % (len(self.sellers) + 1)
            self.sellers.append(agent)

    def unregister(self, agent_id) -> Agent:
        for buyer in self.buyers:
            if buyer.agent_id == agent_id:
                self.buyers.remove(buyer)
                # TODO After shipping: container registers at new location (= destination previous shipment)