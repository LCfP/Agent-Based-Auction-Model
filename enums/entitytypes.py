from enum import Enum

#documentation done 30-05-2018 Meike Koenen

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
    TRANSPORTER = 8
