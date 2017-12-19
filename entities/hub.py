from .region import Region
from environment import Environment

class Hub(Region):
    def __init__(self, env, region_id: int):
        super().__init__(env, region_id)

        self.location = [Environment.region_size*0.5,
                         Environment.region_size*0.5]



