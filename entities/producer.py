from .seller import Seller
from .shipment import Shipment
from enums import EntityTypes
from itertools import count
from random import randint
from tools import route_euclidean_distance, find_hub_coordinates
from collections import namedtuple

class Producer(Seller):
    _ids = count(0)

    def __init__(self, env, region):
        super().__init__(env)

        self.type = EntityTypes.PRODUCER

        self.production_rate = env.config.producer_production_rate()

        self.region = region
        self.location = region.draw_location()
        self.id = next(self._ids)
        self.storage = []
        self.registered_shipments = []

    def produce(self):
    # I rewrote this function so shipments, when produced, are immediately put into storage
    # the storage attribute of producer provides better tracking of shipments per producer
        for _ in range(self.production_rate):
            shipment = Shipment(producer_id=self.id,
                                location=self.location,
                                destination=self._set_destination(),
                                region=self.region)
            self.storage.append(shipment)

    def _set_destination(self):
        coordinates = self.env.regions[randint(0,len(self.env.regions)-1)].draw_location()
        return coordinates

    def bid(self, registrationkey, item : Shipment):
        ''' Minimum shipment biddingvalue consists of:
        1) transport costs from hub to pickup location
        2) transport costs from pickup location to destination'''
        producerbid = namedtuple('producerbid', 'registration_key biddingvalue')
        hub_coords = find_hub_coordinates(self.region)
        transport_cost_from_hub = self.env.config.transport_cost * \
                                  route_euclidean_distance(self.env,hub_coords,item.location)
        transport_cost_to_destination = self.env.config.transport_cost * \
                                        route_euclidean_distance(self.env, item.location, item.destination)
        #TODO add increase of price based on shipping urgency?
        #TODO add standard fees for container functionalties (for example refrigeration)
        total_value = transport_cost_from_hub + transport_cost_to_destination

        producerbid = producerbid(registration_key = registrationkey,
                  biddingvalue = total_value)
        return producerbid