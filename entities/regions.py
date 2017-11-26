from random import randint
from random import choice
from config import Config

class Regions(object):
    region = []
    def create_region(self):
        for i in range(Config.number_of_regions):
            self.region_id = i + 1
            for j in range(Config.number_of_subregions):
                self.hub = [int((j + 1 + i * 4) * Config.subregion_length - (Config.subregion_length / 2)),
                            int(Config.subregion_length / 2)]
                self.region.append([[(j + i * 4) * Config.subregion_length, (j + 1 + i * 4) * Config.subregion_length,
                               0, Config.subregion_length], self.region_id , self.hub])