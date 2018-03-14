from .entity import Entity

class Consumer(Entity):

    def __init__(self,env):
        self.env = env
        self.products = []