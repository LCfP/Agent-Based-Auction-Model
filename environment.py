from config import Config
from entities import *


class Environment(object):

    def __init__(self):
        self.config = Config()

    def setup(self, env, region):
        """
        This method sets-up the initial distribution of the model, e.g. the
        first agents and other entities.
        """
        self.regions = [Region(self, region_id) for region_id in
                        range(self.config.regions)]
        self.containers = {}
        self.producers = {}
        for key in range(self.number_of_containers):
            container = Container(env, region)
            container.container_id = len(self.containers)
            self.containers[key] = container
        for key in range(self.number_of_producers):
            producer = Producer(env, region)
            producer.producer_id = len(self.producers)
            self.producers[key] = producer

        # TODO: setup agents
