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
        self.containers = []
        for number in range(self.config.number_of_containers):
            container = Container(self, choice(self.regions))
            container.id = len(self.containers)
            self.containers.append(container)

                # setup producers
        self.producers = []
        for number in range(self.config.number_of_producers):
            producer = Producer(self, choice(self.regions))
            producer.id = len(self.producers)
            self.producers.append(producer)
