from config import Config
from entities import *
from random import choice


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
        # setup containers
        self.containers = [Container(self, choice(self.regions)) for _ in range(self.config.number_of_containers)]

        # setup producers
        self.producers = [Producer(self, choice(self.regions)) for _ in range(self.config.number_of_producers)]

        # setup transport company (currently only 1 transport company)
        self.transportcompany = Transportcompany(self)
