from random import randint
from random import choice
from config import Config


class Regions(object):

    def __init__(self, region_id):
        self.region_id = region_id

    def region(self):
        region = ([ [((self.region_id+(Config.dimension_regions-1))% (Config.dimension_regions))* Config.region_length, (((self.region_id+(Config.dimension_regions-1))%Config.dimension_regions)+1)* Config.region_length],
                               [(int((self.region_id-1)/Config.dimension_regions))* Config.region_length, (int((self.region_id-1)/Config.dimension_regions) +1)* Config.region_length]])
        print((self.region_id+(Config.dimension_regions-1))%Config.dimension_regions)
        return region
    def hub(self):
        hub = [((self.region_id+(Config.dimension_regions-1))% (Config.dimension_regions)+1)* Config.region_length - (Config.region_length // 2),
               (int((self.region_id - 1) / Config.dimension_regions) + 1) * Config.region_length - (Config.region_length //2)]
        return hub
