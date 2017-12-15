from enum import Enum


class EntityTypes(Enum):
    """
    Defines all Entity types.
    """
    AUCTIONEER = 0
    BUYER = 1
    SELLER = 2
    AGENT = 3  # should not be used
