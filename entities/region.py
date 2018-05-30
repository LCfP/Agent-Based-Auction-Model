from .entity import Entity
from .auctioneer import Auctioneer
import numpy as np
from enums import EntityTypes

#documentation done 30-05-2018 Meike Koenen

class Region(Entity):

"""
All following functions are allocated to the class 'region'
The parameters 'environment' and 'region_id' are assigned to the class
Variables are assigned to all mentioned parameters
An auctioneer is assigned to the class. The region is given a specific geography which is created by the function (self._geography). A type is attached to the region using enums

"""
    def __init__(self, env, region_id: int):
        super().__init__()

        self.env = env

        self.id = region_id

        self.auctioneer = Auctioneer(env, self)

        self.geography = self._geography()

        self.type = EntityTypes.REGION



    def draw_location(self):
        """
        Draws a random coordinate within this region's geography.
        """
        x_coord = np.random.randint(*self.geography[0])
        y_coord = np.random.randint(*self.geography[1])

        return [x_coord, y_coord]

    def _geography(self):
        regions = self.env.config.regions
        side = int(np.sqrt(regions))

        north_south = self.id // side
        west_east = self.id % side

        x_axis = [west_east * self.env.config.region_size,
                  (west_east + 1) * self.env.config.region_size]

        y_axis = [north_south * self.env.config.region_size,
                  (north_south + 1) * self.env.config.region_size]

        return [x_axis, y_axis]

