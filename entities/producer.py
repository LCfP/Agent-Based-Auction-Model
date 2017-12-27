from .seller import Seller
from .shipment import Shipment
from enums import EntityTypes


class Producer(Seller):

    def __init__(self, env, region):
        super().__init__(env)

        self.type = EntityTypes.PRODUCER

        self.production_rate = env.config.producer_production_rate()

        self.region = region
        self.location = region.draw_location()
        self.id = 0

    def produce(self):
        shipments = []

        for _ in range(self.production_rate):
            shipment = Shipment(producer_id=self.registration_id,
                                location=self.location,
                                destination=self._set_destination())
            shipments.append(shipment)

        return shipments

    def _set_destination(self):
        pass  # TODO
