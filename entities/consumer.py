from .entity import Entity

class Consumer(Entity):

    def __init__(self,env):
        super().__init__()
        self.env = env
        self.products = []