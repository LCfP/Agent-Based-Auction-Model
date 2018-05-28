from .entity import Entity
from enums import EntityTypes


class Buyer(Entity):

    def __init__(self, env):
        super().__init__(env)
        self.env = env

        self.type = EntityTypes.BUYER
