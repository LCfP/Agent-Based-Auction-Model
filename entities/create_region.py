from entities import *
from config import Config

def create_regions():
    regions = []
    for i in range(1, (Config.dimension_regions**2 +1)):
            new_region = Regions(i)
            regions.append(new_region)
    return regions

#TODO not sure if I can retrieve the 'local' region values
