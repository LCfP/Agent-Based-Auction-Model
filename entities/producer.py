from entities import *
from config import Config
from random import randint

class Producer(Seller):
    def __init__(self):
        super(Producer, self).__init__()

    def produce(self):
        for _ in range(*Config.production_rate):
            destination_shipment= [randint(*Config.region[0]),  # x axis
                            randint(*Config.region[1])]  # y axis
            shipments.append([self.location, destination_shipment, id(seller)])




"""Ik heb twijfels over in hoeverre dit de gewenste vorm voor shipment is. Bovendien vraag ik me af of
'self.location' goed meegenomen word en of dit hele gebeuren goed uitpakt in de run. Voordat ik het allemaal
ga proberen te verwerken in run wacht ik even tot het doet wat het moet doen."""












