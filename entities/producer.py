from entities import *
from config import Config
from random import randint

class Producer(Seller):
    def __init__(self):
        super(Producer, self).__init__()
    def produce(self):
      shipments = []
      shipments_IDs = {}
      for _ in range(randint(*Config.production_rate)):
            destination_shipment= [randint(*Config.region[0]),  # x axis
                                   randint(*Config.region[1])]  # y axis
            shipments_IDs['Shipment %s' % len(shipments_IDs)] = len(shipments_IDs)
            shipments.append([self.location, destination_shipment, len(shipments_IDs)]) #TODO self.location should not be one fixed number












