from .entity import Entity
from enums import EntityTypes


class Auctioneer(Entity):

    def __init__(self, env, region):
        self.env = env
        self.region = region

        self.type = EntityTypes.AUCTIONEER

        self.entities = {}

    def auction(self):
        """
        Auctions with the buyers and sellers provided to this Auctioneer.
        """
        raise NotImplementedError("TODO")

    def register(self, entity: Entity) -> int:
        """
        Registers an agent with this Auctioneer.
        """
        if entity.type not in self.entities.keys():
            self.entities[entity.type] = {}

        registration_key = self._registration(entity.type)
        self.entities[entity.type][registration_key] = entity

        return registration_key

    def unregister(self, type, registration_key) -> Entity:
        """
        Unregisters an agent from this Auctioneer, using the assigned
        registration key.
        """
        if type not in self.entities.keys():
            raise ValueError("Type `{0}' is not an understood entity!"
                             .format(type))

        return self.entities[type].pop(registration_key, default=False)

    def _registration(self, type):
        max_key = max(self.entities[type].keys(), default=0)

        for key in range(max_key):  # attempt to fill `holes'
            if key not in self.entities[type].keys():
                return key

        return max_key + 1  # new key, one greater than the last
