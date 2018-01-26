from enum import Enum

class ShipmentState(Enum):
    STORAGED = 0
    AWAITING_PICKUP = 1 # Container has won shipment but still has to pickup the shipment
    ON_ROUTE = 2 # Container is loaded and on his way to the shipment destination
    DELIVERED = 3