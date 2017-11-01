from .buyer import Buyer
from .seller import Seller
from operator import attrgetter
from statistics import median
from typing import List


class Auctioneer(object):

    def __init__(self, buyers: List[Buyer], sellers: List[Seller]):
        self.buyers = buyers
        self.sellers = sellers

    def auction(self):
        """
        Auctions with the buyers and sellers provided to this Auctioneer.
        """

        # List of all buyers and sellers:
        print('+++ REGISTER +++')
        print('Buyers:')
        print('       ID            Q     P')
        print('----------------  ------ -----')
        fmt = '{:7} {:8} {:5}'
        for buyer in self.buyers:
            print(fmt.format(id(buyer), buyer.quantity, buyer.item_price))

        print('\nSellers:')
        print('       ID            Q     P')
        print('----------------  ------ -----')
        for seller in self.sellers:
            print(fmt.format(id(seller), seller.quantity, seller.item_price))


        # AUCTION ALGORITHM
        # (1) SELLERS: determine total supply and median item price:
        total_q_s = 0
        auction_items = []
        for seller in self.sellers:
            total_q_s += seller.quantity
            for i in range(seller.quantity):
                auction_items.append(seller.item_price)
        median_p_s = median(sorted(auction_items))

        # (2) BUYERS: determine total demand and median item price:
        total_q_b = 0
        auction_items_b = []
        for buyer in self.buyers:
            total_q_b += buyer.quantity
            for j in range(buyer.quantity):
                auction_items_b.append(buyer.item_price)
        auction_items_b = sorted(auction_items_b, reverse=True)
        median_p_b = median(auction_items_b[0:total_q_s])

        # (3) Determine auction price:
        auction_price = (median_p_s + median_p_b) / 2

        print('\n+++ AUCTION +++')
        print("Total supply:        %s" % total_q_s)
        print("Total demand:        %s" % total_q_b)
        print("Median seller price:  %s" % median_p_s)
        print("Median buyer price:   %s" % median_p_b)
        print("Auction price:        %s" % auction_price)


        # RESULTS
        # Distribution of the auction items:
        buyers = sorted(self.buyers, key=attrgetter('item_price'), reverse=True)

        print('\n+++ RESULTS +++\nID buyer gets Q items:')
        print('       ID            Q')
        print('----------------  ------')
        fmt = '{:7} {:8}'

        for buyer in buyers:
            if total_q_s >= buyer.quantity:
                print(fmt.format(id(buyer), buyer.quantity))
                total_q_s -= buyer.quantity
            elif total_q_s > 0:
                print(fmt.format(id(buyer), total_q_s))
                total_q_s = 0
            else:
                print(fmt.format(id(buyer), 0))