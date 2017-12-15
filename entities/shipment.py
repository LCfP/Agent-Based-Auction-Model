from .entity import Entity
from enums import EntityTypes


class Shipment(Entity):

    def __init__(self, producer_id, location, destination):
        self.producer_id = producer_id
        self.location = location
        self.destination = destination

        self.type = EntityTypes.SHIPMENT

        # TODO: a shipment is more than just this. It contains products!
