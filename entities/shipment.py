from .entity import Entity
from enums import EntityTypes, ShipmentState


class Shipment(Entity):

    def __init__(self, producer_id, location, destination, region):
        self.producer_id = producer_id
        self.location = location
        self.destination = destination

        self.region = region

        self.type = EntityTypes.SHIPMENT
        self.state = ShipmentState.STORAGED
        # TODO: a shipment is more than just this. It contains products!
