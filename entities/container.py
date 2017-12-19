from .buyer import Buyer
from .shipment import Shipment
from enums import EntityTypes
from environment import Environment
from math import sqrt
from .hub import Hub

class Container(Buyer):

    def __init__(self, env, region):
        super().__init__(env)

        self.type = EntityTypes.CONTAINER

        self.region = region
        self.location = region.draw_location()
        self.container_id = 0

    def bid(self, item: Shipment):
            transport_cost_empty =  sqrt(abs(self.location[0] - item.location[0])^2
                                         + abs(self.location[1]-item.location[1])^2)*Environment.transport_cost
            transport_cost_hub = sqrt(abs(item.location[0]-Hub.location[0])^2
                                      + abs(item.location[1]-Hub.location[1]^2))*Environment.transport_cost
            transport_cost_transregion = 0 #TODO Calculate distance hub to hub based on region_id

            transport_cost_destination = sqrt(abs(Hub.destination[0]- item.destination["coordinates"][0])^2
                                            + abs(Hub.destination[1]- item.destination["coordinates"][1])^2)*Environment.transport_costs
            Bid = transport_cost_empty + transport_cost_hub + transport_cost_transregion + transport_cost_destination
            return Bid



