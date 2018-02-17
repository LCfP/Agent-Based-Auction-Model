from .seller import Seller
from .shipment import Shipment
from enums import EntityTypes, ShipmentState
from itertools import count
from random import randint
from tools import route_euclidean_distance, find_hub_coordinates
from collections import namedtuple
from tabulate import tabulate
from math import ceil

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
        self.storage_capacity = self.env.config.storage_capacity
        self.account_value = self.env.config.producer_starting_account_value


    def produce(self):
        # a producer produces according to his production rate if he has room
        # within his storage for the produced shipment
        if self.env.config.debug is True and self.region.id < 1:
            room_before_production = self.storage_capacity-len(self.storage)

        for _ in range(self.production_rate):
            if len(self.storage) < self.storage_capacity:
                shipment = Shipment(producer_id=self.id,
                                    location=self.location,
                                    destination=self._set_destination(),
                                    region=self.region)
                self.storage.append(shipment)

        if self.env.config.debug is True and self.region.id < 1:
            table = (["producer id", self.id],
                     ["storage room before production", room_before_production],
                     ["production rate", self.production_rate],
                     ["storage room after production",
                      self.storage_capacity-len(self.storage) ])
            print (tabulate(table))

    def _set_destination(self):
        coordinates = \
            self.env.regions[randint(0,len(self.env.regions)-1)].draw_location()
        return coordinates

    def bid(self, registrationkey, item : Shipment):
        ''' Minimum shipment biddingvalue consists of:
        1) transport costs from hub to pickup location
        2) transport costs from pickup location to destination'''
        producerbid = namedtuple('producerbid', 'registration_key biddingvalue')
        hub_coords = find_hub_coordinates(self.region)
        transport_cost_from_hub = self.env.config.transport_cost * \
                                  route_euclidean_distance(self.env,
                                                           hub_coords,
                                                           item.location)
        transport_cost_to_destination = self.env.config.transport_cost * \
                                        route_euclidean_distance(self.env,
                                                                 item.location,
                                                                 item.destination)
        #TODO improve biddingvalue based on shipping urgency
        storage_utilisation = len(self.storage) / self.storage_capacity
        # using steps of 10% for urgency
        storage_utilisation = ceil(storage_utilisation * 10)
        urgency = storage_utilisation / 10
        # urgency cost based on region size
        shipping_urgency_cost = urgency * \
                                self.env.config.region_size * \
                                self.env.config.transport_cost
        #TODO add standard fees for container functionalties
        total_value = transport_cost_from_hub + transport_cost_to_destination \
                      + shipping_urgency_cost

        producerbid = producerbid(registration_key = registrationkey,
                                    biddingvalue = total_value)

        if self.env.config.debug is True and self.region.id < 1:
            print("producer %s in region: %s enters bid: %s "
                  "for shipment with id: %s"
                  %(self.id, self.region.id,producerbid, item.id))

        return producerbid

    def pay_invoice(self,invoice):
        '''created this function, because it seems weird to me that auctioneer
        just withdraws money from the account of the producer.'''
        if self.env.config.debug is True:
            account_value_before_payment = self.account_value

        payment_amount = invoice.amount_due
        self.account_value -= payment_amount

        if self.env.config.debug is True:
            print(tabulate([[self.id,account_value_before_payment,
                             payment_amount, invoice.shipment_id,
                             self.account_value]],
                           headers= ["producer_id",
                                     "account value before payment",
                                     "invoice value", "shipment id",
                                     "account value after payment"]))
        return payment_amount

    def losing_auction_response(self):
        # Producer unregisters shipments and corresponding bids,
        # when they are not matched

        for shipment in self.storage:
            if shipment.state == ShipmentState.STORAGED:
                for key in \
                        self.region.auctioneer.entities[EntityTypes.SHIPMENT]:
                    if self.region.auctioneer.entities[EntityTypes.SHIPMENT][
                        key].id \
                            == shipment.id:
                        registrationkey = key
                self.region.auctioneer.unregister(shipment.type, registrationkey)
                self.region.auctioneer.unlist_shipment(registrationkey)