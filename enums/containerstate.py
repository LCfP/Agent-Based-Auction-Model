from enum import Enum

class ContainerState(Enum):
    EMPTY = 0
    NEEDING_TRANSPORT = 1
    AWAITING_TRANSPORT = 2
    PICKUP = 3 # Container has won shipment but still has to pickup the shipment
    DELIVERING = 4 # Container is loaded and on his way to the shipment destination