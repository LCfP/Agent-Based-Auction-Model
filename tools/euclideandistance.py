from math import sqrt
import numpy as np
from config import Config

def euclidean_distance(startcoords : list, endcoords : list):
    xstart = startcoords[0]
    ystart = startcoords[1]
    xend = endcoords[0]
    yend = endcoords[1]
    distance = sqrt((abs(xend - xstart)) ** 2 + (abs(yend - ystart)) ** 2)
    return distance

def find_hub_coordinates(region):
    region_id = region.id
    xcoord = Config.region_size * 0.5 + (region_id % int(np.sqrt(Config.regions))) * Config.region_size
    ycoord = Config.region_size * 0.5 + (region_id // int(np.sqrt(Config.regions))) * Config.region_size
    coords = [xcoord,ycoord]
    return coords

def find_region(env, coordinates):
    ids = []
    for regionid in range(env.config.regions):
        x1 = env.regions[regionid].geography[0][0]
        x2 = env.regions[regionid].geography[0][1]
        y1 = env.regions[regionid].geography[1][0]
        y2 = env.regions[regionid].geography[1][1]

        if coordinates[0] >= x1 and coordinates[0] <= x2 \
                and coordinates[1] >= y1 and coordinates[1] <= y2 :
            ids.append(regionid)
    region_id = min(ids)

    for region in env.regions:
        if region.id == region_id:
            destination_region = region
            return destination_region

def determine_route(env, item1_coordinates, item2_coordinates):
    item1_region = find_region(env, item1_coordinates)
    item2_region = find_region(env, item2_coordinates)

    if item1_region == item2_region:
        startcoords = item1_coordinates
        endcoords = item2_coordinates
        route = [startcoords, endcoords]
        return route
    else:
        '''When moving cross regions, the region hubs have to be used'''
        startcoords = item1_coordinates
        starthubcoords = find_hub_coordinates(item1_region)
        endhubcoords = find_hub_coordinates(item2_region)
        endcoords = item2_coordinates
        route = [startcoords,starthubcoords,endhubcoords,endcoords]
        return route

def route_euclidean_distance(env, item1_coordinates, item2_coordinates):
    route = determine_route(env, item1_coordinates, item2_coordinates)
    total_distance = 0
    for location in range(1,len(route)):
        startcoords = route[location-1]
        endcoords = route[location]
        distance = euclidean_distance(startcoords,endcoords)
        total_distance += distance
    return total_distance

# sum(euclidean_distance(*route[location:location + 2]) for location in range(len(route) - 1))
# should the location + 2 not be lcoation + 1 ???