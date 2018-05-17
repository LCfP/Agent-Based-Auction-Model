from .entity import Entity
from enums import EntityTypes, ShipmentState
from itertools import count


class Shipment(Entity):
    _ids = count(0)

    def __init__(self, producer_id, location, destination, region):
        super().__init__()
        self.producer_id = producer_id
        self.location = location
        self.destination = destination
        self.id = next(self._ids)
        self.region = region

        self.type = EntityTypes.SHIPMENT
        self.state = ShipmentState.STORED
        # TODO: a shipment is more than just this. It contains products!
