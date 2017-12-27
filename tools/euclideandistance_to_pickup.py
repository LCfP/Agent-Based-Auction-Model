from math import sqrt
from entities import Container, Shipment
from config import Config
import numpy as np

# Calculates the distance between a container location and the shipment pickup location
# When traveling between regions, transport is only available between hubs
# A container travels to the hub in his current region, then from that hub to the hub situated in the shipment's region,
# and finally, from that hub to the shipment's location

def euclideandistance_to_pickup(object1 : Container, object2 : Shipment):
    xstart = object1.location[0]
    ystart = object1.location[1]
    xend = object2.location[0]
    yend = object2.location[1]
    regionstart = object1.region.id
    regionend = object2.region

    if regionstart != regionend:
        firstdistance = container_to_hub(object1)
        seconddistance = hub_to_hub(object1,object2)
        thirddistance = hub_to_shipmentlocation(object2)

        total_distance = firstdistance + seconddistance + thirddistance

        return total_distance

    elif regionstart == regionend:
        total_distance = sqrt((abs(xend - xstart)) ** 2 + (abs(yend - ystart)) ** 2)

        return total_distance

def container_to_hub(object1 : Container):
    xstart = object1.location[0]
    ystart = object1.location[1]
    container_region = object1.region.id
    # TODO rewrite using environment
    xhub = Config.region_size/2 + (container_region % int(np.sqrt(Config.regions))* Config.region_size)
    yhub = Config.region_size/2 + (container_region // int(np.sqrt(Config.regions))* Config.region_size)
    distance = sqrt((abs(xhub - xstart)) ** 2 + (abs(yhub - ystart)) ** 2)
    return distance

def hub_to_hub(object1 : Container, object2: Shipment):
    regionstart = object1.region.id
    regionend = object2.region
    # TODO rewrite regionmovement using environment
    xregionmovement = abs(regionstart % int(np.sqrt(Config.regions)) - regionend % int(np.sqrt(Config.regions))) * Config.region_size
    yregionmovement = abs(regionstart // int(np.sqrt(Config.regions)) - regionend // int(np.sqrt(Config.regions))) * Config.region_size

    distance = sqrt(xregionmovement ** 2 + yregionmovement ** 2)
    return distance

def hub_to_shipmentlocation(object2: Shipment):
    xend = object2.location[0]
    yend = object2.location[1]
    shipment_region = object2.region
    #TODO rewrite using environment
    xhub = Config.region_size / 2 + (shipment_region % int(np.sqrt(Config.regions)) * Config.region_size)
    yhub = Config.region_size / 2 + (shipment_region // int(np.sqrt(Config.regions)) * Config.region_size)

    distance = sqrt((abs(xend - xhub)) ** 2 + (abs(yend - yhub)) ** 2)
    return distance