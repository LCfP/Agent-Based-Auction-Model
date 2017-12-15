from config import Config
from entities import *


class Environment(object):

    def __init__(self):
        self.config = Config()

    def setup(self):
        """
        This method sets-up the initial distribution of the model, e.g. the
        first agents and other entities.
        """
        self.regions = [Region(self, region_id) for region_id in
                        range(self.config.regions)]

        # TODO: setup agents
