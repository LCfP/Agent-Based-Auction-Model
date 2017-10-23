from enum import Enum


class BiddingTypes(Enum):
    """
    Defines the Bidder and Seller action types, to be used by the Auctioneer.
    """
    SELL = 0
    BUY = 1
