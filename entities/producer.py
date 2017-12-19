from .seller import Seller
from .shipment import Shipment
from enums import EntityTypes
from random import randint
from environment import Environment

class Producer(Seller):

    def __init__(self, env, region):
        super().__init__(env)

        self.type = EntityTypes.PRODUCER

        self.production_rate = env.config.producer_production_rate()

        self.region = region
        self.location = region.draw_location()
        self.producer_id = 0
    def produce(self, region):
        shipments = []

        for _ in range(self.production_rate):
            shipment = Shipment(producer_id=self.registration_id,
                                location=self.location,
                                destination=self._set_destination(region))
            shipments.append(shipment)

        return shipments

    def _set_destination(self, region):
        shipment_destination = {"coordinates": region.draw_location(),
                                "region_id": randint(1, Environment.regions)}
        return shipment_destination

        # TODO Check validality
