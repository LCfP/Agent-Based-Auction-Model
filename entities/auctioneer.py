from .buyer import Buyer
from .seller import Seller
from typing import List


class Auctioneer(object):

    def __init__(self, buyers: List[Buyer], sellers: List[Seller]):
        self.buyers = buyers
        self.sellers = sellers

    def auction(self):
        """
        Auctions with the buyers and sellers provided to this Auctioneer.
        """
        pass  # TODO

    def _broker_bids(self):
        """
        Helper function to broker the bids into a fair redistribution, according
        to some algorithm.
        """
        pass  # TODO
