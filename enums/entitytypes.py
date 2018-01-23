from enum import Enum


class EntityTypes(Enum):
    """
    Defines all Entity types.
    """
    AUCTIONEER = 0
    BUYER = 1
    SELLER = 2
    CONTAINER = 4
    PRODUCER = 5
    SHIPMENT = 6
    REGION = 7
