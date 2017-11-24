from entities import *
from config import Config
from random import randint

class Producer(Seller):
    def __init__(self):
        super().__init__()
        self.shipments = []



class Shipment(Producer):
    def produce(self):
        for _ in range(*Config.production_rate):
          destination = [randint(*Config.region[0]),  # x axis
                            randint(*Config.region[1])]  # y axis
          self.shipments.append(new Shipment(self.location, destination, self.agent_id))  # See (II)






""" (II) I once again intiated with an empty list, but this time in the in the Producer class. I feel like I'm struggling with where I 
should store the shipments."""












