from config import Config


class Environment(object):

    def __init__(self):
        self.config = Config()

    def setup(self):
        """
        This method sets-up the initial distribution of the model, e.g. the
        first agents and other entities.
        """
        pass

