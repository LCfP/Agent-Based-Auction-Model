from math import sqrt
from entities import Shipment, Region
from config import Config
import numpy as np
from environment import Environment

# Calculates the distance between a shipment pickup location and the shipment destination

def euclideandistance_to_destination(env : Environment, object1 : Shipment):
    xstart = object1.location[0]
    ystart = object1.location[1]
    xend = object1.destination[0]
    yend = object1.destination[1]
    regionstart = object1.region
    regionend = find_regionid(env, object1)

    if regionstart != regionend:
        firstdistance = shipment_to_hub(object1)
        seconddistance = hub_to_hub(env, object1)
        thirddistance = hub_to_shipment_destination(env, object1)

        total_distance = firstdistance + seconddistance + thirddistance

        return total_distance

    elif regionstart == regionend:
        total_distance = sqrt((abs(xend - xstart)) ** 2 + (abs(yend - ystart)) ** 2)

        return total_distance

def shipment_to_hub(object1 : Shipment):
    xstart = object1.location[0]
    ystart = object1.location[1]
    shipment_region = object1.region
    # TODO rewrite using environment
    xhub = Config.region_size/2 + (shipment_region % int(np.sqrt(Config.regions))* Config.region_size)
    yhub = Config.region_size/2 + (shipment_region // int(np.sqrt(Config.regions))* Config.region_size)
    distance = sqrt((abs(xhub - xstart)) ** 2 + (abs(yhub - ystart)) ** 2)
    return distance

def hub_to_hub(env : Environment, object1 : Shipment):
    regionstart = object1.region
    regionend = find_regionid(env, object1)
    # TODO rewrite regionmovement using environment
    xregionmovement = abs(regionstart % int(np.sqrt(Config.regions)) - regionend % int(np.sqrt(Config.regions))) * Config.region_size
    yregionmovement = abs(regionstart // int(np.sqrt(Config.regions)) - regionend // int(np.sqrt(Config.regions))) * Config.region_size

    distance = sqrt(xregionmovement ** 2 + yregionmovement ** 2)
    return distance

def hub_to_shipment_destination(env : Environment, object1: Shipment):
    xend = object1.destination[0]
    yend = object1.destination[1]
    shipment_region = find_regionid(env, object1)
    #TODO rewrite using environment
    xhub = Config.region_size / 2 + (shipment_region % int(np.sqrt(Config.regions)) * Config.region_size)
    yhub = Config.region_size / 2 + (shipment_region // int(np.sqrt(Config.regions)) * Config.region_size)

    distance = sqrt((abs(xend - xhub)) ** 2 + (abs(yend - yhub)) ** 2)
    return distance


def find_regionid(env = Environment, shipment = Shipment):
    ids = []

    for regionid in range(env.config.regions):
        x1 = env.regions[regionid].geography[0][0]
        x2 = env.regions[regionid].geography[0][1]
        y1 = env.regions[regionid].geography[1][0]
        y2 = env.regions[regionid].geography[1][1]

        if shipment.destination[0] >= x1 and shipment.destination[0] <= x2 and shipment.destination[1] >= y1 and shipment.destination[1] <= y2 :
            ids.append(regionid)

    return min(ids)