from random import randint
from random import choice
from config import Config


class Regions(object):

    def __init__(self, region_id, subregion_id):
        self.region_id = region_id
        self.subregion_id = subregion_id

    def region(self):
        global region
        region = ([(self.subregion_id) * Config.subregion_length, (self.subregion_id+1)* Config.subregion_length ],
                               [0, Config.subregion_length])
        return region
    def hub(self):
        global hub
        hub = [(self.subregion_id+1) * Config.subregion_length - (Config.subregion_length // 2),
               Config.subregion_length // 2]
        return hub


def create_regions():
    global regions
    regions = []
    for i in range(1, Config.number_of_regions+1):
        for j in range(Config.number_of_subregions):
            new_region = Regions(i, j + ((i-1)*Config.number_of_regions))
            regions.append(new_region)
    return regions

"Examples"

create_regions()
print(regions[2].hub())
print(regions[2].region())
print(regions[2].region_id)
print(regions[4].region_id)

""""In total there are 16 subregions numbering from 0 to 15 (subregion_id). I've ran some test runs and the 
region_id's fit in properly (e.g. subregion_id 2 has region_id 1 and subregion_id 4 has region_id 2 etc.)."""
