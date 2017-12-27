from .buyer import Buyer
from .shipment import Shipment
from enums import EntityTypes


class Container(Buyer):

    def __init__(self, env, region):
        super().__init__(env)

        self.type = EntityTypes.CONTAINER

        self.region = region
        self.location = region.draw_location()
        self.id = 0

    def bid(self, item: Shipment):
        pass  # TODO
        cost_empty_transport = item.location


