from .entity import Entity
from .auctioneer import Auctioneer
import numpy as np


class Region(Entity):

    def __init__(self, env, region_id: int):
        self.env = env

        self.id = region_id

        self.auctioneer = Auctioneer(env, self)

        self.geography = self._geography()

        print(self.geography)

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

