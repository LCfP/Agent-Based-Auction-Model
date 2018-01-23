from enum import Enum

class ContainerState(Enum):
    EMPTY = 0
    PICKUP = 1 # Container has won shipment but still has to pickup the shipment
    DELIVERING = 2 # Container is loaded and on his way to the shipment destination